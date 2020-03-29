# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:56:31 2020

@author: ASUS
"""
import re
with open("test.txt", "r",encoding='utf-8') as f:
    data = f.readlines()

t=1;
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


import os
ins_list=[];
#print(data)qqq
import thulac  
import jieba      
import keyboard #Using module keyboard                                                                             
for index,thing in enumerate(data):
   if index>=1963:
    s=get_strtime(thing);
    if s:
        print('now is' +str(index)+' line')
        source=thing[s.span()[1]:]
        list1=[]
        seg_list = jieba.cut(source) 
        for thing in seg_list:
            list1.append(thing)
        while 1:
            if ' ' in list1:
                list1.remove(' ')
            elif '\n' in list1:
                list1.remove('\n')
            elif '（' in list1:
                list1.remove('（')
            elif '）' in list1:
                list1.remove('）')
            elif '；' in list1:
                list1.remove('；')
            elif '、' in list1:
                list1.remove('、')
            elif '，' in list1:
                list1.remove('，')
            else :
                break;
        thu_result=list1;
        print(thu_result)
        h=0;
        def hrr(e):
            global t
            t=1
        keyboard.on_release(hrr,suppress=False)
        while True:#making a loop
            try: #used try so that if user pressed other than the given key error will not be shown
                if keyboard.is_pressed('a') and t==1:#if key 'q' is pressed 
                   t=0;
                   del thu_result[0]
                   print('del0:')
                   print(thu_result)
                elif keyboard.is_pressed('s') and t==1:
                   t=0
                   del(thu_result[-1])
                   print('del-1:')
                   print(thu_result)
                elif keyboard.is_pressed('1') and t==1:
                   t=0
                   thu_result[-1]=thu_result[-1][1:]
                   print('del-1:')
                   print(thu_result)
                elif keyboard.is_pressed('2') and t==1:
                   t=0
                   thu_result[-1]=thu_result[-1][:-1]
                   print('del-1:')
                   print(thu_result)
                elif keyboard.is_pressed('enter') and t==1:
                   print('final:')
                   print(thu_result)
                   a=''
                   t=0
                   for thing in thu_result:
                       a=a+thing;
                   ins_list.append(a)
                   del a
                   break
                elif keyboard.is_pressed('q') and t==1:
                   t=0
                   print('pass this')
                   break
                elif keyboard.is_pressed('d'):
                   t=1
                elif keyboard.is_pressed('f'):
                   t=0
                elif keyboard.is_pressed('g') and h==0:
                   h=1;
                   break;
            except BaseException:
                print('why wrong?')
                break #if user pressed other than the given key the loop will break
        keyboard.send('ctrl+L')
        if h==1:
            break;
    #print(data.find(s));

with open("ftest_result.txt","w") as f:
    for thing in ins_list:
        f.write(thing+'\n')  # 自带文件关闭功能，不需要再写f.close()