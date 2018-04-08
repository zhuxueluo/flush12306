#-*- coding:utf-8 -*-
import urllib2
import json
import sys
def remind_wechat():
    #wechat test account
    username= 'wx41dd45a9fd10a591'
    passkey= 'bfb46a29cd90f868b6688a9a6100a7c2'
    tokenurl="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (username,passkey)
    result=urllib2.urlopen(urllib2.Request(tokenurl)).read()
    print 'token_result',result
    dict_result = json.loads(result)
    Gtoken=dict_result['access_token']
    #Gtoken = "8_ZqN-MtHD6wnVWZTvL0slM0tSJEHAhrChgkHWL9Ecq2U38F1s6mqsINGatGyRGPuyp77VlCv2FTpzvRFAEKWqwCIOxfBDlfd9y35SdOGO5qX51UYrKYwka0qL28wXOUiAJAOFL"

    PURL="https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % Gtoken

    #生成post请求信息
    post_data = {}
    msg_content = {}
    msg_content['content'] = 'Leo, flushed successfully!'
    post_data['touser'] = 'oPsva0RsGIcN37ksaR2u4zWT-MC0'
    post_data['msgtype'] = 'text'
    post_data['text'] = msg_content
    post_data['safe'] = '0'
    #json_post_data = json.dumps(post_data,False,False)
    json_post_data='''{
        "text": {
            "content": "Leo, flushed successfully!"
        }, 
        "touser": "oPsva0RsGIcN37ksaR2u4zWT-MC0", 
        "msgtype": "text", 
        "safe": "0"
    }'''
    #通过urllib2.urlopen()方法发送post请求
    request_post = urllib2.urlopen(PURL, json_post_data)
    #read()方法查看请求的返回结果
    print request_post.read()