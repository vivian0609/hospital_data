#coding:utf-8
import pandas as pd
import numpy as np
import openpyxl
import datetime
# 导入相关库-email
from email.mime.multipart import MIMEMultipart  # 构建邮件头信息，包括发件人，接收人，标题等
from email.mime.text import MIMEText  # 构建邮件正文，可以是text，也可以是HTML
from email.mime.application import MIMEApplication  # 构建邮件附件，理论上，只要是文件即可，一般是图片，Excel表格，word文件等
from email.header import Header  # 专门构建邮件标题的，这样做，可以支持标题中文
from email import encoders
from email.mime.base import MIMEBase
import smtplib
import sys
import traceback
import streamlit as st
import mimetypes

class QQSendEmail(object):
	def __init__(self,my_file_from,my_file_to,my_email_Subject,my_email_text,my_receiver,my_annex_path1,my_annex_name1):
		self.my_file_from = my_file_from
		self.my_file_to = my_file_to
		self.my_email_Subject = my_email_Subject
		self.my_email_text = my_email_text
		self.my_receiver = my_receiver
		self.my_annex_path1 = my_annex_path1
		self.my_annex_name1 = my_annex_name1
	
	# 创建email
	def create_email(self,eamil_from,email_to,email_subject,email_text,annex_path1,annex_name1): 
		# 生成一个空的带附件的邮件实例
		message=MIMEMultipart()                                      
	
		# 将正文以文本的形式插入到邮件中
		message.attach(MIMEText(email_text,"plain","utf-8"))        
		message["from"]=Header(eamil_from,"utf-8")                  #生成发件人名称
		message["to"]=Header(email_to,"utf-8")            #生成收件人名称
		message["Subject"]=Header(email_subject,"utf-8")            #生成邮件主题
		
		if annex_path1 != '':
			# # 构造附件1，测试成功，附件有很多类型，现在构建的是xlsx文件
			# attach_table = MIMEApplication(open(annex_path1, 'rb').read())
			# # 给附件1增加标题
			# attach_table.add_header('Content-Disposition', 'attachment',filename=annex_name1)
			# # 这样的话，附件1名称就可以是中文的了，不会出现乱码
			# attach_table.set_charset('utf-8')
			# # 绑定附件1
			# message.attach(attach_table)

			# 构造附件，现在构建的是zip文件
			data = open(annex_path1, 'rb')
			ctype, encoding = mimetypes.guess_type(annex_path1)
			if ctype is None or encoding is not None:
			    ctype = 'application/octet-stream'
			maintype, subtype = ctype.split('/', 1)
			file_msg = MIMEBase(maintype, subtype)
			file_msg.set_payload(data.read())
			data.close()
			encoders.encode_base64(file_msg)  # 把附件编码
			file_msg.add_header('Content-Disposition', 'attachment', filename=annex_name1)  # 修改邮件头
			# 这样的话，附件1名称就可以是中文的了，不会出现乱码
			file_msg.set_charset('utf-8')
			message.attach(file_msg) # 绑定附件1
		
		return message
	
	# 发送email
	def send_email(self,sender,password,receiver,msg):
		
		#try:
		server=smtplib.SMTP_SSL("smtp.qq.com".encode(),465) # 找到发送邮箱的服务器地址
		server.ehlo()
		server.login(sender,password) # 登录我的邮箱
		
		# server.sendmail(sender,receiver,msg.as_string()) # 发送邮件，发件人和收件人的账号以及邮件内容
		# 使用send_message方法而不是sendmail,避免编码问题
		server.send_message(from_addr = sender, to_addrs = receiver, msg = msg)
		
		st.success(f'成功！！！已邮件发送，请及时查收！！！感谢使用。发送时间为：{datetime.datetime.now()}')
		# 关闭连接
		server.quit()
		
		# except Exception:
		# 	st.error(traceback.print_exc())
		# 	st.error("发送失败")
	
	def final_send(self,my_sender,my_password):

		st.write('请耐心等待...')
		my_msg = self.create_email(self.my_file_from,self.my_file_to,self.my_email_Subject,self.my_email_text,self.my_annex_path1,self.my_annex_name1) #传参
		my_receiver = self.my_receiver.split(',')
		
		self.send_email(my_sender,my_password,my_receiver,my_msg)
 