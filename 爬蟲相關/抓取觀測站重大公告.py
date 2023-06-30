"""
抓取公開資訊觀測站新聞
https://mops.twse.com.tw/mops/web/t05sr01_1
"""

import requests as req
from bs4 import BeautifulSoup as bs
import json
import os
import sys

# https://requests.readthedocs.io/en/latest/api/#requests.Response
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# 使用公開資訊站API
# # 來源
# url = "https://openapi.twse.com.tw/v1/opendata/t187ap04_L"
# # 自定義 Header
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
#     # 'Referer': 'http://mops.twse.com.tw/mops/web/t05st01',
#     'Content-type': 'application/json'
# }
# res = req.get(url, headers=headers)
# news = json.loads(res.text)
# print(news[0])

# 觀注的股票代號
stocks = ['3006', '2002', '2303', '2330',
          '3008', '2379', '2603', '3545', '3037']

# 來源
url = "https://mops.twse.com.tw/mops/web/t05sr01_1"
# 自定義 Header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Referer': 'http://mops.twse.com.tw/mops/web/t05st01',
}
res = req.get(url, headers=headers)
soup = bs(res.text, "lxml")

news_table = soup.select("table.hasBorder")[0]
news = news_table.find_all("tr", {'class': ['even', 'odd']})

for topic in news:
    s = topic.select('td')
    # 觀注的項目才顯示
    if s[0].text in stocks:
        print("{0:<7}\t{1:<10s}\t{2}\t{3}\r\n".format(s[0].text, s[1].text, s[2].text+' '+s[3].text,
                                                      s[4].text.replace("\r\n", "")), end="")
