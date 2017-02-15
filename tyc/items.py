# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TycItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company = scrapy.Field()
    enterprise_name = scrapy.Field()
    legal_person_name = scrapy.Field()
    industry = scrapy.Field()
    status = scrapy.Field()
    reg_captial = scrapy.Field()
