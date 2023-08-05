# Copyright (C) 2019 Charlie Hoy <charlie.hoy@ligo.org>
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

import os
import re
import socket
from glob import glob
import pkg_resources

import numpy as np
import pesummary
from pesummary.core.file.read import read as Read
from pesummary.utils.exceptions import InputError
from pesummary.utils.samples_dict import SamplesDict, MCMCSamplesDict
from pesummary.utils.utils import (
    guess_url, logger, make_dir, make_cache_style_file
)
from pesummary import conf


class _Input(object):
    """Super class to handle the command line arguments
    """
    @staticmethod
    def is_pesummary_metafile(proposed_file):
        """Determine if a file is a PESummary metafile or not

        Parameters
        ----------
        proposed_file: str
            path to the file
        """
        extension = proposed_file.split(".")[-1]
        if extension == "h5" or extension == "hdf5" or extension == "hdf":
            from pesummary.core.file.read import (
                is_pesummary_hdf5_file, is_pesummary_hdf5_file_deprecated
            )

            result = any(
                func(proposed_file) for func in [
                    is_pesummary_hdf5_file,
                    is_pesummary_hdf5_file_deprecated
                ]
            )
            return result
        elif extension == "json":
            from pesummary.core.file.read import (
                is_pesummary_json_file, is_pesummary_json_file_deprecated
            )

            result = any(
                func(proposed_file) for func in [
                    is_pesummary_json_file,
                    is_pesummary_json_file_deprecated
                ]
            )
            return result
        else:
            return False

    @staticmethod
    def grab_data_from_metafile(
        existing_file, webdir, compare=None, read_function=Read, **kwargs
    ):
        """Grab data from an existing PESummary metafile

        Parameters
        ----------
        existing_file: str
            path to the existing metafile
        webdir: str
            the directory to store the existing configuration file
        compare: list, optional
            list of labels for events stored in an existing metafile that you
            wish to compare
        read_function: func, optional
            PESummary function to use to read in the existing file
        kwargs: dict
            All kwargs are passed to the `generate_all_posterior_samples`
            method
        """
        f = read_function(existing_file)
        if not f.mcmc_samples:
            f.generate_all_posterior_samples(**kwargs)
            labels = f.labels
            indicies = np.arange(len(labels))
        else:
            labels = list(f.samples_dict.keys())
            indicies = np.arange(len(labels))

        if compare:
            indicies = []
            for i in compare:
                if i not in labels:
                    raise InputError(
                        "Label '%s' does not exist in the metafile. The list "
                        "of available labels are %s" % (i, labels)
                    )
                indicies.append(labels.index(i))
            labels = compare

        parameters = f.parameters
        if not f.mcmc_samples:
            samples = [np.array(i).T for i in f.samples]
            DataFrame = {
                label: SamplesDict(parameters[ind], samples[ind])
                for label, ind in zip(labels, indicies)
            }
            _parameters = lambda label: DataFrame[label].keys()
        else:
            DataFrame = {
                f.labels[0]: MCMCSamplesDict(
                    {
                        label: f.samples_dict[label] for label in labels
                    }
                )
            }
            labels = f.labels
            indicies = np.arange(len(labels))
            _parameters = lambda label: DataFrame[f.labels[0]].parameters
        if f.injection_parameters != []:
            inj_values = f.injection_dict
            for label in labels:
                for param in DataFrame[label].keys():
                    if param not in f.injection_dict[label].keys():
                        f.injection_dict[label][param] = float("nan")
        else:
            inj_values = {
                i: [float("nan")] * len(DataFrame[i]) for i in labels
            }
        for i in inj_values.keys():
            for param in inj_values[i].keys():
                if inj_values[i][param] == "nan":
                    inj_values[i][param] = float("nan")
                if isinstance(inj_values[i][param], bytes):
                    inj_values[i][param] = inj_values[i][param].decode("utf-8")

        if hasattr(f, "priors") and f.priors != {}:
            priors = f.priors
        else:
            priors = {label: {} for label in labels}

        config = []
        if f.config is not None and not all(i is None for i in f.config):
            config = []
            for i in labels:
                config_dir = os.path.join(webdir, "config")
                f.write_config_to_file(i, outdir=config_dir)
                config_file = os.path.join(
                    config_dir, "{}_config.ini".format(i)
                )
                config.append(config_file)
        else:
            for i in labels:
                config.append(None)

        if f.weights is not None:
            weights = {i: f.weights[i] for i in labels}
        else:
            weights = {i: None for i in labels}

        return {
            "samples": DataFrame,
            "injection_data": inj_values,
            "file_version": {
                i: j for i, j in zip(
                    labels, [f.input_version[ind] for ind in indicies]
                )
            },
            "file_kwargs": {
                i: j for i, j in zip(
                    labels, [f.extra_kwargs[ind] for ind in indicies]
                )
            },
            "prior": priors,
            "config": config,
            "labels": labels,
            "weights": weights,
            "indicies": indicies,
            "mcmc_samples": f.mcmc_samples
        }

    @staticmethod
    def grab_data_from_file(
        file, label, config=None, injection=None, read_function=Read,
        file_format=None, **kwargs
    ):
        """Grab data from a result file containing posterior samples

        Parameters
        ----------
        file: str
            path to the result file
        label: str
            label that you wish to use for the result file
        config: str, optional
            path to a configuration file used in the analysis
        injection: str, optional
            path to an injection file used in the analysis
        read_function: func, optional
            PESummary function to use to read in the file
        file_format, str, optional
            the file format you wish to use when loading. Default None.
            If None, the read function loops through all possible options
        kwargs: dict
            Dictionary of keyword arguments fed to the
            `generate_all_posterior_samples` method
        """
        f = read_function(file, file_format=file_format)
        if config is not None:
            f.add_fixed_parameters_from_config_file(config)

        f.generate_all_posterior_samples(**kwargs)
        if injection:
            f.add_injection_parameters_from_file(injection)
        parameters = f.parameters
        samples = np.array(f.samples).T
        DataFrame = {label: SamplesDict(parameters, samples)}
        kwargs = f.extra_kwargs
        if hasattr(f, "injection_parameters"):
            injection = f.injection_parameters
            if injection is not None:
                for i in parameters:
                    if i not in list(injection.keys()):
                        injection[i] = float("nan")
            else:
                injection = {i: j for i, j in zip(
                    parameters, [float("nan")] * len(parameters))}
        else:
            injection = {i: j for i, j in zip(
                parameters, [float("nan")] * len(parameters))}
        version = f.input_version
        if hasattr(f, "priors"):
            priors = f.priors
        else:
            priors = []
        if hasattr(f, "weights"):
            weights = f.weights
        else:
            weights = None
        return {
            "samples": DataFrame,
            "injection_data": {label: injection},
            "file_version": {label: version},
            "file_kwargs": {label: kwargs},
            "prior": {label: priors},
            "weights": {label: weights}
        }

    @property
    def existing(self):
        return self._existing

    @existing.setter
    def existing(self, existing):
        self._existing = existing
        if existing is not None:
            self._existing = os.path.abspath(existing)

    @property
    def existing_metafile(self):
        return self._existing_metafile

    @existing_metafile.setter
    def existing_metafile(self, existing_metafile):
        from glob import glob

        self._existing_metafile = existing_metafile
        if not os.path.isdir(os.path.join(self.existing, "samples")):
            raise InputError("Please provide a valid existing directory")
        files = glob(
            os.path.join(self.existing, "samples", "posterior_samples*")
        )
        if len(files) == 0:
            raise InputError(
                "Unable to find an existing metafile in the existing webdir"
            )
        if len(files) > 1:
            raise InputError(
                "Multiple metafiles in the existing directory. Please either "
                "run the `summarycombine_metafile` executable to combine the "
                "meta files or simple remove the unwanted meta file"
            )
        self._existing_metafile = os.path.join(
            self.existing, "samples", files[0]
        )

    @property
    def style_file(self):
        return self._style_file

    @style_file.setter
    def style_file(self, style_file):
        default = conf.style_file
        if style_file is not None and not os.path.isfile(style_file):
            logger.warn(
                "The file '{}' does not exist. Resorting to default".format(
                    style_file
                )
            )
            style_file = default
        elif style_file is not None and os.path.isfile(style_file):
            logger.info(
                "Using the file '{}' as the matplotlib style file".format(
                    style_file
                )
            )
        elif style_file is None:
            logger.debug(
                "Using the default matplotlib style file"
            )
            style_file = default
        make_cache_style_file(style_file)
        self._style_file = style_file

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        try:
            self._user = os.environ["USER"]
            logger.info(
                conf.overwrite.format("user", conf.user, self._user)
            )
        except KeyError as e:
            logger.info(
                "Failed to grab user information because {}. Default will be "
                "used".format(e)
            )
            self._user = user

    @property
    def host(self):
        return socket.getfqdn()

    @property
    def webdir(self):
        return self._webdir

    @webdir.setter
    def webdir(self, webdir):
        cond1 = webdir is None or webdir == "None" or webdir == "none"
        cond2 = (
            self.existing is None or self.existing == "None"
            or self.existing == "none"
        )
        if cond1 and cond2:
            raise InputError(
                "Please provide a web directory to store the webpages. If "
                "you wish to add to an existing webpage, then pass the "
                "existing web directory under the '--existing_webdir' command "
                "line argument. If this is a new set of webpages, then pass "
                "the web directory under the '--webdir' argument"
            )
        elif webdir is None and self.existing is not None:
            if not os.path.isdir(self.existing):
                raise InputError(
                    "The directory {} does not exist".format(self.existing)
                )
            entries = glob(self.existing + "/*")
            if os.path.join(self.existing, "home.html") not in entries:
                raise InputError(
                    "Please give the base directory of an existing output"
                )
            self._webdir = self.existing
        else:
            if not os.path.isdir(webdir):
                logger.debug(
                    "Given web directory does not exist. Creating it now"
                )
                make_dir(webdir)
            self._webdir = os.path.abspath(webdir)

    @property
    def baseurl(self):
        return self._baseurl

    @baseurl.setter
    def baseurl(self, baseurl):
        self._baseurl = baseurl
        if baseurl is None:
            self._baseurl = guess_url(self.webdir, self.host, self.user)

    @property
    def mcmc_samples(self):
        return self._mcmc_samples

    @mcmc_samples.setter
    def mcmc_samples(self, mcmc_samples):
        self._mcmc_samples = mcmc_samples
        if self._mcmc_samples:
            logger.info(
                "Treating all samples as seperate mcmc chains for the same "
                "analysis."
            )

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels):
        if not hasattr(self, "._labels"):
            if labels is None:
                labels = self.default_labels()
            elif self.mcmc_samples and len(labels) != 1:
                raise InputError(
                    "Please provide a single label that corresponds to all "
                    "mcmc samples"
                )
            elif len(np.unique(labels)) != len(labels):
                raise InputError(
                    "Please provide unique labels for each result file"
                )
            for num, i in enumerate(labels):
                if "." in i:
                    logger.warn(
                        "Replacing the label {} by {} to make it compatible "
                        "with the html pages".format(i, i.replace(".", "_"))
                    )
                    labels[num] = i.replace(".", "_")
            if self.add_to_existing:
                for i in labels:
                    if i in self.existing_labels:
                        raise InputError(
                            "The label '%s' already exists in the existing "
                            "metafile. Please pass another unique label"
                        )
            self._labels = labels

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        if config and len(config) != len(self.labels):
            raise InputError(
                "Please provide a configuration file for each label"
            )
        if config is None and not self.meta_file:
            self._config = [None] * len(self.labels)
        elif self.meta_file:
            self._config = [None] * len(self.labels)
        else:
            self._config = config

    @property
    def injection_file(self):
        return self._injection_file

    @injection_file.setter
    def injection_file(self, injection_file):
        if injection_file and len(injection_file) != len(self.labels):
            if len(injection_file) == 1:
                logger.info(
                    "Only one injection file passed. Assuming the same "
                    "injection for all {} result files".format(len(self.labels))
                )
            else:
                raise InputError(
                    "You have passed {} for {} result files. Please provide an "
                    "injection file for each result file".format(
                        len(self.injection_file), len(self.labels)
                    )
                )
        if injection_file is None:
            injection_file = [None] * len(self.labels)
        self._injection_file = injection_file

    @property
    def injection_data(self):
        return self._injection_data

    @property
    def file_version(self):
        return self._file_version

    @property
    def file_kwargs(self):
        return self._file_kwargs

    @property
    def kde_plot(self):
        return self._kde_plot

    @kde_plot.setter
    def kde_plot(self, kde_plot):
        self._kde_plot = kde_plot
        if kde_plot != conf.kde_plot:
            logger.info(
                conf.overwrite.format("kde_plot", conf.kde_plot, kde_plot)
            )

    @property
    def file_format(self):
        return self._file_format

    @file_format.setter
    def file_format(self, file_format):
        if file_format is None:
            self._file_format = [None] * len(self.labels)
        elif len(file_format) == 1 and len(file_format) != len(self.labels):
            logger.warn(
                "Only one file format specified. Assuming all files are of this format"
            )
            self._file_format = [file_format] * len(self.labels)
        elif len(file_format) != len(self.labels):
            raise InputError(
                "Please provide a file format for each result file"
            )
        else:
            self._file_format = file_format

    @property
    def samples(self):
        return self._samples

    @samples.setter
    def samples(self, samples):
        if isinstance(samples, dict):
            return samples
        self._set_samples(samples)

    def _set_samples(
        self, samples, ignore_keys=["prior", "weights", "labels", "indicies"]
    ):
        """Extract the samples and store them as attributes of self

        Parameters
        ----------
        samples: list
            A list containing the paths to result files
        ignore_keys: list, optional
            A list containing properties of the read file that you do not want to be
            stored as attributes of self
        """
        if not samples:
            raise InputError("Please provide a results file")
        if len(samples) != len(self.labels) and not self.mcmc_samples:
            logger.info(
                "You have passed {} result files and {} labels. Setting "
                "labels = {}".format(
                    len(samples), len(self.labels), self.labels[:len(samples)]
                )
            )
            self.labels = self.labels[:len(samples)]
        labels, labels_dict = None, {}
        weights_dict = {}
        if self.mcmc_samples:
            nsamples = 0.
        for num, i in enumerate(samples):
            idx = num
            if not self.mcmc_samples:
                logger.info("Assigning {} to {}".format(self.labels[num], i))
            else:
                num = 0
            if not os.path.isfile(i):
                raise InputError("File %s does not exist" % (i))
            if self.is_pesummary_metafile(samples[num]):
                data = self.grab_data_from_input(
                    i, self.labels[num], config=None, injection=None
                )
                self.mcmc_samples = data["mcmc_samples"]
            else:
                data = self.grab_data_from_input(
                    i, self.labels[num], config=self.config[num],
                    injection=self.injection_file[num],
                    file_format=self.file_format[num]
                )
                if self.mcmc_samples:
                    data["samples"] = {
                        "{}_mcmc_chain_{}".format(key, idx): item for key, item
                        in data["samples"].items()
                    }
            for key, item in data.items():
                if key not in ignore_keys:
                    if idx == 0:
                        setattr(self, "_{}".format(key), item)
                    else:
                        x = getattr(self, "_{}".format(key))
                        if isinstance(x, dict):
                            x.update(item)
                        elif isinstance(x, list):
                            x += item
                        setattr(self, "_{}".format(key), x)
            if self.mcmc_samples:
                try:
                    nsamples += data["file_kwargs"][self.labels[num]]["sampler"][
                        "nsamples"
                    ]
                except UnboundLocalError:
                    pass
            if "labels" in data.keys():
                stored_labels = data["labels"]
            else:
                stored_labels = [self.labels[num]]
            if "weights" in data.items():
                weights_dict = data["weights"]
            if "prior" in data.keys():
                for label in stored_labels:
                    pp = data["prior"]
                    if pp != {} and label in pp.keys() and pp[label] == []:
                        if len(self.priors):
                            if label not in self.priors["samples"].keys():
                                self.add_to_prior_dict(
                                    "samples/{}".format(label), []
                                )
                        else:
                            self.add_to_prior_dict(
                                "samples/{}".format(label), []
                            )
                    elif pp != {} and label not in pp.keys():
                        for key in pp.keys():
                            if key in self.priors.keys():
                                if label in self.priors[key].keys():
                                    logger.warn(
                                        "Replacing the prior file for {} "
                                        "with the prior file stored in "
                                        "the result file".format(
                                            label
                                        )
                                    )
                            if pp[key] == {}:
                                self.add_to_prior_dict(
                                    "{}/{}".format(key, label), []
                                )
                            elif label not in pp[key].keys():
                                self.add_to_prior_dict(
                                    "{}/{}".format(key, label), []
                                )
                            else:
                                self.add_to_prior_dict(
                                    "{}/{}".format(key, label), pp[key][label]
                                )
                    else:
                        self.add_to_prior_dict(
                            "samples/{}".format(label), []
                        )
            if "labels" in data.keys():
                if num == 0:
                    labels = data["labels"]
                else:
                    labels += data["labels"]
                labels_dict[num] = data["labels"]
        if self.mcmc_samples:
            try:
                self.file_kwargs[self.labels[0]]["sampler"].update(
                    {"nsamples": nsamples, "nchains": len(self.result_files)}
                )
            except (KeyError, UnboundLocalError):
                pass
            _labels = list(self._samples.keys())
            if not isinstance(self._samples[_labels[0]], MCMCSamplesDict):
                self._samples = MCMCSamplesDict(self._samples)
            else:
                self._samples = self._samples[_labels[0]]
        if labels is not None:
            self._labels = labels
            if len(labels) != len(self.result_files):
                result_files = []
                for num, f in enumerate(samples):
                    for ii in np.arange(len(labels_dict[num])):
                        result_files.append(self.result_files[num])
                self.result_files = result_files
            self.weights = {i: None for i in self.labels}
        if weights_dict != {}:
            self.weights = weights_dict

    @property
    def burnin_method(self):
        return self._burnin_method

    @burnin_method.setter
    def burnin_method(self, burnin_method):
        self._burnin_method = burnin_method
        if not self.mcmc_samples and burnin_method is not None:
            logger.info(
                "The {} method will not be used to remove samples as "
                "burnin as this can only be used for mcmc chains.".format(
                    burnin_method
                )
            )
            self._burnin_method = None
        elif self.mcmc_samples and burnin_method is None:
            logger.info(
                "No burnin method provided. Using {} as default".format(
                    conf.burnin_method
                )
            )
            self._burnin_method = conf.burnin_method
        elif self.mcmc_samples:
            from pesummary.core.file import mcmc

            if burnin_method not in mcmc.algorithms:
                logger.warn(
                    "Unrecognised burnin method: {}. Resorting to the default: "
                    "{}".format(burnin_method, conf.burnin_method)
                )
                self._burnin_method = conf.burnin_method
        if self._burnin_method is not None:
            for label in self.labels:
                self.file_kwargs[label]["sampler"]["burnin_method"] = (
                    self._burnin_method
                )

    @property
    def burnin(self):
        return self._burnin

    @burnin.setter
    def burnin(self, burnin):
        _name = "nsamples_removed_from_burnin"
        if burnin is not None:
            samples_lengths = [
                self.samples[key].number_of_samples for key in
                self.samples.keys()
            ]
            if not all(int(burnin) < i for i in samples_lengths):
                raise InputError(
                    "The chosen burnin is larger than the number of samples. "
                    "Please choose a value less than {}".format(
                        np.max(samples_lengths)
                    )
                )
            logger.info(
                conf.overwrite.format("burnin", conf.burnin, burnin)
            )
            burnin = int(burnin)
        else:
            burnin = conf.burnin
        if self.burnin_method is not None:
            arguments, kwargs = [], {}
            if burnin != 0 and self.burnin_method == "burnin_by_step_number":
                logger.warn(
                    "The first {} samples have been requested to be removed "
                    "as burnin, but the burnin method has been chosen to be "
                    "burnin_by_step_number. Changing method to "
                    "burnin_by_first_n with keyword argument step_number="
                    "True such that all samples with step number < {} are "
                    "removed".format(burnin, burnin)
                )
                self.burnin_method = "burnin_by_first_n"
                arguments = [burnin]
                kwargs = {"step_number": True}
            elif self.burnin_method == "burnin_by_first_n":
                arguments = [burnin]
            initial = self.samples.total_number_of_samples
            self._samples = self.samples.burnin(
                *arguments, algorithm=self.burnin_method, **kwargs
            )
            diff = initial - self.samples.total_number_of_samples
            self.file_kwargs[self.labels[0]]["sampler"][_name] = diff
            self.file_kwargs[self.labels[0]]["sampler"]["nsamples"] = \
                self._samples.total_number_of_samples
        else:
            for label in self.samples:
                self.samples[label] = self.samples[label].discard_samples(
                    burnin
                )
                if burnin != conf.burnin:
                    self.file_kwargs[label]["sampler"][_name] = burnin

    @property
    def nsamples(self):
        return self._nsamples

    @nsamples.setter
    def nsamples(self, nsamples):
        if nsamples is not None:
            samples_lengths = [
                self.samples[key].number_of_samples for key in
                self.samples.keys()
            ]
            for num, label in enumerate(self.samples):
                if int(nsamples) < samples_lengths[num]:
                    self.samples[label] = self.samples[label].downsample(
                        int(nsamples)
                    )
                    self.file_kwargs[label]["sampler"]["nsamples"] = int(
                        nsamples
                    )
                else:
                    logger.warn(
                        "Failed to downsample {} to {} because {} is greater "
                        "than the number of samples in the file. Igorning and "
                        "and using all available samples".format(
                            self.result_files[num], int(nsamples), int(nsamples)
                        )
                    )

    @property
    def priors(self):
        return self._priors

    @priors.setter
    def priors(self, priors):
        self._priors = self.grab_priors_from_inputs(priors)

    @property
    def custom_plotting(self):
        return self._custom_plotting

    @custom_plotting.setter
    def custom_plotting(self, custom_plotting):
        self._custom_plotting = custom_plotting
        if custom_plotting is not None:
            import importlib

            path_to_python_file = os.path.dirname(custom_plotting)
            python_file = os.path.splitext(os.path.basename(custom_plotting))[0]
            if path_to_python_file != "":
                import sys

                sys.path.append(path_to_python_file)
            try:
                mod = importlib.import_module(python_file)
                methods = getattr(mod, "__single_plots__", list()).copy()
                methods += getattr(mod, "__comparion_plots__", list()).copy()
                if len(methods) > 0:
                    self._custom_plotting = [path_to_python_file, python_file]
                else:
                    logger.warn(
                        "No __single_plots__ or __comparison_plots__ in {}. "
                        "If you wish to use custom plotting, then please "
                        "add the variable :__single_plots__ and/or "
                        "__comparison_plots__ in future. No custom plotting "
                        "will be done"
                    )
            except ModuleNotFoundError as e:
                logger.warn(
                    "Failed to import {} because {}. No custom plotting will "
                    "be done".format(python_file, e)
                )

    def add_to_prior_dict(self, path, data):
        """Add priors to the prior dictionary

        Parameters
        ----------
        path: str
            the location where you wish to store the prior. If this is inside
            a nested dictionary, then please pass the path as 'a/b'
        data: np.ndarray
            the prior samples
        """
        from functools import reduce

        def build_tree(dictionary, path):
            """Build a dictionary tree from a list of keys

            Parameters
            ----------
            dictionary: dict
                existing dictionary that you wish to add to
            path: list
                list of keys specifying location

            Examples
            --------
            >>> dictionary = {"label": {"mass_1": [1,2,3,4,5,6]}}
            >>> path = ["label", "mass_2"]
            >>> build_tree(dictionary, path)
            {"label": {"mass_1": [1,2,3,4,5,6], "mass_2": {}}}
            """
            if path != [] and path[0] not in dictionary.keys():
                dictionary[path[0]] = {}
            if path != []:
                build_tree(dictionary[path[0]], path[1:])
            return dictionary

        def get_nested_dictionary(dictionary, path):
            """Return a nested dictionary from a list specifying path

            Parameters
            ----------
            dictionary: dict
                existing dictionary that you wish to extract information from
            path: list
                list of keys specifying location

            Examples
            --------
            >>> dictionary = {"label": {"mass_1": [1,2,3,4,5,6]}}
            >>> path = ["label", "mass_1"]
            >>> get_nested_dictionary(dictionary, path)
            [1,2,3,4,5,6]
            """
            return reduce(dict.get, path, dictionary)

        if "/" in path:
            path = path.split("/")
        else:
            path = [path]
        tree = build_tree(self._priors, path)
        nested_dictionary = get_nested_dictionary(self._priors, path[:-1])
        nested_dictionary[path[-1]] = data

    def grab_priors_from_inputs(self, priors):
        """
        """
        from pesummary.core.file.read import read as Read

        prior_dict = {}
        if priors is not None:
            prior_dict = {"samples": {}}
            for i in priors:
                if not os.path.isfile(i):
                    raise InputError("The file {} does not exist".format(i))
            if len(priors) != len(self.labels) and len(priors) == 1:
                logger.warn(
                    "You have only specified a single prior file for {} result "
                    "files. Assuming the same prior file for all result "
                    "files".format(len(self.labels))
                )
                data = Read(priors[0])
                for i in self.labels:
                    prior_dict["samples"][i] = data.samples_dict
            elif len(priors) != len(self.labels):
                raise InputError(
                    "Please provide a prior file for each result file"
                )
            else:
                for num, i in enumerate(priors):
                    logger.info(
                        "Assigning {} to {}".format(self.labels[num], i)
                    )
                    data = Read(priors[num])
                    prior_dict["samples"][self.labels[num]] = data.samples_dict
        return prior_dict

    @property
    def grab_data_kwargs(self):
        return {
            label: dict(regenerate=self.regenerate) for label in self.labels
        }

    def grab_data_from_input(
        self, file, label, config=None, injection=None, file_format=None
    ):
        """Wrapper function for the grab_data_from_metafile and
        grab_data_from_file functions

        Parameters
        ----------
        file: str
            path to the result file
        label: str
            label that you wish to use for the result file
        config: str, optional
            path to a configuration file used in the analysis
        injection: str, optional
            path to an injection file used in the analysis
        file_format, str, optional
            the file format you wish to use when loading. Default None.
            If None, the read function loops through all possible options
        mcmc: Bool, optional
            if True, the result file is an mcmc chain
        """
        if label in self.grab_data_kwargs.keys():
            grab_data_kwargs = self.grab_data_kwargs[label]
        else:
            grab_data_kwargs = self.grab_data_kwargs
        if self.is_pesummary_metafile(file):
            existing_data = self.grab_data_from_metafile(
                file, self.webdir, compare=self.compare_results,
                **grab_data_kwargs
            )
            return existing_data
        else:
            data = self.grab_data_from_file(
                file, label, config=config, injection=injection,
                file_format=file_format, **grab_data_kwargs
            )
            return data

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if email is not None and "@" not in email:
            raise InputError("Please provide a valid email address")
        self._email = email

    @property
    def dump(self):
        return self._dump

    @dump.setter
    def dump(self, dump):
        self._dump = dump

    @property
    def palette(self):
        return self._palette

    @palette.setter
    def palette(self, palette):
        self._palette = palette
        if palette is not conf.palette:
            import seaborn

            try:
                seaborn.color_palette(palette, n_colors=1)
                logger.info(
                    conf.overwrite.format("palette", conf.palette, palette)
                )
                conf.palette = palette
            except ValueError as e:
                raise InputError(
                    "Unrecognised palette. Please choose from one of the "
                    "following {}".format(
                        ", ".join(seaborn.palettes.SEABORN_PALETTES.keys())
                    )
                )

    @property
    def include_prior(self):
        return self._include_prior

    @include_prior.setter
    def include_prior(self, include_prior):
        self._include_prior = include_prior
        if include_prior != conf.include_prior:
            conf.overwrite.format("prior", conf.include_prior, include_prior)
            conf.include_prior = include_prior

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, colors):
        if colors is not None:
            number = len(self.labels)
            if self.existing:
                number += len(self.existing_labels)
            if len(colors) != number and len(colors) > number:
                logger.info(
                    "You have passed {} colors for {} result files. Setting "
                    "colors = {}".format(
                        len(colors), number, colors[:number]
                    )
                )
                self._colors = colors[:number]
                return
            elif len(colors) != number:
                logger.warn(
                    "Number of colors does not match the number of labels. "
                    "Using default colors"
                )
        import seaborn

        number = len(self.labels)
        if self.existing:
            number += len(self.existing_labels)
        colors = seaborn.color_palette(
            palette=conf.palette, n_colors=number
        ).as_hex()
        self._colors = colors

    @property
    def linestyles(self):
        return self._linestyles

    @linestyles.setter
    def linestyles(self, linestyles):
        if linestyles is not None:
            if len(linestyles) != len(self.colors):
                if len(linestyles) > len(self.colors):
                    logger.info(
                        "You have passed {} linestyles for {} result files. "
                        "Setting linestyles = {}".format(
                            len(linestyles), len(self.colors),
                            linestyles[:len(self.colors)]
                        )
                    )
                    self._linestyles = linestyles[:len(self.colors)]
                    return
                else:
                    logger.warn(
                        "Number of linestyles does not match the number of "
                        "labels. Using default linestyles"
                    )
        available_linestyles = ["-", "--", ":", "-."]
        linestyles = ["-"] * len(self.colors)
        unique_colors = np.unique(self.colors)
        for color in unique_colors:
            indicies = [num for num, i in enumerate(self.colors) if i == color]
            for idx, j in enumerate(indicies):
                linestyles[j] = available_linestyles[
                    np.mod(idx, len(available_linestyles))
                ]
        self._linestyles = linestyles

    @property
    def disable_corner(self):
        return self._disable_corner

    @disable_corner.setter
    def disable_corner(self, disable_corner):
        self._disable_corner = disable_corner
        if disable_corner:
            logger.warn(
                "No corner plot will be produced. This will reduce overall "
                "runtime but does mean that the interactive corner plot feature "
                "on the webpages will no longer work"
            )

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        self._notes = notes
        if notes is not None:
            if not os.path.isfile(notes):
                raise InputError(
                    "No such file or directory called {}".format(notes)
                )
            try:
                with open(notes, "r") as f:
                    self._notes = f.read()
            except FileNotFoundError:
                logger.warn(
                    "No such file or directory called {}. Custom notes will "
                    "not be added to the summarypages".format(notes)
                )
            except IOError as e:
                logger.warn(
                    "Failed to read {}. Unable to put notes on "
                    "summarypages".format(notes)
                )

    @property
    def public(self):
        return self._public

    @public.setter
    def public(self, public):
        self._public = public
        if public != conf.public:
            logger.info(
                conf.overwrite.format("public", conf.public, public)
            )

    @property
    def multi_process(self):
        return self._multi_process

    @multi_process.setter
    def multi_process(self, multi_process):
        self._multi_process = int(multi_process)
        if multi_process is not None and int(multi_process) != int(conf.multi_process):
            logger.info(
                conf.overwrite.format(
                    "multi_process", conf.multi_process, multi_process
                )
            )

    @property
    def publication_kwargs(self):
        return self._publication_kwargs

    @publication_kwargs.setter
    def publication_kwargs(self, publication_kwargs):
        self._publication_kwargs = publication_kwargs
        if publication_kwargs != {}:
            allowed_kwargs = ["gridsize"]
            if not any(i in publication_kwargs.keys() for i in allowed_kwargs):
                logger.warn(
                    "Currently the only allowed publication kwargs are {}. "
                    "Ignoring other inputs.".format(
                        ", ".join(allowed_kwargs)
                    )
                )

    @property
    def ignore_parameters(self):
        return self._ignore_parameters

    @ignore_parameters.setter
    def ignore_parameters(self, ignore_parameters):
        self._ignore_parameters = ignore_parameters
        if ignore_parameters is not None:
            for num, label in enumerate(self.labels):
                removed_parameters = [
                    param for param in list(self.samples[label].keys()) for
                    ignore in ignore_parameters if re.match(
                        re.compile(ignore), param
                    )
                ]
                if removed_parameters == []:
                    logger.warn(
                        "Failed to remove any parameters from {}".format(
                            self.result_files[num]
                        )
                    )
                else:
                    logger.warn(
                        "Removing parameters: {} from {}".format(
                            ", ".join(removed_parameters),
                            self.result_files[num]
                        )
                    )
                    for ignore in removed_parameters:
                        self.samples[label].pop(ignore)

    @property
    def default_files_to_copy(self):
        files_to_copy = []
        path = pkg_resources.resource_filename("pesummary", "core")
        scripts = glob(os.path.join(path, "js", "*.js"))
        for i in scripts:
            files_to_copy.append(
                [i, os.path.join(self.webdir, "js", os.path.basename(i))]
            )
        scripts = glob(os.path.join(path, "css", "*.css"))
        for i in scripts:
            files_to_copy.append(
                [i, os.path.join(self.webdir, "css", os.path.basename(i))]
            )

        if not all(i is None for i in self.config):
            for num, i in enumerate(self.config):
                if i is not None and self.webdir not in i:
                    filename = "_".join(
                        [self.labels[num], "config.ini"]
                    )
                    files_to_copy.append(
                        [i, os.path.join(self.webdir, "config", filename)]
                    )
        return files_to_copy

    @staticmethod
    def _make_directories(webdir, dirs):
        """Make the directories to store the information
        """
        for i in dirs:
            if not os.path.isdir(os.path.join(webdir, i)):
                make_dir(os.path.join(webdir, i))

    def make_directories(self):
        """Make the directories to store the information
        """
        if self.publication:
            self.default_directories.append("plots/publication")
        self._make_directories(self.webdir, self.default_directories)

    @staticmethod
    def _copy_files(paths):
        """Copy the relevant file to the web directory

        Parameters
        ----------
        paths: nd list
            list of files you wish to copy. First element is the path of the
            file to copy and second element is the location of where you
            wish the file to be put

        Examples
        --------
        >>> paths = [
        ...    ["config/config.ini", "webdir/config.ini"],
        ...    ["samples/samples.h5", "webdir/samples.h5"]
        ... ]
        """
        import shutil

        for ff in paths:
            shutil.copyfile(ff[0], ff[1])

    def copy_files(self):
        """Copy the relevant file to the web directory
        """
        self._copy_files(self.default_files_to_copy)

    def default_labels(self):
        """Return a list of default labels.
        """
        from time import time

        def _default_label(file_name):
            return "%s_%s" % (round(time()), file_name)

        label_list = []
        if self.result_files is None or len(self.result_files) == 0:
            raise InputError("Please provide a results file")
        elif self.mcmc_samples:
            f = self.result_files[0]
            file_name = os.path.splitext(os.path.basename(f))[0]
            label_list.append(_default_label(file_name))
        else:
            for num, i in enumerate(self.result_files):
                file_name = os.path.splitext(os.path.basename(i))[0]
                label_list.append(_default_label(file_name))

        duplicates = dict(set(
            (x, label_list.count(x)) for x in
            filter(lambda rec: label_list.count(rec) > 1, label_list)))

        for i in duplicates.keys():
            for j in range(duplicates[i]):
                ind = label_list.index(i)
                label_list[ind] += "_%s" % (j)
        if self.add_to_existing:
            for num, i in enumerate(label_list):
                if i in self.existing_labels:
                    ind = label_list.index(i)
                    label_list[ind] += "_%s" % (num)
        return label_list

    @staticmethod
    def get_package_information():
        """Return a dictionary of parameter information
        """
        from pesummary._version_helper import PackageInformation
        from operator import itemgetter

        package_info = PackageInformation().package_info
        package_dir = PackageInformation().package_dir
        if "build_string" in package_info[0]:  # conda list
            headings = ("name", "version", "channel", "build_string")
        else:  # pip list installed
            headings = ("name", "version")
        packages = np.array([
            tuple(pkg[col.lower()] for col in headings) for pkg in
            sorted(package_info, key=itemgetter("name"))
        ], dtype=[(col, "S20") for col in headings]).view(np.recarray)
        return {"packages": packages, "environment": [package_dir]}


