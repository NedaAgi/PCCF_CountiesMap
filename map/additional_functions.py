import math
import networkx as nx
import pandas as pd


def first_n_from_gini_table(df, n):
    df = df.sort_values(by='Gini_Coefficient', ascending=False)
    df = df.round({'Gini_Coefficient': 4})
    df = list(df.itertuples(index=False, name=None))
    labels = df[:n]
    return labels


def read_labels_into_list(file_path):
    with open(file_path, 'r') as file:
        label_list = file.read().splitlines()

    return label_list


def tuples_in_list_to_string(l):
    for i in range(len(l)):
        tuple_string = ', '.join(map(str, l[i]))
        l[i] = tuple_string
    return l


def vector_magnitude(x):
    return math.sqrt(sum(i ** 2 for i in x))


def normalize(x):
    l = vector_magnitude(x)
    return [v / l for v in x]


def network_from_adjacency_matrix():
    connectivity_matrix = pd.read_csv('data/judet_adjacency_matrix.csv')
    connectivity_matrix.index = connectivity_matrix['judet']

    G = nx.from_pandas_adjacency(connectivity_matrix.drop(columns=['judet', 'number_of_neighbours ']))
    G.remove_edges_from(nx.selfloop_edges(G))

    return G
