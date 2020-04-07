# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 19:56:08 2020

@author: ASUS
"""

import re
import os
def mkdir(path):
    # 引入模块
    import os
 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        os.makedirs(path) 
        return True
    else:
        import shutil  
        shutil.rmtree(path)  
        os.mkdir(path)
#        os.makedirs(path) 
        return False
    
def get_strtime(text):
 text = text.replace("年", "-").replace("月", "-").replace("日", " ").replace("/", "-").strip()
 text = re.sub("\s+", " ", text)
 t = ""
 regex_list = [
 # 2013年8月15日 22:46:21
    "(\d{4}.\d{1,2}—\d{4}.\d{1,2})"
    ,"(\d{4}.\d{1,2}—今)"
    # "2013年8月15日 22:46"

 ]
 for regex in regex_list:
     t = re.search(regex, text)
     if t:
#  t = t.group(1)
         return str(t.span()).replace('(','').replace(')','').split(', ')
 else:
  return ''

def get_name(text):
 text = text.replace("年", "-").replace("月", "-").replace("日", " ").replace("/", "-").strip()
 text = re.sub("\s+", " ", text)
 t = ""
# print(text)
 regex_list = [
 # 2013年8月15日 22:46:21
    "(.xls)"
    # "2013年8月15日 22:46"

 ]
 for regex in regex_list:
     t = re.search(regex, text)
     if t:
#  t = t.group(1)
#         print(t)
         return str(t.span()).replace('(','').replace(')','').split(', ')
 else:
  return ''

text='1986.09—1986.09  广州华南理工大学工业管理专业本科生'
a=get_strtime(text)
list1=[]
list2=[]

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
total=''
with open('out_ori.txt',"r",encoding='utf-8') as f:  #相对路径
    total=f.read()
    total=list_del_brackets(total)
    f.close()
with open('out_del_brackets.txt',"w",encoding='utf-8') as f:  #相对路径
    f.write(total)
    f.close()
#print(total[0:500])
#print(re.search(total[0:500],'（'))
#print(list_del_brackets(total[0:500]))
path='file'
mkdir(path)
f1=None
small_time=0
with open('out_del_brackets.txt',"r",encoding='utf-8') as f:  #相对路径
        # 整个文件内容读入total变量
        total = f.readlines();
        for thing in total:
            if get_name(thing):
                name=thing[0:int(get_name(thing)[1])]
            if(get_strtime(thing)):
                begin=int(get_strtime(thing)[0])
                if(begin==0):
                    end=int(get_strtime(thing)[1])
#                    print(int(thing[begin:begin+4]))
                    if(int(thing[begin:begin+4])>small_time):
                        small_time=int(thing[begin:begin+4])
#                        print(small_time)
#                        print(1)
                    with open(os.path.join(path,name+'.txt'),"a",encoding='utf-8') as f1:
                         
                         f1.write(('时间：'+thing[begin:end])+' '+thing[end:].strip(' '))
                         

print(small_time)
#print(list1)