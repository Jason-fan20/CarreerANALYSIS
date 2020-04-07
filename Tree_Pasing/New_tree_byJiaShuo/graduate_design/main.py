from treelib import Node, Tree 


import re   
import load_oritxt
import word2vec_cluster
# =============================================================================
# Del the brackets in txt, list1 is transfromed by txt.readlines() 
# =============================================================================
def list_del_brackets(list1):
    list2=[]
    for thing in list1:
        s=thing
        s=s.replace('（','(')
        s=s.replace('）',')')
        a = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", s)
        a=a.replace('（','')
        a=a.replace('）','')
        a=a.replace('(','')
        a=a.replace(')','')
        list2.append(a)
    return list2
# =============================================================================
# load txt and return str_list, name 'total.txt' del_DZ indicate whether to del 深圳市
#  now unuseful
# =============================================================================
def load_txt(name,del_SZ):
    with open(name, "r",encoding='utf-8') as f:  #相对路径
        # 整个文件内容读入total变量
        total = f.read();
    
    # 文件中的每一行作为列表中的一个字符串元素
    str_list = total.splitlines()
    str_list = list_del_brackets(str_list)
    str_list_index = 0
    # 去掉文本中每条数据最后两个空格
    for s_temp in str_list:
        str_list[str_list_index] = s_temp[0:-2].replace('深圳市','').strip(' ')
        str_list_index = str_list_index + 1
        
    return str_list
# =============================================================================
# remove file
# =============================================================================
def remove_file(name):
    import os, sys
    if(os.path.exists(name)):
        os.remove(name)
        print ('移除文件'+name)
    else:
        print ("要删除的文件不存在！")
class CNode(dict): 
    def __init__(self, id,name=None,count=None,positions=None): 
        self.id = id # Represents a different ID, each node has a different ID eg:0,1,2,3
        self.name = name  #eg: ”深圳市”“南山区“ ”南山街道”       
        super().__init__(self,name=name) # attribute in json export
        self.positions = positions  #position information, eg:”处长”“局长“
        self.count = count # Represents if the node is the last node eg:  ”深圳市 南山区 南山街道 队长”   “南山街道 count=1  南山区count=0
        super().__init__(self,count=count)
        self.txt_info=[]

    def get_prefix(self): 
        pass  
    
    def setname(self,name):
        self.name=name
    def count_plus(self):
        self.count=self.count+1
    def set_count(self,count):
        self.count=count
    def append_txt_info(self,txt):
        self.txt_info.append(txt)
total_sequence=[]
dfs_list=[]
tree_data=[]
class CTree(Tree):
    def __init__(self):
        Tree.__init__(self)
        self.id_num=0 # unique id
# =============================================================================
# input is list of sequence, use this info to buildtree
# =============================================================================
    def build_tree(self, listofseqs):
        n1=tree.create_node(identifier=0, data=CNode(self.id_num,"root",0))
        self.id_num=self.id_num+1
        # add a list of parsed institution names to the tree
        for seq in listofseqs:
            self.add_sequence(seq)
# =============================================================================
# get chilidren name of one node, input is node(CNode) itself            
# =============================================================================
    def children_namelist(self,node_one):
        list1=[]
        for thing in tree.children(node_one.identifier):
            list1.append(thing.data['name'])
        return list1
# =============================================================================
#  getchildrennode_byname, input is one node and its one child name   
# =============================================================================
    def getchildrennode_byname(self,node_one,name):
        for thing in tree.children(node_one.identifier):
            if(thing.data['name']==name):
                return thing
            
# =============================================================================
#         # get the prefix of node n. 
        # e.g. get_prefix(n3) returns [n1,n2,n3]
# =============================================================================
    def get_prefix(self,n):
        global dfs_list
        pointer = tree.get_node(0)
        dfs_list = []
        n_node = self.dfs_search(pointer, n)
        dfs_list.pop(0)
        dfs_list.append(n_node)
        return dfs_list
# =============================================================================
# search from root node, if finding target name return it, and add 
# its parent to list        
# =============================================================================
    def dfs_search(self,root, aim_node_name):
        global dfs_list
#        print(1231231231)
        if root.data['name'] == aim_node_name:
            return root
        children_dict = tree.children(root.identifier)
        for child_key in children_dict:
            ret_node = self.dfs_search(child_key, aim_node_name)
            if ret_node != None:
                dfs_list.insert(0,root)
                return ret_node
        return None
# =============================================================================
# add sequence in tree    
# =============================================================================
    def add_sequence(self,seq):
        p=seq;
        # 将paths list中的每个字符串元素分割成一个新list f，列表中的元素是被' '分割得到的
        f = p.split(' ')
