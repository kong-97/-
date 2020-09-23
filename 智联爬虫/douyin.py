import requests
ts=1588841556
headers = {'authority': 'api.amemv.com',
           'scheme': 'https',
           'path': '/aweme/v1/general/search/single/?keyword=%E5%A7%9C%E5%8D%81%E4%B8%83&offset=0&count=10&is_pull_refresh=0&hot_search=0&latitude=35.420609&longitude=103.862569&ts=1588841556&js_sdk_version=&app_type=normal&manifest_version_code=300&_rticket=1588841557617&ac=wifi&device_id=36746482455&iid=1275069416612829&os_version=8.0.0&channel=baidu&version_code=300&device_type=SM-C7000&language=zh&uuid=353114085094615&resolution=1080*1920&openudid=41c54d85b33579f5&update_version_code=3002&app_name=aweme&version_name=3.0.0&os_api=26&device_brand=samsung&ssmix=a&device_platform=android&dpi=420&aid=1128&as=a135ecdb54f51e8ce30833&cp=cd52ef57473cb6c7e1Yoaw&mas=01f5500c9952752d74880972126489f407cccc1c0ccca6c61ca68c',
           'accept-encoding': 'gzip',
           'x-ss-req-ticket': '1588841557608',
           'sdk-version': '1',
           'x-ss-tc': '0',
           'user-agent': 'com.ss.android.ugc.aweme/300 (Linux; U; Android 8.0.0; zh_CN; SM-C7000; Build/R16NW; Cronet/58.0.2991.0)'}
cookies = {'install_id': '1275069416612829',
           'ttreq': '1$29aa46b0e064fbd059afe865dcf1233725348371',
           'odin_tt': 'bb9883463f86a036b54888c5b39467f862c963d606726a8da9e1c7eb74e55ff33a786b613017e27fbf793b8adfa0a35d',
           'qh[360]': '1'}
url = 'https://api.amemv.com/aweme/v1/general/search/single/?keyword=%E5%A7%9C%E5%8D%81%E4%B8%83&offset=0&count=10&is_pull_refresh=0&hot_search=0&latitude=35.420609&longitude=103.862569&ts=1588841556&js_sdk_version=&app_type=normal&manifest_version_code=300&_rticket=1588841557617&ac=wifi&device_id=36746482455&iid=1275069416612829&os_version=8.0.0&channel=baidu&version_code=300&device_type=SM-C7000&language=zh&uuid=353114085094615&resolution=1080*1920&openudid=41c54d85b33579f5&update_version_code=3002&app_name=aweme&version_name=3.0.0&os_api=26&device_brand=samsung&ssmix=a&device_platform=android&dpi=420&aid=1128&as=a135ecdb54f51e8ce30833&cp=cd52ef57473cb6c7e1Yoaw&mas=01f5500c9952752d74880972126489f407cccc1c0ccca6c61ca68c'

rep = requests.get(url=url, headers=headers)
print(rep.content)