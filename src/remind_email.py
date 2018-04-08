#-*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import json

def remind_mail():
    #mail_host="smtp.163.com"
    mail_host="smtp.126.com"

    mail_user='xxxx'
    mail_pass='xxxx'
    mail_host='xxxx'

    sender = 'xxxx@xxxx'
    receivers = ['yyyy@yyyy']


    mail_msg = u"""
    Hi, flushed ticket. Hurry to pay it.
    """
    message = MIMEText(mail_msg, 'plain', 'utf-8')
    message['From'] = Header(u"just_claim_who_write@xxxx", 'utf-8')
    # the From doesnot need to be the same as the sender(user who logins to smtp server)
    message['To'] =  Header(u"just_claim_who_sendto@yyyy", 'utf-8')
    message['Subject'] = Header(u'Flush 12306 successfully', 'utf-8')


    smtpObj = smtplib.SMTP_SSL() 
    smtpObj.connect(mail_host, 465)
    smtpObj.login(mail_user,mail_pass)  
    smtpObj.sendmail(sender, receivers, message.as_string())