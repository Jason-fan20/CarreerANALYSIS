# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 19:56:08 2020

@author: ASUS
"""

import re
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
         return t
 else:
  return ''


text='1986.09—今  广州华南理工大学工业管理专业本科生'

a=get_strtime(text).span()
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

a=str(a).replace('(','').replace(')','')
print(a.split(', '))
print(text[0:9])
