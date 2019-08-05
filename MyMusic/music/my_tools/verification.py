#   !/usr/bin/env python3

#   -*- coding: utf-8 -*-

#   Created on 2019-05-25  10:00

import re

"""
    验证邮箱地址
"""

def verification(str):
    re_str = re.compile('^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$')
    result = re.match(re_str, str)
    print(result)

    if result is None:
        return "error"
    else:
        return 'ok'

if __name__ == '__main__':
    s = verification('wpf1011467276@gmail.com')
    print(s)

