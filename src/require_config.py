# -*- coding: utf-8 -*-
'''flush requirements'''
#login info username
username = ''
#login info password
password = ''



req = {}

#start station
req['from']=u'出发地'

#destination station
req['to']=u'目的地'

#onboard date
req['date']='2018-05-01'

#possible train number
train_num_arr=['G1935','G1973','G455','G1235','G1231','G169']
#train_num_arr=['G1935']
req['train_num_arr'] = train_num_arr
#二等座：ZE_
seat_level_prefix='ZE_'
req['seat_level_prefix'] = seat_level_prefix

#set passenger name in chinese character, for now support only one passenger
req['passengers']=u'张三'