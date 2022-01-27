import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from io import BytesIO
import base64


def create_heatmap(list1, list2):
    p = pd.read_csv(r'data/transversal_psychological_normalized.csv')
    list2 = [x for x in list2 if x not in list1]
    attr_list = list1 + list2
    p_new = p[attr_list]

    corr = p_new.corr()
    # sum_corr = abs(p_new.corr()).sum().sort_values(ascending=True).index.values
    # corr = p_new[sum_corr].corr()
    corr = corr.iloc[len(list1):, :len(list1)]

    # if len(corr) > 10:
    #     annotation = False
    # else:
    #     annotation = True

    annotation = True
    fig = plt.figure(figsize=(12, 10))
    if len(list1) == len(list2) == 0:
        font_scale = 1
    else:
        font_scale = min(10.0 / max(len(list1), len(list2)), 1.5)
    font_size = font_scale*13
    sns.set(font_scale=font_scale)
    ax = sns.heatmap(corr, annot=annotation, fmt='.2f', linewidth=1, vmin=-1, vmax=1, xticklabels=True,
                     yticklabels=True, cmap=sns.diverging_palette(220, 10, as_cmap=True))
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=font_size)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, fontsize=font_size, rotation_mode='anchor', ha='right')
    ax.figure.tight_layout()
    fig.add_axes(ax)
    img = BytesIO()
    ax.figure.savefig(img, format='png', transparent=True, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.clf()
    return plot_url
