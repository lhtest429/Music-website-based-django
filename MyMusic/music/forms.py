#   !/usr/bin/env python3

#   -*- coding: utf-8 -*-

#   Created on 2019-05-08  14:40

from django import forms

class MyForm(forms.Form):
    email = forms.EmailField()
