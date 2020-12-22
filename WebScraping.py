#!/usr/bin/env python
# coding: utf-8

# # Scraping Data from Amazon

# In[ ]:


import csv,json
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge,EdgeOptions
from selenium import webdriver

def get_url(search_term,page):
    template = "https://www.amazon.in/s?k={}&ref=nb_sb_noss"
    search_term = search_term.replace(' ','+')
    #add item query
    url = template.format(search_term)
    #add page query placeholder
    url+='&page={}'.format(page)
    return url

def extract_record(item):
    """Extract and return data from a single record """
    #description and url
    try:
        atag = item.h2.a
        description = atag.text.strip()
        url = 'https://www.amazon.in/' + atag.get('href')
    except AttributeError:
        description = ''
        return
    #price
    try:
        price_parent = item.find('span','a-price')
        price = price_parent.find('span','a-offscreen').text
    except AttributeError:
        return
    #rating
    try:
        rating = item.i.text
        review_count = item.find('span',{'class' : 'a-size-base','dir':'auto'}).text
    except AttributeError:
        rating = ''
        review_count = ''
    
    result = (description,price,rating,review_count,url)
    return result

def main(searchTerms):
    """Run main program routine"""
    
    #startup the webdriver
    driver = webdriver.Chrome()
    
    records = []
    i = 0
    for term in searchTerms:        
        print(i)
#         url = get_url(term[0],1)
#         driver.get(url)
        for page in range(1,21):
            page_url = get_url(term[0],page)
            print(page_url)
            driver.get(page_url)
            soup = BeautifulSoup(driver.page_source,'html.parser')
            results = soup.find_all('div',{'data-component-type' : 's-search-result'})
            for item in results:
                record = extract_record(item)
                records.append(record)
        i = i + 1
    driver.close()
    return records


# ## Load Keywords from 'finalKeywords.csv'

# In[ ]:


import pandas as pd
keywords = pd.read_csv('finalKeywords.csv',header = None)
keywords = keywords.iloc[:].values


# In[ ]:


data = main(keywords)


# ## Writing Crawled Data into Text Files

# In[ ]:


for i in range(len(data)):
    outF = open(str(i+1) + ".txt", "w",encoding = 'utf-8')
    if data[i]:
        for line in data[i]:
      # write line to output file
            outF.write(line)
            outF.write("\n")
outF.close()

