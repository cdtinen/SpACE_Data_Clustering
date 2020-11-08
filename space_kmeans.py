# -*- coding: utf-8 -*-
"""
Contains functions related to the Kmeans clustering algorithm.
Currently performs Kmeans, calculates the composition of Kmeans clusters, and plots 2D and 3D results.
"""
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go


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
    for i in range(len(data_objects)):
        # The most complicated line of code I have ever written in my entire life.  Basically it just accesses the
        # value where the descriptor = sort_category
        category = data_objects[i].descriptive. \
            loc[data_objects[i].descriptive['descriptor'] == sort_category, 'value'].iloc(0)[0].upper()
        if not (category in comp.columns):
            comp.insert(0, category, 0)
            comp.at[km.labels_[i], category] = 1
        else:
            comp.at[km.labels_[i], category] += 1

    return comp


def plot3D(dataset, clusters, dataobjects, embedded=False, ):
    """This function plots clusters and cluster centers in 3D.
    If embedded is False, the the plot is displayed in a standalone
    modal window and the function returns None.
    If embedded is True, the function returns a Figure object
    to be displayed on a FigureCanvasTkAgg embedded in the GUI."""
    figure, axes = plt.subplots(subplot_kw={"projection": "3d"})
    cx = []
    cy = []
    cz = []
    clusters = clusters.fit(dataset)  # refit to reduced data for plotting
    for i in clusters.cluster_centers_:
        cx.append(i[0])
        cy.append(i[1])
        cz.append(i[2])
    axes.scatter3D(xs=dataset[0], ys=dataset[1], zs=dataset[2], c=clusters.labels_, cmap="tab20")
    axes.scatter3D(xs=cx, ys=cy, zs=cz, marker="x", color="blue", s=50)
    if embedded:
        return figure
    else:
        plt.show()
        return None


def plot2D(dataset, clusters, dataobjects, embedded=False):
    """This function plots clusters and cluster centers in 2D with Plotly."""
    cx = []
    cy = []
    clusters = clusters.fit(dataset)  # refit to reduced data for plotting
    for i in clusters.cluster_centers_:
        cx.append(i[0])
        cy.append(i[1])

    descriptive = [{} for i in range(0, len(dataobjects))]
    for dataobject in dataobjects:
        j = dataobjects.index(dataobject)
        desc_df = dataobject.descriptive
        desc_index = desc_df.loc[desc_df['descriptor'] == 'Type'].index[0]
        value = desc_df.iloc[desc_index, 1].strip(" ")
        descriptive[j]['type'] = value
        desc_index = desc_df.loc[desc_df['descriptor'] == 'Class'].index[0]
        value = desc_df.iloc[desc_index, 1].strip(" ")
        descriptive[j]['class'] = value
        if 'Subclass' in desc_df['descriptor'].values:
            desc_index = desc_df.loc[desc_df['descriptor'] == 'Subclass'].index[0]
            value = desc_df.iloc[desc_index, 1].strip(" ")
            descriptive[j]['subclass'] = value

    strings = []
    for i in descriptive:
        string = ""
        string += 'Type: ' + i['type'] + '\n'
        string += 'Class: ' + i['class'] + '\n'
        if 'subclass' in i and i['subclass'] != 'None':
            string += 'Subclass: ' + i['subclass']
        strings.append(string)

    fig = go.Figure(data=go.Scattergl(x=dataset[0], y=dataset[1],
                                      name="",
                                      mode='markers',
                                      showlegend=False,
                                      marker=dict(
                                          size=8,
                                          color=clusters.labels_,
                                          colorscale='Portland',
                                          showscale=True
                                      ),
                                      text=strings
                                      ))
    # Add centers
    fig.add_trace(
        go.Scattergl(x=cx, y=cy, mode='markers', text=clusters.labels_, showlegend=False, name='Cluster Center',
                     marker=dict(size=10, symbol='x-dot', color='black')))
    fig.show()

    """
    if embedded:
        return fig
    else:
        fig.show()
        return None
    """
    return None
