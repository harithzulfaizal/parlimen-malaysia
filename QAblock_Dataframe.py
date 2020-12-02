# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 10:14:02 2020

@author: Harith Zulfaizal
"""
import re
import string 
import nltk
import pandas as pd
import re
import numpy as np
import malaya
from nltk.tokenize import sent_tokenize, word_tokenize
from mp_name import dict, speaker 


with open('D:/User/Documents/.Parlimen Malaysia/Hansard/P2 M2/txt/DR-01072019.txt', "r", encoding='utf-8') as text_file:
        dr1apr = text_file.read().replace('\n', ' ')
        
dr1apr=dr1apr.replace('’',"'")
dr1apr_tokenize=sent_tokenize(dr1apr)
#print(dr1apr_tokenize)

def remove_noise(data):
    dr1apr_cleaned = []
    
    for i in range(len(data)):
        cleaned = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', data[i])
        dr1apr_cleaned.append(cleaned.lower())
    
    return dr1apr_cleaned

dr1apr_cleaned=remove_noise(dr1apr_tokenize)

"""dr1apr_cleaned2=[]
for i in range(len(dr1apr_cleaned)):
    wordz = ''.join([j for j in dr1apr_cleaned[i] if j not in string.punctuation])
    dr1apr_cleaned2.append(wordz)"""

while("" in dr1apr_cleaned) : 
    dr1apr_cleaned.remove("") 


spldr=''

for i in range(len(dr1apr_cleaned)-1):
    dr1apr_words=word_tokenize(dr1apr_cleaned[i])
    if ']' in dr1apr_words: #[sesi pertanyaan-pertanyaan bagi jawab lisan tamat]
        if 'jawab lisan' and 'tamat]' in dr1apr_cleaned[i]:
            break
        if dr1apr_words[dr1apr_words.index(']')-1]!='ketawa'and dr1apr_words[dr1apr_words.index(']')+1]=='minta' in dr1apr_words:
            #print('\n')
            #print(dr1apr_cleaned[i])
            spldr=spldr+'\n'+dr1apr_cleaned[i]+' '
        else:
            #print(dr1apr_cleaned[i])
            spldr=spldr+dr1apr_cleaned[i]+' '
    else:
        #print(dr1apr_cleaned[i])
        spldr=spldr+dr1apr_cleaned[i]+' '

# =============================================================================
# for i in dr1apr_cleaned:
#     #dr1apr_words=word_tokenize(dr1apr_cleaned[i])
#     if '[sesi pertanyaan-pertanyaan bagi jawab lisan tamat]' in i:
#         break
#     if 'ketawa]' and '] minta' in i:
#             #print('\n')
#             #print(dr1apr_cleaned[i])
#             spldr=spldr+'\n'+i+' '
#     else:
#             #print(dr1apr_cleaned[i])
#             spldr=spldr+i+' '
# 
# =============================================================================
        
# dr1apr_qasplit=spldr.split('\n')
dr1apr_qascleaned=re.split(r'\n', spldr)

for i in dr1apr_qascleaned:
    if 'jawapan-jawapan lisan pertanyaan-pertanyaan' in i:
        dr1apr_qascleaned.remove(i)

df=pd.DataFrame(dict.items(), columns=['mps', 'parliaments/jawatan'])
spkr=pd.DataFrame(speaker.items(), columns=['name', 'parl'])
df['qa']=None
df2=pd.DataFrame()

for i, sent in enumerate(dr1apr_qascleaned):
    dr1apr_qascleaned[i]=sent.replace(' 2018.',' 2018 (tahun).').replace('..','. ').replace('  ',' ').replace('ok.','okay.').replace(' g.',' g').replace('menyemak..','menyemak.').replace('dr.', 'dr').replace('mohd.','mohd').replace('md.','md').replace(' m.',' m')
    
qaqaglob=[]
sg=[]
ex=[]

def gothroughblocks(whatblock):
    
    exmple=sent_tokenize(dr1apr_qascleaned[whatblock])
    #print(exmple)
    ex.append(exmple)
    s=''
    temp_name=''
    for i in exmple:
        x=0  
        for name in df.mps:
            if name in i:
                if name==temp_name: 
                    temp_i=i.replace(name, '')
                    s=s+temp_i+' '+'thru tempname'
                    print(temp_i)
                    print('go thru temp name')
                elif 'tidak hadir]' in i:
                    s=s+'\n'+i+' '+'thru tidak'
                    print('\n'+i)
                    print('go thru tidak hadir')
                    temp_name=name
                else:
                    s=s+'\n'+i+' '+'thru else'
                    print('\n'+i)
                    print('go thru else')
                    temp_name=name
                x=1                
        if x==0:
            s=s+i+' '+'thru x0'
            print(i)
            print('go thru x0')
        
        
    sg.append(s)
    
    qaqa=s.split('\n')
    for i in qaqa:
        if len(i)==0:
            qaqa.remove(i)
        if 'tidak hadir]' in i:
            qaqa.remove(i)
    
    # qaqa[0]=qaqa[0].replace(':',' ')
    
    names=[]
    qa=[]

    qaqaglob.append(qaqa)

    for i in qaqa:
        # for nama in spkr.name:
        #     if nama in i:
        #         qaqa.remove(i)
        for name in df.mps:
            if name in i:
                if '] minta' in i:
                    x=i.index('] minta')
                    #print(i[:x], ' ', i[x+1:])
                    names.append(i[:x])
                    qa.append(i[x+1:])
                    
                if ':' in i:
                    y=i.index(':')
                    #print(i[:x], ' ', i[x+1:])
                    names.append(i[:y])
                    qa.append(i[y+1:])
                    
                    
    #delete last entry if odd columns
    # if len(qa)%2 != 0:
    #     qa.remove(qa[len(qa)-1])
    #     names.remove(names[len(names)-1])
    
    for i, item in enumerate(names):
        for name in df.mps:
            if name in item:
                names[i]=name
    
    #print(names)
    name_ques = [v for i, v in enumerate(names) if i % 2 == 0]
    name_ans = [v for i, v in enumerate(names) if i % 2 != 0]
    
    #print(name_ans)
    
    #print(qa)
    question=[]
    answer=[]
    for i, item in enumerate(qa):
        if i%2==0:
            question.append(item)
        else:
            answer.append(item)
    
    print(len(name_ans), len(question), len(answer))
    
    if len(question)==len(answer):
        test=1
    elif len(question)>len(answer):
        answer.append('NaN')
        name_ans.append('NaN')
    else:
        question.append('NaN')
        name_ques.append('NaN')
        
    print(len(name_ans), len(question), len(answer))
    #print(question)
    #print(answer)
    
    global df1
    df1=pd.DataFrame({'name':name_ques,'question':question, 'answers':answer, 'answered_by':name_ans})
    #df1.set_index('name', inplace=True)
    #print(df)
    #print(df1)
    global df2
    #df2=pd.concat(df1, axis=1)
    df2=df2.append(df1, ignore_index=True)
    #print(df2)
    

gothroughblocks(1)
#for i in range(len(dr1apr_qascleaned)):
    # gothroughblocks((i))
   
    
#print(df2)
# df2.to_csv('qa hansard 03042019.csv')