#        print(f)
        # ['root', 'a', 'b', 'c']
        # ['root', 'a', 'd', 'e', 'f']
        # ['root', 'g', 'h', 'i']
        # ['root', 'j']
        # print(f)
        pointer = self.get_node(0)
        # print(pointer.name)  #root

        # 建树：以root为根, root的每一个直接后继（children字典里的key） 都是.txt中的一个开头字符串
        for i in range(0, len(f)):
#            print(f[i])
#            print(pointer)
#            print('end')
            if f[i] not in tree.children_namelist(tree.get_node(pointer.identifier)):
                # 当前根结点
                root_id = pointer.identifier
                if root_id !=0:
#                    print("id" + str(root_id) + "_name:" + str(pointer.data['name']), end="")
                    pass
                # 插入操作
                if i== len(f)-1:
                    n1=tree.create_node(identifier=self.id_num, parent=pointer.identifier,data=CNode(self.id_num,f[i],1))
                else:
                    n1=tree.create_node(identifier=self.id_num, parent=pointer.identifier,data=CNode(self.id_num,f[i],0))
                self.id_num=self.id_num+1
#                print(self.id_num)

                pointer = n1
                # 新插入的子结点
                if root_id != 0:
#                    print(" id" + str(self.id_num) + "_name:" + str(f[i]), end="")
#                    print(" connection: id"+str(root_id)+"_name-id"+str(self.id_num)+"_name")
                    pass
            else:
                pointer = tree.getchildrennode_byname(pointer,f[i])
                if i== len(f)-1:
                    pointer.data['count']=pointer.data['count']+1
                    pointer.data.count_plus()
        pass

# =============================================================================
#            # return the node corresponding to the prefix
        # e.g. search_prefix("深圳市,南山区,南山街道") returns n3
# =============================================================================
    def search_prefix(self,prefix):
        # return the node corresponding to the prefix
        # e.g. search_prefix("深圳市,南山区,南山街道") returns n3
        prefix_list = prefix.split(",")
        # print(prefix_list)
        prefix_list_len = len(prefix_list)

        p_list_num = 0

        pointer = self.get_node(0)
        for p_node_name in prefix_list:
            is_found = False
            for child_name in tree.children_namelist(tree.get_node(pointer.identifier)):
                # print(child_name+" s_node_name:"+s_node_name)
                if p_node_name == child_name:

                    is_found = True
                    node = tree.getchildrennode_byname(pointer,child_name)
                    break
            if is_found == False:
                print("ERROR: node "+p_node_name+" does not exist!")
                return None

            p_list_num = p_list_num + 1
            if p_list_num == prefix_list_len:
                return node
            pointer = node
        pass
# =============================================================================
#         # merge node a and its child b into one node "a,b", it's a dfs search 
         #from one node
# =============================================================================
    def merge_child(self,a):
        # merge node a and its child b into one node "a,b"
        #comment: In my opinion, merge_child and merge_subtree is a successive procedure, maybe I will use one function to implement this part.
        pointer=a
        while(len(self.children(pointer.identifier))==1):
            if(pointer.data['count']==0):
                old_pointer=pointer
                child_pointer=self.children(pointer.identifier)[0]
                child_pointer.data['name']=pointer.data['name']+'-'+child_pointer.data['name']
#                child_pointer.data.setname(pointer.data['name']+'-'+child_pointer.data['name'])
#                print(child_pointer.data['name'])
#                print(child_pointer.identifier)
#                print('====')
#                print(self.parent(child_pointer.identifier))
                self.move_node(child_pointer.identifier,self.parent(pointer.identifier).identifier)
                pointer=child_pointer
#                print(pointer)
                self.remove_node(old_pointer.identifier)
            else:
                break
        pointer.data.setname(pointer.data['name'])
#        print(self.parent(pointer.identifier))
        for thing in self.children(pointer.identifier):
            self.merge_child(thing)
        pass
# =============================================================================
# use merge_child to compress_tree    
# =============================================================================
    def compress_tree(self):
        # compress all zero count non-branching paths in the tree
        # comment: using count( maybe zero, or 1...2)
        # comment: Using DFS to detect zero count, once finding it, merge it and return true, while true, continue DFS, otherwise end.
        pointer = self.get_node(0)
        self.merge_child(pointer)
        pass
    
# =============================================================================
# visualization part, use tree.tree_d3() to generate data.json file
        #later we will use data.json to visualization
