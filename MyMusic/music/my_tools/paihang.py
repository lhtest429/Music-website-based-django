#   !/usr/bin/env python3

#   -*- coding: utf-8 -*-

#   Created on 2019-05-07  17:09
import json


def get_paihang():
    PAIHANG = []
    no = 1
    with open('music/my_tools/paihang.json', 'r', encoding='utf-8') as fp:
        str = fp.read()
        json_strs = json.loads(str)
        for json_str in json_strs:
            song_id = json_str['id']
            song_name = json_str['name']
            author = json_str['artists'][0]['name']
            album = json_str['album']['name']
            pic = json_str['album']['picUrl']

            # print({"song_id":song_id, "song_name":song_name, "author":author, "album":album, "pic":pic})
            PAIHANG.append({"no": no, "song_id": song_id, "song_name": song_name,
                            "author": author, "album": album, "pic": pic})
            no += 1

    return PAIHANG


if __name__ == '__main__':
    get_paihang()
