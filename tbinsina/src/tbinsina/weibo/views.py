# -*- coding: utf-8 -*-
'''
Created on 2012-8-12

@author: Tony
'''
import time

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
            #获取用户粉丝
            next_cursor=1
            while next_cursor>0:
                fans=client.friendships__followers(screen_name=username,count=200,cursor=next_cursor)
                next_cursor=fans.next_cursor
                print next_cursor
                for fan in fans.users:
                    userinfo=UserInfo(uid=fan.id,username=fan.screen_name,province=fan.province,city=fan.province,location=fan.location,gender=fan.gender,verified=fan.verified)
                    userinfo.save()
            #获取优质粉丝
            '''user_info=client.users__show(screen_name=username)
            user_id=user_info.id
            active_fans=client.friendships__followers__active(uid=user_id,count=200)
            for active_fan in active_fans.users:
                userinfo=UserInfo(uid=active_fan.id,username=active_fan.screen_name,province=active_fan.province,city=active_fan.province,location=active_fan.location,gender=active_fan.gender,verified=active_fan.verified)
                userinfo.save()'''           
    return render_to_response("weibo/operation.html",{'userForm':forms.UserForm()},context_instance=RequestContext(request))

'''发布评论@用户'''
def comments(request):
    access_token=request.session['access_token']
    expires_in=request.session['expires_in']
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    client.set_access_token(access_token, expires_in)
    #获取用户发布的微博id
    weiboids=client.statuses__user_timeline__ids(access_token=access_token,screen_name='爱淘的小可')
    weiboid_list=weiboids.statuses
    #微博内容
    content=' 超级简单的减肥方法，早晚两次迅速见效。买减肥霜还送保鲜膜，超级划算的。千万不要错过。http://t.cn/zWYXkam'
    username=''
    i=0
    #读取用户
    userInfos=UserInfo.objects.filter(gender='f').order_by('-uid').values('username')
    for userinfo in userInfos:
        if len(username)<80:
            #记录该用户是否已经@过
            UserInfo.objects.filter(username=userinfo['username']).update(weibo=weiboid_list[0]) 
            username=username+'@'+userinfo['username']+' '
        else:
            '''每小时发50个评论'''
            if i<50:     
                print str(i)+' ' +username+content
                client.post.comments__create(comment=username+content,id=weiboid_list[0])
                time.sleep(12)
                i=i+1
                username='@'+userinfo['username']+' ' 
            else:
                print "wait 3600 sedonds"
                time.sleep(3600)     
                i=0
        

    return render_to_response("weibo/operation.html",{'userForm':forms.UserForm()},context_instance=RequestContext(request))
    