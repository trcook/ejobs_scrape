# %load ./apsa/spiders/ejobs.py
import scrapy
from scrapy.selector import Selector
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import itertools
import re
from apsa.items import ApsaItem
import yaml

with open('./settings.yaml') as f:
    settings=yaml.load(f)
    f.close()
USERNAME=settings['username']
PASSWORD=settings['password']
SUBFIELD=settings['subfield']
    
class EjobsSpider(scrapy.Spider):
    name = "ejobs"
    allowed_domains = ["apsanet.org"]
    start_urls = ['https://www.apsanet.org/Sign-In?ReturnURL=/CAREERS/eJobs/eJobs-Online']
    def __init__(self):
        self.br=webdriver.Chrome('/Users/tom/Documents/Programming/apsa/chromedriver')
#     def start_requests(self):
#         for url in self.start_urls:
#             yield scrapy.Request(url, self.parse, meta={
#                 'splash': {
#                     'endpoint': 'render.html',
#                     'args': {'wait': 0.5}
#                 }
#             })
    def parse(self, response):
        self.br.get(response.url)
        username=self.br.find_element_by_id('dnn_ctr3337_View_ctl00_tbUserName')
        username.send_keys(USERNAME)
        pwd=self.br.find_element_by_id('dnn_ctr3337_View_ctl00_tbPassword')
        pwd.send_keys(PASSWORD)
        sub=self.br.find_element_by_id('dnn_ctr3337_View_ctl00_btnSignIn')
        sub.click()
        time.sleep(1)
        el=self.br.find_element_by_id('dnn_ctr4356_ViewJobBank_Candidate_lb_JobSearch')
        el.click()
        time.sleep(1)
        subfield=Select(self.br.find_element_by_id('dnn_ctr4356_ViewJobBank_JobSearch_dl_Subfield'))
        subfield.select_by_value(SUBFIELD)
        el=self.br.find_element_by_id('dnn_ctr4356_ViewJobBank_JobSearch_btn_Submit')
        el.click()
        time.sleep(1)    
        # loop over pages
        hxs=Selector(text=self.br.page_source,type='html')
        pages=hxs.xpath('//td[contains(@class,"rgPagerCell")]//div[contains(@class,"rgNumPart")]//a/@href')
        for idx in range(1,len(pages)+1):
            page_link=self.br.find_element_by_xpath('//td[contains(@class,"rgPagerCell")]//div[contains(@class,"rgNumPart")]//a[%s]'%idx)
            page_link.click()
            time.sleep(3)
            hxs=Selector(text=self.br.page_source,type='html')
            rows=hxs.xpath('//table[@class="rgMasterTable"]/tbody/tr')
            outframe=[{"link":i.xpath("td[2]//a/@href").extract()[0],
                       "date":str(i.xpath("td[6]//text()").extract())}
                       for i in rows]
            for idx,i in enumerate(outframe):#enumerate(out[0:3]): # for testing
                request=scrapy.Request(outframe[idx]['link'],self.after_parse)
                request.meta['post_date']=outframe[idx]['date']
                logging.debug("requesting: %s"%request.url)
                yield request

    
    def after_parse(self,response):
        self.br.get(response.url)
        hxs=Selector(text=self.br.page_source,type='html')
        scrapy_item=ApsaItem()
        scrapy_item['start_date']=hxs.xpath('//span[@id="dnn_ctr4356_ViewJobBank_ViewJob_lb_DateAvailable"]/text()').extract()
        scrapy_item['desc']=hxs.xpath('//span[@id="dnn_ctr4356_ViewJobBank_ViewJob_lb_JobText"]//text()').extract()
        scrapy_item['school']=hxs.xpath('//span[@id="dnn_ctr4356_ViewJobBank_ViewJob_lb_Company"]//text()').extract()   
        scrapy_item['url']=response.url
        scrapy_item['post_date']=response.meta['post_date']
        scrapy_item['due_date']=[]
        return scrapy_item
    
#         return scrapy.FormRequest.from_response(
#             response,
#             formdata={'dnn$ctr3337$View$ctl00$tbUserName': 'trcook', 'dnn$ctr3337$View$ctl00$tbPassword': 'Vsyvgu49N'},
#             callback=self.after_login
#             #dont_click=True
#         )
        
#     def after_login(self, response):
#         # check login succeed before going on
#         if "system could not sign you in" in response.body:
#             self.logger.error("Login failed")
#             return
#         output=response.xpath('//li/a/text()').extract()
#         logging.debug("it worked")
#         logging.debug(response.body)