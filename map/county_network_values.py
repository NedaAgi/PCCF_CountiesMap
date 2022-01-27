from scipy.stats import pearsonr
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import networkx as nx
from map.additional_functions import normalize, network_from_adjacency_matrix


def initialize():
    A = network_from_adjacency_matrix()
    edge_values = pd.DataFrame(columns=['1', '2', 'Value'])
    return A, edge_values


def save_values(values):
    values.to_csv('videos/values.csv', index=False, encoding='utf-8-sig')


def build_up_angle_network(attr_list, data_type):
    A, edge_values = initialize()

    G = A

    if data_type == 'economic':
        data_table = 'data/transversal.csv'
        data = pd.read_csv(data_table, usecols=attr_list)
        # normalize the attribute values
        for t in data[data.columns[1:]]:
            data[t] = MinMaxScaler().fit_transform(np.array(data[t]).reshape(-1, 1))

    else:
        data_table = 'data/transversal_psychological_normalized.csv'
        data = pd.read_csv(data_table, usecols=attr_list)

    # calculate normal vector for each node
    for node in nx.nodes(G):
        v = data.loc[data['Name_NUTS3'].apply(lambda x: str(node) == str(x).upper())]
        n = normalize(v.iloc[0][1:])
        # n = v.iloc[0][1:]
        G.nodes[node]['normal'] = n

    values = edge_values

    # angles list
    a_list = {}
    # calculate angle for each pair of vectors
    for e in nx.edges(G):
        s = e[0]
        t = e[1]
        n_s = G.nodes[s]['normal']
        n_t = G.nodes[t]['normal']
        a = 0
        for i in range(len(n_s)):
            a += n_s[i] * n_t[i]
        a_list[(s, t)] = a * G.get_edge_data(*e)['weight']
        values = values.append({'1': s, '2': t, 'Value': format(a, '.5f')}, ignore_index=True)

    nx.set_edge_attributes(G, a_list, 'weight_new')

    # save_values(values)

    return G


def build_up_gdp_correlation_network():
    A, edge_values = initialize()

    G = A
    # create the county network from the adjacency matrix
    G = nx.relabel_nodes(G, {'BUCURESTI': 'MUNICIPIUL BUCURESTI'})

    GDP = pd.read_csv(r'data/longitudinal.csv', usecols=['Judet', 'An', 'gdp pe locuitor'])

    # store the edge values
    values = edge_values

    # correlation values list
    corr_list = {}
    for e in nx.edges(G):
        s = e[0]
        t = e[1]
        v_s = GDP.loc[GDP['Judet'].apply(lambda x: s == str(x).upper())][['gdp pe locuitor']].dropna()
        v_t = GDP.loc[GDP['Judet'].apply(lambda x: t == str(x).upper())][['gdp pe locuitor']].dropna()

        # calculate Pearson-correlation of 'gdp pe locuitor' between the two county
        corr, _ = pearsonr(v_s['gdp pe locuitor'], v_t['gdp pe locuitor'])
        corr_list[(s, t)] = abs(corr)
        values = values.append({'1': s, '2': t, 'Value': format(corr, '.5f')}, ignore_index=True)

    nx.set_edge_attributes(G, corr_list, 'weight_new')
    G = nx.relabel_nodes(G, {'MUNICIPIUL BUCURESTI': 'BUCURESTI'})

    # save_values(values)

    return G

