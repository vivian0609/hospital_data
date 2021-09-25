# cd到目标文件夹再运行，streamlit run vivian_app.py
# pipreqs ./ --encoding=utf8 获取所有依赖包信息
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import re
import os
import base64
import math
from QQSendEmail import *
from ZhihuSpider import *

######################################## 函数部分 ###########################################
# 登录模块
def user_login():
	""" ## 登录模块 """
	col1, col2 = st.columns(2)
	with col1:
		login_name = st.text_input('登录账号（微信昵称/简称，方便统计）')
	with col2:
		placeholder = st.empty()
		login_password = placeholder.text_input('登录密码','123456')
	
	# 判断登录者是否有权限、密码是否正确
	if login_name == '' or login_password == '':
		st.warning('请输入账号密码登录。')
		st.stop()
	elif len(login_name) < 3 or login_name == 'xxx':
		st.warning('所输字符少于3个，请完整输入你的微信名/简称，其中【xxx】形式无效')
		st.stop()
	elif login_password != '123456':
		st.warning('密码错误，请重新输入。若忘记密码，请联系管理员')
		st.stop()
	st.success('登入成功！！！欢迎使用')
	placeholder.empty() # 清空密码窗口
		
	return login_name

# 兴趣调研模块
def base_research():
	col1, col2, col3 = st.columns(3)
	with col1:
		job_type = st.radio("1、您是否从事数据or技术类工作？",('是', '否'))
	with col2:
		is_python = st.selectbox('2、您是否接触过 python？',('是', '否'))
	with col3:
		is_streamlit = '否'
		if st.checkbox('3、接触过 streamlit'):
			is_streamlit = '是'

	""" - 兴趣调研 """
	is_interest = st.multiselect(
		'4、您对以下哪方面内容感兴趣（多选）：',
		['全都感兴趣', 'python', 'streamlit', '知乎热门话题爬取', '邮件发送', '一点兴趣都没有'],
		['全都感兴趣'])
	is_interest = ','.join(is_interest)

	""" - 整体兴趣度 """
	interest_num = st.slider('5、整体的感兴趣程度是多少？（10分为非常感兴趣）', 0, 10, 5)

	return job_type,is_python,is_streamlit,is_interest,interest_num

# 添加外部链接
def show_external_link(link, title):
	href = f'<a href="{link}" title="{title}" target="_blank" rel="noopener noreferrer" data-za-not-track-link="true"><h2 class="HotItem-title">{title}</h2></a>'
	return href

# 文件下载
def get_binary_file_downloader_html(bin_file, file_label='File'):
	with open(bin_file, 'rb') as f:
		data = f.read()
	bin_str = base64.b64encode(data).decode()
	href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">点击下载（浏览器才有效） {file_label}</a>'
	return href

@st.cache
def convert_df(df):
	# Cache the conversion to prevent computation on every rerun
	return df.to_csv().encode('utf_8_sig')

######################################## 正文部分 ###########################################
st.title('欢迎体验！！！')
date_now = str(datetime.date.today())
time_now = str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
form_id = 0
login_name = user_login()

""" - 基础调研 -- 以3种形式表现——单选、列表选择框、复选框 """
job_type,is_python,is_streamlit,is_interest,interest_num = base_research()

"""-----------------------------------------------------"""
""" ## 获取当天知乎top5热门话题 """
if 'is_scraping' not in st.session_state:
	st.session_state.is_scraping = 0
is_zhihu = 0
if st.checkbox('体验【知乎top5热门话题】实时爬取'):
	is_zhihu = 1
	is_new_run = 0
	
	st.session_state.is_scraping += 1
	if st.session_state.is_scraping == 1:
		# 记录信息（只记录一次）
		f = "scrap_log.txt"
		with open(f, "a", encoding="utf-8") as file:   # "a"代表追加内容
			file.write(login_name+'|'+date_now+'|'+time_now+'|'+job_type+'|'+is_python+'|'+is_streamlit+'|'+is_interest+'|'+str(interest_num)+'|'+str(is_zhihu)+ " "+"\n")

	try:
		result = pd.read_csv('result.txt',sep=',')
		time_now = str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
		d1 = datetime.datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')
		d2 = datetime.datetime.strptime(result['get_time'][0], '%Y-%m-%d %H:%M:%S')
		delta = d1 - d2
	except:
		is_new_run = 1
	if is_new_run == 1 or delta.seconds > 3600:
		st.success('您满足实时爬取条件，以下将为你显示即时获取的知乎top5热门话题，点击链接可直接跳转查看')
		# 需修改【ZhihuSpider.py】文件下的cookie设置
		hot_zhihu = ZhihuSpider()
		response = hot_zhihu.web_link()
		count = 0
		result = pd.DataFrame()
		for hot_item in hot_zhihu.hot_items(response):
			temp = pd.DataFrame(hot_item,index = [0])
			temp['get_time'] = str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
			result = pd.concat([result,temp])
			count += 1
			if count > 4:
				break
		result.to_csv('result.txt')
		#result
	else:
		result = result
	for url,title in zip(result['url'],result['index'].astype(str)+'、'+result['title']):
		st.markdown(show_external_link(url, title),unsafe_allow_html=True)

	# 下载文件形式
	# text_tmp = f'【知乎top5热门话题结果表】'
	# st.markdown(get_binary_file_downloader_html('result.txt', text_tmp),unsafe_allow_html=True)
	st.download_button(
		label='点击下载【知乎top5热门话题最新结果表】', data=convert_df(result),
		file_name='result.txt' , mime='text/csv')
	
