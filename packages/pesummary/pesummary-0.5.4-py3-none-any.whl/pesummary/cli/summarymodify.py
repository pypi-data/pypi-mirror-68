#! /usr/bin/env python

# Copyright (C) 2020  Charlie Hoy <charlie.hoy@ligo.org>
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
import numpy as np
import math
import argparse
import json
import h5py
from pathlib import Path

from pesummary.utils.utils import logger, check_file_exists_and_rename
from pesummary.utils.exceptions import InputError
from pesummary.core.command_line import DelimiterSplitAction
from pesummary.gw.inputs import _GWInput
from pesummary.gw.file.meta_file import _GWMetaFile


__doc__ = """This executable is used to modify a PESummary metafile from the
command line"""


class _Input(_GWInput):
    """Super class to handle the command line arguments
    """
    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels):
        self._labels = labels
        if labels is not None and isinstance(labels, dict):
            self._labels = labels
        elif labels is not None:
            raise InputError(
                "Please provide an existing labels and the label you wish "
                "to replace it with `--labels existing:new`."
            )

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, kwargs):
        self._kwargs = kwargs
        if kwargs is not None and isinstance(kwargs, dict):
            self._kwargs = kwargs
        elif kwargs is not None:
            raise InputError(
                "Please provide the label, kwarg and value with '--kwargs "
                "label:kwarg:value`"
            )

    @property
    def replace_posterior(self):
        return self._replace_posterior

    @replace_posterior.setter
    def replace_posterior(self, replace_posterior):
        self._replace_posterior = replace_posterior
        if replace_posterior is not None and isinstance(replace_posterior, dict):
            self._replace_posterior = replace_posterior
        elif replace_posterior is not None:
            raise InputError(
                "Please provide the label, posterior and file path with "
                "value with '--replace_posterior "
                "label;posterior:/path/to/posterior.dat where ';' is the chosen "
                "delimiter and provided with '--delimiter ;`"
            )

    @property
    def remove_posterior(self):
        return self._remove_posterior

    @remove_posterior.setter
    def remove_posterior(self, remove_posterior):
        self._remove_posterior = remove_posterior
        if remove_posterior is not None and isinstance(remove_posterior, dict):
            self._remove_posterior = remove_posterior
        elif remove_posterior is not None:
            raise InputError(
                "Please provide the label and posterior with '--remove_posterior "
                "label:posterior`"
            )

    @property
    def samples(self):
        return self._samples

    @samples.setter
    def samples(self, samples):
        if samples is None:
            raise InputError(
                "Please provide a result file that you wish to modify"
            )
        if len(samples) > 1:
            raise InputError(
                "Only a single result file can be passed"
            )
        samples = samples[0]
        if not self.is_pesummary_metafile(samples):
            raise InputError(
                "Please provide a PESummary metafile to this executable"
            )
        self._samples = samples

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        extension = Path(self.samples).suffix
        if extension == ".h5" or extension == ".hdf5":
            from pesummary.core.file.formats.pesummary import PESummary
            from pandas import DataFrame

            with h5py.File(self.samples, "r") as f:
                data = PESummary._convert_hdf5_to_dict(f)
                for label in data.keys():
                    try:
                        data[label]["posterior_samples"] = DataFrame(
                            data[label]["posterior_samples"]
                        ).to_records(index=False, column_dtypes=np.float)
                    except KeyError:
                        pass
                    except Exception:
                        parameters = data[label]["posterior_samples"]["parameter_names"]
                        if isinstance(parameters[0], bytes):
                            parameters = [
                                parameter.decode("utf-8") for parameter in parameters
                            ]
                        samples = np.array([
                            j for j in data[label]["posterior_samples"]["samples"]
                        ].copy())
                        data[label]["posterior_samples"] = DataFrame.from_dict(
                            {
                                param: samples.T[num] for num, param in
                                enumerate(parameters)
                            }
                        ).to_records(index=False, column_dtypes=np.float)
                self._data = data
        elif extension == ".json":
            with open(self.samples, "r") as f:
                self._data = json.load(f)
        else:
            raise InputError(
                "The extension '{}' is not recognised".format(extension)
            )


