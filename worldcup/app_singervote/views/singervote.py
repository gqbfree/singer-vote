from django.shortcuts import render_to_response
from app_dbop.models import vote_display, vote_rank
from wcproc import *
import os,re,datetime


player_list = ['Tom', 'jack', 'mike', 'jerry', 'joy', 'eric']
player_score = {'Tom':0, 'jack':0, 'mike':0, 'jerry':0, 'joy':0, 'eric':0}

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

def singervote_redirect(response_msg, err_msg, result):
    list_list = []
    feed    = 'False'
    r       = 'False' 
    counter = 0
    for item in player_list:
        q = vote_rank.objects.filter(player=item)
        if q:
            for it in q:
                player_score[item] = it.score

        if result:
            if item in result:
                r = 'True'
            else:
                r = 'False'
        list_list.append([item, r, player_score[item], feed])
        counter += 1
        if counter % 4 == 0:
            feed = 'True'
        else:
            feed = 'False'

    list_dic = {'list_list':list_list, 'response_msg':response_msg, 'err_msg':err_msg} 
    return render_to_response('singervote_display.html', list_dic)
 

def singervote_display(request):
 
    isNotFirst = request.POST.get("isNotFirst", '')
    username   = request.POST.get("username", '')
    admin_key  = request.POST.get("admin_key", '')
    result     = request.POST.getlist('player', '')


    if isNotFirst == '':
        return singervote_redirect('', '', '') 

    isAdmin = 0
    err_msg = '' 
    if isNotFirst == '1':
        if username == '':
            err_msg = 'Failed!!!  Please input your SonicWall English Name Firstly!(For example: Tom)'
            return singervote_redirect('', err_msg, result)

    if isNotFirst == '1' and username != '':
        if singervote_user_validate(username) == False:
            err_msg = 'Your name is invalide, please check it......'
            return singervote_redirect('', err_msg, result)

    if not result:
        err_msg = 'Please chose at least 1 player!'
        return singervote_redirect('', err_msg, result)

    if len(result) > 5:
        err_msg = "You couldn't vote exceed 5 palyers!"
        return singervote_redirect('', err_msg, result)

    q = vote_display.objects.filter(user=username)
    if q:
        err_msg = "You already voted....."
        return singervote_redirect('', err_msg, result)
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
        response_msg += item+', '
        q = vote_rank.objects.filter(player=item)
        if q:
            for it in q:
                it.score += 1
                it.save()
        else:
            g = vote_rank(player=item, score=1)
            g.save()
   
 
    print player_score
    return singervote_redirect(response_msg, err_msg, result)



