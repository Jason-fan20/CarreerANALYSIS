# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 17:45:51 2020

@author: ASUS
"""

import argparse
import logging
import time
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from sklearn.cluster import KMeans

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.WARNING)


def load_gml_2_edge(path,file,k):
        import networkx as nx
        import os
        ins=[]
        G=nx.read_gml(os.path.join(path,str(file)+'.gml'))
        for thing in G.nodes():
#            print(G.nodes())
            if(G.nodes[thing]['ins'] not in ins):
                ins.append(G.nodes[thing]['ins'])
        print('聚类数量为'+str(k))
        print('实际类别数量为:'+str(len(ins)))
        with open('cluster.txt') as f:  #相对路径    
            dict1={}
            lines=f.readlines()
            f.close()
            for thing in lines:
                node=thing.split('\t')[0]
                cid=thing.replace('\n','').split('\t')[-1]
                if cid not in dict1.keys():
                    dict1[cid]=[]
                else:
                    dict1[cid].append(node)
            acc=0
            for thing in dict1.items():
                list1=thing[1]
#                print(list1)
                for index,thing in enumerate(list1):
                    for index1,thing1 in enumerate(list1[index+1:]):
                        if((thing,thing1) in G.edges() or(thing1,thing) in G.edges()):
                            acc=acc+1;
            print('正确率为:'+str(acc/len(G.edges())))
#            return '聚类数量为'+str(k)+' 实际类别数量为:'+str(len(ins))+' 正确率为:'+str(acc/len(G.edges()))+'\n'
            return acc/len(G.edges())
            
#def clusting(path,k):
##    parser = argparse.ArgumentParser()
##    parser.add_argument("model", help="word2vec model path")
##    parser.add_argument("format", help="1 = binary format, 0 = text format", type=int)
##    parser.add_argument("k", help="number of clusters", type=int)
##    parser.add_argument("output", help="output file")
##    args = parser.parse_args()
#    output='cluster.txt'
#    start = time.time()
#    print("Load word2vec model ... ", end="", flush=True)
#    w2v_model = KeyedVectors.load_word2vec_format(path)
##    w2v_model = Word2Vec.load_word2vec_format("./2/output_stwalkone/spatiotemporal_" +str(1988+10*3)+".stwalkone", binary=bool(0))#
#    print("finished in {:.2f} sec.".format(time.time() - start), flush=True)
#    word_vectors = w2v_model.wv.syn0
#    n_words = word_vectors.shape[0]
#    vec_size = word_vectors.shape[1]
#    print("#words = {0}, vector size = {1}".format(n_words, vec_size))
#
#    start = time.time()
#    print("Compute clustering ... ", end="", flush=True)
#    kmeans = KMeans(n_clusters=k, n_jobs=-1, random_state=0)
#    idx = kmeans.fit_predict(word_vectors)
#    print("finished in {:.2f} sec.".format(time.time() - start), flush=True)
#
#    start = time.time()
#    print("Generate output file ... ", end="", flush=True)
#    word_centroid_list = list(zip(w2v_model.wv.index2word, idx))
#    word_centroid_list_sort = sorted(word_centroid_list, key=lambda el: el[1], reverse=False)
#    file_out = open(output, "w")
##    file_out.write("WORD\tCLUSTER_ID\n")
#    for word_centroid in word_centroid_list_sort:
#        line = word_centroid[0] + '\t' +str(word_centroid[1]) + '\n'
#        file_out.write(line)
#    file_out.close()
#    print("finished in {:.2f} sec.".format(time.time() - start), flush=True)
#
#    return
#
#k=10
#clusting('spatiotemporal_2010.stwalkone',k)    
            
def main(name,k):
#    parser = argparse.ArgumentParser()
#    parser.add_argument("model", help="word2vec model path")
#    parser.add_argument("format", help="1 = binary format, 0 = text format", type=int)
#    parser.add_argument("k", help="number of clusters", type=int)
#    parser.add_argument("output", help="output file")
#    args = parser.parse_args()
    output='cluster.txt'
    start = time.time()
#    print("Load word2vec model ... ", end="", flush=True)
    w2v_model = KeyedVectors.load_word2vec_format(name)
#    w2v_model = Word2Vec.load_word2vec_format("./2/output_stwalkone/spatiotemporal_" +str(1988+10*3)+".stwalkone", binary=bool(0))#
#    print("finished in {:.2f} sec.".format(time.time() - start), flush=True)
    word_vectors = w2v_model.wv.syn0
    n_words = word_vectors.shape[0]
    vec_size = word_vectors.shape[1]
#    print("#words = {0}, vector size = {1}".format(n_words, vec_size))

    start = time.time()
#    print("Compute clustering ... ", end="", flush=True)
    kmeans = KMeans(n_clusters=k, n_jobs=-1, random_state=0)
    idx = kmeans.fit_predict(word_vectors)
    print("finished in {:.2f} sec.".format(time.time() - start), flush=True)

    start = time.time()
#    print("Generate output file ... ", end="", flush=True)
    word_centroid_list = list(zip(w2v_model.wv.index2word, idx))
    word_centroid_list_sort = sorted(word_centroid_list, key=lambda el: el[1], reverse=False)
    file_out = open(output, "w")
#    file_out.write("WORD\tCLUSTER_ID\n")
    for word_centroid in word_centroid_list_sort:
        line = word_centroid[0] + '\t' +str(word_centroid[1]) + '\n'
        file_out.write(line)
    file_out.close()
#    print("finished in {:.2f} sec.".format(time.time() - start), flush=True)

    return

if __name__ == "__main__":
    direc = "./gml"
    time_step=4
    dict1={}
    x=[]
    y=[]
    import matplotlib.pyplot as plt
    for p in [0.25,0.5,1,2,4]:
        for q in [0.25,0.5,1,2,4]:
            try:
                dict1[str(p)+' '+str(q)]=[]
                for k in range(5,6):
                    main(direc+"/output_stwalkone/spatiotemporal_" + str(time_step*2+2002) + ".stwalkone"+"p="+str(p)+"q="+str(q),k)
#                    dict1[str(p)+' '+str(q)].append(load_gml_2_edge('gml_file','2010',k))
#                    print(dict1)
                    x.append(str(p)+' '+str(q))
                    y.append(load_gml_2_edge('gml_file','2010',k))
            except Exception:
                print('wrong')
                continue
#    with open('dict1.txt','w') as f:
#         f.write(str(dict1))
    # plot函数作图
    plt.plot(x, y)  
    
    # show函数展示出这个图，如果没有这行代码，则程序完成绘图，但看不到
    plt.show()  
            
