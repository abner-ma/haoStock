#!/usr/bin/python
#-*-coding:UTF-8-*-

import os
import sys
import smtplib
import mimetypes

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.text import MIMEText
from email.header import Header
from email import encoders

class MYSendMail(object):
    def __init__(self):
        self.set_smtp_type()
        self.set_charset()
        self.mail_from = None
        self.sendto_list = []
        self.mailto_list = []
        self.cc_list = []
        self.bcc_list = []
        self.attachment_list = []
        self.attachment_num = 0

    def set_smtp_type(self,mail_type='plain'):
        self.mail_type = mail_type

    def set_charset(self,charset='utf-8'):
        self.charset = charset

    def set_smtp_server(self,server,port,user_name,user_pw,time_out=600,try_time=3):
        self.smtp_server = server
        self.smtp_port = port
        self.smtp_user = user_name
        self.smtp_pw = user_pw
        self.time_out = time_out
        self.try_time = try_time
        if self.mail_from == None:
            self.mail_from = self.smtp_user

    def set_subject(self,subject):
        self.subject = subject

    def set_content(self,content):
        self.content = content

    def set_mailfrom(self,mail_from):
        self.mail_from = mail_from

    def add_mail_to(self,mail_to):
        self.sendto_list.append(mail_to)
        self.mailto_list.append(mail_to)

    def add_cc_to(self,cc_to):
        self.sendto_list.append(cc_to)
        self.cc_list.append(cc_to)

    def add_bcc_to(self,bcc_to):
        self.sendto_list.append(bcc_to)
        self.bcc_list.append(bcc_to)

    def add_attachment(self,filepath,filename=None):
        if filename == None:
            filename = os.path.basename(filepath)
        with open(filepath,'rb') as f:
            file=f.read()

        ctype,encoding = mimetypes.guess_type(filepath)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split('/', 1)
        if maintype == "text":
            with open(filepath) as f:file=f.read()
            attachment = MIMEText(file, _subtype=subtype)
        elif maintype == "image":
            with open(filepath,'rb') as f:file=f.read()
            attachment = MIMEImage(file, _subtype=subtype)
        elif maintype == "audio":
            with open(filepath,'rb') as f:file=f.read()
            attachment = MIMEAudio(file, _subtype=subtype)
        else:
            with open(filepath,'rb') as f:file=f.read()
            attachment = MIMEBase(maintype,subtype)
            attachment.set_payload(file)
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
            encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        attachment.add_header('Content-ID',str(self.attachment_num))
        self.attachment_num +=1
        self.attachment_list.append(attachment)

    def send_mail(self):
        if len(self.attachment_list) == 0:
            self.msg = MIMEText(self.content,self.mail_type,self.charset)
        else:
            self.msg = MIMEMultipart()
            self.msg.attach(MIMEText(self.content,self.mail_type,self.charset))
            for attachment in self.attachment_list:
                self.msg.attach(attachment)

        self.msg['Subject'] = self.subject
        self.msg['From'] = self.mail_from
        self.msg['To'] = ",".join(self.mailto_list)
        if self.cc_list:
            self.msg['cc'] = ",".join(self.cc_list)
        if self.bcc_list:
            self.msg['bcc'] = ",".join(self.bcc_list)

        for a in range(self.try_time):
            try:
                if self.smtp_port == 25:
                    server = smtplib.SMTP(self.smtp_server, self.smtp_port,timeout=self.time_out)
                else:
                    server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port,timeout=self.time_out)
                #server.set_debuglevel(1)
                server.login(self.smtp_user,self.smtp_pw)
                server.sendmail(self.mail_from,self.sendto_list,self.msg.as_string())
                server.quit()
                break
            except Exception as e:
                print(e)

