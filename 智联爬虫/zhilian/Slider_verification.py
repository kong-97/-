"""滑块验证"""
import random
import time
from selenium.webdriver import Chrome

from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SliderVerification():

    def get_snap(self, chorme):
        """
        对整个网页截图，保存成图片,然后用PIL.Image拿到图片对象
        :return: 图片对象
        """
        chorme.save_screenshot('snap.png')
        page_snap_obj = Image.open('snap.png')
        return page_snap_obj

    def get_image(self, chorme, class_name, num):
        """
        从网页的网站截图中，截取验证码图片
        :return: 验证码图片
        """
        # img = WebDriverWait(chorme, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        img = WebDriverWait(chorme, 10).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        time.sleep(2)  # 保证图片刷新出来
        localtion = img.location
        size = img.size

        top = localtion['y']
        bottom = localtion['y'] + size['height']
        left = localtion['x']
        right = localtion['x'] + size['width']

        page_snap_obj = self.get_snap(chorme)
        crop_img_obj = page_snap_obj.crop((left, top, right, bottom))
        crop_img_obj.save(f'{num}.png')
        return crop_img_obj

    def get_distance(self, image1, image2):
        """
        拿到滑动验证码需要移动的距离
        :param image1: 没有缺口的图片对象
        :param image2: 有缺口的图片对象
        :return: 需要移动的距离
        """
        threshold = 60
        left = 50
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                rgb1 = image1.load()[i, j]
                rgb2 = image2.load()[i, j]
                res1 = abs(rgb1[0] - rgb2[0])
                res2 = abs(rgb1[1] - rgb2[1])
                res3 = abs(rgb1[2] - rgb2[2])
                if not (res1 < threshold and res2 < threshold and res3 < threshold):
                    return i-7
        return i-7

    def get_tracks(self, distance):
        """
        拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
        匀变速运动基本公式
        1> v = v0 + at
        2> s = v0t + (at^2)/2
        3> v^2 - v0^2 = 2as
        :param distance:需要移动的距离
        :return:存放每0.3秒移动的距离
        """
        # 初速度
        v = 0
        # 单位时间为0.2秒来统计轨迹，轨迹即0.3秒内的位移
        t = 0.3
        # 位移/轨迹列表，列表内的一个元素代表0.3秒内的位移
        tracks = []
        # 当前的位移
        current = 0
        # 到达mid值开始减速
        mid = distance*4/5
        while current < distance:
            if current < mid:
                # 加速度越小单位时间的位移越小，模拟的轨迹就越多越详细
                a = 2
            else:
                a = -3
            # 初速度
            v0 = v
            # 0.3秒时间内的位移
            s = v0*t+0.5*a*(t**2)
            # 当前的位置
            current += s
            # 添加到轨迹列表
            tracks.append(round(s))

            # 速度已经达到v，该速度作为下次的初速度
            v = v0 + a*t
        if current > distance:
            tracks.append(distance - current)
        return tracks

    def click(self, block, chrome):  # 自定义点击函数,模拟人工点击
        action = ActionChains(chrome)
        action.click_and_hold(block).perform()
        time.sleep(random.randint(1, 10) / 10)
        action.release(block).perform()


# options = Options()
# # options.add_argument('--headless')
# # options.add_argument('--disable-gpu')
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# path = r'E:\web1905\Spider\xpy905_spider\day04\chromedriver.exe'
# chrome = Chrome(path, options=options)
# slider = SliderVerification()
# chrome.get('https://account.geetest.com/login')

# button = WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_radar_tip')))
# email = chrome.find_element_by_xpath('//div[contains(@class,"ivu-form-item-required")][1]//input')
# pwd = chrome.find_element_by_xpath('//div[contains(@class,"ivu-form-item-required")][2]//input')
# email.send_keys('12345@qq.com')
# time.sleep(2)
# pwd.send_keys('123456')
# time.sleep(3)
#
# button.click()
#
# image1 = slider.get_image(chrome)
#
# button = WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
# button.click()
#
# image2 = slider.get_image(chrome)
#
# distance = slider.get_distance(image1,image2)
#
# tracks = slider.get_tracks(distance)
#
# button = WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
# ActionChains(chrome).click_and_hold(button).perform()
# for track in tracks:
#     ActionChains(chrome).move_by_offset(xoffset=track, yoffset=0).perform()
# time.sleep(0.5)
# ActionChains(chrome).release().perform()
# time.sleep(20)


