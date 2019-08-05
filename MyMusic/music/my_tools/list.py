#   !/usr/bin/env python3

#   -*- coding: utf-8 -*-

#   Created on 2019-05-12  20:21


# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# import re
#
# driver = webdriver.Chrome()
#
# url = "https://music.mli.im/music.web"
# driver.get(url)
#
# WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.ID, 'like-lists'))
#     # 如果这里使用xpath只能获取到标签，不能到具体的信息，如文本
# ).click()
#
# # driver.find_element_by_id('like-lists').click()
#
#
#
# box = driver.find_element_by_id("mCSB_1_container").get_attribute('class')
#
# if box == "mCSB_container":
#     lists = driver.find_element_by_xpath('//*[@id="mCSB_1_container"]/div[4]')
#     print(lists)


import requests
from lxml import etree
import time

"""
    获取榜单排行的json数据
"""

url = "https://music.163.com/discover/toplist?id=3778678"

html = requests.get(url).content.decode('utf-8')

page = etree.HTML(html)

# print(html)
#
# trs = page.xpath('//tr')
#
# print(trs)
#
# for tr in trs:
#     img = tr.xpath('.//td[2]//img/@src')
#     song_id = tr.xpath('.//div[@class="tt"]//span[@class="ply "]/@data-res-id')
#     name = tr.xpath('.//div[@class="ttc"]//b/@title')
#     author = tr.xpath('.//td[4]/div/@title')
#
#     print(song_id, name, author, img)
#     break

str = page.xpath('//textarea[@id="song-list-pre-data"]/text()')

print(str)

