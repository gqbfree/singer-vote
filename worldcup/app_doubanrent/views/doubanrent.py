# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
import os,re,datetime
import json

def doubanrent_read(pagenum):
    rent_info = []
    total     = pagenum * 10
    with open("/home/qingbo_gao/martin/scrapy/project/douban_rent/douban_data_utf8.json") as f:
        for line in f.readlines():
            j = json.loads(line)   
            rent_info.append([j['title'], j['link'], j['desc']])
            total -= 1
            if not total:
                break
    
    return rent_info


def doubanrent_redirect(response_msg, rent_info, page_num):
    rent_info = doubanrent_read(page_num)
    list_dict = {'rent_info':rent_info, 'response_msg':response_msg} 
    return render_to_response('doubanrent_display.html', list_dict)


def doubanrent_display(request):
    page     = request.POST.get("page", '')
    district = request.POST.get("district", '')

    response_msg = ''
    rent_info    = []
    page_num     = 0 

    if not page.isdigit():
        return doubanrent_redirect(response_msg, rent_info, 1)
    else:
        page_num = int(page)
    
    if page_num > 50:
        return doubanrent_redirect(response_msg, rent_info, 1)
 
    return doubanrent_redirect(response_msg, rent_info, page_num)



