# -*- coding: utf-8 -*-
"""
Contains functions related to the Kmeans clustering algorithm.
Currently performs Kmeans, calculates the composition of Kmeans clusters, and plots 2D and 3D results.
"""
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def do_Kmeans(num_clusters, dataset):
    """This function accepts a integer number of clusters and a pandas dataframe of shape n_samples x n_features it
    fits the dataset, and returns a kmeans object which has attributes that describe the cluster centroids,
    and which cluster each sample is in """
    kmeans = KMeans(n_clusters=num_clusters).fit(dataset)
    return kmeans


def calculate_composition(km, num_clusters, data_objects, sort_category):
    """This function accepts a kmeans object, a number of clusters and a list of data objects, and a category to sort
    by and calculates the composition of each cluster, it returns a pandas dataframe with the composition of each
    cluster.  Composition dataframe is of shape clusters x categories. Each row is a cluster, and each column is a
    category """
    comp = pd.DataFrame(index=range(num_clusters))
    comp.index.name = "Cluster No."
    for i in range(len(data_objects)):
        # The most complicated line of code I have ever written in my entire life.  Basically it just accesses the
        # value where the descriptor = sort_category
        if sort_category in data_objects[i].descriptive.descriptor.values:
            category = data_objects[i].descriptive. \
                loc[data_objects[i].descriptive['descriptor'] == sort_category, 'value'].iloc(0)[0].upper()
        else:
            category = "None specified"
        if not (category in comp.columns):
            comp.insert(0, category, 0)
            comp.at[km.labels_[i], category] = 1
        else:
            comp.at[km.labels_[i], category] += 1

    return comp


def plot3D(dataset, clusters, embedded=False, master=None):
    """This function plots clusters and cluster centers in 3D.
    If embedded is False, the the plot is displayed in a standalone
    modal window, master is ignored, and the funtion returns None.
    If embedded is True, master must be specified (the parent widget
    for the canvas), and the function returns a canvas object
    to be displayed in the visualization panel in the GUI."""

    if embedded:
        figure = Figure()
        canvas = FigureCanvasTkAgg(figure, master=master)
        canvas.draw()
        axes = figure.add_subplot(111, projection="3d")
    else:
        figure, axes = plt.subplots(subplot_kw={"projection": "3d"})

    cx = []
    cy = []
    cz = []
    clusters = clusters.fit(dataset)  # refit to reduced data for plotting
    for i in clusters.cluster_centers_:
        cx.append(i[0])
        cy.append(i[1])
        cz.append(i[2])
    scatter = axes.scatter3D(xs=dataset[0], ys=dataset[1], zs=dataset[2], c=clusters.labels_, cmap="viridis")
    axes.scatter3D(xs=cx, ys=cy, zs=cz, marker="x", color="black", s=50)

    axes.legend(*scatter.legend_elements(), loc='upper left', bbox_to_anchor=(1.1, 1),
                title="Cluster #", fontsize='small', title_fontsize='small', fancybox=True,
                borderpad=0.2, borderaxespad=0.3, labelspacing=0.2, handletextpad=1, markerscale=1, edgecolor='black')

    if embedded:
        return canvas
    else:
        plt.show()
        return None


def plot2D(dataset, clusters, embedded=False, master=None):
    """This function plots clusters and cluster centers in 3D.
    If embedded is False, the the plot is displayed in a standalone
    modal window, master is ignored, and the funtion returns None.
    If embedded is True, master must be specified (the parent widget
    for the canvas), and the function returns a canvas object
    to be displayed in the visualization panel in the GUI."""

    if embedded:
        figure = Figure()
        canvas = FigureCanvasTkAgg(figure, master=master)
        canvas.draw()
        axes = figure.add_subplot()
    else:
        figure, axes = plt.subplots()

    cx = []
    cy = []
    clusters = clusters.fit(dataset)  # refit to reduced data for plotting
    for i in clusters.cluster_centers_:
        cx.append(i[0])
        cy.append(i[1])
    scatter = axes.scatter(x=dataset[0], y=dataset[1], c=clusters.labels_, cmap="viridis")
    axes.scatter(x=cx, y=cy, marker="x", color="black", s=50)

    axes.legend(*scatter.legend_elements(), loc='upper left', bbox_to_anchor=(1, 1),
                title="Cluster #", fontsize='small', title_fontsize='small', fancybox=True,
                borderpad=0.2, borderaxespad=0.3, labelspacing=0.2, handletextpad=1, markerscale=1, edgecolor='black')

    if embedded:
        return canvas
    else:
        plt.show()
        return None
