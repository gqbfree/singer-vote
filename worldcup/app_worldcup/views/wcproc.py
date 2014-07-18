from django.shortcuts import render_to_response
from app_dbop.models import Guess, Score, vote_display, vote_rank
import os,re,datetime

def worldcup_login(request):
    now = datetime.datetime.now()
    worldcup_rank_list()
    return render_to_response('worldcup_login.html', {'current_date' : now} )

def worldcup_score_collect():
    f = open('/home/qingbo_gao/martin/mysite/worldcup/app_worldcup/views/user.conf', 'r')
    c = f.read()
    user_list = c.split('\n')
    f.close()

    for it in user_list:
        q = Guess.objects.filter(user=it)
        if q:
            score = 0
            for it2 in q:
                score += int(it2.score)
            fp = Score(user=it2.user, score=score)
            fp.save()    

def worldcup_score_calc(radio_name, result):
    radio_name.strip()
    q = Guess.objects.filter(match=radio_name, result=result)
    if q:
        for it in q:
            it.score = 1
            it.save()


def worldcup_rank_list():
    list_rank = []
    list_item = []
    q = Score.objects.all().order_by('-score')
    if q:
        for it1 in q:
            list_item = [it1.user, it1.score]
            list_rank.append(list_item)
    return list_rank

def worldcup_user_validate(username):
    if username.lower() == 'admin_martin':
        return True
    f = open('/home/qingbo_gao/martin/mysite/worldcup/app_worldcup/views/user.conf', 'r')
    c = f.read()
    user_list = c.split('\n')
    f.close()
    if username.lower() in user_list:
        return True
    return False 
     

def worldcup_history(request, para):
    user = para.lower()
    if worldcup_user_validate(user) == False:
        err_msg = "Invalid user!"    
        return render_to_response('worldcup_history.html', {'err_msg':err_msg})
    
    list_list = []
    counter = 0
    feed = 'false'
    q = Guess.objects.filter(user=user)
    if q:
        for it in q:
            if counter != 0 and counter % 4 == 0:
                feed = 'True'
            else:
                feed = 'False'
            counter += 1

            contry = it.match.split('-')
            l = ['', 'win', 'draw', 'lose']
            list_list.append([contry[0], contry[1], it.match, l[it.result], feed])

    list_dic = {"list_list":list_list, "username":user}

    return render_to_response('worldcup_history.html', list_dic)


def worldcup_guess(request):
   
    isNotFirst = request.POST.get("isNotFirst", '')
    username   = request.POST.get("username", '')
    admin_key  = request.POST.get("admin_key", '')

    isAdmin = 0

    err_msg = '' 
    if isNotFirst == '1':
        if username == '':
            response_msg = ''
            err_msg = 'Failed!!!  Please input your SonicWall English Name Firstly!(For example: Tom)'

    if isNotFirst == '1' and username != '':
        if worldcup_user_validate(username) == False:
            err_msg = 'Your name is invalide, please check it......'

    if admin_key == 'ok' and username == 'admin_martin':
        isAdmin = 1
    elif admin_key == '' and username == 'admin_martin':
        isAdmin = 2
    else:
        isAdmin = 3

    now = datetime.datetime.now()
    if isAdmin == 2 or isAdmin == 1:
        now = now - datetime.timedelta(days=1)
    str_date = now.strftime('%Y-%m-%d')
    str_date = str_date[0:10]

    if isAdmin == 3:
        str_expired = now.strftime('%H') 
        int_expired = int(str_expired)
        if int_expired < 8 or int_expired >= 21:
            list_dic = {"expired":"1"}
            return render_to_response('worldcup_guess.html', list_dic) 

 
    file_conf =  open('/home/qingbo_gao/martin/mysite/worldcup/app_worldcup/views/match.conf', 'r')
    file_str  =  file_conf.read()
    file_conf.close()

    file_contry = re.findall(r'^'+str_date+':(.*)', file_str, re.M)
   
         
    aa = file_contry[0]
    
    if aa == '':
        aa = ('','')
    list_contry = aa.split(',')
    
    list_list = []
    response_msg  = "Your choice is ----- "
    counter = 0
    feed = 'false'
    for item in list_contry:
        contry = item.split('-')
        radio_name = item 
        result = request.POST.get(radio_name, '')

        if counter != 0 and counter % 4 == 0:
            feed = 'True'
        else:
            feed = 'False' 
        counter += 1

        list_list.append([contry[0], contry[1], radio_name, result, feed])
        response_msg += contry[0]+":"+result+"...."

        if err_msg == '' and result != '':
            r_dic = {"win":1, "draw":2, "lose":3}
            r = r_dic[result]
            if isAdmin == 1:
                worldcup_score_calc(radio_name, r)
                worldcup_score_collect() 
            elif isAdmin == 3:
                g1 = Guess(user=username, match=radio_name, result=r, primarykey=username+'+'+radio_name)
                g1.save()

    if err_msg != '' or isNotFirst != '1':
        response_msg = ''

    worldcup_score_collect()

    list_rank = worldcup_rank_list()
    list_dic = {"list_list":list_list, "response_msg":response_msg, "err_msg":err_msg, "username":username, "list_rank":list_rank}
   
    if isAdmin == 2:
        list_dic["admin"]="1"

    if isAdmin == 1:
        list_dic = {}
 
    return render_to_response('worldcup_guess.html', list_dic)


