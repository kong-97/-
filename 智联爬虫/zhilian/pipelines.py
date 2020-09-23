# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from csv import DictWriter

from zhilian.items import *


class ZhilianPipeline(object):

    def __init__(self):
        self.citys = 'citys.csv'
        self.companies = 'companies.csv'
        self.positions = 'positions.csv'

    def save_csv(self, item, filename):
        has_header = os.path.exists(filename)
        with open(filename, 'a') as f:
            writer = DictWriter(f, fieldnames=item.keys())
            if not has_header:
                writer.writeheader()
            writer.writerow(item)

    def save_mongo(self, item, spider):
        spider.db.python.insert(item)

    def process_item(self, item, spider):
        if not item: return
        if isinstance(item, CitysItem):
            self.save_csv(item, self.citys)
        elif isinstance(item, CompanyItem):
            self.save_csv(item, self.companies)
        elif isinstance(item, PositionItem):
            self.save_mongo(item, spider)
        return item
