# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 14:44:20 2020

@author: ASUS
"""
import re
import total2viz
from jpype import *
#startJVM(getDefaultJVMPath(), "-Djava.class.path=D:/NLP/hanlp/hanlp-1.7.4.jar;D:/NLP/hanlp",
#         "-Xms1g",
#         "-Xmx1g")

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

def list_del(list_):
    list_num1=[]
    list_num=[]
    for i in range(0,len(list_)):
        for j in range(i+1,len(list_)):
            if(list_[i] in list_[j]):
                list_num1.append(i)
    for i in range(0,len(list_)):
        if(i not in list_num1):
            list_num.append(i)
   
    list_new=[]	
    if(list_num):
        for thing in list_num:
            list_new.append(list_[thing])
    else:
            list_new=list_;
    return list_new;
HanLP = JClass('com.hankcs.hanlp.HanLP')

CRFnewSegment = HanLP.newSegment("crf")

#with open("ins.txt", "r",encoding='utf-8') as f:
#    a = f.read()       
#    a=a.replace('\n',' ')
#    data=a.split(' ')

##load data

with open("out_ori.txt", "r",encoding='utf-8') as f:
    data = f.readlines()

data1=[]
for index,thing in enumerate(data):
        s=get_strtime(thing);
        if s:
            data1.append(thing[s.span()[1]+2:])
data=data1
times=6
str_=[]
num_=[]
for thing in range(1,times):  
    with open(str(thing)+".txt", "r") as f:
        a = f.readlines()
    num_=[]
    for thing in a:
        thing=thing.replace('(',' ').replace(')',' ').replace(',',' ').replace('\n',' ').replace('\'',' ')
        thing=thing.split(' ')
        str_.append(thing[2])
        num_.append(thing[5])
for i  in  range(0,len(num_)):
    for j in range(i+1,len(num_)):
        if(num_[j]>num_[i]):
           num_[j],num_[i]=num_[i],num_[j]
           str_[j],str_[i]=str_[i],str_[j]
#print(str_)
#for thing in 
#    print(thing.split(' '))



 
with open("total.txt","w") as f:
        dict_=[]
        for index,thing in enumerate(data):
#            if index<10:
        #            term_list = CRFnewSegment.seg(thing)
                        source=thing
                        term_list = CRFnewSegment.seg(source)
                        mid_temp=-1
                        total_list=[]
    #                    print(term_list)
#                        print('total is:')
#                        print(term_list)
                        for index_1,thing_1 in enumerate(term_list):
                            thing_1=str(thing_1)
                            if 'nt' in thing_1 and 'nnt' not in thing_1:
                                first_element=thing_1.split('/')[0]
                                mid_temp=index_1
#                                print(thing_1)
                                break
                        for index_1,thing_1 in enumerate(term_list):
                                thing_1=str(thing_1)
                                for thing in str_:
    #                                print(2)
                                    if(mid_temp==-1):
#                                        print(thing)
#                                     print(len(str(thing_1.split('/')[0])))
#                                     print(str(len(str_))+'123')
#                                     print(3)
                                     if(len(str(thing_1.split('/')[0]))>=len(thing)):
#                                        print(2)
                                        if(thing[0:len(str_)] in str(thing_1.split('/')[0][-len(thing):])):
#                                            print(2)
#                                            print(1)
                                            first_element=thing_1.split('/')[0]
                                            mid_temp=index_1
#                        print('f is '+first_element)
                        if(mid_temp==-1):
                            continue;
                        total_list.append(first_element)
                        for index_1,thing_1 in enumerate(term_list):
                            if(index_1>mid_temp):
                                thing_1=str(thing_1)
                                for thing in str_:
    #                                print(thing)
    #                                print(str(thing_1.split('/')[0][-1]))
    #                                if(thing == '办'):
    #                                print(thing)
                                 if(len(str(thing_1.split('/')[0]))>=len(thing)):
                                    if(thing[0:len(str_)] in str(thing_1.split('/')[0][-len(thing):])):
    #                                    print(1)
                                        element=''
                                        for time_temp in range(mid_temp+1,index_1+1):
                                            element=element+str(term_list[time_temp]).split('/')[0]
                                        total_list.append(element)
                                        mid_temp=index_1;
                                        break;
#                        print('final is')
#                        print(total_list)
                        str_mid=''
                        total_list=list_del(total_list)
#                        print(total_list)
                        for thing in total_list:
                            str_mid=str_mid+thing+' ';
                        str_mid=str_mid+' '+'\n';
                        f.write(str_mid) 
total2viz.main()
#shutdownJVM()                      