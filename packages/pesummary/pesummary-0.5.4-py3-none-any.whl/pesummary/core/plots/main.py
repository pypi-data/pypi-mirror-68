#! /usr/bin/env python

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

import os
import importlib

from pesummary.core.plots.latex_labels import latex_labels
from pesummary.utils.utils import logger, get_matplotlib_backend
from pesummary.core.plots import plot as core
from pesummary.core.plots import interactive

import matplotlib
matplotlib.use(get_matplotlib_backend(parallel=True))
import matplotlib.pyplot as plt
import numpy as np


class _PlotGeneration(object):
    """Super class to handle the plot generation for a given set of result
    files

    Parameters
    ----------
    savedir: str
        the directory to store the plots
    webdir: str
        the web directory of the run
    labels: list
        list of labels used to distinguish the result files
    samples: dict
        dictionary of posterior samples stored in the result files
    kde_plot: Bool
        if True, kde plots are generated instead of histograms, Default False
    existing_labels: list
        list of labels stored in an existing metafile
    existing_injection_data: dict
        dictionary of injection data stored in an existing metafile
    existing_samples: dict
        dictionary of posterior samples stored in an existing metafile
    same_parameters: list
        list of paramerers that are common in all result files
    injection_data: dict
        dictionary of injection data for each result file
    result_files: list
        list of result files passed
    colors: list
        colors that you wish to use to distinguish different result files
    disable_comparison: bool, optional
        whether to make comparison plots, default is True.
        if disable_comparison is False and len(labels) == 1, no comparsion plots
        will be generated
    disable_interactive: bool, optional
        whether to make interactive plots, default is False
    disable_corner: bool, optional
        whether to make the corner plot, default is False
    """
    def __init__(
        self, savedir=None, webdir=None, labels=None, samples=None,
        kde_plot=False, existing_labels=None, existing_injection_data=None,
        existing_samples=None, existing_weights=None, same_parameters=None,
        injection_data=None, colors=None, custom_plotting=None,
        add_to_existing=False, priors={}, include_prior=False, weights=None,
        disable_comparison=False, linestyles=None, disable_interactive=False,
        multi_process=1, mcmc_samples=False, disable_corner=False
    ):
        self.package = "core"
        self.webdir = webdir
        self.savedir = savedir
        self.labels = labels
        self.mcmc_samples = mcmc_samples
        self.samples = samples
        self.kde_plot = kde_plot
        self.existing_labels = existing_labels
        self.existing_injection_data = existing_injection_data
        self.existing_samples = existing_samples
        self.existing_weights = existing_weights
        self.same_parameters = same_parameters
        self.injection_data = injection_data
        self.colors = colors
        self.custom_plotting = custom_plotting
        self.add_to_existing = add_to_existing
        self.priors = priors
        self.include_prior = include_prior
        self.linestyles = linestyles
        self.make_interactive = not disable_interactive
        self.make_corner = not disable_corner
        self.multi_process = multi_process
        self.pool = self.setup_pool()
        self.make_comparison = (
            not disable_comparison and self._total_number_of_labels > 1
        )
        self.weights = (
            weights if weights is not None else {i: None for i in self.labels}
        )

        if self.same_parameters is not None and not self.mcmc_samples:
            self.same_samples = {
                param: {
                    key: item[param] for key, item in self.samples.items()
                } for param in self.same_parameters
            }
        else:
            self.same_samples = None

        for i in self.samples.keys():
            self.check_latex_labels(self.samples[i].keys())

        self.plot_type_dictionary = {
            "oned_histogram": self.oned_histogram_plot,
            "sample_evolution": self.sample_evolution_plot,
            "autocorrelation": self.autocorrelation_plot,
            "oned_cdf": self.oned_cdf_plot,
            "custom": self.custom_plot
        }
        if self.make_corner:
            self.plot_type_dictionary.update({"corner": self.corner_plot})
        if self.make_comparison:
            self.plot_type_dictionary.update(dict(
                oned_histogram_comparison=self.oned_histogram_comparison_plot,
                oned_cdf_comparison=self.oned_cdf_comparison_plot,
                box_plot_comparison=self.box_plot_comparison_plot,
            ))
        if self.make_interactive:
            self.plot_type_dictionary.update(
                dict(
                    interactive_corner=self.interactive_corner_plot
                )
            )
            if self.make_comparison:
                self.plot_type_dictionary.update(
                    dict(
                        interactive_ridgeline=self.interactive_ridgeline_plot
                    )
                )

    @staticmethod
    def save(fig, name, close=True, format="png"):
        """Save a figure to disk.

        Parameters
        ----------
        fig: matplotlib.pyplot.figure
            Matplotlib figure that you wish to save
        name: str
            Name of the file that you wish to write it too
        close: Bool, optional
            Close the figure after it has been saved
        format: str, optional
            Format used to save the image
        """
        n = len(format)
        if ".%s" % (format) != name[-n - 1:]:
            name += ".%s" % (format)
        fig.savefig(name, format=format)
        if close:
            plt.close()

    @property
    def _total_number_of_labels(self):
        _number_of_labels = 0
        for item in [self.labels, self.existing_labels]:
            if isinstance(item, list):
                _number_of_labels += len(item)
        return _number_of_labels

    @staticmethod
    def check_latex_labels(parameters):
        """Check to see if there is a latex label for all parameters. If not,
        then create one

        Parameters
        ----------
        parameters: list
            list of parameters
        """
        for i in parameters:
            if i not in list(latex_labels.keys()):
                latex_labels[i] = i.replace("_", " ")

    @property
    def savedir(self):
        return self._savedir

    @savedir.setter
    def savedir(self, savedir):
        self._savedir = savedir
        if savedir is None:
            self._savedir = self.webdir + "/plots/"

    def setup_pool(self):
        """Setup a pool of processes to speed up plot generation
        """
        from multiprocessing import Pool

        pool = Pool(processes=self.multi_process)
        return pool

    def generate_plots(self):
        """Generate all plots for all result files
        """
        for i in self.labels:
            logger.debug("Starting to generate plots for {}".format(i))
            self._generate_plots(i)
            if self.make_interactive:
                logger.debug(
                    "Starting to generate interactive plots for {}".format(i)
                )
                self._generate_interactive_plots(i)
        if self.add_to_existing:
            self.add_existing_data()
        if self.make_comparison:
            logger.debug("Starting to generate comparison plots")
            self._generate_comparison_plots()

    def check_prior_samples_in_dict(self, label, param):
        """Check to see if there are prior samples for a given param

        Parameters
        ----------
        label: str
            the label used to distinguish a given run
        param: str
            name of the parameter you wish to return prior samples for
        """
        cond1 = "samples" in self.priors.keys()
        if cond1 and label in self.priors["samples"].keys():
            cond1 = self.priors["samples"][label] != []
            if cond1 and param in self.priors["samples"][label].keys():
                return self.priors["samples"][label][param]
            return None
        return None

    def add_existing_data(self):
        """
        """
        from pesummary.utils.utils import _add_existing_data

        self = _add_existing_data(self)

    def _generate_plots(self, label):
        """Generate all plots for a a given result file
        """
        if self.make_corner:
            self.try_to_make_a_plot("corner", label=label)
        self.try_to_make_a_plot("oned_histogram", label=label)
        self.try_to_make_a_plot("sample_evolution", label=label)
        self.try_to_make_a_plot("autocorrelation", label=label)
        self.try_to_make_a_plot("oned_cdf", label=label)
        if self.custom_plotting:
            self.try_to_make_a_plot("custom", label=label)

    def _generate_interactive_plots(self, label):
        """Generate all interactive plots and save them to an html file ready
        to be imported later
        """
        self.try_to_make_a_plot("interactive_corner", label=label)
        if self.make_comparison:
            self.try_to_make_a_plot("interactive_ridgeline")

    def _generate_comparison_plots(self):
        """Generate all comparison plots
        """
        self.try_to_make_a_plot("oned_histogram_comparison")
        self.try_to_make_a_plot("oned_cdf_comparison")
        self.try_to_make_a_plot("box_plot_comparison")

    def try_to_make_a_plot(self, plot_type, label=None):
        """Wrapper function to _try_to_make_a_plot

        Parameters
        ----------
        plot_type: str
            String to describe the plot that you wish to try and make
        label: str
            The label of the results file that you wish to plot
        """
        self._try_to_make_a_plot(
            [label], self.plot_type_dictionary[plot_type],
            "Failed to generate %s plot because {}" % (plot_type)
        )

    @staticmethod
    def _try_to_make_a_plot(arguments, function, message):
        """Try to make a plot. If it fails return an error message and continue
        plotting

        Parameters
        ----------
        arguments: list
            list of arguments that you wish to pass to function
        function: func
            function that you wish to execute
        message: str
            the error message that you wish to be printed.
        """
        try:
            function(*arguments)
        except RuntimeError:
            try:
                from matplotlib import rcParams

                original = rcParams['text.usetex']
                rcParams['text.usetex'] = False
                function(*arguments)
                rcParams['text.usetex'] = original
            except Exception as e:
                logger.info(message.format(e))
        except Exception as e:
            logger.info(message.format(e))
        finally:
            plt.close()

    def corner_plot(self, label):
        """Generate a corner plot for a given result file

        Parameters
        ----------
        label: str
            the label for the results file that you wish to plot
        """
        if self.mcmc_samples:
            samples = self.samples[label].combine
        else:
            samples = self.samples[label]
        self._corner_plot(
            self.savedir, label, samples, latex_labels, self.webdir
        )

    @staticmethod
    def _corner_plot(savedir, label, samples, latex_labels, webdir):
        """Generate a corner plot for a given set of samples

        Parameters
        ----------
        savedir: str
            the directory you wish to save the plot in
        label: str
            the label corresponding to the results file
        samples: dict
            dictionary containing PESummary.utils.utils.Array objects that
            contain samples for each parameter
        latex_labels: str
            latex labels for each parameter in samples
        webdir: str
            the directory where the `js` directory is located
        """
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fig, params, data = core._make_corner_plot(samples, latex_labels)
            _PlotGeneration.save(
                fig, os.path.join(
                    savedir, "corner", "{}_all_density_plots".format(
                        label
                    )
                )
            )
            combine_corner = open(
                os.path.join(webdir, "js", "combine_corner.js")
            )
            combine_corner = combine_corner.readlines()
            params = [str(i) for i in params]
            ind = [
                linenumber for linenumber, line in enumerate(combine_corner)
                if "var list = {}" in line
            ][0]
            combine_corner.insert(
                ind + 1, "    list['{}'] = {};\n".format(label, params)
            )
            new_file = open(
                os.path.join(webdir, "js", "combine_corner.js"), "w"
            )
            new_file.writelines(combine_corner)
            new_file.close()
            combine_corner = open(
                os.path.join(webdir, "js", "combine_corner.js")
            )
            combine_corner = combine_corner.readlines()
            params = [str(i) for i in params]
            ind = [
                linenumber for linenumber, line in enumerate(combine_corner)
                if "var data = {}" in line
            ][0]
            combine_corner.insert(
                ind + 1, "    data['{}'] = {};\n".format(label, data)
            )
            new_file = open(
                os.path.join(webdir, "js", "combine_corner.js"), "w"
            )
            new_file.writelines(combine_corner)
            new_file.close()

    def _mcmc_iterator(self, label, function):
        """If the data is a set of mcmc chains, return a 2d list of samples
        to plot. Otherwise return a list of posterior samples
        """
        if self.mcmc_samples:
            function += "_mcmc"
            return self.same_parameters, self.samples[label], getattr(
                self, function
            )
        return self.samples[label].keys(), self.samples[label], getattr(
            self, function
        )

    def oned_histogram_plot(self, label):
        """Generate oned histogram plots for all parameters in the result file

        Parameters
        ----------
        label: str
            the label for the results file that you wish to plot
        """
        import math

        error_message = (
            "Failed to generate oned_histogram plot for %s because {}"
        )

        iterator, samples, function = self._mcmc_iterator(
            label, "_oned_histogram_plot"
        )

        prior = lambda param: self.check_prior_samples_in_dict(
            label, param
        ) if self.include_prior else None

        arguments = [
            (
                [
                    self.savedir, label, param, samples[param],
                    latex_labels[param], self.injection_data[label][param],
                    self.kde_plot, prior(param), self.weights[label],
                    self.package
                ], function, error_message % (param)
            ) for param in iterator
        ]
        self.pool.starmap(self._try_to_make_a_plot, arguments)

    def oned_histogram_comparison_plot(self, label):
        """Generate oned comparison histogram plots for all parameters that are
        common to all result files

        Parameters
        ----------
        label: str
            the label for the results file that you wish to plot
        """
        error_message = (
            "Failed to generate a comparison histogram plot for %s because {}"
        )
        for param in self.same_parameters:
            arguments = [
                self.savedir, param, self.same_samples[param],
                latex_labels[param], self.colors, self.kde_plot,
                self.linestyles, self.package
            ]
            self._try_to_make_a_plot(
                arguments, self._oned_histogram_comparison_plot,
                error_message % (param)
            )
            continue

    @staticmethod
    def _oned_histogram_comparison_plot(
        savedir, parameter, samples, latex_label, colors, kde=False,
        linestyles=None, package="core"
    ):
        """Generate a oned comparison histogram plot for a given parameter

        Parameters
        ----------
        savedir: str
            the directory you wish to save the plot in
        parameter: str
            the name of the parameter that you wish to make a oned comparison
            histogram for
        samples: dict
            dictionary of pesummary.utils.utils.Array objects containing the
            samples that correspond to parameter for each result file. The key
            should be the corresponding label
        latex_label: str
            the latex label for parameter
        colors: list
            list of colors to be used to distinguish different result files
        kde: Bool, optional
            if True, kde plots will be generated rather than 1d histograms
        linestyles: list, optional
            list of linestyles used to distinguish different result files
        """
        module = importlib.import_module(
            "pesummary.{}.plots.plot".format(package)
        )
        same_samples = [val for key, val in samples.items()]
        fig = module._1d_comparison_histogram_plot(
            parameter, same_samples, colors, latex_label,
            list(samples.keys()), kde=kde, linestyles=linestyles
        )
        _PlotGeneration.save(
            fig, os.path.join(
                savedir, "combined_1d_posterior_{}".format(parameter)
            )
        )

    @staticmethod
    def _oned_histogram_plot(
        savedir, label, parameter, samples, latex_label, injection, kde=False,
        prior=None, weights=None, package="core"
    ):
        """Generate a oned histogram plot for a given set of samples

        Parameters
        ----------
        savedir: str
            the directory you wish to save the plot in
        label: str
            the label corresponding to the results file
        parameter: str
            the name of the parameter that you wish to plot
        samples: PESummary.utils.utils.Array
            array containing the samples corresponding to parameter
        latex_label: str
            the latex label corresponding to parameter
        injection: float
            the injected value
        kde: Bool, optional
            if True, kde plots will be generated rather than 1d histograms
        prior: PESummary.utils.utils.Array, optional
            the prior samples for param
        weights: PESummary.utils.utils.Array, optional
            the weights for each samples. If None, assumed to be 1
        """
        import math
        module = importlib.import_module(
            "pesummary.{}.plots.plot".format(package)
        )

        if math.isnan(injection):
            injection = None

        fig = module._1d_histogram_plot(
            parameter, samples, latex_label, injection, kde=kde, prior=prior,
            weights=weights
        )
        _PlotGeneration.save(
            fig, os.path.join(
                savedir, "{}_1d_posterior_{}".format(label, parameter)
            )
        )

    @staticmethod
    def _oned_histogram_plot_mcmc(
        savedir, label, parameter, samples, latex_label, injection, kde=False,
        prior=None, weights=None, package="core"
    ):
        """Generate a oned histogram plot for a given set of samples for
        multiple mcmc chains

        Parameters
        ----------
        savedir: str
            the directory you wish to save the plot in
        label: str
            the label corresponding to the results file
        parameter: str
            the name of the parameter that you wish to plot
        samples: dict
            dictionary of PESummary.utils.utils.Array objects containing the
            samples corresponding to parameter for multiple mcmc chains
        latex_label: str
            the latex label corresponding to parameter
        injection: float
            the injected value
        kde: Bool, optional
            if True, kde plots will be generated rather than 1d histograms
        prior: PESummary.utils.utils.Array, optional
            the prior samples for param
        weights: PESummary.utils.utils.Array, optional
            the weights for each samples. If None, assumed to be 1
        """
        import math
        from pesummary.utils.samples_dict import Array

        module = importlib.import_module(
            "pesummary.{}.plots.plot".format(package)
        )

        if math.isnan(injection):
            injection = None
        same_samples = [val for key, val in samples.items()]
        fig = module._1d_histogram_plot_mcmc(
            parameter, same_samples, latex_label, injection, kde=kde,
            prior=prior, weights=weights
        )
        _PlotGeneration.save(
            fig, os.path.join(
                savedir, "{}_1d_posterior_{}".format(label, parameter)
            )
        )
        fig = module._1d_histogram_plot(
            parameter, Array(np.concatenate(same_samples)), latex_label,
            injection, kde=kde, prior=prior, weights=weights
        )
        _PlotGeneration.save(
            fig, os.path.join(
                savedir, "{}_1d_posterior_{}_combined".format(label, parameter)
            )
        )

    def sample_evolution_plot(self, label):
        """Generate sample evolution plots for all parameters in the result file

        Parameters
        ----------
        label: str
            the label for the results file that you wish to plot
        """
        error_message = (
            "Failed to generate a sample evolution plot for %s because {}"
        )
        iterator, samples, function = self._mcmc_iterator(
            label, "_sample_evolution_plot"
        )
        arguments = [
            (
                [
                    self.savedir, label, param, samples[param],
                    latex_labels[param], self.injection_data[label][param]
                ], function, error_message % (param)
            ) for param in iterator
        ]
        self.pool.starmap(self._try_to_make_a_plot, arguments)

    @staticmethod
    def _sample_evolution_plot(
        savedir, label, parameter, samples, latex_label, injection
    ):
        """Generate a sample evolution plot for a given set of samples

        Parameters
        ----------
        savedir: str
            the directory you wish to save the plot in
        label: str
            the label corresponding to the results file
        parameter: str
            the name of the parameter that you wish to plot
        samples: PESummary.utils.utils.Array
            array containing the samples corresponding to parameter
        latex_label: str
            the latex label corresponding to parameter
        injection: float
            the injected value
        """
        fig = core._sample_evolution_plot(
            parameter, samples, latex_label, injection
        )
        _PlotGeneration.save(
            fig, os.path.join(
                savedir, "{}_sample_evolution_{}".format(label, parameter)
            )
        )

    @staticmethod
    def _sample_evolution_plot_mcmc(
        savedir, label, parameter, samples, latex_label, injection
    ):
        """Generate a sample evolution plot for a given set of mcmc chains

        Parameters
        ----------
        savedir: str
            the directory you wish to save the plot in
        label: str
            the label corresponding to the results file
        parameter: str
            the name of the parameter that you wish to plot
        samples: dict
            dictionary containing pesummary.utils.utils.Array objects containing
            the samples corresponding to parameter for each chain
        latex_label: str
            the latex label corresponding to parameter
        injection: float
            the injected value
        """
        same_samples = [val for key, val in samples.items()]
        fig = core._sample_evolution_plot_mcmc(
            parameter, same_samples, latex_label, injection
        )
        _PlotGeneration.save(
            fig, os.path.join(
                savedir, "{}_sample_evolution_{}".format(label, parameter)
            )
        )

    def autocorrelation_plot(self, label):
        """Generate autocorrelation plots for all parameters in the result file

        Parameters
        ----------
        label: str
            the label for the results file that you wish to plot
        """
        error_message = (
            "Failed to generate an autocorrelation plot for %s because {}"
        )
        iterator, samples, function = self._mcmc_iterator(
            label, "_autocorrelation_plot"
        )
        arguments = [
            (
                [self.savedir, label, param, samples[param]],
                function, error_message % (param)
            ) for param in iterator
        ]
        self.pool.starmap(self._try_to_make_a_plot, arguments)

    @staticmethod
    def _autocorrelation_plot(savedir, label, parameter, samples):
        """Generate an autocorrelation plot for a given set of samples

        Parameters
        ----------
        savedir: str
            the directory you wish to save the plot in
        label: str
            the label corresponding to the results file
        parameter: str
            the name of the parameter that you wish to plot
        samples: PESummary.utils.utils.Array
            array containing the samples corresponding to parameter
        """
        fig = core._autocorrelation_plot(parameter, samples)
        _PlotGeneration.save(
            fig, os.path.join(
                savedir, "{}_autocorrelation_{}".format(
                    label, parameter
                )
            )
        )

    @staticmethod
    def _autocorrelation_plot_mcmc(savedir, label, parameter, samples):
        """Generate an autocorrelation plot for a list of samples, one for each
        mcmc chain

        Parameters
        ----------
        savedir: str
            the directory you wish to save the plot in
        label: str
            the label corresponding to the results file
        parameter: str
            the name of the parameter that you wish to plot
        samples: dict
            dictioanry of PESummary.utils.utils.Array objects containing the
            samples corresponding to parameter for each mcmc chain
        """
        same_samples = [val for key, val in samples.items()]
        fig = core._autocorrelation_plot_mcmc(parameter, same_samples)
        _PlotGeneration.save(
            fig, os.path.join(
                savedir, "{}_autocorrelation_{}".format(
                    label, parameter
                )
            )
        )

    def oned_cdf_plot(self, label):
        """Generate oned CDF plots for all parameters in the result file

        Parameters
        ----------
        label: str
            the label for the results file that you wish to plot
        """
        error_message = (
            "Failed to generate a CDF plot for %s because {}"
        )
        iterator, samples, function = self._mcmc_iterator(
            label, "_oned_cdf_plot"
        )
        arguments = [
            (
                [
                    self.savedir, label, param, samples[param],
                    latex_labels[param]
                ], function, error_message % (param)
            ) for param in iterator
        ]
        self.pool.starmap(self._try_to_make_a_plot, arguments)

    @staticmethod
    def _oned_cdf_plot(savedir, label, parameter, samples, latex_label):
        """Generate a oned CDF plot for a given set of samples

        Parameters
        ----------
        savedir: str
            the directory you wish to save the plot in
        label: str
            the label corresponding to the results file
        parameter: str
            the name of the parameter that you wish to plot
        samples: PESummary.utils.utils.Array
            array containing the samples corresponding to parameter
        latex_label: str
            the latex label corresponding to parameter
        """
        fig = core._1d_cdf_plot(parameter, samples, latex_label)
        _PlotGeneration.save(
            fig, os.path.join(
                savedir + "{}_cdf_{}".format(label, parameter)
            )
        )

    @staticmethod
    def _oned_cdf_plot_mcmc(savedir, label, parameter, samples, latex_label):
        """Generate a oned CDF plot for a given set of samples, one for each
        mcmc chain

        Parameters
        ----------
        savedir: str
            the directory you wish to save the plot in
        label: str
            the label corresponding to the results file
        parameter: str
            the name of the parameter that you wish to plot
        samples: dict
            dictionary of PESummary.utils.utils.Array objects containing the
            samples corresponding to parameter for each mcmc chain
        latex_label: str
            the latex label corresponding to parameter
        """
        same_samples = [val for key, val in samples.items()]
        fig = core._1d_cdf_plot_mcmc(parameter, same_samples, latex_label)
        _PlotGeneration.save(
            fig, os.path.join(
                savedir + "{}_cdf_{}".format(label, parameter)
            )
        )

    def interactive_ridgeline_plot(self, label):
        """Generate an interactive ridgeline plot for all paramaters that are
        common to all result files
        """
        error_message = (
            "Failed to generate an interactive ridgeline plot for %s because {}"
        )
        for param in self.same_parameters:
            arguments = [
                self.savedir, param, self.same_samples[param],
                latex_labels[param], self.colors
            ]
            self._try_to_make_a_plot(
                arguments, self._interactive_ridgeline_plot,
                error_message % (param)
            )
            continue

    @staticmethod
    def _interactive_ridgeline_plot(
        savedir, parameter, samples, latex_label, colors
    ):
        """Generate an interactive ridgeline plot for
        """
        same_samples = [val for key, val in samples.items()]
        _ = interactive.ridgeline(
            same_samples, list(samples.keys()), xlabel=latex_label,
            colors=colors, write_to_html_file=os.path.join(
                savedir, "interactive_ridgeline_{}.html".format(parameter)
            )
        )

    def interactive_corner_plot(self, label):
        """Generate an interactive corner plot for a given result file

        Parameters
        ----------
        label: str
            the label for the results file that you wish to plot
        """
        self._interactive_corner_plot(
            self.savedir, label, self.samples[label], latex_labels
        )

    @staticmethod
    def _interactive_corner_plot(savedir, label, samples, latex_labels):
        """Generate an interactive corner plot for a given set of samples

        Parameters
        ----------
        savedir: str
            the directory you wish to save the plot in
        label: str
            the label corresponding to the results file
        samples: dict
            dictionary containing PESummary.utils.utils.Array objects that
            contain samples for each parameter
        latex_labels: str
            latex labels for each parameter in samples
        """
        parameters = samples.keys()
        data = [samples[parameter] for parameter in parameters]
        latex_labels = [latex_labels[parameter] for parameter in parameters]
        _ = interactive.corner(
            data, latex_labels, write_to_html_file=os.path.join(
                savedir, "corner", "{}_interactive.html".format(label)
            )
        )

    def oned_cdf_comparison_plot(self, label):
        """Generate oned comparison CDF plots for all parameters that are
        common to all result files

        Parameters
        ----------
        label: str
            the label for the results file that you wish to plot
        """
        error_message = (
            "Failed to generate a comparison CDF plot for %s because {}"
        )
        for param in self.same_parameters:
            arguments = [
                self.savedir, param, self.same_samples[param],
                latex_labels[param], self.colors, self.linestyles
            ]
            self._try_to_make_a_plot(
                arguments, self._oned_cdf_comparison_plot,
                error_message % (param)
            )
            continue

    @staticmethod
    def _oned_cdf_comparison_plot(
        savedir, parameter, samples, latex_label, colors, linestyles=None
    ):
        """Generate a oned comparison CDF plot for a given parameter

        Parameters
        ----------
        savedir: str
            the directory you wish to save the plot in
        parameter: str
            the name of the parameter that you wish to make a oned comparison
            histogram for
        samples: dict
            dictionary of pesummary.utils.utils.Array objects containing the
            samples that correspond to parameter for each result file. The key
            should be the corresponding label
        latex_label: str
            the latex label for parameter
        colors: list
            list of colors to be used to distinguish different result files
        linestyles: list, optional
            list of linestyles used to distinguish different result files
        """
        keys = list(samples.keys())
        same_samples = [samples[key] for key in keys]
        fig = core._1d_cdf_comparison_plot(
            parameter, same_samples, colors, latex_label, keys, linestyles
        )
        _PlotGeneration.save(
            fig, os.path.join(
                savedir, "combined_cdf_{}".format(parameter)
            )
        )

    def box_plot_comparison_plot(self, label):
        """Generate comparison box plots for all parameters that are
        common to all result files

        Parameters
        ----------
        label: str
            the label for the results file that you wish to plot
        """
        error_message = (
            "Failed to generate a comparison box plot for %s because {}"
        )
        for param in self.same_parameters:
            arguments = [
                self.savedir, param, self.same_samples[param],
                latex_labels[param], self.colors
            ]
            self._try_to_make_a_plot(
                arguments, self._box_plot_comparison_plot,
                error_message % (param)
            )
            continue

    @staticmethod
    def _box_plot_comparison_plot(
        savedir, parameter, samples, latex_label, colors
    ):
        """Generate a comparison box plot for a given parameter

        Parameters
        ----------
        savedir: str
            the directory you wish to save the plot in
        parameter: str
            the name of the parameter that you wish to make a oned comparison
            histogram for
        samples: dict
            dictionary of pesummary.utils.utils.Array objects containing the
            samples that correspond to parameter for each result file. The key
            should be the corresponding label
        latex_label: str
            the latex label for parameter
        colors: list
            list of colors to be used to distinguish different result files
        """
        same_samples = [val for key, val in samples.items()]
        fig = core._comparison_box_plot(
            parameter, same_samples, colors, latex_label,
            list(samples.keys())
        )
        _PlotGeneration.save(
            fig, os.path.join(savedir, "combined_boxplot_{}".format(parameter))
        )

    def custom_plot(self, label):
        """Generate custom plots according to the passed python file

        Parameters
        ----------
        label: str
            the label for the results file that you wish to plot
        """
        import importlib

        if self.custom_plotting[0] != "":
            import sys

            sys.path.append(self.custom_plotting[0])
        mod = importlib.import_module(self.custom_plotting[1])

        methods = [getattr(mod, i) for i in mod.__single_plots__]
        for num, i in enumerate(methods):
            fig = i(
                list(self.samples[label].keys()), self.samples[label]
            )
            _PlotGeneration.save(
                fig, os.path.join(
                    self.savedir, "{}_custom_plotting_{}".format(label, num)
                )
            )
