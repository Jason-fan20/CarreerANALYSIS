he#####################
# STWalk1
# Learns trajectory representation of graph nodes by considering spatial and temporal neighbors together
#####################

import random
from gensim.models import Word2Vec
import networkx as nx
import sys
from multiprocessing import cpu_count
import time
import argparse
import os
import node2vec
import numpy as np
import scipy.io
from collections import defaultdict
from time import perf_counter
from datetime import timedelta
from gensim.models import KeyedVectors
from multiprocessing import cpu_count
def read_graph(G, directed=False): 

    if not directed:
        G = G.to_undirected()
        
    probs = defaultdict(dict)
    for node in G.nodes():
        probs[node]['probabilities'] = dict()
        
#    print(nx.info(G) + "\n---------------------------------------\n")
    return G, probs

def process(G,p,q,max_walks, node,walks_len=3,workers=None):
    
    Graph, init_probabilities = read_graph(G)
    G = node2vec.Graph(Graph, init_probabilities, p, q, max_walks, walks_len, workers)
    G.compute_probabilities()
    walks = G.generate_random_walks(node)
    
    return  walks

def createSpaceTimeGraph(G_list, time_window, start_node, time_step):
    """
     time step is necessary because we want representation only for last time step and
     we will create the space-time graph for [time_step, time_step-1,time_step-2,...,time_step-time_window]
    """
    G = G_list[-1]
    for time1 in range(1, time_window + 1):
        # MS revised
        past_node = start_node.split("_")[0] + "_" + str(time_step - time1)
        extend  = "_" + str(time_step - time1)
        # MS revised
        if past_node not in G_list[-time1 - 1]:
            continue
        else:
            G.add_edge(start_node, past_node+extend,weight=0)

            G_past = G_list[-time1 - 1]

            # considering first level neighbors
            past_neighbors = list(G_past.neighbors(past_node))
            temp = []

            # considering second level neighbors
            for elt in past_neighbors:
                temp = temp + list(G_past.neighbors(elt))

            # merging list of level-1 and level-2 neighbors
            past_neighbors = past_neighbors + temp
            past_neighbors.append(past_node)

            # subgraph of G_past containing nodes from "past_neighbors" and edges between those nodes.
            past_subgraph = G_past.subgraph(past_neighbors)

            # MS revised relabeling the subgraph
            relabeled_subgraph = nx.relabel_nodes(past_subgraph, lambda node: node +extend)
            
            # merge current graph with past subgraphs
            G = nx.compose(G, relabeled_subgraph)
            #print(G.edges)
            #print('123')
            start_node = past_node
    #nt(nx.node_link_data(G))
#    nx.write_gml(G, './1/Space_graph/'+str(start_node.split("_")[0])+'_'+str(1976+time_step)+'.gml')
    return G


def random_walk(SpaceTimegraph, path_length, rand=random.Random(0), start=None):
    """ Returns a truncated random walk.
        path_length: Length of the random walk.
        removed = alpha: probability of restarts.
        start: the start node of the random walk.
    """
    print([start])
    G = SpaceTimegraph
    if start:
        path = [start]
        print(path)
    else:
        sys.exit("ERROR: Start node not mentioned for random_walk")

    while len(path) < path_length:
        cur = path[-1]
        #print(start)
       # print(cur)
       # print(path)
        #print(1)
        if len(G[cur]) > 0:
            # MS revised split because of extended words
            #path.append(rand.choices(list([g.split("_")[0] for g in G[cur]]).split("_")[0],weights=[100-G[cur][adjnode]['weight'] for adjnode in list(G[cur])])[0])
#            print(cur)
#            print(G[cur])
#            for adjnode in list(G[cur]):
#                print(G[cur][adjnode]['weight'])
#            next_node = rand.choices(list(G[cur]),weights=[100-G[cur][adjnode]['weight'] for adjnode in list(G[cur])])[0]
           # print(G[cur])
           next_node = rand.choices(list(G[cur]),weights=[1 for adjnode in list(G[cur])])[0]
           # print('123')
            #print(next_node)
           path.append(next_node)

        else:
            break
    path_new = []
    for word in path:
        path_new.append(word.split("_")[0])
    #print(path_new)
