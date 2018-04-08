# -*- coding: utf-8 -*-
import selenium
import time
from selenium import webdriver
import sys

import beepalarm
from beepalarm import alarm_fourbeep
from beepalarm import alarm_twobeep
'''config tickets set to auto'''
def busy_find_first_element(dr,xpath):
    first = None
    '''about 6s if round=200'''
    tries=200
    round = 0
    while True:
        round=round+1
        if(round>=tries):
            print 'Refresh page manually: tried too many times to',xpath
            alarm_twobeep(1)
            round = 0
        elements = dr.find_elements_by_xpath(xpath)
        if(len(elements)>0):
            first = elements[0]
            break
    return first
    
    
    
def refresh_page(dr):
    myprofile_xpath = '//*[@id="login_user"]';
    myprofile_btn = busy_find_first_element(dr,myprofile_xpath)
    busy_click(myprofile_btn)
    time.sleep(1)
    bookpage_xpath = '//*[@id="selectYuding"]/a'
    bookpage_btn = busy_find_first_element(dr,bookpage_xpath)
    busy_click(bookpage_btn)
    time.sleep(1)
    
def final_check_passanger():
    print 'final check needs to be done in future version'
    

def get_ticket_id_map(dr,train_num_arr):
    result = {}
    tr_arr = dr.find_elements_by_xpath('//div[@id="t-list"]/table/tbody/tr')
    for train_num in train_num_arr:
        print 'find ticket id of',train_num
        ticket_id = None
        for tr in tr_arr:
            anchor_arr = tr.find_elements_by_xpath('./td/div/div/div/a')
            if len(anchor_arr)>0 and anchor_arr[0].text == train_num:
                ticket_id = tr.get_attribute('id')[7:]
                break
        if ticket_id != None:
            result[train_num] = ticket_id
    return result
    
def busy_click(btn):
    import selenium.common.exceptions
    from selenium.common.exceptions  import WebDriverException
    click_finished = False
    while not click_finished:
        try:
            btn.click()
            click_finished = True
        except WebDriverException as e:
            print 'go on click',e

def start_slave(req):
    from multiprocessing import Process
    import slave_flush
    
    slave_process = Process(target=slave_flush.slave_flush,args=(req,))
    slave_process.start()
        

def flush_after_login(dr, req):
    booktickets = busy_find_first_element(dr,'//*[@id="selectYuding"]/a')
    booktickets.click()
    
    

    #print '2. input from, to and date on page'
    fromstation = dr.find_element_by_id('fromStationText')
    #dr.execute_script("arguments[0].value=arguments[1];", fromstation,req['from'])
    fromstation.clear()
    fromstation.click()
    fromstation.send_keys(req['from'])

    floataddr = dr.find_element_by_id('citem_0')
    floataddr.click()
    time.sleep(0.5)
    
    
    tostation = dr.find_element_by_id('toStationText')
    #dr.execute_script("arguments[0].value=arguments[1];", tostation,req['to'])
    tostation.clear()
    tostation.click()#'''must click'''
    tostation.send_keys(req['to'])
    
    floataddr2 = dr.find_element_by_id('citem_0')
    floataddr2.click()
    time.sleep(0.5)
    
    train_date = dr.find_element_by_id('train_date')
    dr.execute_script("arguments[0].value=arguments[1];", train_date,'2018-05-01')
    #train_date.clear()
    #train_date.send_keys(req['date'])
    #time.sleep(0.5)
    
    '''print '3. input \'go\' in console'
    while True:
        cmd= raw_input('ready to go?')
        if cmd=='g' or cmd=='G':
            print 'don\'t interference with the page'
            break'''
    req['ticket_id'] = {}
    while req['ticket_id'] == {}:
        searchbtn=busy_find_first_element(dr,'//*[@id="query_ticket"]')
        busy_click(searchbtn)
        #init train ticket id        
        print 'get_ticket_id_map',req['train_num_arr']
        ticket_id_map = get_ticket_id_map(dr, req['train_num_arr'])
        req['ticket_id'] = ticket_id_map
        print 'req',req

    
    round=0
    bookbtn = None
    hitonce = False
    while True:
        round = round+1
        if round%100 == 0:
            refresh_page(dr)
        print round
        searchbtn=busy_find_first_element(dr,'//*[@id="query_ticket"]')
        loaded_new=False
        while not loaded_new:
            busy_click(searchbtn)
            tabrow = dr.find_elements_by_xpath('//div[@id="t-list"]/table/tbody/tr')
            if len(tabrow) > 0:
                loaded_new=True
        

        ticket_id = req['ticket_id']
        for key in ticket_id:
            tr_g1935 = busy_find_first_element(dr,'//*[@id="ticket_'+ticket_id[key]+'"]')
            g1935 = busy_find_first_element(tr_g1935,'//*[@id="' + req['seat_level_prefix']+ ticket_id[key] + '"]')
            if g1935.text!=u'\u65e0':
                print '============================================================='+key
                bookbtn = busy_find_first_element(tr_g1935,'./td[13]/a')
                hitonce = True
                break
        if hitonce:
            break
    '''book'''
    if bookbtn!= None:
        
        bookbtn.click()
        passenger = busy_find_first_element(dr,'//*[@id="normalPassenger_0"]')
        passenger.click()
        passname = busy_find_first_element(dr,'//*[@id="passenger_name_1"]')
        if passname.get_attribute('value')== u'\u6797\u78ca':
            submit = busy_find_first_element(dr,'//*[@id="submitOrder_id"]')
            submit.click()
            final_check_passanger()
            real_submit = busy_find_first_element(dr,'//*[@id="qr_submit_id"]')
            busy_click(real_submit)
        print 'got time:', time.ctime()
        alarm_fourbeep(4)
        import remind_wechat
        remind_wechat.remind_wechat()
        while True:
            cmd= raw_input('[e]xit? ')
            if cmd=='e' or cmd=='E':
                break
def dump_cookies(webdriver):
    cookies_obj = webdriver.get_cookies()
    import json
    cookies_json = json.dumps(cookies_obj)
    cookies_file = open('cookies.dat','w')
    cookies_file.write(cookies_json)
    cookies_file.close()
if __name__ == "__main__":
    concurrent = 0
    if len(sys.argv) == 2:
        concurrent = int(sys.argv[1])
        print 'will start 1 master and',concurrent,'slaves'
    import require_config
    req = require_config.req
    
    starttime = time.ctime()
    dr  = webdriver.Chrome()
    dr.maximize_window()
    url='https://kyfw.12306.cn/otn/leftTicket/init'
    dr.get(url)


    loginbtn = busy_find_first_element(dr,'//*[@id="login_user"]')
    loginbtn.click()

    username = busy_find_first_element(dr,'//*[@id="username"]')
    username.send_keys(require_config.username)
    password = busy_find_first_element(dr,'//*[@id="password"]')
    password.send_keys(require_config.password)


    print 'login(just click the capcha and login button)'

    while True:
        login_user = dr.find_element_by_id('login_user')
        if login_user.text ==u'\u767b\u5f55':
            print 'please login'
            time.sleep(0.5)
        else:
            break
        
        
        
    dump_cookies(dr)
    for i in range(concurrent):
        start_slave(req)
    flush_after_login(dr,req)


        
        
        
        
        
        




'''start check bill
busy_find_first_element
//*[@id="ticket_4f000G193807"]/td[13]/a
//*[@id="ZE_4f0000D3080H"]

def bookticket(elements):'''
    


    
    