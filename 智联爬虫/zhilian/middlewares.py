# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import random
import time

from PIL import Image
from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse
from selenium.webdriver import Chrome, ActionChains, Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import ui, expected_conditions as EC

from zhilian import mongo_
from zhilian.Slider_verification import SliderVerification
from selenium.webdriver.support.wait import WebDriverWait


class ZhilianSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        spider.db = mongo_.db
        if 'python' not in spider.db.list_collection_names():
            spider.db.create_collection('python')

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s' % spider.name)
        mongo_._client.close()
        spider.logger.info('mongo_server closed: %s')

class ZhilianDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signals.spider_closed)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DownloaderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        # options.add_argument('--disable-infobars')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # path = r'E:\chromedriver.exe'
        self.driver = Firefox(firefox_binary='D:\\fire fox\\firefox.exe', executable_path='D:\geckodriver.exe')
        self.driver.maximize_window()

    def process_request(self, request, spider):
        if request.url == 'https://www.zhaopin.com/':
            self.driver.get(request.url)
            time.sleep(3)
            self.driver.find_element_by_css_selector('.risk-warning__content button').click()
            time.sleep(1)
            # 模拟登陆
            self.driver.execute_script('var q=document.documentElement.scrollLeft=500')
            username: WebElement = self.driver.find_element_by_css_selector('.zp-passport-widget-by-'
                                                                            'username__username-box input')
            username.send_keys('18193287155')
            time.sleep(2)
            self.driver.find_element_by_css_selector('.zp-passport-widget-by-'
                                                     'username__password-box input').send_keys('wwq123')
            time.sleep(0.5)
            self.driver.find_element_by_css_selector('.zp-passport-widget-by-username__submit').click()
            """
               1、登录之后判断是否有滑块验证，
               有则验证，
               没有则判断是否有更新公告，
               有则点击同意，
               2、输入关键词搜索，
               没有信息则返回None，有则获取公司链接，有下一页则接着获取下一页
            """
            time.sleep(3)
            if self.is_element_exist('.geetest_holder'):
                """滑块验证"""
                slider = SliderVerification()
                button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
                slider.click(button, self.driver)
                JS2 = 'return document.getElementsByClassName("geetest_canvas_fullbg geetest_' \
                      'fade geetest_absolute")[0].toDataURL("image/png");'
                im_info2 = self.driver.execute_script(JS2)  # 执行js文件得到带图片信息的图片数据
                im_base64_ = im_info2.split(',')[1]  # 拿到base64编码的图片信息
                image1 = base64.b64decode(im_base64_)  # 转为bytes类型
                with open('bg.png', 'wb') as f:  # 保存图片到本地
                    f.write(image1)
                slider.click(button, self.driver)
                JS = 'return document.getElementsByClassName("geetest_canvas_bg geetest_' \
                     'absolute")[0].toDataURL("image/png");'
                # 执行 JS 代码并拿到图片 base64 数据
                im_info = self.driver.execute_script(JS)  # 执行js文件得到带图片信息的图片数据
                im_base64 = im_info.split(',')[1]  # 拿到base64编码的图片信息
                image2 = base64.b64decode(im_base64)  # 转为bytes类型
                with open('slice.png', 'wb') as f:  # 保存图片到本地
                    f.write(image2)
                img1 = Image.open('bg.png')
                img2 = Image.open('slice.png')
                distance = slider.get_distance(img1, img2)
                tracks = slider.get_tracks(distance)
                tra = 0
                test = self.driver.find_element_by_css_selector('.geetest_slider')
                for track in tracks:
                    tra += track
                    ActionChains(self.driver).click_and_hold(button).move_to_element_with_offset(to_element=test,
                                                                                                 xoffset=tra+27,
                                                                                                 yoffset=0).perform()
                time.sleep(0.5)
                ActionChains(self.driver).click_and_hold(button).move_to_element_with_offset(to_element=test,
                                                                                             xoffset=tra + 25,
                                                                                             yoffset=0).perform()
                ActionChains(self.driver).release().perform()
                time.sleep(5)
                err = self.driver.find_elements_by_css_selector(css_selector='.geetest_panel_error_content')
                if len(err) == 2:
                    self.driver.find_element_by_xpath('//div[@class="geetest_panel_error_content"][1]').click()
            if self.is_element_exist('.privacy-protocol-update'):
                """判断是否有更新公告，有则点击同意按钮关闭公告"""
                time.sleep(1)
                self.driver.find_element_by_css_selector('.privacy-protocol-update .a--filled').click()
            time.sleep(3)
            self.driver.find_element_by_css_selector('.zp-top-menu__header .fl a').click()
            time.sleep(3)
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.execute_script('var q=document.documentElement.scrollTop=2000')
            time.sleep(5)
            html = self.driver.page_source
            return HtmlResponse(request.url, body=html.encode('utf-8'))
        elif request.meta.get('city', False):
            self.driver.get(request.url)
            """等待职位内容盒子出现"""
            ui.WebDriverWait(self.driver, timeout=60).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, 'contentpile__content'))
            )
            # 判断职位内容盒子是否存在，若存在则获取职位内容若不存在则返回None
            if self.is_element_exist('.contentpile__content'):
                time.sleep(0.5)
                companies = ''
                page = 1
                # 开始获取职位内容
                while True:
                    time.sleep(5)
                    # 定位职位内容的最后一个元素
                    target = self.driver.find_element_by_xpath(
                        '//div[@class="contentpile__content"]/'
                        'div[contains(@class,"contentpile__content__wrapper")][last()]')
                    # 拖动滚轮到职位内容的最后一个元素的位置，让下一页的按钮出现在可见区域
                    self.driver.execute_script('arguments[0].scrollIntoView();', target)
                    # 获取一个页面的数据赋值给 html
                    html = self.driver.page_source
                    # 每页的数据相加赋值给 companies
                    companies += html
                    # 获取该页面最大页码数（登录后最大页码为pagemax，未登录最大页码为3）
                    try:
                        pagemax = self.driver.find_element_by_xpath('//span[@class="soupager__index"][last()]').text
                    except:
                        pagemax = self.driver.find_element_by_xpath('//span[contains(@class,'
                                                                    '"soupager__index--active")]').text
                        print('该城市只有一页数据')
                    if pagemax == '...':
                        pagemax = self.driver.find_element_by_xpath('//span[@class="soupager__index"][last()-1]').text
                    if page < int(pagemax):
                        page += 1
                        code = request.meta.get('code')
                        self.driver.get(f'https://sou.zhaopin.com/?p={page}&jl={code}&kw=python&kt=3')
                        print(f'---第{page}页---')
                        ui.WebDriverWait(self.driver, timeout=60).until(
                            EC.visibility_of_all_elements_located(
                                (By.CLASS_NAME, 'contentpile__content'))
                        )
                    else:
                        break
                return HtmlResponse(request.url, body=companies.encode('utf-8'))
            # 此处应该判断一下页面中有没有出现‘未找到相关职位’的提示，若没有则是请求被拒绝，爬虫被识别出来，记录到日志中
            else:
                print('该城市没有Python相关职位')
                raise IgnoreRequest
        elif request.meta.get('position', False):
            self.driver.get(request.url)
            s = random.randint(1, 6)
            time.sleep(s)
            self.driver.execute_script('var q=document.documentElement.scrollTop=500')
            time.sleep(2)
            html = self.driver.page_source
            return HtmlResponse(request.url, body=html.encode('utf-8'))

    def is_element_exist(self, css):
        """
        由于Selenium没有判断元素是否存在的方法，自定义判断函数
        :param css: 要查找元素的css样式
        :return: 找到唯一一个该元素返回True，找到多个或没有找到返回False
        """
        s = self.driver.find_elements_by_css_selector(css_selector=css)
        if len(s) == 0:
            print('未找到该元素')
            return False
        elif len(s) == 1:
            return True
        else:
            print(f'找到{len(s)}个元素')
            return False