class Input(_Input):
    """Class to handle the core command line arguments

    Parameters
    ----------
    opts: argparse.Namespace
        Namespace object containing the command line options

    Attributes
    ----------
    result_files: list
        list of result files passed
    compare_results: list
        list of labels stored in the metafile that you wish to compare
    add_to_existing: Bool
        True if we are adding to an existing web directory
    existing_samples: dict
        dictionary of samples stored in an existing metafile. None if
        `self.add_to_existing` is False
    existing_injection_data: dict
        dictionary of injection data stored in an existing metafile. None if
        `self.add_to_existing` is False
    existing_file_version: dict
        dictionary of file versions stored in an existing metafile. None if
        `self.add_to_existing` is False
    existing_config: list
        list of configuration files stored in an existing metafile. None if
        `self.add_to_existing` is False
    existing_labels: list
        list of labels stored in an existing metafile. None if
        `self.add_to_existing` is False
    user: str
        the user who submitted the job
    webdir: str
        the directory to store the webpages, plots and metafile produced
    baseurl: str
        the base url of the webpages
    labels: list
        list of labels used to distinguish the result files
    config: list
        list of configuration files for each result file
    injection_file: list
        list of injection files for each result file
    publication: Bool
        if true, publication quality plots are generated. Default False
    kde_plot: Bool
        if true, kde plots are generated instead of histograms. Default False
    samples: dict
        dictionary of posterior samples stored in the result files
    priors: dict
        dictionary of prior samples stored in the result files
    custom_plotting: list
        list containing the directory and name of python file which contains
        custom plotting functions. Default None
    email: str
        the email address of the user
    dump: Bool
        if True, all plots will be dumped onto a single html page. Default False
    hdf5: Bool
        if True, the metafile is stored in hdf5 format. Default False
    notes: str
        notes that you wish to add to the webpages
    disable_comparison: Bool
        if True, comparison plots and pages are not produced
    disable_interactive: Bool
        if True, interactive plots are not produced
    """
    def __init__(self, opts, ignore_copy=False, extra_options=None):
        logger.info("Command line arguments: %s" % (opts))
        self.opts = opts
        self.style_file = self.opts.style_file
        self.result_files = self.opts.samples
        self.meta_file = False
        if self.result_files is not None and len(self.result_files) == 1:
            self.meta_file = self.is_pesummary_metafile(self.result_files[0])
        self.existing = self.opts.existing
        self.compare_results = self.opts.compare_results
        self.add_to_existing = False
        if self.existing is not None:
            self.add_to_existing = True
            self.existing_metafile = None
            self.existing_data = self.grab_data_from_metafile(
                self.existing_metafile, self.existing,
                compare=self.compare_results
            )
            self.existing_samples = self.existing_data["samples"]
            self.existing_injection_data = self.existing_data["injection_data"]
            self.existing_file_version = self.existing_data["file_version"]
            self.existing_file_kwargs = self.existing_data["file_kwargs"]
            self.existing_priors = self.existing_data["prior"]
            self.existing_config = self.existing_data["config"]
            self.existing_labels = self.existing_data["labels"]
            self.existing_weights = self.existing_data["weights"]
        else:
            self.existing_labels = None
            self.existing_weights = None
            self.existing_samples = None
            self.existing_file_version = None
            self.existing_file_kwargs = None
            self.existing_priors = None
            self.existing_config = None
            self.existing_injection_data = None
        self.user = self.opts.user
        self.webdir = self.opts.webdir
        self.baseurl = self.opts.baseurl
        self.mcmc_samples = self.opts.mcmc_samples
        self.labels = self.opts.labels
        self.weights = {i: None for i in self.labels}
        self.config = self.opts.config
        self.injection_file = self.opts.inj_file
        self.publication = self.opts.publication
        self.publication_kwargs = self.opts.publication_kwargs
        self.default_directories = [
            "samples", "plots", "js", "html", "css", "plots/corner", "config"
        ]
        self.make_directories()
        self.regenerate = self.opts.regenerate
        if extra_options is not None:
            for opt in extra_options:
                setattr(self, opt, getattr(self.opts, opt))
        self.kde_plot = self.opts.kde_plot
        self.priors = self.opts.prior_file
        self.file_format = self.opts.file_format
        self.samples = self.opts.samples
        self.ignore_parameters = self.opts.ignore_parameters
        self.burnin_method = self.opts.burnin_method
        self.burnin = self.opts.burnin
        self.nsamples = self.opts.nsamples
        self.custom_plotting = self.opts.custom_plotting
        self.email = self.opts.email
        self.dump = self.opts.dump
        self.hdf5 = not self.opts.save_to_json
        self.palette = self.opts.palette
        self.include_prior = self.opts.include_prior
        self.colors = self.opts.colors
        self.linestyles = self.opts.linestyles
        self.disable_corner = self.opts.disable_corner
        self.notes = self.opts.notes
        self.disable_comparison = self.opts.disable_comparison
        self.disable_interactive = self.opts.disable_interactive
        self.multi_process = self.opts.multi_process
        self.multi_threading_for_plots = self.multi_process
        self.package_information = self.get_package_information()
        if not ignore_copy:
            self.copy_files()


