# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from app_dbop.models import vote_display, vote_rank, vote_admin
from wcproc import *
import os,re,datetime
import json

password = 'grace!@#'

def singervote_admin_validate(request):
    pwd = request.COOKIES.get('pwd','')
    if pwd != password:
        return False
    else:
        return True


def singervote_admin_logout(request):
    response = HttpResponse('logout!')
    response.delete_cookie('pwd')
    return HttpResponseRedirect('/login/')    


def singervote_admin_login(request):
    pwd = request.POST.get('password', '')
    if pwd == password:
        response = HttpResponseRedirect('/admin/')
        response.set_cookie('pwd', pwd, 3600)
        return response
    else:
        return render_to_response('singervote_login.html', {'err_msg':'password is wrong!'} )        


def singervote_play(reqeust, player_id):
    q = vote_rank.objects.filter(id=player_id)
    anynomous = singervote_get_anynomous()
    list_dic = {}
    if q:
        for it in q:
            url = it.url
            name= it.name
            player = it.player
            it.play_time += 1
            it.save()
            list_dic = {'player':it.player, 'song_name':it.name, 'anynomous':anynomous}
    return render_to_response('singervote_play.html', list_dic)

def singervote_set_ranksort(request, value):
    q = vote_admin.objects.all()
    if q:
        for it in q:
            if value == '0':
                it.ranksort = 0 
            else:
                it.ranksort = 1
            it.save()
    else:
        q = vote_admin(ranksort = 0)
        q.save()
    err_msg = "set successfully!"
    return singervote_admin_redirect(err_msg)


def singervote_set_anynomous(request, value):
    q = vote_admin.objects.all()
    if q:
        for it in q:
            if value == '1':
                it.anynomous = 1
            else:
                it.anynomous = 0
            it.save()
    else:
        q = vote_admin(anynomous = 1)
        q.save() 
    err_msg = "Set successfully!"
    return singervote_admin_redirect(err_msg)

def singervote_set_enablevote(request, value):
    q = vote_admin.objects.all()
    if q:
        for it in q:
            if value == '1':
                it.enablevote= 1
            else:
                it.enablevote= 0
            it.save()
    else:
        q = vote_admin(enablevote= 0)
        q.save() 
    err_msg = "Set successfully!"
    return singervote_admin_redirect(err_msg)

def singervote_player_add(request):
    if singervote_admin_validate(request) == False:    
        return HttpResponseRedirect('/login/')    

    player_name = request.POST.get('add_player_name', '')
    url  = request.POST.get('add_song_url', '')
    name = request.POST.get('add_song_name', '')
    share= request.POST.get('add_song_share', '')        
    if player_name == '':
        err_msg = 'please input player name!'
        return singervote_admin_redirect(err_msg)

    if share == 'yes':
        share_flag = 1 
    else:
        share_flag = 0 

    q = vote_rank(player=player_name, name=name, url=url, score=0, del_flag=0, share_flag=share_flag)
    q.save()

    err_msg = 'Operation successfully!' 
    return singervote_admin_redirect(err_msg)


def singervote_player_del(request, player_id):
    if singervote_admin_validate(request) == False:    
        return HttpResponseRedirect('/login/')    

    singervote_admin_validate(request)    
    del_id = int(player_id)
    q = vote_rank.objects.filter(id=del_id)
    if q:
        for it in q:
            it.del_flag = 1
            it.save()
    return singervote_admin_redirect('') 
       
 
def singervote_get_anynomous():
    q = vote_admin.objects.all()
    if q:
        for it in q:
            return it.anynomous
    return 1
    

def singervote_admin_redirect(err_msg):
    list_list = []
    anynomous = 1
    ranksort  = 0
    q = vote_admin.objects.all()
    if q:
        for it in q:
            anynomous = it.anynomous
            ranksort  = it.ranksort
            enablevote= it.enablevote
    
    q = vote_rank.objects.filter(del_flag=0).order_by('-score')                
    if q:
        for it in q:
            if it.share_flag == 1:
                share = 'YES'
            else:
                share = 'NO'
            list_list.append([it.id, it.player, it.score, it.name, it.url, share])    

    list_dic = {"list_list":list_list, 'err_msg':err_msg, 'anynomous':anynomous, 'ranksort':ranksort, 'enablevote':enablevote}
    return render_to_response('singervote_admin.html', list_dic)


