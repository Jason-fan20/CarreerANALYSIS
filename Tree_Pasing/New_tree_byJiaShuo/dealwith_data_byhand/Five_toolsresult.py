# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:31:00 2020

@author: ASUS
"""
#with open("test.txt", "r",encoding='utf-8') as f:
#    data = f.readlines()
#    #print(data)
#for thing in data:
#    print(thing.strip('\n'))
#source='';
#for thing in data:
##    source=source+thing;
#source='广州华南理工大学工业管理专业本科生'
#import jieba                                                            
# 
#seg_list = jieba.cut(source, cut_all=True)                  
# 
#print("Full Mode: " + " ".join(seg_list)) # 全模式                      
##Full Mode: 
# 
#seg_list = jieba.cut(source, cut_all=False)                 
#
#print("Default Mode: " + " ".join(seg_list)) # 默认模式/精确模式       
##Default Mode: 
# 
#seg_list = jieba.cut(source)   
#list1=[]
#for thing in seg_list:
#    list1.append(thing)
#del list1[0]
#print(list1) 
#                  
# 
#print("Default Mode: " + " ".join(seg_list)) # 默认精确模式            
##Default Mode: 
# 
#seg_list = jieba.cut_for_search(source) # 搜索引擎模式     
# 
#print("Search Mode: " + " ".join(seg_list)) # 搜索引擎模式              
#Search Mode: 
    
#
#from snownlp import SnowNLP                                            
# 
#s = SnowNLP(source)                                        
#print(s.words)
#print(' '.join(s.words))                                               

#import pkuseg                                                            
# 
#pku_seg = pkuseg.pkuseg()                                                   
# 
#print(' '.join(pku_seg.cut(source)))          

#import thulac                                                               
# 
#thu_lac = thulac.thulac(seg_only=True)
#                                      
##Model loaded succeed
# 
#thu_result = thu_lac.cut(source, text=True)                     
# 
#print(thu_result)        
#
#from pyhanlp import HanLP                                                   
# 
#han_word_seg = HanLP.segment(source)                            
# 
#print(' '.join([term.word for term in han_word_seg]))                                                                                   
#
#
#
#with open("ftest_result.txt","w") as f:
#    for thing in data:
#        f.write(thing)  # 自带文件关闭功能，不需要再写f.close()

a=['123','123']
del a[0]
print(a)
print('clear')
