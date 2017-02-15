#coding:utf-8
from selenium.webdriver.common.keys import Keys  
import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pymongo
import xlrd
import time 

import scrapy
from tyc.items import TycItem
import logging
from scrapy.http import Request


class TycSpider(scrapy.Spider):
    name = 'tyc'
    allowed_domains = ['tianyancha.com']
    fname = "C:\\Users\\Administrator\\Desktop\\test.xlsx"
    workbook = xlrd.open_workbook(fname)
    sheet = workbook.sheet_by_name('Sheet1')
    urls = list()
    cols = sheet.col_values(0)
    i = 1
    #要爬取的url
    start_urls =['http://www.tianyancha.com/search?key={}&checkFrom=searchBox' .format(col) for col in cols]     

    def parse(self,response):
        #用phantomJs模拟浏览器，添加headers
        start = time.clock()
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36"
        )
        browser = webdriver.PhantomJS(desired_capabilities=dcap)
        browser.get(response.url)
        time.sleep(4)
        #获取企业url
        try:
            url = browser.find_element_by_class_name('query_name').get_attribute('href')
            browser.quit()
            self.logger.info('成功搜索到 %s',url)
            end = time.clock()
            print ("查询企业用时%f s" %(end-start))
            yield Request(url = url,callback = self.parse_detail)
            
        except Exception as e:
            self.logger.info('经查询没有这个企业！')
            browser.quit()

    def parse_detail(self,response):
        #获取企业对外投资情况
        start = time.clock()
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36"
        )
        browser = webdriver.PhantomJS(desired_capabilities=dcap)
     
        browser.get(response.url)
        self.logger.info('url %s', response.url)
        time.sleep(7)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        # driver.implicitly_wait(10)
        browser.quit()
        item = TycItem()
        
      
        try:
            name = soup.select('.base-company')[0].text.split(' ')[0]
            self.logger.info('企业名 %s',name)
            inv = soup.select('#nav-main-outInvestment .m-plele')
            print (len(inv))
            for i in inv:
                inv = i.select('div')
                companyName = inv[0].text
                legalPerson = inv[2].text
                industry = inv[3].text    
                state = inv[4].text
                invest = inv[5].text
                item['company'] = name
                item['enterprise_name'] = companyName
                item['legal_person_name'] = legalPerson
                item['industry'] = industry
                item['status'] = state
                item['reg_captial'] = invest
                end = time.clock()
                print ("获取对外投资用时:%f s" % (end-start))
                yield (item)
        except Exception as e:
            self.logger.info('这个企业没有对外投资！')