# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 14:44:20 2020

@author: ASUS
"""
import re
#import total2viz
from jpype import *
try:
    startJVM(getDefaultJVMPath(), "-Djava.class.path=D:/NLP/hanlp/hanlp-1.7.4.jar;D:/NLP/hanlp",
             "-Xms1g",
             "-Xmx1g")
except Exception:
    pass

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
times=4
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

def list_del_brackets(txt):
        s=txt
        s=s.replace('（','(')
        s=s.replace('）',')')
        s=s.replace('\n','tom_cat')
        a = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", s)
        a=a.replace('（','')
        a=a.replace('）','')
        a=a.replace('(','')
        a=a.replace(')','')
        a=a.replace('tom_cat','\n')
#        print(a)
        return a

def target_in_termlist(target,index,termlist):
    for index1,thing in enumerate(termlist):  
        if(target in str(thing).split('/')[0][-len(str(thing)):]and index1>=index):
#            print(target)
#            print(str(thing))
            return True
    return False

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def find_firstchar(str1,str_1_list):
    str_list=list(str1)
    count=0
    for each_char in str_list:
        count+=1
        for str_1 in str_1_list:
            try:
#                print(''.join(str_list[count:count+len(str_1)])+' '+str_1)
#                print(str_1)
                if(count+len(str_1)<len(str1)):
                    if (''.join(str_list[count:count+len(str_1)])==str_1):
#                       print(str_1)
                       return count+len(str_1)
            except Exception:
                continue
    return False
with open("total.txt","w") as f:
        dict_=[]
        for index,thing in enumerate(data[0:]):
#            if index<10:
        #            term_list = CRFnewSegment.seg(thing)
                        source=thing.replace('\n','').strip(' ')
                        term_list = CRFnewSegment.seg(source)
                        mid_temp=-1
#                        print(term_list)
                        total_list=[]
                        for index_1,thing_1 in enumerate(term_list):
                            thing_1=str(thing_1)
                            if 'nt' in thing_1 and 'nnt' not in thing_1:
                                first_element=thing_1.split('/')[0]
#                                print(first_element)
                                mid_temp=index_1
                                thing_1=first_element
                                while(find_firstchar(thing_1,str_)):
                                    total_list.append(thing_1[0:find_firstchar(thing_1,str_)])
#                                    print(1)
                                    thing_1=thing_1[find_firstchar(thing_1,str_):]
                                if(thing_1):
                                    total_list.append(thing_1)
#                                    print(thing_1)
                                break
#                            else:
#                                total_list.append(thing_1.split('/')[0])
#                        print('f is '+first_element)
                        end=False
#                        print("?")
                        for index_1,thing_1 in enumerate(term_list):
                            temp=0
                            if(index_1>mid_temp and is_Chinese(str(thing_1)[0])):
                                thing_1=str(thing_1)
                                for thing in str_:
                                    if(len(str(thing_1.split('/')[0]))>=len(thing)):
                                        if(thing[0:len(str_)] in str(thing_1.split('/')[0][-len(thing):])):
        #                                    print(1)
                                            element=''
                                            for time_temp in range(mid_temp+1,index_1+1):
                                                element=element+str(term_list[time_temp]).split('/')[0]
                                            total_list.append(element)
                                            mid_temp=index_1;
                                            temp=1
                                            break;
                                if(temp==0):
                                    first_element=thing_1.split('/')[0]
    #                                print(first_element)
                                    mid_temp=index_1
                                    thing_1=first_element
                                    while(find_firstchar(thing_1,str_)):
                                        total_list.append(thing_1[0:find_firstchar(thing_1,str_)])
    #                                    print(1)
                                        thing_1=thing_1[find_firstchar(thing_1,str_):]
                                    if(thing_1):
                                        total_list.append(thing_1)
#                                        print(total_list)
#                                    print('pri'+str(end))
#                                    if(end==False and target_in_termlist(thing[0:len(str_)],index_1,term_list)==True):
#                                        print(target_in_termlist(thing[0:len(str_)],index_1,term_list))
#                                        print(end)
#                                    print(end)
                                
#                        print('final is')
#                        print(total_list)
                        str_mid=''
                        total_list=list_del(total_list)
#                        print(total_list)
                        for thing in total_list:
                            str_mid=str_mid+thing+' ';
                        if(total_list):
                            str_mid=str_mid+' '+'\n';
                            str_mid=str_mid
                        f.write(str_mid) 
#total2viz.main()
#shutdownJVM()                      