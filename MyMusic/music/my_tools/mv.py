#   !/usr/bin/env python3

#   -*- coding: utf-8 -*-

#   Created on 2019-05-13  16:12
import csv

import requests
import time
import json


# "https://api.imjad.cn/cloudmusic/?type=search&search_type=1004&s=taylor&offset=0"
# "https://api.imjad.cn/cloudmusic/?type=search&search_type=1004&s=taylor&offset=20"

# url = "https://api.imjad.cn/cloudmusic/?type=mv&id=10866251"
#
# str = requests.get(url).content.decode('utf-8')
#
# print(str)

def get_mv_list(num):
    n = 0

    with open("mv_list.json", 'a', encoding='utf-8') as fp:
        fp.write('[')
        for i in range(int(num)):
            url = 'https://api.imjad.cn/cloudmusic/?type=search&search_type=1004&s=taylor&offset={}'.format(str(n))
            n += 20

            json_str = requests.get(url).content.decode('utf-8')

            print(json_str)
            fp.write(json_str + ',')

            time.sleep(2)
        fp.write(']')


def get_mv_info():
    with open('mv_list.json', 'r', encoding='utf-8') as fp:
        json_str = fp.read()
        dicts = json.loads(json_str)
        # print(dicts)
        for d in dicts:
            mvs = d['result']['mvs']
            with open('music/my_tools/mv.json', 'a', encoding='utf-8') as f:
                f.write('[')
                for mv in mvs:
                    mv_id = mv['id']
                    url = "https://api.imjad.cn/cloudmusic/?type=mv&id={}".format(mv_id)
                    detail = requests.get(url).content.decode('utf-8')
                    print(detail)
                    f.write(detail + ",")
                f.write(']')


def get_mv():
    MV_INFO = []
    with open('E:\pyCharm\Django_study\MyMusic\music\my_tools\mv.json', 'r', encoding='utf-8') as fp:
        json_str = fp.read()
        dicts = json.loads(json_str)
        for d in dicts:
            mv_id = d['data']['id']
            mv_name = d['data']['name']
            mv_author = d['data']['artistName']
            mv_desc = d['data']['desc']
            mv_pic = d['data']['cover']
            playCount = str(d['data']['playCount'])
            publishTime = d['data']['publishTime']
            try:
                mv_url_240 = d['data']['brs']['240']
            except:
                mv_url_240 = ""
            try:
                mv_url_480 = d['data']['brs']['480']
            except:
                mv_url_480 = ""
            try:
                mv_url_720 = d['data']['brs']['720']
            except:
                mv_url_720 = ""
            try:
                mv_url_1080 = d['data']['brs']['1080']
            except:
                mv_url_1080 = ""

            if len(playCount) > 4:
                playCount = playCount[:-4] + "万"

            if mv_url_240 == "" and mv_url_480 == "" and mv_url_720 == "" and mv_url_1080 == "":
                continue

            else:
                mv_info = {
                    "mv_id": mv_id,
                    "mv_name": mv_name,
                    "mv_author": mv_author,
                    "mv_desc": mv_desc,
                    "mv_pic": mv_pic,
                    "playCount": playCount,
                    "publishTime": publishTime,
                    "mv_url_240": mv_url_240,
                    "mv_url_480": mv_url_480,
                    "mv_url_720": mv_url_720,
                    "mv_url_1080": mv_url_1080
                }

                MV_INFO.append(mv_info)

    header = ["mv_id", 'mv_name', "mv_author", "mv_desc", "mv_pic", "playCount",
              "publishTime", 'mv_url_240', "mv_url_480", "mv_url_720", "mv_url_1080"]
    with open('mv.csv', 'a', encoding='utf-8', newline="") as fp:
        writer = csv.DictWriter(fp, header)  # 传入文件对象和表头信息
        writer.writeheader()  # 把表头文件写入文件
        writer.writerows(MV_INFO)  # 写入数据

    return MV_INFO


def get_mv_url(mv_id):
    url = "https://api.imjad.cn/cloudmusic/?type=mv&id={}".format(mv_id)
    json_str = requests.get(url).content.decode('utf-8')
    json_dict = json.loads(json_str)
    try:
        mv_url_240 = json_dict['data']['brs']['240']
    except:
        mv_url_240 = ""
    try:
        mv_url_480 = json_dict['data']['brs']['480']
    except:
        mv_url_480 = ""
    try:
        mv_url_720 = json_dict['data']['brs']['720']
    except:
        mv_url_720 = ""
    try:
        mv_url_1080 = json_dict['data']['brs']['1080']
    except:
        mv_url_1080 = ""

    return {"mv_url_240":mv_url_240, "mv_url_480":mv_url_480,
            "mv_url_720":mv_url_720, "mv_url_1080":mv_url_1080}

if __name__ == '__main__':
    # get_mv_list(input("输入一个数: "))
    # get_mv_info()
    get_mv()