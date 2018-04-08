#-*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import json

def remind_email():
    mail_user='xxxx'
    mail_pass='xxxx'
    mail_host="xxxx"

    sender = 'realsender@smtpserver'
    receivers = ['realreceiver@anothersmtpserver']


    mail_msg = u"""
    Hi, flushed ticket. Hurry to pay it.
    """
    message = MIMEText(mail_msg, 'plain', 'utf-8')
    message['From'] = Header(u"claimed_sender_in_mail_content@claimedserver", 'utf-8')
    # the From doesnot need to be the same as the sender(user who logins to smtp server)
    message['To'] =  Header(u"claimed_receiver_in_mail_content@claimedserver2", 'utf-8')
    message['Subject'] = Header(u'Flush 12306 successfully', 'utf-8')


    smtpObj = smtplib.SMTP_SSL() 
    smtpObj.connect(mail_host, 465)
    smtpObj.login(mail_user,mail_pass)  
    smtpObj.sendmail(sender, receivers, message.as_string())