class Input(_Input):
    """Class to handle the command line arguments

    Parameters
    ----------
    opts: argparse.Namespace
        Namespace object containing the command line options

    Attributes
    ----------
    samples: str
        path to a PESummary meta file that you wish to modify
    labels: dict
        dictionary of labels that you wish to modify. Key is the existing label
        and item is the new label
    """
    def __init__(self, opts, ignore_copy=False):
        logger.info("Command line arguments: %s" % (opts))
        self.opts = opts
        self.existing = None
        self.webdir = self.opts.webdir
        self.samples = self.opts.samples
        self.labels = self.opts.labels
        self.kwargs = self.opts.kwargs
        self.replace_posterior = self.opts.replace_posterior
        self.remove_posterior = self.opts.remove_posterior
        self.hdf5 = not self.opts.save_to_json
        self.overwrite = self.opts.overwrite
        self.data = None


def command_line():
    """Generate an Argument Parser object to control the command line options
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--labels", dest="labels", nargs='+', action=DelimiterSplitAction,
        help=("labels you wish to modify. Syntax: `--labels existing:new` "
              "where ':' is the default delimiter"),
        default=None
    )
    parser.add_argument(
        "-s", "--samples", dest="samples", default=None, nargs='+',
        help="Path to PESummary meta file you wish to modify"
    )
    parser.add_argument(
        "-w", "--webdir", dest="webdir", default="./", metavar="DIR",
        help="Directory to write the output file"
    )
    parser.add_argument(
        "--save_to_json", action="store_true", default=False,
        help="save the modified data in json format"
    )
    parser.add_argument(
        "--delimiter", dest="delimiter", default=":",
        help="Delimiter used to seperate the existing and new quantity"
    )
    parser.add_argument(
        "--kwargs", dest="kwargs", nargs='+', action=DelimiterSplitAction,
        help=("kwargs you wish to modify. Syntax: `--kwargs label/kwarg:item` "
              "where '/' is a delimiter of your choosing (it cannot be ':'), "
              "kwarg is the kwarg name and item is the value of the kwarg"),
        default=None
    )
    parser.add_argument(
        "--overwrite", action="store_true", default=False,
        help=("Overwrite the supplied PESummary meta file with the modified "
              "version")
    )
    parser.add_argument(
        "--replace_posterior", nargs='+', action=DelimiterSplitAction,
        help=("Replace the posterior for a given label. Syntax: "
              "--replace_posterior label;a:/path/to/posterior.dat where "
              "';' is a delimiter of your choosing (it cannot be '/' or ':'), "
              "a is the posterior you wish to replace and item is a path "
              "to a one column ascii file containing the posterior samples "
              "(/path/to/posterior.dat)"),
        default=None
    )
    parser.add_argument(
        "--remove_posterior", nargs='+', action=DelimiterSplitAction,
        help=("Remove a posterior distribution for a given label. Syntax: "
              "--remove_posterior label:a where a is the posterior you wish to remove"),
        default=None
    )
    return parser


def _check_label(data, label, message, logger_level="warn"):
    """Check that a given label is stored in the data. If it is not stored
    print a warning message

    Parameters
    ----------
    data: dict
        dictionary containing the data
    label: str
        name of the label you wish to check
    message: str
        message you wish to print in logger when the label is not stored
    logger_level: str, optional
        the logger level of the message
    """
    if label not in data.keys():
        getattr(logger, logger_level)(message)
        return False
    return True


def _modify_labels(data, labels=None):
    """Modify the existing labels in the data

    Parameters
    ----------
    data: dict
        dictionary containing the data
    labels: dict
        dictionary of labels showing the existing label, key, and the new
        label, item
    """
    for existing, new in labels.items():
        if existing not in data.keys():
            logger.warn(
                "Unable to find label '{}' in the root of the metafile. "
                "Checking inside the groups".format(existing)
            )
            for key in data.keys():
                if existing in data[key].keys():
                    data[key][new] = data[key].pop(existing)
        else:
            data[new] = data.pop(existing)
    return data


def _modify_kwargs(data, kwargs=None):
    """Modify kwargs that are stored in the data

    Parameters
    ----------
    data: dict
        dictionary containing the data
    kwargs: dict
        dictionary of kwargs showing the label as key and kwarg:value as the
        item
    """
    from pesummary.core.file.formats.base_read import Read

    def add_to_meta_data(data, label, string):
        kwarg, value = string.split(":")
        try:
            _group, = Read.paths_to_key(kwarg, data[label]["meta_data"])
            group = _group[0]
        except ValueError:
            group = "other"
        if group == "other" and group not in data[label]["meta_data"].keys():
            data[label]["meta_data"]["other"] = {}
        data[label]["meta_data"][group][kwarg] = value
        return data

    message = "Unable to find label '{}' in the metafile. Unable to modify kwargs"
    for label, item in kwargs.items():
        check = _check_label(data, label, message.format(label))
        if check:
            if isinstance(item, list):
                for _item in item:
                    data = add_to_meta_data(data, label, _item)
            else:
                data = add_to_meta_data(data, label, item)
    return data


def _modify_posterior(data, kwargs=None):
    """Replace a posterior distribution that is stored in the data

    Parameters
    ----------
    data: dict
        dictionary containing the data
    kwargs: dict
        dictionary of kwargs showing the label as key and posterior:path as the
        item
    """
    def _replace_posterior(data, string):
        posterior, path = string.split(":")
        _data = np.genfromtxt(path, usecols=0)
        if math.isnan(_data[0]):
            _data = np.genfromtxt(path, names=True, usecols=0)
            _data = _data[_data.dtype.names[0]]
        if posterior in data[label]["posterior_samples"].dtype.names:
            data[label]["posterior_samples"][posterior] = _data
        else:
            from numpy.lib.recfunctions import append_fields

            data[label]["posterior_samples"] = append_fields(
                data[label]["posterior_samples"], posterior, _data, usemask=False
            )
        return data

    message = "Unable to find label '{}' in the metafile. Unable to modify posterior"
    for label, item in kwargs.items():
        check = _check_label(data, label, message.format(label))
        if check:
            if isinstance(item, list):
                for _item in item:
                    data = _replace_posterior(data, _item)
            else:
                data = _replace_posterior(data, item)
    return data


def _remove_posterior(data, kwargs=None):
    """Remove a posterior distribution that is stored in the data

    Parameters
    ----------
    data: dict
        dictionary containing the data
    kwargs: dict
        dictionary of kwargs showing the label as key and posterior as the item
    """
    def _rmfield(array, *fieldnames_to_remove):
        return array[
            [name for name in array.dtype.names if name not in fieldnames_to_remove]
        ]

    message = "Unable to find label '{}' in the metafile. Unable to remove posterior"
    for label, item in kwargs.items():
        check = _check_label(data, label, message.format(label))
        if check:
            group = "posterior_samples"
            if isinstance(item, list):
                for _item in item:
                    data[label][group] = _rmfield(data[label][group], _item)
            else:
                data[label][group] = _rmfield(data[label][group], item)
    return data


def modify(data, function, **kwargs):
    """Modify the data according to a given function

    Parameters
    ----------
    data: dict
        dictionary containing the data
    function:
        function you wish to use to modify the data
    kwargs: dict
        dictionary of kwargs for function
    """
    func_map = {
        "labels": _modify_labels,
        "kwargs": _modify_kwargs,
        "add_posterior": _modify_posterior,
        "rm_posterior": _remove_posterior,
    }
    return func_map[function](data, **kwargs)


def main(args=None):
    """
    """
    parser = command_line()
    opts = parser.parse_args(args=args)
    args = Input(opts)
    if not args.overwrite:
        meta_file = os.path.join(
            args.webdir, "modified_posterior_samples.{}".format(
                "h5" if args.hdf5 else "json"
            )
        )
        check_file_exists_and_rename(meta_file)
    else:
        meta_file = args.samples
    if args.labels is not None:
        modified_data = modify(args.data, "labels", labels=args.labels)
    if args.kwargs is not None:
        modified_data = modify(args.data, "kwargs", kwargs=args.kwargs)
    if args.replace_posterior is not None:
        modified_data = modify(args.data, "add_posterior", kwargs=args.replace_posterior)
    if args.remove_posterior is not None:
        modified_data = modify(args.data, "rm_posterior", kwargs=args.remove_posterior)
    logger.info(
        "Saving the modified data to '{}'".format(meta_file)
    )
    if args.hdf5:
        _GWMetaFile.save_to_hdf5(
            modified_data, list(modified_data.keys()), None, meta_file,
            no_convert=True
        )
    else:
        _GWMetaFile.save_to_json(modified_data, meta_file)


if __name__ == "__main__":
    main()