class PostProcessing(object):
    """Super class to post process the input data

    Parameters
    ----------
    inputs: argparse.Namespace
        Namespace object containing the command line options
    colors: list, optional
        colors that you wish to use to distinguish different result files

    Attributes
    ----------
    result_files: list
        list of result files passed
    compare_results: list
        list of labels stored in the metafile that you wish to compare
    add_to_existing: Bool
        True if we are adding to an existing web directory
    existing_samples: dict
        dictionary of samples stored in an existing metafile. None if
        `self.add_to_existing` is False
    existing_injection_data: dict
        dictionary of injection data stored in an existing metafile. None if
        `self.add_to_existing` is False
    existing_file_version: dict
        dictionary of file versions stored in an existing metafile. None if
        `self.add_to_existing` is False
    existing_config: list
        list of configuration files stored in an existing metafile. None if
        `self.add_to_existing` is False
    existing_labels: list
        list of labels stored in an existing metafile. None if
        `self.add_to_existing` is False
    user: str
        the user who submitted the job
    webdir: str
        the directory to store the webpages, plots and metafile produced
    baseurl: str
        the base url of the webpages
    labels: list
        list of labels used to distinguish the result files
    config: list
        list of configuration files for each result file
    injection_file: list
        list of injection files for each result file
    publication: Bool
        if true, publication quality plots are generated. Default False
    kde_plot: Bool
        if true, kde plots are generated instead of histograms. Default False
    samples: dict
        dictionary of posterior samples stored in the result files
    priors: dict
        dictionary of prior samples stored in the result files
    custom_plotting: list
        list containing the directory and name of python file which contains
        custom plotting functions. Default None
    email: str
        the email address of the user
    dump: Bool
        if True, all plots will be dumped onto a single html page. Default False
    hdf5: Bool
        if True, the metafile is stored in hdf5 format. Default False
    same_parameters: dict
        list of parameters that are common in all result files
    disable_comparison: bool
        whether or not to make comparison plots/pages when mutiple results
        files are present
    """
    def __init__(self, inputs, colors="default"):
        self.inputs = inputs
        self.result_files = self.inputs.result_files
        self.existing = self.inputs.existing
        self.compare_results = self.inputs.compare_results
        self.add_to_existing = False
        if self.existing is not None:
            self.add_to_existing = True
            self.existing_metafile = self.inputs.existing_metafile
            self.existing_samples = self.inputs.existing_samples
            self.existing_injection_data = self.inputs.existing_injection_data
            self.existing_file_version = self.inputs.existing_file_version
            self.existing_file_kwargs = self.inputs.existing_file_kwargs
            self.existing_priors = self.inputs.existing_priors
            self.existing_config = self.inputs.existing_config
            self.existing_labels = self.inputs.existing_labels
            self.existing_weights = self.inputs.existing_weights
        else:
            self.existing_metafile = None
            self.existing_labels = None
            self.existing_weights = None
            self.existing_samples = None
            self.existing_file_version = None
            self.existing_file_kwargs = None
            self.existing_priors = None
            self.existing_config = None
            self.existing_injection_data = None
        self.user = self.inputs.user
        self.host = self.inputs.host
        self.webdir = self.inputs.webdir
        self.baseurl = self.inputs.baseurl
        self.mcmc_samples = self.inputs.mcmc_samples
        self.labels = self.inputs.labels
        self.weights = self.inputs.weights
        self.config = self.inputs.config
        self.injection_file = self.inputs.injection_file
        self.injection_data = self.inputs.injection_data
        self.publication = self.inputs.publication
        self.kde_plot = self.inputs.kde_plot
        self.samples = self.inputs.samples
        self.priors = self.inputs.priors
        self.custom_plotting = self.inputs.custom_plotting
        self.email = self.inputs.email
        self.dump = self.inputs.dump
        self.hdf5 = self.inputs.hdf5
        self.file_version = self.inputs.file_version
        self.file_kwargs = self.inputs.file_kwargs
        self.palette = self.inputs.palette
        self.colors = self.inputs.colors
        self.linestyles = self.inputs.linestyles
        self.include_prior = self.inputs.include_prior
        self.notes = self.inputs.notes
        self.disable_comparison = self.inputs.disable_comparison
        self.disable_interactive = self.inputs.disable_interactive
        self.disable_corner = self.inputs.disable_corner
        self.multi_process = self.inputs.multi_threading_for_plots
        self.package_information = self.inputs.package_information
        self.same_parameters = []
        if self.mcmc_samples:
            self.samples = {label: self.samples.T for label in self.labels}

    @property
    def same_parameters(self):
        return self._same_parameters

    @same_parameters.setter
    def same_parameters(self, same_parameters):
        parameters = [list(self.samples[key]) for key in self.samples.keys()]
        params = list(set.intersection(*[set(l) for l in parameters]))
        self._same_parameters = params
