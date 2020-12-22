#!/usr/bin/env python
# coding: utf-8

# ## IMPORTING LIBRARIES

# In[ ]:


# Importing Modules

import nltk                            # Importing nltk to download list of stopwords
import os                              # Importing os to get paths from system
from nltk.corpus import stopwords      # Importing stopWords
import numpy as np                     # numpy module for mathematical calculations
from collections import OrderedDict    # library to sort dictionary
from nltk.stem import PorterStemmer    # PorterStemmer to perform Stemming
import pickle


# ## DECLARING GLOBAL VARIABLES

# In[ ]:


#Declaring Global variables

stopwords = set(stopwords.words('english'))                            #stopwords

punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~''' + '"'               #punctuations

path = os.getcwd()                                                     #getting current working directory

path = path + '\\data'                                           #getting the path of dataset

dir_list = os.listdir(path)   # getting all files in a folder in sepcified path

ps = PorterStemmer()

invertedIndex = {}      # Dictionary for Inverted Index


# ## Valid Characters

# In[ ]:


valid_char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
             'u','v', 'w', 'x', 'y','z','0','1','2','3','4','5','6','7','8','9']


# ## PRE-PROCESSING

# In[ ]:


def preprocess(file):
    tokens = file.split('\n')
    tokens = tokens[0]
    final_desc = ''
    for x in tokens.lower():
        if x not in valid_char:
            final_desc+= ' '
        else:
            final_desc+=x
    final_tokens = []
    for w in final_desc.split(' '):
        w = ps.stem(w)
        if w not in stopwords and w!=' ' and w!='' and w not in valid_char:
            final_tokens.append(w)
    return final_tokens


# # TASK 1

# ## CREATING INVERTED INDEX
#     Logarithmic term frequency in for each term in each document is calculated

# In[ ]:


#Creating Inverted_Index

# Traversing Each File to create Inverted Index
i = 0
tf_docs = {}
tf_idf_scr = {}
for file in dir_list:
    print(i)
    f = path + '\\' + file
    docID = file[:-4]
    tf_docs[docID] = {}
    tf_idf_scr[docID] = {}
    file = open(f,encoding = 'utf-8').read()
    tokens = preprocess(file)  # Calling Preprocessing function to get tokens
    for token in tokens:                                 # Creating Posting_List for each index
        if token not in invertedIndex.keys():
            invertedIndex[token] = {}
            invertedIndex[token][docID] = 1
        elif docID not in invertedIndex[token].keys():
            invertedIndex[token][docID] = 1 
        elif docID in invertedIndex[token].keys():
            invertedIndex[token][docID] = invertedIndex[token][docID] + 1
        tf_docs[docID][token] = invertedIndex[token][docID]
        if tf_docs[docID][token]:
            tf_idf_scr[docID][token] = 1 + np.log2(tf_docs[docID][token])
    i = i+1


# ## WRITING INVERTED INDEX IN TEXT FILE

# In[ ]:


with open('newIndex.txt', 'w', encoding = 'utf-8') as f: 
    for key, value in invertedIndex.items():
        posting_list = "{"
        for pkey,pvalue in value.items():
            if pkey!=list(value.keys())[-1]:
                posting_list = str(posting_list) + str(pkey) + "=" + str(pvalue) + ","
            else:
                posting_list = str(posting_list) + str(pkey) + "=" + str(pvalue)
        posting_list = posting_list + "}"
        f.write('{}({})==>{}\n\n\n\n\n\n\n'.format(key, len(value),posting_list))


# In[ ]:


pickle_out = open("invertedIndex.pickle","wb")
pickle.dump(invertedIndex,pickle_out)
pickle_out.close()


# In[ ]:


with open('invertedIndex.pickle','rb') as f:
    invertedIndex = pickle.load(f)


# In[ ]:


len(invertedIndex)


# In[ ]:


len(collection)


# ## CALCULATING DOCUMENT FREQUENCY

# In[ ]:


df = {}
for word in invertedIndex.keys():
    df[word] = len(invertedIndex[word])


# ## CALCULATING INVERSE DOCUMENT FREQUENCY

# In[ ]:


idf = {}
M = len(invertedIndex)
for word in invertedIndex.keys():
    idf[word] = np.log2((M+1) / df[word])


# ## CALCULATING TF-IDF SCORES FOR ALL TERMS IN VOCABULARY

# In[ ]:


for key,value in tf_idf_scr.items():
    for tkey,tvaue in value.items():
        tf_idf_scr[key][tkey]*=idf[tkey]


# ## IMPLEMENTING VECTOR SPACE MODEL

# In[ ]:


def vectorSpaceModel(query,tfidf_scr):
    query_vocab = preprocess(query)
    query_wc = {}
    query_list = query.split(' ')
    for i in range(len(query_list)):
        query_list[i] = ps.stem(query_list[i])
    for word in query_vocab:
        query_wc[word] = query_list.count(word)
    relevance_scores = {}
    for doc_id in tfidf_scr.keys():
        score = 0
        # finding dot product between query and document
        for word in query_vocab:
            if word in invertedIndex.keys() and word in tfidf_scr[doc_id].keys():
                score += query_wc[word] * tfidf_scr[doc_id][word]
            else:
                score = 0
        relevance_scores[doc_id] = score
    sorted_value = OrderedDict(sorted(relevance_scores.items(), key=lambda x: x[1], reverse = True))
    top_10 = {k: sorted_value[k] for k in list(sorted_value)[:10]}
    return top_10


# ### Example Queries

# In[ ]:


query1 = 'Dell Inspiron laptop'
query2 = 'Playstation'
query3 = 'Nintendo switches'
query4 = 'shirts and pant'
query5 = 'real me pro'


# In[ ]:


top1 = vectorSpaceModel(query1,tf_idf_scr)    #returns top 5 documents using VSM
top2 = vectorSpaceModel(query2,tf_idf_scr)    #returns top 5 documents using VSM
top3 = vectorSpaceModel(query3,tf_idf_scr)    #returns top 5 documents using VSM
top4 = vectorSpaceModel(query4,tf_idf_scr)    #returns top 5 documents using VSM
top5 = vectorSpaceModel(query5,tf_idf_scr)    #returns top 5 documents using VSM


# In[ ]:


relevant_docs = []
for key in top2.keys():
    relevant_docs.append(key)


# In[ ]:


for file in relevant_docs:
    print('Document Number = ' + file)
    f = path + '\\' + file + '.txt'
    content = open(f,encoding = 'utf-8').read()
    print(content)


# # TASK 2

# ## Finding Best Seller

# In[ ]:


m_factors = {
    '4.5-5.0' : 1,
    '4.0-4.5' : 0.9,
    '3.5-4.0' : 0.8,
    '3.0-3.5' : 0.7,
    '2.5-3.0' : 0.6,
    '2.0-2.5' : 0.5,
    '1.5-2.0' : 0.4,
    '1.0-1.5' : 0.3,
    '0.5-1.0' : 0.2,
    '0.0-0.5' : 0.1,
    '-1' : -1
}


# In[ ]:


def findBestSellProduct(rel_docs):
    best_sell = []
    factors = {}
    for doc in rel_docs:
        factors[doc] = []
        fp = open(path + '\\' + doc + str('.txt'),encoding = 'utf-8')
        for i, line in enumerate(fp):
            if i == 2:
                if line[:3]!='':
                    factors[doc].append(line[:3])
                else:
                    factors[doc].append(-1)
            elif i == 3:
                if line!='':
                    factors[doc].append(line)
                else:
                    factors[doc].append(-1)
            elif i > 3:
                break
        fp.close()
        for key,value in factors.items():
            if value[0]!='\n':
                value[0] = float(value[0])
            else:
                value[0] = -1
            if value[1]!='\n':
                value[1] = int(value[1][:-1])
            else:
                value[1] = -1
        basis_factors = {}
        for key,value in factors.items():
            if value[0]<0 or value[1] < 0:
                basis_factors[key] = -1
            else:
                if np.ceil(value[0])-value[0]>0.5:
                    m_factor = str(np.floor(value[0])) + '-' + str(np.floor(value[0])+0.5)
                else:
                    m_factor = str(np.ceil(value[0])-0.5) + '-' + str(np.ceil(value[0]))
                rating_range = m_factor
                basis_factors[key] = np.multiply(value[0],value[1])*m_factors[rating_range]
        values = list(basis_factors.values())
        value = np.max(values)
        for key,val in basis_factors.items():
            if val == value:
                best_sell.append(key)
                break
        return best_sell[0]
        


# ## Input Cell

# In[ ]:


print('Few Examples Queries\n')
print('1)laptop')
print('2)Playstation')
print('3)Nintendo switches')
print('4)shirts and pant')
print('5)real me pro')
query = input('ENTER THE QUERY')
rdocs = vectorSpaceModel(query,tf_idf_scr,)
bestSellProduct = findBestSellProduct(rdocs)


# ## Printing Best Product

# In[ ]:


print(bestSellProduct)


# In[ ]:


file = bestSellProduct
print('Document Number = ' + file)
f = path + '\\' + file + '.txt'
content = open(f,encoding = 'utf-8').read()
print(content)

