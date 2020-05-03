# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 10:55:22 2020

@author: ASUS
"""
import numpy as np
import re
#from utils.similarity import calEuclidDistanceMatrix
#from utils.knn import myKNN
#from utils.laplacian import calLaplacianMatrix
#from utils.dataloader import genTwoCircles
#from utils.ploter import plot
#from sklearn.cluster import KMeans
import networkx as nx
#import total2viz
from jpype import *
try:
    startJVM(getDefaultJVMPath(), "-Djava.class.path=D:/NLP/hanlp/hanlp-1.7.4.jar;D:/NLP/hanlp",
             "-Xms1g",
             "-Xmx1g")
except Exception:
    pass

#HanLP = JClass('com.hankcs.hanlp.HanLP')
#
#CRFnewSegment = HanLP.newSegment("crf")
#source='共青团深圳市宝安区委员会办公'
#term_list = CRFnewSegment.seg(source)
##print(term_list)
#thing_1='深圳市罗湖区教育局勤工俭学基建办公室  '
#str_=['区','团','局']
#total_list=[]
#def find_firstchar(str1,str_1_list):
#    str_list=list(str1)
#    count=0
#    for each_char in str_list:
#        for str_1 in str_1_list:
#            try:
##                print(''.join(str_list[count:count+len(str_1)])+' '+str_1)
##                print(str_1)
#                if(count+len(str_1)<len(str1)):
#                    if (''.join(str_list[count:count+len(str_1)])==str_1):
#                       return count
#            except Exception:
#                continue
#        count=count+1
#    return False
#while(find_firstchar(thing_1,str_)):
#                total_list.append(thing_1[0:find_firstchar(thing_1,str_)+1])
##                                            print(find_firstchar(thing_1,thing_2))
#                thing_1=thing_1[find_firstchar(thing_1,str_)+1:]
#print(total_list)
#import networkx as nx
#G = nx.Graph()
#nx.neighbors
#G.add_node('root')
#G.add_node('root1')
#G.add_node('root2')
#G.nodes['root1']['name']='123'
#G.add_edge('root','root1',weight=1)
##for thing in G.neighbors('root'):
##    print(thing['name'])
#print(G.nodes())
#def add_node(G,name):
#    G.add_node('213')
#add_node(G,'123')
#print(G.nodes())
#print([thing for thing in d.values()])
##    print(thing)
#print(fun)
#print(total_list)
nid=0
def get_child_by_level_name(G,node,level,name,nid1=False):
    for thing in G.neighbors(node):
        if(G.nodes[thing]['level']==level+1 and name==G.nodes[thing]['name']):
            return thing  
    if(nid1==False):
        global nid
        nid=nid+1
        nid2=nid+1
    else:
        nid2=nid1
    G.add_node(str(nid2))
    G.nodes[str(nid2)]['level']=level+1
    G.nodes[str(nid2)]['name']=name
    G.add_edge(node,str(nid2),weight=1/level)
    return str(nid2)
def creat_g_fromlist(list1):	
#    from fuzzywuzzy import fuzz
    G=nx.Graph()
    G.add_node('-1')
    G.nodes['-1']['level']=0
    G.nodes['-1']['name']='root'
    value_list=[list(value.keys())[0] for value in list1]
    global nid
    nid=int(max(value_list))
    for person in list1:
        nid1=int(list(person.keys())[0])
        ins=person.values()
        ins_list=list(ins)[0].split(' ')
        next_node='-1'
        for index,thing in enumerate(ins_list):
            level=index+1
            if(index==len(ins_list)-1):
                next_node=get_child_by_level_name(G,next_node,level,thing,nid1)
            else:
                next_node=get_child_by_level_name(G,next_node,level,thing)
    	
    from fuzzywuzzy import fuzz
    for thing in G.nodes():
        for thing1 in G.nodes():
            if(thing!=thing1 and G.nodes[thing]['level']==1 and G.nodes[thing1]['level']==1):            
                tempScore = fuzz.partial_ratio(G.nodes[thing]['name'], G.nodes[thing1]['name'])
                if(tempScore<80):
                    G.add_edge(thing,thing1,2)
                else:
                    G.add_edge(thing,thing1,1/tempScore)
    G1=nx.Graph()
    for index,source_node in enumerate(value_list):
        for target_node in value_list[index:]:
            G1.add_node(source_node)
            G1.add_node(target_node)
            if(nx.shortest_path_length(G,source=source_node,target=target_node)<2):
                G1.add_edge(source_node,target_node)
                
#    G.remove_node('-1')
    return G1     

def get_child_by_level_name(G,node,level,name,nid1=False):
    for thing in G.neighbors(node):
        if(G.nodes[thing]['level']==level+1 and name==G.nodes[thing]['name']):
            return thing  
    if(nid1==False):
        global nid
        nid=nid+1
        nid2=nid+1
    else:
        nid2=nid1
    G.add_node(str(nid2))
    G.nodes[str(nid2)]['level']=level+1
    G.nodes[str(nid2)]['name']=name
    G.add_edge(node,str(nid2),weight=1/level)
    return str(nid2)
def creat_fuzzy_g(list1,ratio):	
#    from fuzzywuzzy import fuzz
    from fuzzywuzzy import fuzz
    G1=nx.Graph()
    value_list=[list(value.keys())[0] for value in list1]
    ins_list=[list(value.values())[0] for value in list1]
    for index,source_node in enumerate(value_list):
        for index1,target_node in enumerate(value_list[index:]):
            G1.add_node(source_node)
            G1.add_node(target_node)
            if(fuzz.partial_ratio(ins_list[index],ins_list[index1])<ratio):
                G1.add_edge(source_node,target_node)            
#    G.remove_node('-1')
    return G1         
list1=[{'200': '公安局 南山分局 政治处副主任'}, {'1': '公安局 南山分局 副局长党委委员'}, {'2': '公安局 南山分局 南头派出所履职副所长'}, {'3': '公安局 南山分局 粤海派出所综合室主任'}, {'4': '公安局 政治部 综合处警察权益保障科副主任科员'}, {'5': '公安局 政治部 训练处教育科科长'}, {'6': '公安局 宝安分局 副局长党委委员'}, {'7': '公安局 宝安分局 第一局长、党委副书记'}, {'8': '公安局 办公室办事员'}, {'9': '公安局 蛇口公安分局四海派出所见习'}, {'10': '公安局 葵冲派出所教导员'}, {'11': '公安局 经济犯罪侦查支队一大队一副中队长'}, {'12': '公安局 罗湖分局洪湖派出所 见习'}, {'13': '公安局 罗湖分局洪湖派出所 科员'}, {'14': '公安局 桂园派出所社区防范队队长'}, {'15': '公安局 东晓派出所教导员'}, {'16': '公安局 福田分局 经侦大队 履行大队长职责'}, {'17': '公安局 福田分局 经侦大队 大队长'}, {'18': '公安局 福田分局 刑警大队大队长'}, {'19': '公安局 福田分局 莲花派出所案件侦查队队长'}, {'20': '公安局 福田分局梅林派出所刑警队队长'}, {'21': '深圳特区 报社 政文部记者'}, {'22': '深圳特区 报社 时事部编辑'}, {'23': '深圳特区 报业集团 广告中心主任助理'}, {'24': '深圳特区 报业集团 对外新闻部 编辑'}, {'25': '深圳特区 报业集团 对外新闻部 助理调研员'}, {'26': '深圳特区 报 广告部总经理'}, {'27': '深圳特区 报 港澳台新闻部编辑'}, {'28': '深圳特区 报 记者部记者'}, {'29': '深圳特区 报 新媒体部负责人'}, {'30': '深圳特区 报 中国新闻部主任'}, {'31': '深圳特区 报社人事处干部调配科副科长'}, {'32': '深圳特区 报报业集团人力资源开发中心调配部主管'}, {'33': '深圳特区 报编委办公室 秘书'}, {'34': '深圳特区 报编委办公室 主任科员副科长'}, {'35': '深圳能源集团 股份有限公司 企业文化部总监'}, {'36': '深圳能源集团 股份有限公司 管理部燃料运营计划高'}, {'37': '深圳能源集团 股份有限公司 产权法律部总监'}, {'38': '深圳能源集团 股份有限公司 规划发展部常规能源高级经'}, {'39': '深圳能源集团 企业文化部党支部支部书记'}, {'40': '深圳能源集团 党委工作部党支部书记'}, {'41': '深圳能源集团 规划发展部计划与统计高级经理'}, {'42': '政府 办公厅 综合处主任科员'}, {'43': '政府 办公厅 第一秘书处主任科员'}, {'44': '政府 办公厅 第二秘书处副处长'}, {'45': '政府 办公厅 副主任科员'}, {'46': '政府 应急管理办公室 预案综合处副处长'}, {'47': '政府 应急管理办公室 应急指挥处调研员'}, {'48': '政府 口岸办公室秘书处 科员'}, {'49': '政府 口岸办公室秘书处 主任科员'}, {'50': '政府 投资项目审计中心计财处副处长'}, {'51': '政府 法制办行政法规处副处长'}, {'52': '运输局 交管员'}, {'53': '运输局 运政管理科科长'}, {'54': '运输局 办公室科员'}, {'55': '运输局 福田分局稽查科 副科长'}, {'56': '运输局 福田分局稽查科 主任科员'}, {'57': '运输局 建设处录用公务员'}, {'58': '运输局 规划建设处主任科员'}, {'59': '深圳大学 行政学系团委书记政治辅导员'}, {'60': '深圳大学 校友会办公室主任'}, {'61': '深圳大学 校友联络部主任'}, {'62': '深圳大学 贸易系国际金融贸易专业学生'}, {'63': '深圳大学 信息工程学院辅导员'}, {'64': '光明新区 人力资源办组织科科长'}, {'65': '光明新区 社会管理局副局长'}, {'66': '光明新区 城市管理局副局长'}, {'67': '光明新区 光明党工委书记、办事处主任'}, {'68': '光明新区 综合办公室副主任'}, {'69': '人民政府 办公厅 信访办 综合处主任科员'}, {'70': '人民政府 办公厅 信访办 办理处处长'}, {'71': '人民政府 办公厅 第二秘书处主任科员'}, {'72': '人民政府 办公厅 社会一处副处长'}, {'73': '人民政府 外事办公室国际化促进处处长'}, {'74': '人民政府 应急管理办公室秘书处副处长'}, {'75': '人民政府 文化产业发展办公室副主任'}, {'76': '人民检察院 政治处 科员'}, {'77': '人民检察院 政治处 副主任科员'}, {'78': '人民检察院 科员试用期'}, {'79': '人民检察院 侦查三处主任科员'}, {'80': '人民检察院 党组成员 、反贪污贿赂局局长'}, {'81': '人民检察院 党组成员 反贪污贿赂局局'}, {'82': '人民检察院 干部助理检察员'}, {'83': '人民检察院 反贪污贿赂侦查二科副科长'}, {'84': '人民检察院 反贪污贿赂局副局长'}, {'85': '妈湾发电总厂 运行部长'}, {'86': '妈湾发电总厂 生产准备部副部长'}, {'87': '妈湾发电总厂 脱硫工程部负责人'}, {'88': '妈湾发电总厂 检修部部长'}, {'89': '妈湾发电总厂 检修总监'}, {'90': '中山大学 电子与信息系统专业学生'}, {'91': '中山大学 历史学专业学习'}, {'92': '中山大学 经济学专业学生'}, {'93': '中山大学 经济法专业学生'}, {'94': '中学教师'}, {'95': '纪委 检查室 科员'}, {'96': '纪委 检查室 副主任'}, {'97': '纪委 主任科员'}, {'98': '纪委 信访室主任'}, {'99': '纪委 案件审理室主任'}, {'100': '纪委 书记、区监委副主任人'}, {'101': '政法委 研究室副主任'}, {'102': '政法委 综合指导处副主任科员'}, {'103': '政法委 政策法规处副处长'}, {'104': '政法委 维稳一处处长'}, {'105': '水务集团 罗芳污水处理厂党支部书记'}, {'106': '水务集团 维修中心副主任'}, {'107': '水务集团 沙头角水厂副厂长'}, {'108': '水务集团 信息中心副主任'}, {'109': '深圳 是交通局运政监督分局机场交管站长'}, {'110': '深圳 巴士集团公共汽车分公司副总经理'}, {'111': '深圳 市坪山区环境保护和水务局调研员'}, {'112': '深圳 劳动时报编辑'}, {'113': '住房和建设局 财务审计处处长'}, {'114': '住房和建设局 勘察设计处处长'}, {'115': '住房和建设局 物业监管处处长'}, {'116': '农产品 股份有限公司 运通 事业部业务一部长'}, {'117': '农产品 股份有限公司 运通 一部长'}, {'118': '农产品 股份有限公司 资产经营总部副总经理'}, {'119': '农产品 股份有限公司 总经理办公室主任 助理'}, {'120': '农产品 批发公司公共关系部统计员总经理办公'}, {'121': '农产品 集团股份有限公司 规划发展总部总经理'}, {'122': '农产品 集团股份有限公司 运通三部总经理'}, {'123': '中国人民大学 法律系知识产权法第二学位班学生'}, {'124': '中国人民大学 区域经济学专业硕士研究生学习'}, {'125': '中国人民大学 档案系历史文献学专业学生'}, {'126': '教育局 党组 成员副局长'}, {'127': '教育局 党组 副书记区政府教育督导室主'}, {'128': '教育局 人事科干部副科长'}, {'129': '教育局 副局长'}, {'130': '教育局 专职党委副兼纪委书记'}, {'131': '广州铁路集团 公司长沙铁路总公司长沙机务段助理会计'}, {'132': '广州铁路集团 公司财务处出纳清算科会计稽查科等助'}, {'133': '广州铁路集团 公司资金结算中心计划部副经理会计师'}, {'134': '广东省 英德市团委书记'}, {'135': '广东省 沙头角林场干部'}, {'136': '广东省 茂名市人事局科员'}, {'137': '广东省英德市政府 党组成员市长助理'}, {'138': '广东省英德市政府 市长党组成员，市委政法委副书'}, {'139': '广东省英德市政府 副市长党组成员'}, {'140': '盐田港股份有限公司 港务部、操作部经理'}, {'141': '盐田港股份有限公司 安全管理委员会办公室副主'}, {'142': '盐田港股份有限公司 办公室主任'}, {'143': '龙华新区 民治办事处党工委委员副主任'}, {'144': '龙华新区 龙华办事处副处级领导干部'}, {'145': '龙华新区 观湖党工委委员、办事处副主任'}, {'146': '人事局 调配处副主任科员'}, {'147': '人事局 人事编制信息处处长'}, {'148': '人事局 政策法规处'}, {'149': '人大常委 会专职委员'}, {'150': '人大常委 会财政经济工作委员会主任'}, {'151': '人大常委 会龙岗街道工作委员会副主任'}, {'152': '人大常委 会办公室 副主任'}, {'153': '人大常委 会办公室 科员副主任科员'}, {'154': '中级人民法院 科员'}, {'155': '中级人民法院 研究室副主任科员'}, {'156': '中级人民法院 审判管理办公室副主任审判员'}, {'157': '社会保险基金管理局 医疗保险处副调研员'}, {'158': '社会保险基金管理局 宝安分局副调研员'}, {'159': '社会保险基金管理局 党委委员总会计师'}, {'160': '监察局 预防 腐败室副主任'}, {'161': '监察局 预防 和研究室副主任'}, {'162': '监察局 廉政教育处主任科员'}, {'163': '监察局 政策法规室主任科员'}, {'164': '监察局 宣教和教研室主任科员'}]
G=creat_g_fromlist(list1)
G1=creat_fuzzy_g(list1,10)

#print(G.nodes['100'])  
##print(G.nodes())
#g=G1
##nodeNum=len(g.nodes())
#m=nx.to_numpy_matrix(g)
##Laplacian = calLaplacianMatrix(m)
##
##x, V = np.linalg.eig(Laplacian)
###print(x)
###print(V)
##x = zip(x, range(len(x)))
##x = sorted(x, key=lambda x:x[0])
##H = np.vstack([V[:,i] for (v, i) in x]).T
##print(m)
#Lbar=getNormLaplacian(m)
#k=2
#kEigVal,kEigVec=getKSmallestEigVec(Lbar,k)
##print("k eig val are %s" % kEigVal)
##print("k eig vec are %s" % kEigVec)
#checkResult(Lbar,kEigVec,kEigVal,k)
# 
##跳过k means，用最简单的符号判别的方法来求点的归属
# 
#clusterA=[i for i in range(0,nodeNum) if kEigVec[i,1]>0]
#clusterB=[i for i in range(0,nodeNum) if kEigVec[i,1]<0]
# 
##draw graph
#colList=dict.fromkeys(g.nodes())
#for node,score in colList.items():
#	if node in clusterA:
#		colList[node]='red'
#	else:
#		colList[node]='green'
#list1=[thing for thing in colList.values()]
#plt.figure(figsize=(8,8))
#pos=nx.spring_layout(g)
#nx.draw_networkx_edges(g,pos,alpha=0.4,edge_labels=nx.get_edge_attributes(g, 'weight'))
##nx.draw_networkx_edge_labels(g, pos, edge_labels=nx.get_edge_attributes(g, 'weight'))
#nx.draw_networkx_nodes(g,pos,nodelist=colList.keys(),
#		node_color=list1)
##		cmap=list(plt.cm.Reds_r))
#nx.draw_networkx_labels(g,pos,font_size=10,font_family='sans-serif')
#plt.axis('off')
#plt.title("karate_club spectral clustering")
#plt.savefig("spectral_clustering_result.png")
#plt.show()  
#          
##     
##import numpy as np
##from sklearn import datasets
###X, y = datasets.make_blobs(n_samples=500, n_features=6, centers=5, cluster_std=[0.4, 0.3, 0.4, 0.3, 0.4], random_state=11)           
##print(X)
##from sklearn.cluster import SpectralClustering
##y_pred = SpectralClustering().fit_predict(H)
##from sklearn import metrics
##print (metrics.calinski_harabaz_score(X, y_pred))
##print(y_pred)