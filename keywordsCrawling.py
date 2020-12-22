#!/usr/bin/env python
# coding: utf-8

# ## Crawling Search Keywords 

# ## Extracting keywords using SELENIUM Web Browser and Parsing HTML tags with Beutiful Soup

# In[1]:


import csv,json
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge,EdgeOptions
from selenium import webdriver

def get_url(search_term):
    template = "https://www.amazon.in/s?k={}&ref=nb_sb_noss"
    search_term = search_term.replace(' ','+')
    #add item query
    url = template.format(search_term)
    #add page query placeholder
    url+='&page{}'
    return template.format(search_term)

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

def main():
    """Run main program routine"""
    
    #startup the webdriver
    driver = webdriver.Chrome()
    
    records = []
#     url = get_url(search_term)
    url = 'https://ahrefs.com/blog/top-amazon-searches/'
    driver.get(url)
    
    for page in range(1,21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source,'html.parser')
        results = soup.find_all('td',{'class' : 'column-2'})
    
    driver.close()
    
    #save data to csv file
    with open('keyword.csv','w',newline = '',encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['keywords'])
        writer.writerows(results)


# In[2]:


main()


# ## Getting all the keywords

# In[10]:


import pandas as pd
keywords = pd.read_csv('keyword.csv',header = None)
keywords = keywords.iloc[:].values


# ## Removing Duplicate Keywords

# In[5]:


finalKeywords = [] 
for i in keywords: 
    if i not in finalKeywords: 
        finalKeywords.append(i) 


# ## Storing All Final Keywords in CSV File

# In[7]:


with open('finalKeywords.csv','w',newline = '',encoding = 'utf-8') as f:
      writer = csv.writer(f)
      for i in finalKeywords:
          writer.writerow(i)

