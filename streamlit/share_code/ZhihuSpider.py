# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 14:23:12 2021

@author: vivian
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

class ZhihuSpider:
    def __init__(self):
        """初始化变量"""
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            "Cookie": '_xsrf=BJ1fs2zqregNfHAhPzq4TVxRB3b1NBhX; d_c0="AHCo81IVWg-PToMIt0OsSpg7B6mrCKmDqdI=|1556523425"; q_c1=219169cce15a42c6a292fdf824a5aa5b|1582958602000|1556523441000; _zap=291f96cb-63dd-45d9-af59-f5fd6198d3e0; _9755xjdesxxd_=32; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1630589126,1631342997,1631346002,1631937887; SESSIONID=dzrk4qTCwpVcqtbo8XoR316fu3Rc4X4n7QE6Fo743wU; __snaker__id=V9dBTy9Jflz3z5ca; JOID=UF4WAU4Ts5V2NkHvMBMgypHLlnUic8zmGgU0vnJjx8YUQDKJWnPS1hc1QOs2ZLgFxy1nOtKvn88SKZkIq1KM8qw=; osd=V14TBkgUs5BxMEbvNRQmzZHOkXMlc8nhHAI0u3VlwMYRRzSOWnbV0BA1RewwY7gAwCtgOteomcgSLJ4OrFKJ9ao=; YD00517437729195%3AWM_NI=dCZ0EFkiUiBQoZfTxY3LVgwntCtr6G5aR3vhhz8qfKwT6mx3wHD5qKKRF7AXelDG%2FrMMhg5idpgFjg4HkqjV3pMbC9%2Bt81%2FgJuHuQiTrzT6LKKTtD2vGJ%2BASu57pZn9%2FY0g%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eebaf32586ba86a7c93e989e8ba3d45a978a9eabf873b2ecbea6f05f96b9f995b82af0fea7c3b92aa89d96d1c84ea9b79b8ac15bad86aab5fb53f1949a88f666b89dbc93b54df7bf9ed4f564aca6f892e541b58cfa8efb39b5988cd6f441898e8ad8c454a7b48ca8ae7a8f93a888b863a8b0a9a7e96df898a592e95ef1b08383c233e9acf8d2ae6d8aab8896d46398aeb6b5b54889959c95c73ab69986ccc459b7ebf991d966fbf197d1e637e2a3; YD00517437729195%3AWM_TID=7UgHlwTIvL5AAQUVURYu37puQjEQ1%2Fsp; gdxidpyhxdE=kK4knuK0ZC8L1jVwU9VGYtzuyzYDgVCq0Peo%2BlJlBbVBa%5CE%2BH3d%2B%2Fi%2BORs7aid7Occ42%2FEo6Ipm%2FwmjHEbpNOH%2B16Ts%2FwfosOXhaj6mM9Tw%2BG%2BQDrX8jznvpWx%2B86KwnHcUKnX41UxMjghIp4sjsBgi%2BiItPRRtVjQ4mS1Tsn1nie5w8%3A1631942152327; captcha_session_v2="2|1:0|10:1631941599|18:captcha_session_v2|88:SnlGSWYxZWdzYS9VYXhoVnhoWjR5OVFjMkorSFFpeXBTMVRqQmVYZDFCT0xVcWhYcFVtNkp6OW4vWDJ6ZHZvLw==|89fda8d79c7a09c4a7a7009b548d9075b41e06fe311333e1e7363b33f3983e26"; captcha_ticket_v2="2|1:0|10:1631941608|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfOGl5eTcuZklFQ2RPUFQ3WC5qRFBWc2l4Y2ZvemZTVE9OTXAwQkV0cjVaNVlUR3oyRG5Id0pQczFyeFZ1R1JwRUtnLm1MalFkYi1LUktFcHZScGNsdXJoaVRlcjVqeEl1QkE5UmJiVGphSmFqYk9UNG5PczhUQ1RZU0NuNnNQLmtVdjdLYW1EU3lDNF9IUkFwSnZqSGJNTi4xWUFPbFgxOGo5TU1CXy1DR29fQ01zZ0NmVWx1bTVrRWgxc3B1S2tKVXZTQjR0c1FTYTVHdWQ2OFZJNkE0aVRGc1hCV0hYLXRKNVNBdjI5Sy5IQXlIaWtTZnlPTUZmemN4RW5VZGdEbHppRFUtQzlURi1mYy0wdGVma1BoOFgxWGRzcUdHaVktb0Y0c1QyTlo1eVpZSGFCMi1Zcnd6YlcyVHNldFl5MFpHUWY1Zi5MZXo5MUh5aFluNWZrTTg5a2I3VXdGNzF1dnp5WXVEem1PWHpaSmpNTDctNDlHYjltX2VCV0EtN25QeTJudDJXTHlCX01fNzJuNHZBOHU4WkFBb1NtbU81Ljd0RlQwYUxmTUpPaVJUQ3pmRHdZZ1E2VTlNa2NWTURTQzA4WVhqY3ZJeXguOE8tQ0lGMFMtNkpyNGtidC1EdlYwMFhXS2thNTZoTG1Sbk9nNnhudkxELVRobktwMyJ9|90fb49878ce1a5ab37a4bb67cdce8f7f3b194db7e93a90e826221ecab3166532"; z_c0="2|1:0|10:1631941608|4:z_c0|92:Mi4xS05DeUJ3QUFBQUFBY0tqelVoVmFEeVlBQUFCZ0FsVk42TUV5WWdDdzhHZkh4S2VaMGxzMmlaYm9oRDg0Z19Gcnln|1a6d384ebe8bc1713ee671304afd2bf4be3b81ef23cd0067453f1f38e43edbcf"; tshl=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1631942942; tst=h; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1631942946|1631937885'
        }
        self.session = requests.Session()

    def web_link(self, url='https://www.zhihu.com/hot'):
        """网页连接"""
        try:
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            else:
                return None
        except requests.RequestException:
            return None

    def hot_items(self, hot_rep):
        """解析热榜上的top50话题"""
        bf = BeautifulSoup(hot_rep.text, 'html.parser')
        if bf:
            hot_items = bf.find_all('section', class_='HotItem')
            item_message = {}
            for hot_item in hot_items:

                # 话题名次
                item_message['index'] = hot_item.find('div', class_='HotItem-rank').string
                # 话题标题
                item_message['title'] = hot_item.find(class_='HotItem-title').string

                hot_item_content = hot_item.find('div', class_='HotItem-content')
                # 话题网页链接
                item_message['url'] = hot_item_content.a.attrs['href']
                item_message['id'] = item_message['url'].split('/')[-1]
                # 话题描述
                excerpt = hot_item_content.find('p', class_='HotItem-excerpt')
                if excerpt:
                    item_message['excerpt'] = excerpt.string
                else:
                    item_message['excerpt'] = None
                # 话题热度值
                metrics = hot_item_content.find('div', class_='HotItem-metrics').get_text()
                item_message['hot'] = re.search(r"\d+", metrics).group()
                yield item_message