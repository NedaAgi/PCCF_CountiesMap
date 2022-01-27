# coding=utf-8
from flask import Flask, render_template, request, url_for, flash, redirect, json
from map.data_functions import *
import re
from map.county_network_values import *
from correlation_heatmap.create_correlation_heatmap import *

app = Flask(__name__)

# Number of listed attributes ordered by their Gini index value
n = 20
n_corr = 20  # for correlation heatmap


@app.route('/', methods=["GET", "POST"])
def root():
    return redirect('/attribute')


# attribute vector map
@app.route('/attribute', methods=["GET", "POST"])
def attribute():
    economic_attributes = get_economic_attributes(n)
    psychological_attributes = get_psychological_attributes(n)
    if request.method == "GET":
        return render_template('attribute.html', attributes1=economic_attributes, attributes2=psychological_attributes)
    else:
        selected_attributes = request.form.keys()
        regex = re.compile(r'.*,.*,.*')
        selected_attributes = [a for a in selected_attributes if regex.match(a)]
        selected_attributes_list = [re.search('(.*),.*,.*', a).group(1) for a in selected_attributes]
        selected_attributes = [a for a in selected_attributes_list]
        selected_attributes.append('Name_NUTS3')

        if request.form.get('submit_form1'):
            data_type = 'economic'
        else:
            data_type = 'psychological'

        G = build_up_angle_network(selected_attributes, data_type)

        mapping = {'BUCURESTI': 'BUCHAREST', 'DAMBOVITA': 'DÂMBOVITA', 'VALCEA': 'VÂLCEA'}
        G = nx.relabel_nodes(G, mapping)

        l = list(nx.get_edge_attributes(G, 'weight_new').values())
        l.append(1)
        l.sort(reverse=True)

        edges = list(map(list, G.edges(data=True)))
        edgesDict = {'edges': edges}

        return render_template('attribute.html', attributes1=economic_attributes, attributes2=psychological_attributes,
                               network=json.dumps(edgesDict), attributes=selected_attributes_list, limits=l)


# gdp-correlation map
@app.route('/gdp', methods=["GET", "POST"])
def gdp_correlation():
    G = build_up_gdp_correlation_network()

    mapping = {'BUCURESTI': 'BUCHAREST', 'DAMBOVITA': 'DÂMBOVITA', 'VALCEA': 'VÂLCEA'}
    G = nx.relabel_nodes(G, mapping)

    l = list(nx.get_edge_attributes(G, 'weight_new').values())
    l.append(1)
    l.sort(reverse=True)

    edges = list(map(list, G.edges(data=True)))
    edgesDict = {'edges': edges}

    return render_template('gdp_correlation.html', network=json.dumps(edgesDict), limits=l)


@app.route('/corr', methods=["GET", "POST"])
def correlation_heatmap():
    economic_attributes = get_economic_attributes(n_corr)
    psychological_attributes = get_psychological_attributes(n_corr)

    if request.method == "GET":
        return render_template('correlation_heatmap.html', economic_attributes=economic_attributes,
                               psychological_attributes=psychological_attributes)
    else:
        regex1 = re.compile(r'.*_1')
        list1 = [(re.search('(.*)_1', a).group(1)) for a in request.form.keys() if regex1.match(a)]

        regex2 = re.compile(r'.*_2')
        list2 = [(re.search('(.*)_2', a).group(1)) for a in request.form.keys() if regex2.match(a)]

        plot_url = create_heatmap(list1, list2)
        return render_template('correlation_heatmap.html', economic_attributes=economic_attributes,
                               psychological_attributes=psychological_attributes, plot_url=plot_url)


# app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

if __name__ == "__main__":
    app.run()
