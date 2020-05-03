# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 19:10:06 2020

@author: ASUS
"""
import re
import os

if(os.path.exists('./input')):
    print('存在')
else:
    os.makedirs('./input')
    
if(os.path.exists('./output')):
    print('存在')
else:
    os.makedirs('./output')
list_=os.listdir('./input')
for index,mid_dir in enumerate(list_):
    with open('./input/'+mid_dir, "r+",encoding='utf-8') as f:  # 打开文件
#     try:
        text = f.read()  # 读取文件
        text =text.replace("-", "—").replace("－", "—").strip()
        #print(text)
        # 对文本处理一下 # 2015-8-31  2015-12-28
        #text = text.replace("年", "-").replace("月", "-").replace("日", " ").replace("/", "-").strip()
        
        # 2019年10月27日 9:46:21
        "(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})"
        # 2019年10月27日 9:46"
        "(\d{4}-\d{1,2}-\d{1,2})"
        # 2019年10月27日
        "(\d{4}-\d{1,2}-\d{1,2})"
        # 2019年10月
        "(\d{4}-\d{1,2})"
        
        def get_strtime(text):
        # text = text.replace(".", "-").strip()
        # print(text)
         text = re.sub("\s+", " ", text)
        # print(text)
         t = ""
         regex_list = [
         # 2013年8月15日 22:46:21
            "(\d{4}.\d{1,2}—\d{4}.\d{1,2})",
            "(\d{4}.\d{1,2}—今)"
        
         ]
         for regex in regex_list:
             t = re.findall(regex, text)
        # print(t)
             if t:
#                    print(text)
#                    print(t)
                    return t
         else:
             print("没有获取到有效日期")
          
         return t
        
        def replace_char(string,str_,s_index,e_index):
            string = list(string)
            for thing in range(s_index,e_index+1):    
                string[thing] = str_[thing-s_index]
            return ''.join(string)
        
        
        start_index=[]
        end_index=[]
        start_time=[]
        start_month=[]
        end_month=[]
        end_time=[]
        
        for thing in get_strtime(text):
            start_index.append(re.search(thing,text).span()[0])
            end_index.append(re.search(thing,text).span()[1])
            start_time.append(text[re.search(thing,text).span()[0]:re.search(thing,text).span()[0]+4])
            start_month.append(text[re.search(thing,text).span()[0]+5:re.search(thing,text).span()[0]+7])
            end_month.append(text[re.search(thing,text).span()[0]+13:re.search(thing,text).span()[0]+15])
            end_time.append(text[re.search(thing,text).span()[0]+8:re.search(thing,text).span()[0]+12])
            text
        #print(start_time)
        #print(start_month)
        #print(end_month)
        total_text=''
        total_text=total_text+text[0:start_index[0]]
        for index,thing in enumerate(start_index):
            if index<len(start_index)-1:
                content=text[start_index[index]:start_index[index+1]]
                if (int(end_time[index])-int(start_time[index]))>1:
                    for time in range(int(start_time[index]),int(end_time[index])-1):
                        temp_content=content
                        content=replace_char(content,str(time),0,3)
                        content=replace_char(content,str(time+1),8,11)
                        content=replace_char(content,start_month[index],13,14)
                        total_text=total_text+content
                        content=temp_content
                    content=replace_char(content,str(int(end_time[index])-1),0,3)
                    total_text=total_text+content
                    
                else:
                    total_text=total_text+content
            else:
#                print(content)
                content=text[start_index[index]:]
                first_p=content.split('\n')[0]
                second_p=content.split('\n')[1]
                content=first_p+'\n'+'时间：'
                if (int(end_time[index])-int(start_time[index]))>1:
                    for time in range(int(start_time[index]),int(end_time[index])-1):
                        if(time!=int(start_time[index])):
                            temp_content=content
                            content=replace_char(content,str(time),0,3)
                            content=replace_char(content,str(time+1),8,11)
                            content=replace_char(content,start_month[index],13,14)
                            total_text=total_text+content
                            content=temp_content
                        else:
                            temp_content=content
                            content=replace_char(content,str(time),0,3)
                            content=replace_char(content,str(time+1),8,11)
                            content=replace_char(content,start_month[index],13,14)
                            total_text=total_text+content
                            content=temp_content
                    content=replace_char(content,str(int(end_time[index])-1),0,3)
                    total_text=total_text+content.replace('时间：','')
                    
                else:
                    total_text=total_text+content.replace('时间：','')
                total_text=total_text+second_p
#                print(1)
#                print(content)
#                if (int(end_time[index])-int(start_time[index]))>1:
#                    for time in range(int(start_time[index]),int(end_time[index])-1):
#                        temp_content=content
#                        content=replace_char(content,str(time),0,3)
#                        content=replace_char(content,str(time+1),8,11)
#                        content=replace_char(content,start_month[index],13,14)
#                        if total_text[-3:]!='时间：':
#                            total_text=total_text+'\n时间：'+content
#                        else:
#                            total_text=total_text+content
#                        content=temp_content
#                        content=replace_char(content,str(int(end_time[index])-1),0,3)
#                    if total_text[-3:]!='时间：':
#                        total_text=total_text+'\n时间：'+content
#                    else:
#                        total_text=total_text+content
#                    
#                    
#                else:
#                    if total_text[-3:]!='时间：':
#                        if total_text[-3:]!='时间：':
#                            total_text=total_text+'\n时间：'+content
#                        else:
#                            total_text=total_text+content
#                    else:
#                        if total_text[-3:]!='时间：':
#                            total_text=total_text+'\n时间：'+content
#                        else:
#                total_text=total_text+content
        print(total_text)
        with open('./output/'+mid_dir, "w+",encoding='utf-8') as f:  # 打开文件
            f.write(total_text)     
#     except BaseException:
#        print("第"+mid_dir+"个文件error")
#        continue   

