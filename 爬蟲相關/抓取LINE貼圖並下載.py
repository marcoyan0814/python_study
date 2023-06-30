"""
抓取LINE貼圖
https://store.line.me/stickershop/product/28698/zh-Hant
"""

import requests as req
from bs4 import BeautifulSoup as bs
import json
import os
import sys

# https://requests.readthedocs.io/en/latest/api/#requests.Response
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# 存放路徑
folderPath = "stickers"

# Line 貼圖來源
url = "https://store.line.me/stickershop/product/28698/zh-Hant"
# 自定義 Header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
res = req.get(url, headers=headers)

soup = bs(res.text, "lxml")
# print(soup.prettify())
# 取得貼圖主要資訊
ld_json = soup.select('html script[type="application/ld+json"]')[0].contents[0]
productInfo = json.loads(ld_json)
# 新資料夾 id_貼圖名稱
fd = f"{folderPath}/{productInfo['sku']}_{productInfo['name']}"

# 解析貼圖資料
items = soup.select("ul.FnStickerList > li.FnStickerPreviewItem")

# 若有貼圖資料才繼續
if items:
    # 不存在就建立路徑
    if not os.path.exists(fd):
        os.makedirs(fd)

    # 貼圖物件
    stickers = []
    for item in items:
        stickerInfo = json.loads(item['data-preview'])
        obj = {
            "id": stickerInfo['id'],
            "url": stickerInfo['animationUrl'],
            "filename": f"{productInfo['sku']}_{stickerInfo['id']}.png"
        }
        stickers.append(obj)

    # 下載貼圖
    if stickers:
        for sticker in stickers:
            os.system(
                f"curl -s {sticker['url']} -o {fd}/{sticker['filename']}")
            print(f"{sticker['url']} 下載成功，存至 {fd}/{sticker['filename']}")
