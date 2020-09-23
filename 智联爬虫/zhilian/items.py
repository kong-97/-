# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CitysItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    code = scrapy.Field()
    pinyin = scrapy.Field()


class CompanyItem(scrapy.Item):
    company_url = scrapy.Field()


class PositionItem(scrapy.Item):
    _id = scrapy.Field()
    newtime = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    worktime = scrapy.Field()
    education = scrapy.Field()
    count = scrapy.Field()
    company_name = scrapy.Field()
    company_industry = scrapy.Field()
    company_size = scrapy.Field()
    describ = scrapy.Field()