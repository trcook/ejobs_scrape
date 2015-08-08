# %load ./apsa/pipelines.py

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import re
import logging
from apsa.items import ApsaItem
class ApsaPipeline(object):
    def process_item(self, item, spider):        
        x=re.findall('((?:send|submit|receive).+?(?:by|before).*?((?:sep|oct|nov|dec|jan).+?\s\d{0,3}))',item['desc'][0],flags=re.IGNORECASE)
        if len(x)==0:
            x=re.findall('((?:review|deadline|screening).+?((?:sep|oct|nov|dec|jan).{0,10}?\s\d{0,3}))',item['desc'][0],re.IGNORECASE)
        if len(x)==0:
            x=re.findall('((?:accepted).+?((?:sep|oct|nov|dec|jan).{0,10}?\s\d{1,2}))',item['desc'][0],flags=re.IGNORECASE)
        if len(x)==0:
            x=re.findall('((?:screening|review|deadline).+?(\d{1,2}.{0,4}(?:sep|oct|nov|dec|jan).+\s))',item['desc'][0],flags=re.IGNORECASE)
        if len(x)!=0:
            item['due_date']=x[0][1]
        else:
            item['due_date']=x
        return item