# =============================================================================
    def creat_ori_viznode(self,name,parent):
        temp={}
        temp['name']=name
        temp['parent']=parent
        temp['children']=[]
        return temp
    
    def creat_leaf_viznode(self,name,parent):
        temp={}
        temp['name']=name
        temp['parent']=parent
        return temp
    
    def dfs_toviz(self,root,str_1):
     if len(self.children(root.identifier)) == 0:
         global total_sequence
         total_sequence.append(str_1+' '+root.data['name'])
         return
     # 如果该root仅有一个孩子
     if len(self.children(root.identifier)) == 1:
         # python3的dict.keys()返回的是dict_keys对象,支持iterable但不支持indexable,so将其强制转化成list
         root_only_child = self.children(root.identifier)[0]
         str_1=str_1+' '+root.data['name']
         # print(root_only_child)
         # 孩子结点的名称 是children字典中的key
         self.dfs_toviz(root_only_child,str_1)
         return
     else:
         str_1=str_1+' '+root.data['name']
         for c in self.children(root.identifier):
             self.dfs_toviz(c,str_1)
         # result是先序遍历序列
         return 
 
    def deal_sequence(self,list_1):
        global tree_data
        tree_data=[]
        for index1,thing in enumerate(list_1):
            temp=thing.strip(' ').split(' ')
            first_list=[]
            for index,thing_1 in enumerate(temp):
                if index==0:
                    if(not bool(len(tree_data))):
                        tree_data.append(self.creat_ori_viznode(thing_1,'empty'))
                    else:
                        first_list=tree_data[0]['children']
                elif index<len(temp)-1:
                    parent=temp[index-1]
                    children=temp[index]
                    if(not bool(len(first_list))):
                        first_list.append(self.creat_ori_viznode(children,parent))
                        first_list=first_list[-1]['children']
                    else:
                        name_list=[]
                        for thing_2 in first_list:
                            name_list.append(thing_2['name'])
    #                    1print(name_list)
                        if(children not in name_list):
                            first_list.append(self.creat_ori_viznode(children,parent))
                            first_list=first_list[-1]['children']
    #                        print(first_list)
    #                        print(123)
                        else:
                            first_list=first_list[name_list.index(children)]['children']
                else:
                    parent=temp[index-1]
                    children=temp[index]
                    first_list.append(self.creat_leaf_viznode(children,parent))
        return tree_data
                
    def make_json(self,tree_data):
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
        
    def tree_d3(self):
        root = self.get_node(0)
        global total_sequence
        total_sequence=[]
        self.dfs_toviz(root,'')
        tree_data=self.deal_sequence(total_sequence)
        self.make_json(tree_data)
        pass
        #comment: input is tree self, output is d3_data_structure
        #comment:  eg: 	[{"name": "root", "parent": "empty", "children": [{"name": "华南理工大学", "parent": "root", "children": [{"name": "工业管理工程", "parent": "华南理工大学", "children": [{"name": "	专业", "parent": "工业管理工程"}, {"name": "专业", "parent": "工业管理工程"}]}, {"name": "船舶与海洋工程", "parent": "华南理工大学", "children": [{"name": "系", "parent": "船	舶与海洋工程", "children": [{"name": "内燃机专业", "parent": "系"}]}]}
# =============================================================================
# d3 visualiaziton part end
# =============================================================================
        
# =============================================================================
#         graphviz visualiaztion part, use 
#         tree.to_graphviz('source1.gv')
#         tree.show_graphviz('source1.gv')
#         please
# =============================================================================
    def show_graphviz(self,name):
        with open(name, "r",encoding='utf-8') as f:
            dot1 = f.read()
#        print(dot1)
        import graphviz
        remove_file('source.gv')
        remove_file('source.gv.pdf')
        dot=graphviz.Source(dot1)
        dot.view()
# =============================================================================
#  graphviz visualiaztion part end       
# =============================================================================
        
# =============================================================================
# This is some work made by JiaShuo, it has no relationship with tree itself
        #latex the data will be used by spatial temporal graph
# =============================================================================
    def everynode_count(self,node):
        pointer = node
        if(len(tree.children(pointer.identifier))>=1):
            for thing in tree.children(pointer.identifier):         
                pointer.data['count']=pointer.data['count']+tree.everynode_count(thing)
                pointer.data.set_count(pointer.data['count'])
            return pointer.data['count']
        else:
            return node.data['count']
        
    def get_first_child_bycount(self):
        dict1={}
        for pointer in tree.children(0):
            if(pointer.data['count']>=1):
                dict1[pointer.data['name']]=pointer.data['count']
        after = dict(sorted(dict1.items(), key=lambda e: e[1],reverse=True))
        self.fcl=after
    
    def find_repeat_element(self):
        dict1=self.fcl
        import copy
        dict2=copy.deepcopy(dict1)      
        for index,thing in enumerate(dict1.items()):
            for index1,thing1 in enumerate(dict1.items()):
                    if(index1>index and len(thing1[0])>=1 and len(thing[0])>=1):
