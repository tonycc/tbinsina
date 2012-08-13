# -*- coding: utf-8 -*-
'''
Created on 2012-8-12

@author: Tony
'''
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from tbinsina.weibo import forms
from tbinsina.weibo.models import UserInfo

from tbinsina.weiboapi.weibo import APIClient

APP_KEY = '1279033890' # app key
APP_SECRET = '392001a59101bc9bee428429247f6251' # app secret
CALLBACK_URL = 'http://127.0.0.1:8000/login_check' # callback url

def index(request):
    return render_to_response("weibo/login.html",{},context_instance=RequestContext(request))

def login(request):

    
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client.get_authorize_url()
    return HttpResponseRedirect(url)

def login_check(request):
    code=request.GET.get('code',None)
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    r=client.request_access_token(code)
    access_token=r.access_token
    expires_in=r.expires_in
    
    request.session['access_token']=access_token
    request.session['expires_in']=expires_in
    
    return render_to_response("weibo/operation.html",{'userForm':forms.UserForm()},context_instance=RequestContext(request))

def get_fans(request):
    access_token=request.session['access_token']
    expires_in=request.session['expires_in']
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    client.set_access_token(access_token, expires_in)
    
    if request.method=="POST":
        form=forms.UserForm(request.POST.copy())
        if form.is_valid():
            username=form.cleaned_data['username']
            cur=1
            while cur<3:
                fans=client.friendships__followers(screen_name=username,count=200,cursor=cur)
                for fan in fans.users:
                    userinfo=UserInfo(uid=fan.id,username=fan.screen_name,province=fan.province,city=fan.province,location=fan.location,gender=fan.gender,verified=fan.verified)
                    userinfo.save()
                cur=cur+1
    return render_to_response("weibo/operation.html",{'userForm':forms.UserForm()},context_instance=RequestContext(request))