#    print(len(path_new))
    return path_new


def create_vocab(G_list, num_restart, path_length, nodes, time_step, rand=random.Random(0), time_window=1,p=0.25,q=0.25):
    walks = []

    nodes = list(nodes)

    # number of path is equal to number of restarts per node
    for cnt in range(num_restart):
        print(cnt/num_restart)
        rand.shuffle(nodes)
        start = time.time()
        for node in list(nodes):
            G = createSpaceTimeGraph(G_list, time_window, node, time_step)
            temp=0
            for thing in G.neighbors(node):
                temp=1
#            print([start][0])
#            walks.append(random_walk(SpaceTimegraph=G, path_length=path_length, rand=rand, start=node))
            if(temp==1):
                walks.append(process(G,p,q,1,node=node,walks_len=path_length+1,workers=None)[0])
                print(random_walk(SpaceTimegraph=G, path_length=path_length, rand=rand, start=node))
    print("Vocabulary created")
    return walks


def STWalk1(input_direc, output_file, number_restart, walk_length, representation_size, time_step,
            time_window_size, workers, vocab_window_size,p,q):
    """
    This function generates representation for all nodes in space-time-graph of all nodes of graph at t=time_step
    however we will consider only representations of nodes present in graph at t = time_step
    """
    if time_window_size > time_step:
        sys.exit("ERROR: time_window_size(=" + str(time_window_size) + ") cannot be more than time_step(=" + str(
            time_step) + "):")

    G_list = [nx.read_gml(input_direc + "/" + str(i*2+2002) + ".gml") for i in
              range(time_step - time_window_size, time_step + 1)]

    # get list of nodes
    nodes = G_list[-1].nodes()
    print("Creating vocabulary...")
    walks = create_vocab(G_list, num_restart=number_restart, path_length=walk_length, nodes=nodes,
                         rand=random.Random(0), time_step=time_step, time_window=time_window_size,p=p,q=q)
    

    # time-step is decremented by 1, because, time steps are from 0 to time_step-1=total time_step length
    print("Generating representation...")
#    print(walks)
    model = Word2Vec(walks, size=representation_size, window=vocab_window_size, min_count=0, workers=workers)

    model.wv.save_word2vec_format(output_file)
    print("Representation File saved: " + output_file)
    print
    return


if __name__ == '__main__':
    print('dataset =', '2')
    '''
    if arg.dataset not in ["epinion","dblp",'ciao']:
        print("Invalid dataset.\nAllowed datsets are epinion, dblp, ciao")
        sys.exit(0)
    # by default we use Epinion dataset for experiment
    '''
    direc = "./gml"
    max_timestep = 19 # Epinion dataset has 0 to 109 graphs
    '''
    if arg.dataset == "ciao":
        direc = "../"+arg.dataset
        max_timestep = 114
    elif arg.dataset == "dblp":
        direc = "../"+arg.dataset
        max_timestep = 44
    '''
    number_restart = 20
    walk_length = 10
    representation_size = 16
    vocab_window_size = 5
    time_window_size = 5  # number of previous time steps graphs plus current time step graph

    if not os.path.exists(direc+"/output_stwalkone"):
        os.makedirs(direc+"/output_stwalkone")

    workers = cpu_count()
    seq = []

    for t in range(0, max_timestep+1):
        if (t + 1) % time_window_size == 0:
            seq.append(t)
    p=1
    q=1
    for t in seq:
        print("\nGenerating " + str(representation_size) + " dimension embeddings for nodes")
        time_step = t
        if(time_step ==4):
            start = time.time()
            STWalk1(input_direc=direc + "/input_graphs",
                    output_file=direc + "/output_stwalkone/spatiotemporal_" + str(time_step*2+2002) + ".stwalkone"+"p="+str(p)+"q="+str(q),
                    number_restart=number_restart,
                    walk_length=walk_length, vocab_window_size=vocab_window_size,
                    representation_size=representation_size, time_step=time_step, time_window_size=time_window_size - 1,
                    workers=workers,p=p,q=q)