#                        print(3)
                        if(thing1[0] in thing[0]):
                            dict2[thing1[0]]=thing[1]+thing1[1]
                            del dict2[thing[0]]
                            del dict1
                            self.fcl=dict2
                            return 1
                        if(thing[0] in thing1[0]):
                            dict2[thing[0]]=thing[1]+thing1[1]
                            del dict2[thing1[0]]
                            del dict1
                            self.fcl=dict2
                            return 1
        return 0

    def del_repeat_element(self):
        while(tree.find_repeat_element()):
#            print(self.fcl.items())
            pass
        self.fcl=dict(sorted(self.fcl.items(), key=lambda e: e[1],reverse=True))
#        print(self.fcl)
        
    def get_ins_byins(self,ins):
        for thing in self.fcl.items():
            if(thing[0] in ins and thing[0]!=''):
                return thing[0]
        return 'Othertype'
            
    def txt200_vector(self,path):
        self.vector=[]
        import os
        small_time=9999
        max_time=0
        def file_name(file_dir):
            for root, dirs, files in os.walk(file_dir):
#                print(root)  # 当前目录路径
#                print(dirs)  # 当前路径下所有子目录
#                print(files)  # 当前路径下所有非目录子文件
                return files
        for thing in file_name(path):
            with open(os.path.join(path,thing),"r",encoding='utf-8') as f:  #相对路径
                lines=f.readlines()
                time_record=[]
                for index,line in enumerate(lines):
                    time=line.split(' ')[0].split('时间：')[1][0:4]
                    ins=tree.get_ins_byins(line.split(' ')[1])
                    if(time not in time_record):
                        if(index==len(lines)-1):
                            if(small_time>int(time)):
                                small_time=int(time)
                            if(max_time<int(time)):
                                max_time=int(time)
                        time_record.append(time)
                        self.vector.append(thing.split('.xls')[0]+' '+time+' '+ins)
#        print(self.vector)
        print(small_time)
        print(max_time)
    def generate_gmlfile(self,path):
        import networkx as nx
        import os
        load_oritxt.mkdir(path)
        for time in range(2002,2011):
            node=[]
            edge=[]
            G = nx.Graph()
            for index,thing in enumerate(self.vector):
#                print(thing)
                name=thing.split(' ')[0]
                time_0=int(thing.split(' ')[1])
                ins=thing.split(' ')[2]
                for thing1 in self.vector[index+1:]:
                    name1=thing1.split(' ')[0]
                    time_1=int(thing1.split(' ')[1])
                    ins1=thing1.split(' ')[2]
                    if(time_0 == time and time_1==time):
                        if(name not in G.nodes()):
                            G.add_node(name)
                            G.nodes[name]['ins']=ins1
                        if(name1 not in G.nodes()):
                            G.add_node(name1)
                            G.nodes[name1]['ins']=ins1
                        edge_single=name+' '+name1
                        if(ins1==ins and edge_single not in edge):              
                            edge.append(edge_single)
                            G.nodes[name1]['ins']=ins1
                            G.nodes[name]['ins']=ins1
            for edge_s in edge:
                G.add_edge(edge_s.split(' ')[0],edge_s.split(' ')[1])
            nx.write_gml(G, os.path.join(path,str(time)+'.gml'))    
            print(time)
                    
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
        with open('clustering.txt') as f:  #相对路径    
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
                for index,thing in enumerate(list1):
                    for index1,thing1 in enumerate(list1[index+1:]):
                        if((thing,thing1) in G.edges() or(thing1,thing) in G.edges()):
                            acc=acc+1;
            print('正确率为:'+str(acc/len(G.edges())))
                        
                    
            
#        print(dict1)
        
#        print(dict1)
        
tree = CTree()
import sys
#f = open('output_result1.txt', 'a')
#
#sys.stdout = f
#sys.stderr = f # redirect std err, if necessary
name='out_ori.txt'
del_SZ=1 #'delete '深圳市' or not
list1=load_txt(name,del_SZ)
list1=list1[0:]
tree.build_tree(list1)
tree.get_first_child_bycount()
tree.del_repeat_element()

#tree.txt200_vector('output')
#tree.generate_gmlfile('gml_file')
#tree.move_node(4, 8)
tree.add_sequence("中欧 国际 阿妹 姐姐")
prefix_last_note = tree.search_prefix("中欧,国际,阿妹,姐姐")
prefix_node_list = tree.get_prefix("姐姐")
#print(prefix_node_list)
#for n in prefix_node_list:
#    print(n.data['name'])
tree.everynode_count(tree.get_node(0))
#print(tree.get_ins_byins('深圳特区'))
#for thing in tree.children(0):
#    if(thing.data['count']>2):
#       print(thing.data['name']+str(thing.data['count']))
tree.show(data_property="count")
tree.compress_tree()
tree.tree_d3()
tree.to_graphviz('source1.gv')
tree.show_graphviz('source1.gv')
tree.show(data_property="name")
#print(tree.get_node(1).data['count'])
#print(tree.to_json(with_data=True))
