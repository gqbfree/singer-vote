# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
import os,re,datetime
import json

def doubanrent_read(page_num):
    rent_info = []
    list_dict = {}
    per_page  = 20
    total_num = 1000
    total_page= 0
    start     = 0
    item_count= 0
#    with open("/home/qingbo_gao/martin/scrapy/project/douban_rent/douban_info_utf8.json") as f:
#        j = json.loads(f.readline())
#        if not j:
#            total_num = int("".join(j['total_num']))
#    print total_num

    total_page = total_num/per_page+ 1

    if page_num == 0 or total_page == 1:
        page_num = 1
    elif page_num > total_page:
        page_num = total_page

    start = (page_num - 1) * per_page + 1
    with open("/home/qingbo_gao/martin/scrapy/project/douban_rent/douban_data_utf8.json") as f:
        for line in f.readlines():
            j = json.loads(line) 
            item_count += 1  
            if item_count < start:
                continue
            elif item_count > start + per_page :
                break
            else:
                rent_info.append([j['title'], j['link'], j['desc']])

    list_dict = {'rent_info':rent_info, 'response_msg':'', 'page_num':page_num, 'page_prev':page_num-1, 'page_next':page_num+1} 
    return list_dict 


def doubanrent_redirect(response_msg, rent_info, page_num):
    list_dict = doubanrent_read(page_num)    
    return render_to_response('doubanrent_display.html', list_dict)


def doubanrent_display(request, page):
    response_msg = ''
    rent_info    = []
    page_num     = 0 

    district = request.POST.get("district", '')
    if not page.isdigit():
        return doubanrent_redirect(response_msg, rent_info, 1)
    else:
        page_num = int(page)
    
    if page_num > 50:
        return doubanrent_redirect(response_msg, rent_info, 1)
 
    return doubanrent_redirect(response_msg, rent_info, page_num)



