import pandas as pd
from map.additional_functions import *


def get_economic_attributes(n):
    ps = pd.read_csv(r'data/transversal_gini_weights.csv')
    ps = ps[60:]
    labels_economic = read_labels_into_list('data/economic_labels.txt')
    ps = ps[ps['Attribute'].isin(labels_economic)]
    labels_economic = first_n_from_gini_table(ps, n)
    labels_economic = tuples_in_list_to_string(labels_economic)

    return labels_economic


def get_psychological_attributes(n):
    ps = pd.read_csv(r'data/psychological_gini_weights.csv')
    labels_psychological = first_n_from_gini_table(ps, n)
    labels_psychological = tuples_in_list_to_string(labels_psychological)

    return labels_psychological
