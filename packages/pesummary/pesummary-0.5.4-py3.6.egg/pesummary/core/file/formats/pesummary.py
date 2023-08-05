# Copyright (C) 2018  Charlie Hoy <charlie.hoy@ligo.org>
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from glob import glob
import os

import h5py
import json
import numpy as np
import configparser
import warnings

from pesummary.core.file.formats.base_read import Read
from pesummary.utils.samples_dict import (
    MCMCSamplesDict, MultiAnalysisSamplesDict, SamplesDict, Array
)
from pesummary.utils.utils import logger


deprecation_warning = (
    "This file format is out-of-date and may not be supported in future "
    "releases."
)


class PESummary(Read):
    """This class handles the existing posterior_samples.h5 file

    Parameters
    ----------
    path_to_results_file: str
        path to the results file you wish to load

    Attributes
    ----------
    parameters: nd list
        list of parameters stored in the result file for each analysis stored
        in the result file
    samples: 3d list
        list of samples stored in the result file for each analysis stored
        in the result file
    samples_dict: nested dict
        nested dictionary of samples stored in the result file keyed by their
        respective label
    input_version: str
        version of the result file passed.
    extra_kwargs: list
        list of dictionaries containing kwargs that were extracted from each
        analysis
    injection_parameters: list
        list of dictionaries of injection parameters for each analysis
    injection_dict: dict
        dictionary containing the injection parameters keyed by their respective
        label
    prior: dict
        dictionary of prior samples stored in the result file
    config: dict
        dictionary containing the configuration file stored in the result file
    labels: list
        list of analyses stored in the result file
    weights: dict
        dictionary of weights for each sample for each analysis

    Methods
    -------
    to_dat:
        save the posterior samples to a .dat file
    to_bilby:
        convert the posterior samples to a bilby.core.result.Result object
    to_latex_table:
        convert the posterior samples to a latex table
    generate_latex_macros:
        generate a set of latex macros for the stored posterior samples
    write_config_to_file:
        write the config file stored in the result file to file
    """
    def __init__(self, path_to_results_file):
        super(PESummary, self).__init__(path_to_results_file)
        self.load(self._grab_data_from_pesummary_file, **self.load_kwargs)
        self.samples_dict = None

    @property
    def load_kwargs(self):
        return dict()

    @classmethod
    def load_file(cls, path):
        if os.path.isdir(path):
            files = glob(path + "/*")
            if "home.html" in files:
                path = glob(path + "/samples/posterior_samples*")[0]
            else:
                raise FileNotFoundError(
                    "Unable to find a file called 'posterior_samples' in "
                    "the directory %s" % (path + "/samples"))
        if not os.path.isfile(path):
            raise FileNotFoundError("%s does not exist" % path)
        return cls(path)

    @staticmethod
    def _grab_data_from_pesummary_file(path, **kwargs):
        """
        """
        func_map = {"h5": PESummary._grab_data_from_hdf5_file,
                    "hdf5": PESummary._grab_data_from_hdf5_file,
                    "json": PESummary._grab_data_from_json_file}
        return func_map[Read.extension_from_path(path)](path, **kwargs)

    @staticmethod
    def _convert_hdf5_to_dict(dictionary, path="/"):
        """
        """
        mydict = {}
        for key, item in dictionary[path].items():
            if isinstance(item, h5py._hl.dataset.Dataset):
                mydict[key] = np.array(item)
            elif isinstance(item, h5py._hl.group.Group):
                mydict[key] = PESummary._convert_hdf5_to_dict(
                    dictionary, path=path + key + "/")
        return mydict

    @staticmethod
    def _grab_data_from_hdf5_file(path, **kwargs):
        """
        """
        function = kwargs.get(
            "grab_data_from_dictionary", PESummary._grab_data_from_dictionary)
        f = h5py.File(path, 'r')
        data = PESummary._convert_hdf5_to_dict(f)
        existing_data = function(data)
        f.close()
        return existing_data

    @staticmethod
    def _grab_data_from_json_file(path, **kwargs):
        function = kwargs.get(
            "grab_data_from_dictionary", PESummary._grab_data_from_dictionary)
        with open(path) as f:
            data = json.load(f)
        return function(data)

    @staticmethod
    def _grab_data_from_dictionary(dictionary):
        """
        """
        labels = list(dictionary.keys())
        if "version" in labels:
            labels.remove("version")

        parameter_list, sample_list, inj_list, ver_list = [], [], [], []
        meta_data_list, weights_list = [], []
        prior_dict, config_dict = {}, {}
        mcmc_samples = False
        for num, label in enumerate(labels):
            if label == "version":
                continue
            data, = Read.load_recursively(label, dictionary)
            if "mcmc_chains" in data.keys():
                mcmc_samples = True
                dataset = data["mcmc_chains"]
                chains = list(dataset.keys())
                parameters = [j for j in dataset[chains[0]].dtype.names]
                samples = [
                    [np.array(j.tolist()) for j in dataset[chain]] for chain
                    in chains
                ]
            else:
                posterior_samples = data["posterior_samples"]
                new_format = (h5py._hl.dataset.Dataset, np.ndarray)
                if isinstance(posterior_samples, new_format):
                    parameters = [j for j in posterior_samples.dtype.names]
                    samples = [np.array(j.tolist()) for j in posterior_samples]
                else:
                    parameters = \
                        posterior_samples["parameter_names"].copy()
                    samples = [
                        j for j in posterior_samples["samples"]
                    ].copy()
                if isinstance(parameters[0], bytes):
                    parameters = [
                        parameter.decode("utf-8") for parameter in parameters
                    ]
            parameter_list.append(parameters)
            if "injection_data" in data.keys():
                inj = data["injection_data"]["injection_values"].copy()

                def parse_injection_value(_value):
                    if isinstance(_value, (list, np.ndarray)):
                        _value = _value[0]
                    if isinstance(_value, bytes):
                        _value = _value.decode("utf-8")
                    if isinstance(_value, str):
                        if _value.lower() == "nan":
                            _value = np.nan
                        elif _value.lower() == "none":
                            _value = None
                    return _value
                inj_list.append({
                    parameter: parse_injection_value(value)
                    for parameter, value in zip(parameters, inj)
                })
            sample_list.append(samples)
            config = None
            if "config_file" in data.keys():
                config = data["config_file"]
            config_dict[label] = config
            if "meta_data" in data.keys():
                meta_data_list.append(data["meta_data"])
            else:
                meta_data_list.append({"sampler": {}, "meta_data": {}})
            if "weights" in parameters or b"weights" in parameters:
                ind = (
                    parameters.index("weights") if "weights" in parameters
                    else parameters.index(b"weights")
                )
                weights_list.append(Array([sample[ind] for sample in samples]))
            else:
                weights_list.append(None)
            if "version" in data.keys():
                version = data["version"]
            else:
                version = "No version information found"
            ver_list.append(version)
            if "priors" in data.keys():
                priors = data["priors"]
            else:
                priors = dict()
            prior_dict[label] = priors
        reversed_prior_dict = {}
        for label in labels:
            for key, item in prior_dict[label].items():
                if key in reversed_prior_dict.keys():
                    reversed_prior_dict[key][label] = item
                else:
                    reversed_prior_dict.update({key: {label: item}})
        return {
            "parameters": parameter_list,
            "samples": sample_list,
            "injection": inj_list,
            "version": ver_list,
            "kwargs": meta_data_list,
            "weights": {i: j for i, j in zip(labels, weights_list)},
            "labels": labels,
            "config": config_dict,
            "prior": reversed_prior_dict,
            "mcmc_samples": mcmc_samples
        }

    @property
    def samples_dict(self):
        return self._samples_dict

    @samples_dict.setter
    def samples_dict(self, samples_dict):
        if self.mcmc_samples:
            outdict = MCMCSamplesDict(
                self.parameters[0], [np.array(i).T for i in self.samples[0]]
            )
        else:
            if all("log_likelihood" in i for i in self.parameters):
                likelihood_inds = [self.parameters[idx].index("log_likelihood")
                                   for idx in range(len(self.labels))]
                likelihoods = [[i[likelihood_inds[idx]] for i in self.samples[idx]]
                               for idx, label in enumerate(self.labels)]
            else:
                likelihoods = [None] * len(self.labels)
            outdict = MultiAnalysisSamplesDict({
                label:
                    SamplesDict(
                        self.parameters[idx], np.array(self.samples[idx]).T
                    ) for idx, label in enumerate(self.labels)
            })
        self._samples_dict = outdict

    @property
    def injection_dict(self):
        return {
            label: self.injection_parameters[num] for num, label in
            enumerate(self.labels)
        }

    @staticmethod
    def save_config_dictionary_to_file(config_dict, filename, outdir="./"):
        """Save a dictionary containing the configuration settings to a file

        Parameters
        ----------
        config_dict: dict
            dictionary containing the configuration settings
        filename: str
            the name of the file you wish to write to
        outdir: str, optional
            path indicating where you would like to configuration file to be
            saved. Default is current working directory
        """
        config = configparser.ConfigParser()
        config.optionxform = str
        if config_dict is None:
            logger.warn("No config data found. Unable to write to file")
            return

        for key in config_dict.keys():
            config[key] = config_dict[key]

        with open("%s/%s" % (outdir, filename), "w") as configfile:
            config.write(configfile)

    def write_config_to_file(self, label, outdir="./"):
        """Write the config file stored as a dictionary to file

        Parameters
        ----------
        label: str
            the label for the dictionary that you would like to write to file
        outdir: str, optional
            path indicating where you would like to configuration file to be
            saved. Default is current working directory
        """
        if label not in list(self.config.keys()):
            raise ValueError("The label %s does not exist." % label)
        self.save_config_dictionary_to_file(
            self.config[label], outdir=outdir,
            filename="%s_config.ini" % (label)
        )

    def to_bilby(self):
        """Convert a PESummary metafile to a bilby results object
        """
        from bilby.core.result import Result
        from bilby.core.prior import Prior, PriorDict
        from pandas import DataFrame

        objects = dict()
        for num, label in enumerate(self.labels):
            priors = PriorDict()
            logger.warn(
                "No prior information is known so setting it to a default")
            priors.update({parameter: Prior() for parameter in self.parameters[num]})
            posterior_data_frame = DataFrame(
                self.samples[num], columns=self.parameters[num])
            bilby_object = Result(
                search_parameter_keys=self.parameters[num],
                posterior=posterior_data_frame, label="pesummary_%s" % label,
                samples=self.samples[num], priors=priors)
            objects[label] = bilby_object
        return objects

    def to_dat(self, label="all", outdir="./"):
        """Convert the samples stored in a PESummary metafile to a .dat file

        Parameters
        ----------
        label: str, optional
            the label of the analysis that you wish to save. By default, all
            samples in the metafile will be saved to seperate files
        outdir: str, optional
            path indicating where you would like to configuration file to be
            saved. Default is current working directory
        """
        if label != "all" and label not in list(self.labels) and label is not None:
            raise ValueError("The label %s does not exist." % label)
        if label == "all" or label is None:
            labels = list(self.labels)
        else:
            labels = [label]
        for num, label in enumerate(labels):
            ind = self.labels.index(label)
            np.savetxt(
                "%s/pesummary_%s.dat" % (outdir, label), self.samples[ind],
                delimiter="\t", header="\t".join(self.parameters[ind]),
                comments='')

    def to_latex_table(self, labels="all", parameter_dict=None, save_to_file=None):
        """Make a latex table displaying the data in the result file.

        Parameters
        ----------
        labels: list, optional
            list of labels that you want to include in the table
        parameter_dict: dict, optional
            dictionary of parameters that you wish to include in the latex
            table. The keys are the name of the parameters and the items are
            the descriptive text. If None, all parameters are included
        save_to_file: str, optional
            name of the file you wish to save the latex table to. If None, print
            to stdout
        """
        import os

        if save_to_file is not None and os.path.isfile("{}".format(save_to_file)):
            raise FileExistsError(
                "The file {} already exists.".format(save_to_file)
            )
        if labels != "all" and isinstance(labels, str) and labels not in self.labels:
            raise ValueError("The label %s does not exist." % (labels))
        elif labels == "all":
            labels = list(self.labels)
        elif isinstance(labels, str):
            labels = [labels]
        elif isinstance(labels, list):
            for ll in labels:
                if ll not in list(self.labels):
                    raise ValueError("The label %s does not exist." % (ll))

        table = self.latex_table(
            [self.samples_dict[label] for label in labels], parameter_dict,
            labels=labels
        )
        if save_to_file is None:
            print(table)
        elif os.path.isfile("{}".format(save_to_file)):
            logger.warn(
                "File {} already exists. Printing to stdout".format(save_to_file)
            )
            print(table)
        else:
            with open(save_to_file, "w") as f:
                f.writelines([table])

    def generate_latex_macros(
        self, labels="all", parameter_dict=None, save_to_file=None,
        rounding=2
    ):
        """Generate a list of latex macros for each parameter in the result
        file

        Parameters
        ----------
        labels: list, optional
            list of labels that you want to include in the table
        parameter_dict: dict, optional
            dictionary of parameters that you wish to generate macros for. The
            keys are the name of the parameters and the items are the latex
            macros name you wish to use. If None, all parameters are included.
        save_to_file: str, optional
            name of the file you wish to save the latex table to. If None, print
            to stdout
        rounding: int, optional
            number of decimal points to round the latex macros
        """
        import os

        if save_to_file is not None and os.path.isfile("{}".format(save_to_file)):
            raise FileExistsError(
                "The file {} already exists.".format(save_to_file)
            )
        if labels != "all" and isinstance(labels, str) and labels not in self.labels:
            raise ValueError("The label %s does not exist." % (labels))
        elif labels == "all":
            labels = list(self.labels)
        elif isinstance(labels, str):
            labels = [labels]
        elif isinstance(labels, list):
            for ll in labels:
                if ll not in list(self.labels):
                    raise ValueError("The label %s does not exist." % (ll))

        macros = self.latex_macros(
            [self.samples_dict[i] for i in labels], parameter_dict,
            labels=labels, rounding=rounding
        )
        if save_to_file is None:
            print(macros)
        else:
            with open(save_to_file, "w") as f:
                f.writelines([macros])


