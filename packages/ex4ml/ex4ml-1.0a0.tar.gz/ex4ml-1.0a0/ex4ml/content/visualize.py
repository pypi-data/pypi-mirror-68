#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Helper functions for visualizing data.
"""

import colorsys
import os
import numpy as np
from scipy import stats
from sklearn.decomposition import PCA
from matplotlib import transforms

try:
    import matplotlib.pyplot as plt
except ImportError as err:
    if err.name == '_tkinter':
        raise ModuleNotFoundError("matplotlib is using 'TkAgg' backend which requires 'tkinter'."
                                  + " Either change the backend (import matplotlib; matplotlib.use(backend)), "
                                  + " (https://matplotlib.org/tutorials/introductory/usage.html#backends)"
                                  + " or install 'tkinter'"
                                  + " (https://stackoverflow.com/questions/4783810/install-tkinter-for-python).")
    raise

from mpl_toolkits.axes_grid1 import make_axes_locatable

# Use ggplot by default but user has the ability to change that
plt.style.use("ggplot")


def create_color_map(labels):
    """Maps label names to colors equidistant from each other.

    Args:
        labels (set): The set of labels to create a color map for.

    Returns:
        dict: The labels (keys) with assigned colors (values).
    """

    hsv_tuples = [(x * 1.0 / len(labels), .8, .8)
                  for x, _ in enumerate(labels)]
    rgb_tuples = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    return {label: rgb_tuples[i] for i, label in enumerate(labels)}


def plot_scatter(view, target, title=None, file_path=None, show=True, calculate_pca="2d"):
    """
    Plot a scatter plot of a particular view's principal components with a target used as the color.

    Args:
        view (iterable): An iterable of the data in a view to plot.
        target (iterable): An iterable of the target of the data used as a color index. Must be same length as view.
        title (str): The title on the plot.
        file_path (str, optional): The file path to save the image. Defaults to ``None``.
        show (bool, optional): Show the resulting plot in matplotlib viewer. Defaults to ``True``.
        calculate_pca (str, optional): Number of dimensions of the plot to produce if using PCA and whether to use PCA.
            Defaults to ``"2d"``.
    """

    # Always start by clearing previous figures.
    plt.clf()

    # Determine available labels and label colors.
    labels = set(target)
    label_colors = create_color_map(labels)

    # Check if using PCA and compute it if so.
    # Then, plot the values of the (transformed) data.
    if calculate_pca == "2d" or len(view[0]) == 2:
        # Calculate PCA.
        if calculate_pca == "2d":
            pca = PCA(n_components=2)
            view = pca.fit_transform(view)
        x_values, y_values = zip(*view)

        # Create the scatter plot.
        for label in labels:
            indexes_to_plot = [i for i, sample_target in enumerate(
                target) if sample_target == label]
            x_values_to_plot = [x_values[i] for i in indexes_to_plot]
            y_values_to_plot = [y_values[i] for i in indexes_to_plot]

            plt.scatter(x_values_to_plot, y_values_to_plot, c=[
                        label_colors[label]] * len(x_values_to_plot), label=label)

        # Add a legend, title, and axis labels.
        plt.legend(labels)
        if title:
            plt.title(title)
        if calculate_pca == "2d":
            plt.xlabel(
                f"PC1\n Explained Variance: {pca.explained_variance_ratio_[0]:.2f}")
            plt.ylabel(
                f"PC2\n Explained Variance: {pca.explained_variance_ratio_[1]:.2f}")
            plt.tight_layout()

        # Save the figure if a path was specified.
        # Show the figure if requested.
        if file_path:
            dirs, _ = os.path.split(file_path)
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            plt.savefig(file_path)
        if show:
            plt.show()

    elif calculate_pca == "3d" or len(view[0]) == 3:
        raise NotImplementedError("Not yet plotting in 3d.")
    else:
        raise ValueError(
            "Entry for calculate_pca incompatible." +
            "Either bad option or data has more than 3 dimensions and no option selected.")


def calculate_histogram_bin_count(data, bin_method):
    """Calculate histogram bin count from data and a particular bin method

    Args:
        data (iterable): The 1-dimensional data to calculate the histogram bin count for
        bin_method (str): The bin count computation method. One of ``'scott'`` or ``'fd'``. Defaults to ``'fd'``.

    Returns:
        int: The number of bins to use.
    """
    if bin_method is None:
        return None
    if bin_method == "fd":
        inter_quartile_range = stats.iqr(data, interpolation='midpoint')
        return int(2 * inter_quartile_range * len(data) ** (-1 / 3))
    if bin_method == "scott":
        return int(3.49 * np.std(data) * len(data) ** (-1 / 3))
    return bin_method


def plot_hist(view, title, file_path=None, show=True, calculate_pca=True, bin_count="fd"):
    """Plot a scatter plots of a particular view's principal components with a target used as the color.

    Args:
        view (iterable): An iterable of the data in a view to plot.
        title (str): The title on the plot.
        file_path (str, optional): The file path to save the image. Defaults to ``None``.
        show (bool, optional): Show the resulting plot in matplotlib viewer. Defaults to ``True``.
        calculate_pca (bool, optional): Whether to use PCA or use a single dimension. Defaults to ``True``.
        bin_count (any): The bin count computation method. One of ``'scott'``, ``'fd'``, or ``x_num`` for specific
            value. Defaults to ``'fd'``.
    """

    # Always start by clearing previous figures.
    plt.clf()

    # Calculate PCA if specified.
    if calculate_pca:
        pca = PCA(n_components=1)
        view = pca.fit_transform(view)
    else:
        if hasattr(view[0], '__iter__'):
            raise ValueError(
                "Provided view has more than one dimension and you selected to not calculate PCA." +
                "Unable to plot histogram.")

    plt.hist(view, density=True, bins=calculate_histogram_bin_count(view, bin_count))

    # density line
    kde_view = np.array(view)
    if kde_view.ndim > 1:
        kde_view = kde_view.flatten()
    kde = stats.gaussian_kde(kde_view)
    x_values = np.linspace(min(kde_view), max(kde_view))
    plt.plot(x_values, kde(x_values))

    # Add titles and labels.
    if title:
        plt.title(title)
    if calculate_pca:
        plt.xlabel(
            f"PC1 of Principal Components\nExplained Variance: {pca.explained_variance_ratio_[0]:.2f}")

    # Save the figure if a path was specified.
    # Show the figure if requested.
    if file_path:
        dirs, _ = os.path.split(file_path)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        plt.savefig(file_path)
    if show:
        plt.show()


def plot_joint(view, target, title=None, file_path=None, show=True, calculate_pca="2d", bin_count="fd"):
    """
    Plot a join plot (scatter + histograms) of a particular view's principal components with a target used as the color.

    Args:
        view (iterable): An iterable of the data in a view to plot.
        target (iterable): An iterable of the target of the data used as a color index. Must be same length as view.
        title (str): The title on the plot.
        file_path (str, optional): The file path to save the image. Defaults to ``None``.
        show (bool, optional): Show the resulting plot in matplotlib viewer. Defaults to ``True``.
        calculate_pca (str, optional): Number of dimensions of the plot to produce if using PCA and whether to use PCA.
            Defaults to ``"2d"``.
        bin_count (any): The bin count computation method. One of ``'scott'``, ``'fd'``, or ``(x_num, y_num)`` for
            specific values. Defaults to ``'fd'``.
    """

    # Always start by clearing previous figures.
    plt.clf()

    # Determine available labels and label colors.
    labels = set(target)
    label_colors = create_color_map(labels)

    if calculate_pca == "2d" or len(view[0]) == 2:
        # Calculate PCA.
        if calculate_pca == "2d":
            pca = PCA(n_components=2)
            view = pca.fit_transform(view)
        x_values, y_values = zip(*view)

        _, ax_scatter = plt.subplots()

        # the scatter plot:
        for label in labels:
            indexes_to_plot = [i for i, sample_target in enumerate(
                target) if sample_target == label]
            x_values_to_plot = [x_values[i] for i in indexes_to_plot]
            y_values_to_plot = [y_values[i] for i in indexes_to_plot]

            ax_scatter.scatter(x_values_to_plot, y_values_to_plot, c=[
                               label_colors[label]] * len(x_values_to_plot), label=label)

        ax_scatter.legend(labels)

        ax_scatter.set_aspect(1.)

        # Create new axes on the right and on the top of the current axes.
        # The first argument of the new_vertical(new_horizontal) method is
        # the height (width) of the axes to be created in inches.
        divider = make_axes_locatable(ax_scatter)
        ax_histx = divider.append_axes("top", 1.2, pad=0.1, sharex=ax_scatter)
        ax_histy = divider.append_axes(
            "right", 1.2, pad=0.1, sharey=ax_scatter)

        # Make some labels invisible.
        ax_histx.xaxis.set_tick_params(labelbottom=False)
        ax_histy.yaxis.set_tick_params(labelleft=False)

        if isinstance(bin_count, (str, int)):
            x_bins = calculate_histogram_bin_count(x_values, bin_count)
            y_bins = calculate_histogram_bin_count(x_values, bin_count)
        else:
            x_bins = calculate_histogram_bin_count(x_values, bin_count[0])
            y_bins = calculate_histogram_bin_count(x_values, bin_count[1])

        # Plot joint histograms.
        ax_histx.hist(x_values, density=True, bins=x_bins)
        ax_histy.hist(y_values, density=True, bins=y_bins, orientation='horizontal')

        # Remove labels from the plot.
        plt.xlabel("")
        plt.ylabel("")
        plt.title("")

        base = plt.gca().transData
        rot = transforms.Affine2D().rotate_deg(270)
        # density line x-axis
        x_kde_view = np.array(x_values)
        if x_kde_view.ndim > 1:
            x_kde_view = x_kde_view.flatten()
        x_kde = stats.gaussian_kde(x_kde_view)
        x_values = np.linspace(min(x_kde_view), max(x_kde_view))
        ax_histx.plot(x_values, x_kde(x_values))

        # density line y-axis
        y_kde_view = np.array(y_values)
        if y_kde_view.ndim > 1:
            y_kde_view = y_kde_view.flatten()
        y_kde = stats.gaussian_kde(y_kde_view)
        y_values = np.linspace(min(y_kde_view), max(y_kde_view))
        ax_histy.plot(y_values, y_kde(y_values), transform=rot+base)

        # Add title and axis labels to individual parts of the plot.
        if title:
            ax_histx.set_title(title)
        else:
            ax_histx.set_title(view)
        if calculate_pca == "2d":
            ax_scatter.set_xlabel(
                f"PC1\n Explained Variance: {pca.explained_variance_ratio_[0]:.2f}")
            ax_scatter.set_ylabel(
                f"PC2\n Explained Variance: {pca.explained_variance_ratio_[1]:.2f}")
            plt.tight_layout()
        else:
            ax_scatter.set_xlabel("x")
            ax_scatter.set_ylabel("y")

        # Save the figure if a path was specified.
        # Show the figure if requested.
        if file_path:
            dirs, _ = os.path.split(file_path)
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            plt.savefig(file_path)
        if show:
            plt.show()

    elif calculate_pca == "3d" or len(view[0]) == 3:
        raise NotImplementedError("Not yet plotting in 3d.")
    else:
        raise ValueError(
            "Entry for calculate_pca incompatible." +
            "Either bad option or data has more than 3 dimensions and no option selected.")
