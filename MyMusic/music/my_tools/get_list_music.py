#   !/usr/bin/env python3

#   -*- coding: utf-8 -*-

#   Created on 2019-05-04  11:11
import csv
import urllib.request,os,json, time
from lxml import etree
from requests_html import HTMLSession
import execjs,requests,random
import base64,codecs
from Crypto.Cipher import AES


"""
    根据歌单id获取网易云歌单的歌曲
"""

MUSIC = []

def to_16(key):
    while len(key) % 16 != 0:
        key += '\0'
    return str.encode(key)

def AES_encrypt(text, key, iv): #text为密文，key为公钥，iv为偏移量
    bs = AES.block_size
    pad2 = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    encryptor = AES.new(to_16(key), AES.MODE_CBC,to_16(iv))
    encrypt_aes = encryptor.encrypt(str.encode(pad2(text)))
    encrypt_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
    return encrypt_text

def RSA_encrypt(text, pubKey, modulus):
    text=text[::-1]
    rs=int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)

def set_proxy():
    proxy = [
        '117.114.149.10:45801',
        '163.125.114.95:8118',
        "60.13.42.183:9999",
        "117.91.249.180:9999",
        "221.210.120.153:54402",
        '47.105.146.57:8118'
    ]
    return random.choice(proxy)

def set_user_agent():
    USER_AGENTS = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]
    user_agent = random.choice(USER_AGENTS)
    return user_agent

#获取i值的函数，即随机生成长度为16的字符串
get_i=execjs.compile(r"""
    function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
""")

class WanYiYun():
    def __init__(self, list_id, music_list_id):
        self.music_list_id = music_list_id
        # self.playlist_url='https://music.163.com/playlist?id=2624438246'  #歌单地址
        self.playlist_url='https://music.163.com/playlist?id={}'.format(list_id)    #歌单地址
        self.song_url='https://music.163.com/weapi/song/enhance/player/url?csrf_token='
        self.g = '0CoJUm6Qyw8W8jud'#buU9L(["爱心", "女孩", "惊恐", "大笑"])的值
        self.b = "010001"#buU9L(["流泪", "强"])的值
        # buU9L(Rg4k.md)的值
        self.c = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.i=get_i.call('a',16)#随机生成长度为16的字符串
        self.iv = "0102030405060708"  # 偏移量

        self.headers={
            'User-Agent':set_user_agent(),
            'Referer':'https://music.163.com/',
            'Content-Type':'application/x-www-form-urlencoded',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'upgrade-insecure-requests': '1'
        }

    #由于歌单内容是通过JS生成的，所以此处运用requests_html这个库来实现JS渲染从而获得歌单
    def get_music_list(self):
        session = HTMLSession()
        response = session.get(self.playlist_url)  #===================================
        html = etree.HTML(response.content.decode())
        song_list = html.xpath("//ul[@class='f-hide']/li/a")
        music_list = []
        for song in song_list:
            music_id = song.xpath('.//@href')
            music_name = song.xpath('.//text()')
            music_list.append({'id': music_id, 'name': music_name})

        return music_list

    def get_params(self, id):    #id为歌曲id
        encText=str({'ids': "[" + str(id) + "]", 'br': 128000, 'csrf_token': ""})
        return AES_encrypt(AES_encrypt(encText,self.g, self.iv), self.i, self.iv)

    def get_encSecKey(self):
        return RSA_encrypt(self.i, self.b, self.c)

    def download(self):
        music_list=self.get_music_list()
        for music in music_list:
            try:
                print(music)

                music_id = music['id'][0].split('=')[1]
                music_name = music['name'][0]
                time.sleep(1)
                page = requests.get(
                    'https://music.163.com/song?id={}'.format(music_id)).content.decode('utf-8')
                page = etree.HTML(page)
                author_album = page.xpath('//div[@class="m-lycifo"]//div[@class="cnt"]//a/text()')
                author = author_album[0]
                album = author_album[1]
                formdata = {'params': self.get_params(music_id),
                            'encSecKey': self.get_encSecKey()}
                response = requests.post(self.song_url, headers=self.headers, data=formdata)
                download_url = json.loads(response.content)["data"][0]["url"]

                print(music_name, download_url, author, album)

                if download_url:
                    print(music_name, download_url, author, album)
                    # value = {"music_id":music_id, "music_name": music_name, "music_url": download_url, "music_author": author,
                    #          "music_album": album,"music_list_id": self.music_list_id}

                    value = [(music_id, music_name,
                             download_url, author,
                             album,self.music_list_id)]

                    with open("music.csv", 'a', encoding="utf-8", newline="") as fp:
                        writer = csv.writer(fp)
                        writer.writerows(value)

                    # return value
                    # MUSIC.append(value)
                    # if not os.path.exists("music"):
                    #     os.mkdir('music')
                    #
                    # try:
                    #     # 根据音乐url地址，用urllib.request.retrieve直接将远程数据下载到本地
                    #     urllib.request.urlretrieve(download_url, 'music/' + music_name+ '.mp3')
                    #     print('Successfully Download:'+music_name+ '.mp3')
                    # except:
                    #     print('Download wrong~')


                    # 写入csv


                else:
                    # return ""
                    print('XXXXXXXX')

            except:
                print(music_name, "出错！！！")
                break


def run():
    # header = ['music_id', 'music_name', 'music_url', 'music_author', 'music_album', 'music_list_id']
    # with open("music.csv", 'a', encoding="utf-8", newline="") as fp:
    #     writer = csv.DictWriter(fp, header)  # 传入文件对象和表头信息
    #     writer.writeheader()  # 把表头文件写入文件
        # writer.writerows(MUSIC)  # 写入数据

    va = [
          {'list_id': '2546440248', 'music_list_id': 988},
          {'list_id': '2575079513', 'music_list_id': 989},
          {'list_id': '2504609940', 'music_list_id': 990},
          {'list_id': '2549684428', 'music_list_id': 991},
    ]

    for i in va:
        list_id = i.get('list_id')
        music_list_id = i.get('music_list_id')

        wanyiyun = WanYiYun(list_id, music_list_id)
        wanyiyun.download()


    # return MUSIC

if __name__ == '__main__':
    run()

