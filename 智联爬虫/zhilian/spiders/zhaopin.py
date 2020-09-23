# -*- coding: utf-8 -*-
import json
import re

from scrapy import Request
from zhilian.items import *


class ZhaopinSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    # start_urls = ['https://www.zhaopin.com/']

    def start_requests(self):
        """
        访问智联首页，登录后跳转到我的智联页面，点击'切换城市'按钮，跳转到选择城市页面
        :return:城市页面的HtmlResponse
        """
        url = 'https://www.zhaopin.com/'
        response = Request(url, callback=self.parse_index, meta={'index': True})
        yield response

    def parse_index(self, response):
        """
        解析 start_requests(self)返回的响应，
        将城市信息保存到数据库，（yield item）
        获取到城市信息开始请求每个城市的页面 （yield Request）
        :param response: 所有城市页面的HtmlResponse
        :return:
        """
        if response.status == 200:
            html = response.text
            s = re.search(r'<script>__INITIAL_STATE__=(.*?)</script>', html)
            json_data = s.groups()[0]
            data = json.loads(json_data)
            cityMapList = data['cityList']['cityMapList']  # dict
            count = 0
            for letter, citys in cityMapList.items():
                for city in citys:
                    count += 1
                    item = CitysItem()
                    item['name'] = city['name']
                    item['url'] = city['url']
                    item['code'] = city['code']
                    item['pinyin'] = city['pinyin']
                    yield item
                    # l_city = []
                    l_city = ['临洮', '西宁', '拉萨']
                    # l_city = ['临洮', '广河', '郑州', '重庆', '海口', '深圳', '兰州', '拉萨', '西宁', '呼和浩特', '银川',
                    #           '太原', '石家庄', '济南', '长春', '乌鲁木齐', '西安', '广州', '天津', '北京', '上海',
                    #           '成都', '杭州', '哈尔滨', '沈阳', '合肥', '南京', '福州', '南昌', '南宁', '贵阳',
                    #           '长沙', '武汉', '昆明', '香港', '澳门']
                    if item['name'] in l_city:
                        url = f'https://sou.zhaopin.com/?jl={item["code"]}&kw=python&kt=3'
                        print(f'---{item["name"]}---')
                        yield Request(url=url, callback=self.parse_city, meta={'city': True, 'code': item['code']})

    def parse_city(self, response):
        if response.status == 200:
            divs = response.xpath('//div[@class="contentpile__content"]/'
                                  'div[contains(@class,"contentpile__content__wrapper")]')
            for div in divs:
                item = CompanyItem()
                item['company_url'] = div.xpath('.//a[@class="contentpile__content__wrapper__item__info"]'
                                                '/@href').get()
                yield item
                yield Request(url=item['company_url'], callback=self.parse_company, meta={'position': True})

    def parse_company(self, response):
        if response.status == 200:
            item = PositionItem()
            item['newtime'] = response.xpath('//div[@class="summary-plane"]//'
                                     'div[@class="summary-plane__top"]/span/text()').get()
            item['name'] = response.xpath('//div[@class="summary-plane"]//h3/text()').get()
            item['salary'] = response.xpath('//div[@class="summary-plane"]//span[@class="summary-plane__salary"]/'
                                            'text()').get()
            item['city'] = response.xpath('//div[@class="summary-plane"]//ul[@class="summary-plane__info"]/'
                                  'li[1]/a/text()').get()
            item['worktime'] = response.xpath('//div[@class="summary-plane"]//ul[@class="summary-plane__info"]/'
                                      'li[2]/text()').get()
            item['education'] = response.xpath('//div[@class="summary-plane"]//ul[@class="summary-plane__info"]/'
                                               'li[3]/text()').get()
            item['count'] = response.xpath('//div[@class="summary-plane"]//ul[@class="summary-plane__info"]/li[4]/'
                                           'text()').get()
            item['company_name'] = response.xpath('//div[@class="company"]//a[@class="company__title"]/text()').get()
            item['company_industry'] = response.xpath('//div[@class="company"]/div[@class="company__detail"]/'
                                                      'button[1]/text()').get()
            item['company_size'] = response.xpath('//div[@class="company"]/div[@class="company__detail"]/'
                                                  'button[2]/text()').get()
            item['describ'] = response.xpath('//div[@class="describtion__detail-content"]//text()').extract()
            yield item
