#   !/usr/bin/env python3

#   -*- coding: utf-8 -*-

#   Created on 2019-05-12  15:47
import csv
import requests
from lxml import etree
import time


def get_music_info(list_id, music_list_id):
    i = 0
    url = "https://music.163.com/playlist?id={}".format(list_id)
    html = requests.get(url).content.decode('utf-8')
    content = etree.HTML(html)
    song_ids = content.xpath('//div[@id="song-list-pre-cache"]//a/@href')
    for song_id in song_ids:
        i += 1
        if i > 10:
            break

        song_id = song_id[song_id.index('=')+1:]
        url = "https://music.163.com/song?id={}".format(song_id)
        info_page = requests.get(url).content.decode('utf-8')
        page_content = etree.HTML(info_page)

        img = page_content.xpath('//img[@class="j-img"]/@src')
        title = page_content.xpath('//em[@class="f-ff2"]/text()')
        author = page_content.xpath('//a[@class="s-fc7"]/text()')[0]
        album = page_content.xpath('//a[@class="s-fc7"]/text()')[1]

        info = [
            (song_id, img[0], title[0], author, album, music_list_id)
        ]
        with open("song2.csv", 'a', encoding="utf-8", newline="") as fp:
            writer = csv.writer(fp)  # 创建writer对象
            writer.writerows(info)

        print(info)
        time.sleep(1)


    # return INFO

if __name__ == '__main__':
    va = [
        {'list_id': '2760389790', 'music_list_id': 1061},
        {'list_id': '2651023300', 'music_list_id': 1062},
        {'list_id': '2756282456', 'music_list_id': 1063},
        {'list_id': '2727771521', 'music_list_id': 1064},
    ]

    for i in va:
        print("=========================== " + str(i.get('music_list_id')) + " ===========================")
        get_music_info(i.get('list_id'), i.get('music_list_id'))



    # get_music_info('2790812763')