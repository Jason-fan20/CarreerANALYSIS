# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import re
def get_strtime(text):
 text = text.replace("年", "-").replace("月", "-").replace("日", " ").replace("/", "-").strip()
 text = re.sub("\s+", " ", text)
 t = ""
 regex_list = [
 # 2013年8月15日 22:46:21
    "(\d{4}.\d{1,2}—\d{4}.\d{1,2})"
    # "2013年8月15日 22:46"

 ]
 for regex in regex_list:
     t = re.search(regex, text)
 if t:
#  t = t.group(1)
  return t
 else:
  return ''

def list_2_dic(list1):
    #print(list1)
    dict1={}
    #循环统计数字出现的个数并将其添加到字典集合中
    for i in list1:
        skey=dict1.get(i)#获取字典中的键的值
        if skey==None:#判断键的值是否为空
            dict1[i]=1
        else:
            dict1[i]+=1
    #print(dict1)
    #获取字典中的键和值
    sk=dict1.keys()
    sv=dict1.values()
    #循环判断列表中的众数
    
    
    #将字典中的值转换为列表类型并进行排序反转
    sl=list(sv)
    sl.sort()
    sl.reverse()
    dict2={}
    for i in sl:
        for j in sk:
            # 循环判断字典中的值是否与列表中的值相等若相等则值存入一个新的字典中
            if dict1[j]==i:
                dict2[j] = i
    return dict2


def var_detect(var,target):
    a=var.values();
    b=var.keys();
    if target in a:
        return 0;
    else:
        return 1;
from jpype import *

#startJVM(getDefaultJVMPath(), "-Djava.class.path=D:/NLP/hanlp/hanlp-1.7.4.jar;D:/NLP/hanlp",
#         "-Xms1g",
#         "-Xmx1g")

HanLP = JClass('com.hankcs.hanlp.HanLP')

CRFnewSegment = HanLP.newSegment("crf")

#with open("out.txt", "r",encoding='utf-8') as f:
#    data = f.readlines()
#for index,thing in enumerate(data):
#    if(len(str(thing))>20):
#        if(index<60):
#            term_list = CRFnewSegment.seg(thing)
#            print(term_list)
var1=[]
var2=[]
var3=[]     
times=6;
#with open("out_ori.txt", "r",encoding='utf-8') as f:
#    data = f.readlines() 

with open("ins.txt", "r",encoding='utf-8') as f:
    a = f.read()       
    a=a.replace('\n',' ')
    data=a.split(' ')
for time in range(1,times):
    dict_=[]
    for index,thing in enumerate(data):
    #            term_list = CRFnewSegment.seg(thing)
                    source=thing
                    term_list = CRFnewSegment.seg(source)
                    for thing_1 in term_list:
                        thing_1=str(thing_1)
                        thing_1=thing_1.split('/')[0]
                        if(len(thing_1)>=time):
                            dict_.append(thing_1[-time:])          
    with open(str(time)+".txt","w") as f:
        for thing in list_2_dic(dict_).items():
            if(thing[1]>=10):
                f.write(str(thing)+'\n') 
                    
        
#Segment = JClass("com.hankcs.hanlp.seg.Segment")
#Term = JClass("com.hankcs.hanlp.seg.common.Term")
#
#segment = HanLP.newSegment().enableOrganizationRecognize(True)
#for sentence in sentences:
#
#term_list = segment.seg(sentence)
#print(term_list)
#
#print("n========== 机构名 标准分词器已经全部关闭 ==========n")
#print(CRFnewSegment.seg(sentences[0]))
#
#segment = HanLP.newSegment('crf').enableOrganizationRecognize(True)