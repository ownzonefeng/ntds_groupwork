#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 14:24:52 2018

@author: wentao
"""

import numpy as np
import pandas as pd
import time

def compute_adj_matrix():
    routes = pd.read_csv("routes.dat", names = ['Airline', 'Airline_ID', 'S_Port', 'S_ID', 
                                            'D_Port', 'D_ID', 'Codeshare', 'Stops', 'Equipment'])
# S_Port*D_Port = 3407*3448
    
    airlines = pd.read_csv("airlines.dat",names = ['Airline_ID','Name','Alias','IATA','ICAO','Callsign','Country','Active'])
                                              
#S stands for source; D stands for destination


# replace '\N' in Airline_ID with NaN and then turn the Airline_ID into numbers
# '\N' is escape character, so we need to add '\' before to refer to it
    routes_ = routes.copy()
    routes_.Airline_ID = pd.to_numeric(routes_.Airline_ID.replace(['\\N'],value=[np.nan]))#.value_counts()#.sort_index()


# merge routes_ with airlines on Airline_ID and connect every Aieline with 'Active' info
# We are cleaning out the routes that the Airline is no longer active any more
#( in this case, we just select the routes with Active == 'Y')
    route1 = pd.merge(routes_,airlines[['Airline_ID','Active']].copy().drop_duplicates('Airline_ID'))
    route_active = route1.loc[(route1.Active=='Y')].copy()
# route_active = pd.concat([route_active,noID],axis=0) 
# This step adds routes that is ambigious about the activeness due to the lack of Airline_ID
# If it is commented out, it means that we don't take these routes into consideration


# find out unique airports of active routes
    port = pd.concat([route_active.S_Port,route_active.D_Port],axis=0).drop_duplicates()#.sort_values().get_values()

# number the ports starts with 0, which can then be used as adjacency matrix index
    port_idx = port.sort_values().reset_index().drop('index',axis=1).copy()
    port_idx.rename(columns={0:'Port'},inplace=True)
    port_idx.index.names = ['index']
    port_idx.set_index('Port')
    port_idx = port_idx.reset_index()


    merge1 = pd.merge(route_active[['S_Port','D_Port']],port_idx,left_on = 'S_Port',right_on = 'Port').rename(columns={'index':'S_index'}).drop('Port',axis=1)
    merge2 = pd.merge(merge1,port_idx,left_on = 'D_Port',right_on = 'Port').rename(columns={'index':'D_index'}).drop('Port',axis=1)

# calculate the weights of every routes in terms of airport index
    resultidx = merge2.groupby(['S_index','D_index']).size().reset_index().rename(columns={0:'counts'})

# number of nodes equal to number of unique airport
    n_nodes = len(port)
    adj_matrix = np.zeros([n_nodes, n_nodes])

# looping time is 1.47s
    for i in range(len(resultidx)):
        adj_matrix[resultidx.S_index[i]][resultidx.D_index[i]] = resultidx.counts[i]
    return adj_matrix

#########################################################################################################################

def compute_shortest_path_lengths(adj_matrix, source_node):
    dist_matrix = np.copy(adj_matrix[source_node, :])
    dist_matrix[source_node] = -1
    for i in range(adj_matrix.shape[0]):
        non_zero_idx = np.where(dist_matrix == i + 1)[0]
        zero_idx = np.where(dist_matrix == 0)[0]
        next_neighbor = adj_matrix[non_zero_idx, :]
        if next_neighbor[:, zero_idx].any() == 0:
            break
        next_neighbor = np.sum(next_neighbor[:, zero_idx], axis = 0)
        next_neighbor[np.where(next_neighbor > 0)] = 1 * (i + 2)
        dist_matrix[zero_idx] = next_neighbor
    dist_matrix[dist_matrix == 0] = -1 * np.inf
    dist_matrix[source_node] = 0
    #shortest_path_lengths = list(dist_matrix)
    return list(dist_matrix)

def compute_diameter(adj_matrix):
    dist_matrix = np.zeros(adj_matrix.shape)
    for source_node in range(adj_matrix.shape[0]):
        dist_ = np.c_[dist_matrix[0:source_node + 1, source_node].reshape(1, source_node + 1), adj_matrix[source_node, source_node + 1:].reshape(1, 3286 - source_node)][0]
        dist_[source_node] = -1
        for i in range(adj_matrix.shape[0]):
            non_zero_idx = np.where(dist_ == i + 1)[0]
            zero_idx = np.where(dist_ == 0)[0]
            next_neighbor = adj_matrix[non_zero_idx, :]
            if next_neighbor[:, zero_idx].any() == 0:
                dist_matrix[source_node,:] = dist_
                break
            next_neighbor = np.sum(next_neighbor[:, zero_idx], axis = 0)
            next_neighbor[np.where(next_neighbor > 0)] = 1 * (i + 2)
            dist_[zero_idx] = next_neighbor
    return np.max(dist_matrix)
    
#source_node = 200; # i is between 0 -- (n - 1)
adj_matrix = compute_adj_matrix()

adj_matrix[adj_matrix > 1] = 1
start_time = time.time()
#dist_matrix_final = shortest_path_accelerated(adj_matrix, source_node)
dia = compute_diameter(adj_matrix) #Diameter 14
elap = time.time() - start_time
print('Time of running: ', elap,'s; DIA: ', dia, sep = '')
#original time of running: 148.18129301071167s


































