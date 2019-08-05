#   !/usr/bin/env python3

#   -*- coding: utf-8 -*-

#   Created on 2019-05-06  14:41

import requests,time
from lxml import etree

"""
    获取网易云歌单的id、标题、图片、标签
    以及歌曲的风格、语种
"""

# url = "https://music.163.com/discover/playlist/"
# url = "https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=0"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "referer": "https://music.163.com/"
}

data = {
    "order": "hot",
    "cat": "全部",
    "limit": "35",
    "offset": "0"
}

SONG_LIST = []
STYLE = {}

def request_page(url, x):
    data["offset"] = x
    html = requests.get(url, headers=headers, data=data).content.decode('utf-8')

    # 爬取音乐列表内容
    parse_page(html)

    # 获取语种
    # music_type(html)




def parse_page(html):
    time.sleep(1)
    html =etree.HTML(html)
    divs = html.xpath('//*[@id="m-pl-container"]/li/div')
    for div in divs:
        list_url = div.xpath('./a/@href')[0]
        list_id = list_url[list_url.index('=')+1:]
        list_title = div.xpath('./a/@title')[0]
        img = div.xpath('./img/@src')[0]
        list_img = img[:img.index('?')]

        page = requests.get(
            'https://music.163.com/playlist?id={}'.format(list_id),
            headers=headers,
            data={"id": "{}".format(list_id)}
        )
        page_content = etree.HTML(page.content.decode('utf-8'))
        list_tag = " ".join(page_content.xpath('//a[@class="u-tag"]/i/text()'))

        print(list_url, list_id, list_title, list_img, list_tag)

        SONG_LIST.append({"list_id": list_id, "list_title": list_title, "list_img": list_img, "list_tag": list_tag})


def music_type(html):
    html = etree.HTML(html)
    language = html.xpath('//*[@id="cateListBox"]/div[2]/dl[1]/dd//a/text()')
    style = html.xpath('//*[@id="cateListBox"]/div[2]/dl[2]/dd//a/text()')

    print("语种：", language)
    print("风格：", style)

    STYLE["music_language"] = language
    STYLE["music_style"] = style


def run():
    n = input("要爬几页（歌单）：")
    x = 0
    for i in range(int(n)):
        # 一页有35个
        url = "https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={}".format(x)
        x += 35
        request_page(url, str(x))
        time.sleep(2)

    # return STYLE
    return SONG_LIST


if __name__ == '__main__':
    i = run()
    # print(i)



