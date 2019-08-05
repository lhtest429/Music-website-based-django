#   !/usr/bin/env python3

#   -*- coding: utf-8 -*-

#   Created on 2019-05-12  18:29

import requests, time
from lxml import etree


url = "https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=35"

# 0 35 70

LIST = []

def get_list():
    for i in range(10):
        n = i*35
        print(n)
        url = "https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={}".format(int(n))

        html = requests.get(url).content.decode('utf-8')
        page = etree.HTML(html)

        lis = page.xpath('//*[@id="m-pl-container"]//li')
        for li in lis:
            list_img = li.xpath('./div/img[@class="j-flag"]/@src')
            list_title = li.xpath('./div/a/@title')
            list_id = li.xpath('./div/a/@href')

            detail = requests.get('https://music.163.com/playlist?id={}'.format(list_id)).content.decode('utf-8')
            detail = etree.HTML(detail)
            tags_li = detail.xpath('//a[@class="u-tag"]//i/text()')

            tags = " ".join(tags_li)

            rel_list_id = list_id[0][13:]

            list_info = {"list_id": rel_list_id, "list_title": list_title[0],
                         'list_img': list_img[0], 'list_tags':tags_li}
            print(list_info)
            LIST.append(list_info)

            return

    return LIST

if __name__ == '__main__':
    get_list()