# -*- coding: utf-8 -*-
'''
Created on 2012-8-12

@author: Tony
'''
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uid=models.CharField(max_length=20)
    username=models.CharField(max_length=30)
    province=models.CharField(max_length=10,blank=True)
    city=models.CharField(max_length=10,blank=True)
    location=models.CharField(max_length=60,blank=True)
    gender=models.CharField(max_length=5,blank=True)
    verified=models.CharField(max_length=5,blank=True)
    weibo=models.CharField(max_length=50,blank=True)
    
    def __unicode__(self):       
        return self.username
    
    class Meta:
        ordering=['username']
    
    class Admin:
        pass
    