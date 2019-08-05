#   !/usr/bin/env python3

#   -*- coding: utf-8 -*-

#   Created on 2019-05-07  19:25

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re


url = 'https://muc.cheshirex.com/'

# driver = webdriver.Chrome()

# 静默启动浏览器
options = webdriver.ChromeOptions()
options.add_argument("headless")

# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(chrome_options=options)


def search(search_website, music_name):
    """

    :param music_name: 要搜索的歌曲名
    :param search_website: 要在那个网站搜索，网易云、QQ、酷狗、酷我、虾米、百度、咪咕。。。
    :return:
    """
    driver.get(url)

    WebDriverWait(driver, 10).until(
        # EC.presence_of_all_elements_located((By.ID, "skhvbklbfv"))
        EC.presence_of_element_located((By.ID, "j-validator"))  # 如果这里使用xpath只能获取到标签，不能到具体的信息，如文本
    )

    # 点击音乐名称，根据音乐名称搜索
    driver.find_element_by_xpath('//*[@id="j-nav"]/li[1]').click()

    # 填入数据
    input_tag = driver.find_element_by_id('j-input')
    input_tag.send_keys(music_name)

    # 选择要搜索的网站
    wangyiyun = driver.find_element_by_xpath('//*[@id="j-type"]/label[1]')
    qq = driver.find_element_by_xpath('//*[@id="j-type"]/label[2]')
    kugou = driver.find_element_by_xpath('//*[@id="j-type"]/label[3]')
    kuwo = driver.find_element_by_xpath('//*[@id="j-type"]/label[4]')
    xiami = driver.find_element_by_xpath('//*[@id="j-type"]/label[5]')
    baidu = driver.find_element_by_xpath('//*[@id="j-type"]/label[6]')
    migu = driver.find_element_by_xpath('//*[@id="j-type"]/label[8]')
    lizhi = driver.find_element_by_xpath('//*[@id="j-type"]/label[9]')

    if search_website == "netease":
        wangyiyun.click()
    elif search_website == "qq":
        qq.click()
    elif search_website == "kugou":
        kugou.click()
    elif search_website == "kuwo":
        kuwo.click()
    elif search_website == "xiami":
        xiami.click()
    elif search_website == "baidu":
        baidu.click()
    elif search_website == "migu":
        migu.click()
    elif search_website == "lizhi":
        lizhi.click()

    # 搜索

    search_but = driver.find_element_by_id('j-submit')
    search_but.click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "aplayer-more"))  # 如果这里使用xpath只能获取到标签，不能到具体的信息，如文本
    )
    sucess_back = driver.find_element_by_id('j-back')
    style = sucess_back.value_of_css_property('display')
    if "block" in style:
        music_url = driver.find_element_by_id('j-src-btn').get_attribute('href')
        music_name_author = driver.find_element_by_id('j-src-btn').get_attribute('download')
        pic = driver.find_element_by_xpath('//*[@id="j-player"]/div[1]').get_attribute('style')

        if music_url:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="j-player"]/div[1]/div'))
                # 如果这里使用xpath只能获取到标签，不能到具体的信息，如文本
            ).click()

        # driver.find_element_by_xpath('//*[@id="j-player"]/div[1]/div').click()

        pic = re.split(r'\"', pic)[1]

        music_info = music_name_author[:music_name_author.index('.')]

        print(pic, music_info, music_url)

        return [pic,music_info, music_url]


if __name__ == '__main__':

    search('netease', input("输入歌曲名："))
