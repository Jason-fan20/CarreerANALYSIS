# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 17:04:31 2020

@author: ASUS
"""

#from fuzzywuzzy import fuzz
#tempScore = fuzz.partial_ratio('公安局 南山分局 政治处副主任2', '公安局 南山分局 副局长党委委员1')
#print(tempScore)
#
####-*- encoding:utf-8 -*-
##import sys
###reload(sys)
###sys.setdefaultencoding('utf-8')
##import numpy as np
##from numpy import *
### X=[ [1,2,1,1],
###     [3,3,1,2],
###     [3,5,4,3],
###     [5,4,5,4],
###     [5,6,1,5],
###     [6,5,2,6],
###     [8,7,1,2],
###     [9,8,3,7]]
### X=np.array(X).T#这里注意，[1,2,1,1]在numpy的眼中是一列
## 
## 
##np.linalg.eig
##X=[[-1,1,0],
##[-4,3,0],
##[1,0,2]]
# 
#X=matrix(X)
#eigenvalue,featurevector=np.linalg.eig(X)
#print("eigenvalue=",eigenvalue)
#print("featurevector=",featurevector)

#import networkx as nx
#G = nx.Graph()
#G.add_node('root')
#G.add_node('root')
#G.add_node('root1')
#G.add_node('root2')
#G.nodes['root1']['name']='123'
#G.add_edge('root','root1',weight=1)
#G.add_edge('root','root1',weight=1)
#G.add_edge('root1','root',weight=1)
#G.add_node('root')
##print(G.nodes())
##print(G.edges())
#
#import random
#print(random.random())

list1=[1,1,1,1,2,2,2,2]
list2=[2,2,2,3,3,3,3,3]
label_list=list1
y_pred=list2
acc_final=0
value_list=label_list
#        print(value_list)
for index,thing in  enumerate(value_list):
    acc=0
#            print(len(value_list)-2)
    for index1,thing1 in  enumerate(value_list):
        if(index1!=index):
            if(index<=(len(value_list)-1) and index1<=(len(value_list)-1)):
#                print(123)
                if(y_pred[index]==y_pred[index1] and value_list[index]==value_list[index1]):
                    acc=acc+1;
                if(y_pred[index]!=y_pred[index1] and value_list[index]!=value_list[index1]):
                    acc=acc+1;
    if(index==0):
        acc_final=acc/(len(value_list)-1)
    else:
        acc_final=(acc_final+acc/(len(value_list)-1))/2
#print(acc_final)
from sklearn import metrics
print(metrics.adjusted_mutual_info_score(list1, list2))


from fuzzywuzzy import fuzz
print(fuzz.partial_ratio('123','123'))