st.warning('请知悉：若请求当时与上一次爬取相隔1个小时以上，可以启动实时爬取；否则显示的是当天已获取的最新内容')

"""-----------------------------------------------------"""
""" ## 热门话题互动 """
if is_zhihu == 0:
	try:
		st.warning('注意：由于您未体验上述【知乎top5热门话题】实时爬取功能，则默认调取当天已获取的最新内容')
		result = pd.read_csv('result.txt',sep=',')
		# 下载文件形式
		text_tmp = f'【知乎top5热门话题结果表】'
		st.markdown(get_binary_file_downloader_html('result.txt', text_tmp),unsafe_allow_html=True)

		with st.expander("当天已获取的最新内容，请自行展开查看："):
			for url,title in zip(result['url'],result['index'].astype(str)+'、'+result['title']):
				st.markdown(show_external_link(url, title),unsafe_allow_html=True)
	except:
		pass

try:
	st.write('\n')
	title_list = st.multiselect('top5热门话题中，您最感兴趣的是（请选择对应序号）：',list(result['index']))
	user_point = []
	for i in range(0,len(title_list)):
		title_list_tmp1 = title_list[i]
		user_point_tmp1 = st.text_area(f'对序号为 {title_list_tmp1} 的话题感兴趣原因 or 您对该话题有啥想法？')
		is_zhihu_report = st.selectbox('您是否会考虑前往知乎发表自己的想法？',('是', '否'))
		user_point.append(user_point_tmp1)
	# title_list,user_point,is_zhihu_report
	
except:
	st.warning('你还未进行任何爬取，该模块无法继续')
	title_list = []
	user_point = []
	is_zhihu_report = '否'

"""-----------------------------------------------------"""
""" ## 源码获取 """
is_send_code = 0
email = ''
send_time = ''
if st.checkbox('源码获取'):
	user_log = pd.read_csv('user_log.txt', sep = '|')
	is_send_code = 1
	my_sender = "1090421150@qq.com"
	my_password = "wppyudpqzugyidcb"
	file_path = 'share_code.zip'
	my_file_from = "蓝魅紫熏-vivian" # 邮件发送方命名
	my_file_to = login_name # 邮件接收方命名
	my_email_Subject = "源码" # 邮件主题
	my_email_text = "Dear:\n 附件为制作该网页的所有源代码，请及时查收，感谢使用。\n 如有任何意见，可直接回复该邮件交流 \n --from: 蓝魅紫熏(vivian)" # 邮件内容(数据结果总数据量&内部报价)
	my_annex_path1 = file_path # 附件1存在的路径
	my_annex_name1 = 'share_code.zip' # 附件1的名称
	
	email = st.text_input(f'请正确填写您想接收的邮箱：')
	my_receiver = email # 逗号分隔，','
	if my_receiver in list(user_log['email']):
		st.warning('已发送过源码，点击提交按钮也不再重复发送！！！')
	#my_receiver

submitted = st.button('提交')
st.info('若想通过邮箱自动获取源码，需点击此按钮提交(已发送过的不会重复发送)，此操作会保存客官填写的所有记录，若不想留下任何信息，可私信获取源码，但不一定及时回复~')
if submitted and my_receiver not in list(user_log['email']):
	# 统计使用者的情况
	try:
		user_id = user_log[(user_log['login_name']==login_name)&(user_log['login_date']==date_now)].user_id.unique()[0]
	except:
		user_id = 1 + len(user_log[(user_log['login_name']!=login_name)&(user_log['login_date']==date_now)].login_name.unique())
	user_cnt = 1 + len(user_log[(user_log['login_name']==login_name)&(user_log['login_date']==date_now)])

	st.info(f'您是今天第{user_id}个提交的贵客，并且是第{user_cnt}次提交。')

	with st.spinner('处理中...请稍等...'):
		if is_send_code == 1:
			# 发送邮件
			send_email = QQSendEmail(my_file_from,my_file_to,my_email_Subject,my_email_text,my_receiver,my_annex_path1,my_annex_name1)
			send_email.final_send(my_sender,my_password)
			send_time = str(datetime.datetime.today())
		# 保存提交的每个人的操作填写记录
		f = "user_log.txt"
		interest_title = ';'.join([str(i) for i in title_list])
		user_point = ';'.join(user_point)
		with open(f, "a", encoding="utf-8") as file:   # "a"代表追加内容
			file.write(login_name+'|'+date_now+'|'+time_now+'|'+str(user_id)+'|'+str(user_cnt)+'|'+job_type+'|'+is_python+'|'+is_streamlit+'|'+is_interest+'|'+str(interest_num)+'|'+str(is_zhihu)+'|'+interest_title+'|'+user_point+'|'+is_zhihu_report+'|'+str(is_send_code)+'|'+email+'|'+send_time + " "+"\n")
		#st.success('成功！！！')

# 庆祝气球
is_good = 0
if st.button('客官，留个赞再走呀（说不定会有惊喜呢）'):
	is_good = is_good + 1
	st.balloons()