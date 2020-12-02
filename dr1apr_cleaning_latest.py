# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:22:56 2020

@author: User
"""

import re
import string 
import json
import nltk
from nltk import hmm
import pandas as pd
import numpy as np
import malaya
from nltk.tokenize import word_tokenize, sent_tokenize


with open('D:/User/Documents/.Parlimen Malaysia/DR-01042019emil.txt', "r", encoding='utf-8') as text_file:
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

with open('D:/User/Documents/.Parlimen Malaysia/dr1apr_cleaned2_latest.txt', 'w', encoding='utf-8') as text_file:
    print(dr1apr_cleaned, file=text_file)
#print(dr1apr_cleaned2)

print(dr1apr_cleaned[4219])
with open('dr1apr_qablock_trial_latest.txt','w', encoding='utf-8') as text_file:
    for i in range(len(dr1apr_cleaned)-1):
        dr1apr_words=word_tokenize(dr1apr_cleaned[i])
        if ']' in dr1apr_words:
            if '[sesi pertanyaan-pertanyaan bagi jawab lisan tamat]' in dr1apr_cleaned[i]:
                break
            if dr1apr_words[dr1apr_words.index(']')-1]!='ketawa'and dr1apr_words[dr1apr_words.index(']')+1]=='minta' in dr1apr_words:
                print('\n')
                print(dr1apr_cleaned[i])
                text_file.write('\n')
                text_file.write(dr1apr_cleaned[i])
                text_file.write(' ')
            else:
                print(dr1apr_cleaned[i])
                text_file.write(dr1apr_cleaned[i])
                text_file.write(' ')
        else:
            print(dr1apr_cleaned[i])
            text_file.write(dr1apr_cleaned[i])
            text_file.write(' ')

with open('dr1apr_qablock_trial_latest.txt', 'r', encoding='utf-8') as text_file:
    dr1apr_qa=text_file.read()
    
malay_stopwords=json.load(open('tokenized_stopwords.json'))
stopwords=malay_stopwords
    
dr1apr_qasplit=dr1apr_qa.split('\n')
dr1apr_qascleaned=remove_noise(dr1apr_qasplit)

df=pd.DataFrame(dr1apr_qascleaned)
df.to_csv('dr1apr_qablocks_latest.csv', index=False)

outpath = 'qablock_dr1apr_latest.json'
with open(outpath, "w") as f:
    f.write(json.dumps(dr1apr_qascleaned))

    
dr1apr_qascleaned2=[]
for i in range(len(dr1apr_qascleaned)):
    wordz = ''.join([j for j in dr1apr_qascleaned[i] if j not in string.punctuation])
    dr1apr_qascleaned2.append(wordz)

    
dr1apr_qascleaned2x=[]
for i in dr1apr_qascleaned2:
    stemmed=malaya.stem.sastrawi(i)
    dr1apr_qascleaned2x.append(word_tokenize(stemmed))
    
tempdr1apr=[]
for i in range(len(dr1apr_qascleaned2x)):
    resultwords  = [word for word in dr1apr_qascleaned2x[i] if word.lower() not in stopwords]
    result = ' '.join(resultwords)
    tempdr1apr.append(result)
    
dr1apr_final=[]
for i in tempdr1apr:
    dr1apr_final.append(word_tokenize(i))
    
while("" in dr1apr_final) : 
    dr1apr_final.remove("") 

outpath = 'nestedlist_dr1apr_trial_latest.json'
with open(outpath, "w") as f:
    f.write(json.dumps(dr1apr_final))

for i in dr1apr_final:
    if len(i)==0:
        dr1apr_final.remove(i)

    
print(dr1apr_final)
print(df)
    
             