#dot = Digraph(comment='The Test Table')
#dot.node('Root', 'Root')
import re
with open("output_result1.txt", "r") as f:
    a = f.readlines()
    
from graphviz import Digraph
dot = Digraph(comment='The Test Table')
# 添加圆点A,A的标签是Dot A
#dot.node('Root', 'Root')
 
data=[]
First_node=[]
Total_node=[]
edge_info=[]
for thing in a :
    thing=thing.replace(' ','').replace('\n','').replace('_name:',' ')
    temp=thing.split(' ')
    id1=temp[0].split('id')[1]
    id1_name=temp[1].split('id')[0]
    id2=temp[1].split('id')[1]
    id2_name=temp[2].split('connection')[0]
    Total_node.append(id1+'+'+id1_name)
    Total_node.append(id2+'+'+id2_name)
    edge_info.append(id1+'+'+id2)
#for index1,thing1 in enumerate(data):
#    if(index1<100):
#        temp=thing1.split(' ')
#        First_node.append(temp[0])
#        for index2,thing2 in enumerate(temp):
#            Total_node.append(thing2)
#            if(index2<len(temp)-1):
#                edge_info.append(temp[index2]+'+'+temp[index2+1])
#print(Total_node)
Total_node=list(set(Total_node))
edge_info=list(set(edge_info))
First_node=list(set(First_node))
#print(Total_node)
#print(edge_info)
#print(edge_info)
for thing in Total_node:
    s=thing.split('+')
    dot.node(s[0], s[1])

# 添加圆点 B, B的标签是Dot B
#for thing in First_node:
#    dot.edge('Root', thing, '1')
    
for thing in edge_info:
    s=thing.split('+')
    dot.edge(s[0], s[1], '1')
# dot.view()
# 添加圆点 C, C的标签是Dot C
#dot.node(name='C', label= 'Dot C',color='red')
# dot.view()
#print(dot.view())
dot.render('test-table2.gv', view=True)




