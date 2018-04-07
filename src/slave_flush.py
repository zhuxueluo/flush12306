# -*- coding: utf-8 -*-
def slave_flush(req):
    import selenium
    import time
    from selenium import webdriver
    cookies_obj = read_cookie()
    if not cookies_obj:
        print 'no cookies loaded'
        return
    
    
    dr = webdriver.Chrome()
    url='https://kyfw.12306.cn/otn/leftTicket/init'
    dr.get(url)
    dr.delete_all_cookies()
    for cookie in cookies_obj:
        dr.add_cookie(cookie)
    import main_flush
    main_flush.flush_after_login(dr,req)
    
def read_cookie():
    import json
    cookiesfile = open('cookies.dat')
    cookies_json = cookiesfile.read()
    cookies_obj = json.loads(cookies_json)
    return cookies_obj
    
