import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sqlite3

THREESHOLD = 7000 #the maximum size of the node, to avoid huge sizes in graph printing

def plotGraph(database_path): 
    conn = sqlite3.connect(database_path)
    df = pd.read_sql("SELECT * FROM network", conn)
    data = df[['domain', 'traffic_from', 'traffic_to']]
    data.insert(0,'from', "localhost")
    data.columns = ['from','to','traffic_from', 'traffic_to']
    

    #Set figure size
    plt.figure(3, figsize=(14,8))


    # Build the graph
    G=nx.from_pandas_edgelist(data, 'from', 'to', create_using=nx.Graph())
    pos=nx.spring_layout(G)

    labels = {}
    sizes = []
    for node in G.nodes():
        if(node=='localhost'): sizes.append(0)
        else:
                row = data.loc[data['to'] == node].values
                imp = int((row[0][2]+row[0][3])/256)
                if(imp>THREESHOLD): sizes.append(THREESHOLD)
                else: sizes.append(imp)

    nx.draw(G,pos, with_labels=True,
            node_size=sizes,
            node_color='skyblue', 
            width=1.0,
            edge_color='orange',
            font_size=12,
            font_color="#333333")

    #text padding
    x_values, y_values = zip(*pos.values())
    x_max = max(x_values)
    x_min = min(x_values)
    x_margin = (x_max - x_min) * 0.25
    plt.xlim(x_min - x_margin, x_max + x_margin)

    plt.show()
