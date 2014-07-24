# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from app_dbop.models import vote_display, vote_rank, vote_admin
from wcproc import *
import os,re,datetime

def singervote_play(reqeust, player_id):
    q = vote_rank.objects.filter(id=player_id)
    anynomous = singervote_get_anynomous()
    list_dic = {}
    if q:
        for it in q:
            url = it.url
            name= it.name
            player = it.player
            list_dic = {'player':it.player, 'song_name':it.name, 'anynomous':anynomous}
    return render_to_response('singervote_play.html', list_dic)


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

def singervote_player_add(request):
    player_name = request.POST.get('add_player_name', '')
    url  = request.POST.get('add_song_url', '')
    name = request.POST.get('add_song_name', '')        
    if player_name == '':
        err_msg = 'please input player name!'
        return singervote_admin_redirect(err_msg)

    q = vote_rank.objects.filter(player=player_name, del_flag=0)
    if q:
        err_msg = 'The player existed already!'
        return singervote_admin_redirect(err_msg)
    else:
        q = vote_rank(player=player_name, name=name, url=url, score=0, del_flag=0)
        q.save()

    err_msg = 'Operation successfully!' 
    return singervote_admin_redirect(err_msg)

def singervote_player_del(request, player_id):
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
    anynomous = singervote_get_anynomous()
    q = vote_rank.objects.filter(del_flag=0).order_by('-score')                
    if q:
        for it in q:
            list_list.append([it.id, it.player, it.score, it.name, it.url])    

    list_dic = {"list_list":list_list, 'err_msg':err_msg, 'anynomous':anynomous}
    return render_to_response('singervote_admin.html', list_dic)


def singervote_admin_proc(request):
    isNotFirst = request.POST.get("isNotFirst", '')
    password = request.POST.get("password", '')

    if isNotFirst != '1':
        return singervote_admin_redirect('')
    if password != '9527':
        err_msg = 'The password is incorrect!'
        return singervote_admin_redirect(err_msg)

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

def singervote_user_redirect(response_msg, err_msg, result):
    list_list = []
    feed    = 'False'
    r       = 'False' 
    counter = 0

    q = vote_rank.objects.filter(del_flag=0).order_by('id')
    if q:
        for it in q:
            if result:
                if it.id in result:
                    r = 'True'
                else:
                    r = 'False'
            url = it.url
            prefix = url[0:7]
            if prefix.lower() == 'http://':
                url = url[7:]
            if not url.startswith('www.'):
                url = 'www.'+url
            list_list.append([it.player, it.id, r, it.score, it.name, url, feed])
            counter += 1
            if counter % 7 == 0:
                feed = 'True'
            else:
                feed = 'False'
    
    anynomous = 1
    q = vote_admin.objects.all()
    if q:
        for it in q:
            anynomous = it.anynomous
    
    list_dic = {'list_list':list_list, 'response_msg':response_msg, 'err_msg':err_msg, 'anynomous':anynomous} 
    return render_to_response('singervote_display.html', list_dic)
 

def singervote_display(request):
 
    isNotFirst = request.POST.get("isNotFirst", '')
    username   = request.POST.get("username", '')
    admin_key  = request.POST.get("admin_key", '')
    result     = request.POST.getlist('player_id', '')

    if isNotFirst == '':
        return singervote_user_redirect('', '', '') 

    isAdmin = 0
    err_msg = '' 
    if isNotFirst == '1':
        if username == '':
            err_msg = 'Failed!!!  Please input your SonicWall English Name Firstly!(For example: Tom)'
            return singervote_user_redirect('', err_msg, result)

    if isNotFirst == '1' and username != '':
        if singervote_user_validate(username) == False:
            err_msg = 'Your name is invalide, please check it......'
            return singervote_user_redirect('', err_msg, result)

    if not result:
        err_msg = 'Please chose at least 1 player!'
        return singervote_user_redirect('', err_msg, result)

    if len(result) > 5:
        err_msg = "You couldn't vote exceed 5 palyers!"
        return singervote_user_redirect('', err_msg, result)

    q = vote_display.objects.filter(user=username)
    if q:
        err_msg = "You already voted....."
        return singervote_user_redirect('', err_msg, result)
    else:
        vote = ''
        for it in result:
            vote += it
            vote += ','
        q = vote_display(user=username, vote=vote)
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
 
    return singervote_user_redirect(response_msg, err_msg, result)



