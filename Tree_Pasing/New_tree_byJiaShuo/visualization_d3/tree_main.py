# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 20:48:05 2020

@author: ASUS
"""

id_num = 0
import sys


#sys.stdout = f
#sys.stderr = f # redirect std err, if necessary

class TreeNode:
    def __init__(self, name, id):
        self.name = name
        self.children = {}

        self.id = id

def construct_tree(paths):
    global id_num
    root = TreeNode('root',0)
    for p in paths:
        # 将paths list中的每个字符串元素分割成一个新list f，列表中的元素是被' '分割得到的
        f = p.split(' ')
        # ['root', 'a', 'b', 'c']
        # ['root', 'a', 'd', 'e', 'f']
        # ['root', 'g', 'h', 'i']
        # ['root', 'j']
        # print(f)
        pointer = root
        # print(pointer.name)  #root

        # 建树：以root为根, root的每一个直接后继（children字典里的key） 都是.txt中的一个开头字符串
        for i in range(0, len(f)):
            if f[i] not in pointer.children.keys():
                # 当前根结点
                root_id = pointer.id
                if root_id !=0:
                    print("id" + str(root_id) + "_name:" + str(pointer.name), end="")
                    pass
                # 插入操作
                id_num = id_num + 1
                node = TreeNode(f[i],id_num)
                pointer.children[f[i]] = node

                pointer = node
                # 新插入的子结点
                if root_id != 0:
                    print(" id" + str(id_num) + "_name:" + str(f[i]), end="")
                    print(" connection: id"+str(root_id)+"_name-id"+str(id_num)+"_name")
                    pass
            else:
                pointer = pointer.children[f[i]]
    return root
#    print(dfs(root))
    # {'a': <__main__.TreeNode object at 0x02C02D50>, 'g': <__main__.TreeNode object at 0x07010250>, 'j': <__main__.TreeNode object at 0x07042B90>}

    # dfs(root)返回以root树结点为根的遍历结果字符串
    # traversal_str = dfs(root)
    # 最外层加括号，表示以root为根的大树
    # tree2lin = '(' + tree2lin + ')'
    # return traversal_str

#
def dfs(root):
 if len(root.children) == 0:
     return root.name
 children = root.children
 # 如果该root仅有一个孩子
 if len(children) == 1:
     # python3的dict.keys()返回的是dict_keys对象,支持iterable但不支持indexable,so将其强制转化成list
     root_only_child = list(root.children.keys())[0]
     # print(root_only_child)
     # 孩子结点的名称 是children字典中的key
     return root.name + ' ' + dfs(root.children[root_only_child])
 else:
     result = root.name
     for c in children:
         result += ' (' + dfs(children[c]) + ') '
     # result是先序遍历序列
     return result
 
###################################viz
#def merge_node(source,target):
    
#def find_singal_node_chain(root):
sn_sequence=[]
def dfs_for_fsnc(root,str_1):
 if len(root.children) == 0:
     sn_sequence.append(str_1+' '+root.name)
 children = root.children
 # 如果该root仅有一个孩子
 if len(children) == 1:
     # python3的dict.keys()返回的是dict_keys对象,支持iterable但不支持indexable,so将其强制转化成list
     root_only_child = list(root.children.keys())[0]
     str_1=str_1+' '+root.name+'single_node'
     # print(root_only_child)
     # 孩子结点的名称 是children字典中的key
     dfs_for_fsnc(root.children[root_only_child],str_1)
     return
 else:
     str_1=str_1+' '+root.name
     for c in children:
         dfs_for_fsnc(children[c],str_1)
     # result是先序遍历序列
     return 
         # result是先序遍历序列
         
def logic2sequence(sequence,logic):
    start_bool=0
    total_se=''
    small_se=''
    for index,thing in enumerate(logic):
     if(index<len(logic)):
        if((logic[index]==1 and logic[index+1]==1) and (start_bool==0)):
            start_bool=1
            small_se=small_se+sequence[index]+sequence[index+1]
        elif((logic[index]==1) and (start_bool==1)):
            small_se=small_se+sequence[index+1]
        elif(start_bool==1):
            total_se=total_se+small_se+' '
            start_bool=0
#            print(small_se)
        else:
            total_se=total_se+sequence[index]+' '
    return total_se.replace('single_node','').strip(' ')
def merge_node_bysequence(sn_sequence1):
    new_sequence=[]
    for thing in sn_sequence1:
        thing=thing.replace('root ','')
        logic_list=[]
        for index,thing_1 in enumerate(thing.split(' ')):
            if('single_node'  in thing_1):
                logic_list.append(1)
            else:
                logic_list.append(0)
        new_sequence.append(logic2sequence(thing.split(' '),logic_list))
    return new_sequence
###################################viz

viz_temp={}
def creat_ori_viznode(name,parent):
    temp={}
    temp['name']=name
    temp['parent']=parent
    temp['children']=[]
    return temp

def creat_leaf_viznode(name,parent):
    temp={}
    temp['name']=name
    temp['parent']=parent
    return temp

total_sequence=[]
def dfs_toviz(root,str_1):
 if len(root.children) == 0:
     total_sequence.append(str_1+' '+root.name)
 children = root.children
 # 如果该root仅有一个孩子
 if len(children) == 1:
     # python3的dict.keys()返回的是dict_keys对象,支持iterable但不支持indexable,so将其强制转化成list
     root_only_child = list(root.children.keys())[0]
     str_1=str_1+' '+root.name
     # print(root_only_child)
     # 孩子结点的名称 是children字典中的key
     dfs_toviz(root.children[root_only_child],str_1)
     return
 else:
     str_1=str_1+' '+root.name
     for c in children:
         dfs_toviz(children[c],str_1)
     # result是先序遍历序列
     return 
    # with open(r'C:\Users\dell\Desktop/total.txt', encoding="UTF-8") as f:  # /会被转义，加r；默认"只读"
    
def deal_sequence(list_1):
    tree_data=[]
    for index1,thing in enumerate(list_1):
        temp=thing.strip(' ').split(' ')
        first_list=[]
        for index,thing_1 in enumerate(temp):
            if index==0:
                if(not bool(len(tree_data))):
                    tree_data.append(creat_ori_viznode(thing_1,'empty'))
                else:
                    first_list=tree_data[0]['children']
            elif index<len(temp)-1:
                parent=temp[index-1]
                children=temp[index]
                if(not bool(len(first_list))):
                    first_list.append(creat_ori_viznode(children,parent))
                    first_list=first_list[-1]['children']
                else:
                    name_list=[]
                    for thing_2 in first_list:
                        name_list.append(thing_2['name'])
#                    1print(name_list)
                    if(children not in name_list):
                        first_list.append(creat_ori_viznode(children,parent))
                        first_list=first_list[-1]['children']
#                        print(first_list)
#                        print(123)
                    else:
                        first_list=first_list[name_list.index(children)]['children']
            else:
                parent=temp[index-1]
                children=temp[index]
                first_list.append(creat_leaf_viznode(children,parent))
    return tree_data
                
def make_json(tree_data):
    import json
    with open('data.json', 'w') as f:
        json.dump(tree_data, f,ensure_ascii=False)
#        print('ok')
        
    def conversion_coding(file_name, before='gbk', after='utf8'):
        # 此处转化文件编码，默认源文件编码为gbk，转换为utf8。
        # 原理： 读取文件中所有的内容（缓存到内存中），然后覆盖原文件（将缓存中的内容重新存入新文件）
        try:
            with open(file_name,'r',encoding = before ) as f:
                file_data = f.readlines()
            with open(file_name,'w',encoding = after) as f:
                f.writelines(file_data)
        except Exception as e:
            print('转换文件“{0}”失败！:{1}'.format(file_name, e))
    conversion_coding('data.json')                
   ###################################viz    
def main(argv=None):
    with open('total.txt', "r") as f:  #相对路径
        # 整个文件内容读入total变量
        total = f.read();
    
    # 文件中的每一行作为列表中的一个字符串元素
    str_list = total.splitlines()
    # print(str_list)
    
    str_list_index = 0
    # 去掉文本中每条数据最后两个空格
    for s_temp in str_list:
        str_list[str_list_index] = s_temp[0:-2]
        str_list_index = str_list_index + 1
    # print(str_list)
#    f = open('output_result1.txt', 'a')
#
#    sys.stdout = f
#    sys.stderr = f # redirect std err, if necessary
    # temps = "['深圳市公安局 办公室', '深圳市公安局 办公室', '深圳市公安局 办公室 调研科', '深圳市公安局 指挥部 调研处 调研科', '深圳市警察局 办公室 警务科']"
    root=construct_tree(str_list)
    ###################################viz
    dfs_toviz(root,'')
    tree_data=deal_sequence(total_sequence)
    make_json(tree_data)
    ###################################viz
    dfs_for_fsnc(root,'')
    #print(sn_sequence)
    str_list=merge_node_bysequence(sn_sequence)
#            print(thing)
#    print(str_list)
    global id_num
    id_num=0
    f = open('output_result2.txt', 'a')
    sys.stdout = f
    sys.stderr = f # redirect std err, if necessary
    root1=construct_tree(str_list)
    dfs_toviz(root1,'')
    tree_data=deal_sequence(total_sequence)
    make_json(tree_data)
main()
#print(1)
#dfs_toviz(root,'')
#deal_sequence(total_sequence)
#make_json(tree_data)
###################################merge
#! /usr/bin/env python
# -*- coding: utf-8 -*-