def singervote_admin_proc(request):
    if singervote_admin_validate(request) == False:    
        return HttpResponseRedirect('/login/')    

    ip = request.META['REMOTE_ADDR']
    isNotFirst = request.POST.get("isNotFirst", '')
    if isNotFirst != '1':
        return singervote_admin_redirect('')
    return singervote_admin_redirect('')


def singervote_user_validate(username):
    if username.lower() == 'admin_martin':
        return True
    f = open('/home/qingbo_gao/martin/mysite/worldcup/app_singervote/views/user.conf', 'r')
    c = f.read()
    user_list = c.split('\n')
    f.close()
    if username.lower() in user_list:
        return True
    return False 

def douban_shanghai_rent():
    rent_info = []
    with open("/home/qingbo_gao/martin/scrapy/project/douban_rent/douban_data_utf8.json") as f:
        for line in f.readlines():
            j = json.loads(line)   
            rent_info.append([j['title'], j['link'], j['desc']])
    
    return rent_info


def singervote_user_redirect(response_msg, err_msg, result, share):
    list_list = []
    feed    = 'False'
    r       = 'False'
    enter   = 7 
    counter = 0

    anynomous = 1
    ranksort  = 0
    q = vote_admin.objects.all()
    if q:
        for it in q:
            anynomous = it.anynomous
            ranksort  = it.ranksort
            enablevote= it.enablevote

    if ranksort == 0:   
        q = vote_rank.objects.filter(del_flag=0, share_flag=share).order_by('id')
    else:
        q = vote_rank.objects.filter(del_flag=0, share_flag=share).order_by('-score')
    
    if q:
        for it in q:
            if result:
                if str(it.id) in result:
                    r = 'True'
                else:
                    r = 'False'
            url = it.url
            prefix = url[0:7]
            if prefix.lower() == 'http://':
                url = url[7:]
            if not url.startswith('www.'):
                url = 'www.'+url
            list_list.append([it.player, it.id, r, it.score, it.name, url, it.play_time, feed])
            counter += 1
            if counter % 6 == 0:
                feed = 'True'
            else:
                feed = 'False'
  
    tt = vote_display.objects.filter(share_flag=share).count()
    
    rent_info = douban_shanghai_rent() 
 
    list_dic = {'list_list':list_list, 'response_msg':response_msg, 'err_msg':err_msg, 'anynomous':anynomous, 'enablevote':enablevote, 'tt':tt, 'rent_info':rent_info} 
    if share == 0:
        return render_to_response('singervote_display.html', list_dic)
    else:
        return render_to_response('singervote_share.html', list_dic)

def singervote_share(request):
    return singervote_display(request,1)    

def singervote_race(request):
    return singervote_display(request,0)

def singervote_display(request, share):
 
    isNotFirst = request.POST.get("isNotFirst", '')
    username   = request.POST.get("username", '')
    admin_key  = request.POST.get("admin_key", '')
    result     = request.POST.getlist('player_id', '')
 
    if isNotFirst == '':
        return singervote_user_redirect('', '', '', share) 

    isAdmin = 0
    err_msg = '' 
    if isNotFirst == '1':
        if username == '':
            err_msg = 'Failed!!!  Please input your SonicWall English Name Firstly!(For example: Tom)'
            return singervote_user_redirect('', err_msg, result, share)

    if isNotFirst == '1' and username != '':
        if singervote_user_validate(username) == False:
            err_msg = 'Your name is invalide, please check it......'
            return singervote_user_redirect('', err_msg, result, share)

    if not result:
        err_msg = 'Please chose at least 1 player!'
        return singervote_user_redirect('', err_msg, result, share)

    if len(result) > 10:
        err_msg = "You couldn't vote exceed 10 palyers!"
        return singervote_user_redirect('', err_msg, result, share)

    q = vote_display.objects.filter(user=username, share_flag=share)
    if q:
        err_msg = "You already voted....."
        return singervote_user_redirect('', err_msg, result, share)
    else:
        vote = ''
        ip = request.META['REMOTE_ADDR']
        for it in result:
            vote += it
            vote += ','
        q = vote_display(user=username, vote=vote, ip=ip, share_flag=share)
        q.save()

    list_list = []
    response_msg  = "Your choice is : "
  
    for item in result:
        q = vote_rank.objects.filter(id=item)
        if q:
            for it in q:
                it.score += 1
                response_msg += it.name+', '
                it.save()
        else:
            err_msg = 'The player you chose is invalid!'
 
    return singervote_user_redirect(response_msg, err_msg, result, share)



