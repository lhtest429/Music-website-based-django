#   !/usr/bin/env python3

#   -*- coding: utf-8 -*-

#   Created on 2019-05-24  21:10

import hashlib

"""
    md5加密
"""


def md5_encrypt(str):
    h = hashlib.md5()
    h.update(str.encode(encoding='utf-8'))

    return h.hexdigest()


if __name__ == '__main__':
    s = md5_encrypt("123")
    print(s)
