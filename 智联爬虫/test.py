import time

from appium import webdriver

# 定义设备参数
from scrapy.http import HtmlResponse

cap = {
    "platformName": "Android",
    "platformVersion": "10",
    "deviceName": "8UR4C19C06011639",
    "appPackage": "com.ss.android.ugc.aweme",
    "appActivity": "com.ss.android.ugc.aweme.main.MainActivity",
    "noReset": True,
    "unicodekeyboard": True,
    "resetkeyboard": True,
    "automationName": "UiAutomator2"
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', cap)


def get_size():
    # 获取设备屏幕大小
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return x, y


def scroll_(l):
    x1 = int(l[0] * 0.5)
    y1 = int(l[1] * 0.9)
    y2 = int(l[1] * 0.25)
    while True:
        if '暂时没有更多了' in driver.page_source:
            break
        else:
            driver.swipe(x1, y1, x1, y2)
            time.sleep(0.2)


def search_():
    time.sleep(2)
    driver.find_element_by_id('bxp').click()
    time.sleep(2)
    driver.find_element_by_id('ai2').send_keys('姜十七')
    time.sleep(0.5)
    driver.find_elements_by_id('g7l')[0].click()
    time.sleep(2)
    h = driver.page_source
    with open('search.txt', 'w', encoding='utf8') as f:
        f.write(h)
    print(driver.get_display_density())
    return driver


def search_user():
    """
    用户搜索
    :return:
    """
    driver = search_()
    time.sleep(1)
    l = get_size()
    scroll_(l)
    html = driver.page_source
    print(html)


def fans_list():
    """
    用户粉丝
    :return:
    """
    search_()
    time.sleep(2)
    driver.find_element_by_xpath('//android.widget.HorizontalScrollView[@resource-id=\"com.ss.android.ugc.aweme:id/f2w\"]/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[3]/android.widget.TextView[@resource-id=\"android:id/text1\"]').click()
    # driver.find_element_by_xpath('//android.widget.FrameLayout[@resource-id="com.ss.android.ugc.aweme:id/n0"]/android.widget.RelativeLayout/android.widget.ImageView').click()
    time.sleep(1)
    driver.find_elements_by_id('com.ss.android.ugc.aweme:id/ccn')[0].click()
    time.sleep(0.5)
    fans = 'new UiSelector().text("粉丝")'
    driver.find_element_by_android_uiautomator(fans).click()
    time.sleep(2)
    l = get_size()
    scroll_(l)
    html = driver.page_source
    print(html)


def zuopin():
    """
    用户作品
    :return:
    """
    driver = search_()
    time.sleep(2)
    driver.find_element_by_xpath('//android.widget.HorizontalScrollView[@resource-id=\"com.ss.android.ugc.aweme:id/f2w\"]/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[3]/android.widget.TextView[@resource-id=\"android:id/text1\"]').click()
    # driver.find_element_by_xpath('//android.widget.FrameLayout[@resource-id="com.ss.android.ugc.aweme:id/n0"]/android.widget.RelativeLayout/android.widget.ImageView').click()
    time.sleep(1)
    driver.find_elements_by_id('com.ss.android.ugc.aweme:id/ccn')[0].click()
    time.sleep(0.5)
    h = driver.page_source
    re = HtmlResponse(h)
    print(re.headers)
    print(re)
    print(re.text)
    with open('zuopin.txt', 'w', encoding='utf8') as f:
        f.write(h)
    # l = get_size()
    # scroll_(l)
    # html = driver.page_source
    # print(html)

keyword = '%E6%90%9E%E7%AC%91'
cursor = '0'
count = '20'
current_timestamp = str(int(time.time() * 1000))
url = "https://aweme.snssdk.com/aweme/v1/discover/search/?cursor=" + cursor + "&keyword=" + keyword + "&count=" + count + "&type=1&ts=" + current_timestamp[
                                                                                                                                               :-3] + "&app_type=lite&os_api=23&device_type=HTC%20M8w&device_platform=android&ssmix=a&iid=96273560785&manifest_version_code=242&dpi=480&uuid=990072002918973&version_code=242&app_name=douyin_lite&version_name=2.4.2&openudid=e2246348cbfb50f5&device_id=70181717931&resolution=1080*1776&os_version=6.0&language=zh&device_brand=htc&ac=wifi&update_version_code=2420&aid=2329&channel=tengxun&_rticket=" + current_timestamp + "&as=a111111111111111111111&cp=a000000000000000000000&mas"
# zuopin()
# search_()
# fans_list()

# search_user()



import requests
url = 'https://www.xiaohua.com/hot/'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'}
cookies = {'UM_distinctid':'1720d59c21c3a8-015585bd6d5432-5a1a321f-100200-1720d59c21d3f7',
           'CNZZDATA1277476924':'1886769971-1589358444-https%253A%252F%252Fwww.baidu.com%252F%7C1589358444',
           'ASP.NET_SessionId':'je5jytrkmtohrddfdjvkwjwa','xiaohua_web_userid':'118303',
           'xiaohua_web_userkey':'74/HZq8TSRzIzTuQlFDkB8rYyRN0Sh8ossB1vvwTtNvQOv1q5J4EYw=='}
proxies = {'http': '121.193.143.249:80'}
requests.get(url=url, headers=headers, cookies=cookies, proxies=proxies)





