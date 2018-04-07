# -*- coding: utf-8 -*-
'''flush requirements'''
#login info username
username = ''
#login info password
password = ''



req = {}

#start station
req['from']=u'\u5f90\u5dde'

#destination station
req['to']=u'\u82cf\u5dde'

#onboard date
req['date']='2018-05-01'

#possible train number
train_num_arr=['G1935','G1973','G455','G1235','G1231','G169']

#二等座：ZE_
seat_level_prefix='ZE_'

#set passenger name in chinese character
parr=[u'张三']
req['passengers']=parr