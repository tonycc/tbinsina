# -*- coding: utf-8 -*-
'''
Created on 2012-8-12

@author: Tony
'''
from django import forms


class UserForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput,label='')