class PESummaryDeprecated(PESummary):
    """
    """
    def __init__(self, path_to_results_file):
        warnings.warn(deprecation_warning)
        super(PESummaryDeprecated, self).__init__(path_to_results_file)

    @property
    def load_kwargs(self):
        return {
            "grab_data_from_dictionary": PESummaryDeprecated._grab_data_from_dictionary
        }

    @staticmethod
    def _grab_data_from_dictionary(dictionary):
        """
        """
        labels = list(dictionary["posterior_samples"].keys())

        parameter_list, sample_list, inj_list, ver_list = [], [], [], []
        meta_data_list, weights_list = [], []
        for num, label in enumerate(labels):
            posterior_samples = dictionary["posterior_samples"][label]
            if isinstance(posterior_samples, (h5py._hl.dataset.Dataset, np.ndarray)):
                parameters = [j for j in posterior_samples.dtype.names]
                samples = [np.array(j.tolist()) for j in posterior_samples]
            else:
                parameters = \
                    dictionary["posterior_samples"][label]["parameter_names"].copy()
                samples = [
                    j for j in dictionary["posterior_samples"][label]["samples"]
                ].copy()
                if isinstance(parameters[0], bytes):
                    parameters = [
                        parameter.decode("utf-8") for parameter in parameters
                    ]
            parameter_list.append(parameters)
            if "injection_data" in dictionary.keys():
                inj = dictionary["injection_data"][label]["injection_values"].copy()

                def parse_injection_value(_value):
                    if isinstance(_value, (list, np.ndarray)):
                        _value = _value[0]
                    if isinstance(_value, bytes):
                        _value = _value.decode("utf-8")
                    if isinstance(_value, str):
                        if _value.lower() == "nan":
                            _value = np.nan
                        elif _value.lower() == "none":
                            _value = None
                    return _value
                inj_list.append({
                    parameter: parse_injection_value(value)
                    for parameter, value in zip(parameters, inj)
                })
            sample_list.append(samples)
            config = None
            if "config_file" in dictionary.keys():
                config, = Read.load_recursively("config_file", dictionary)
            if "meta_data" in dictionary.keys():
                data, = Read.load_recursively("meta_data", dictionary)
                meta_data_list.append(data[label])
            else:
                meta_data_list.append({"sampler": {}, "meta_data": {}})
            if "weights" in parameters or b"weights" in parameters:
                ind = (
                    parameters.index("weights") if "weights" in parameters
                    else parameters.index(b"weights")
                )
                weights_list.append(Array([sample[ind] for sample in samples]))
            else:
                weights_list.append(None)
        if "version" in dictionary.keys():
            version, = Read.load_recursively("version", dictionary)
        else:
            version = {label: "No version information found" for label in labels
                       + ["pesummary"]}
        if "priors" in dictionary.keys():
            priors, = Read.load_recursively("priors", dictionary)
        else:
            priors = dict()
        for label in list(version.keys()):
            if label != "pesummary" and isinstance(version[label], bytes):
                ver_list.append(version[label].decode("utf-8"))
            elif label != "pesummary":
                ver_list.append(version[label])
            elif isinstance(version["pesummary"], bytes):
                version["pesummary"] = version["pesummary"].decode("utf-8")
        return {
            "parameters": parameter_list,
            "samples": sample_list,
            "injection": inj_list,
            "version": ver_list,
            "kwargs": meta_data_list,
            "weights": {i: j for i, j in zip(labels, weights_list)},
            "labels": labels,
            "config": config,
            "prior": priors
        }
