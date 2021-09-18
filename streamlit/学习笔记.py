1、登录模块
	col1, col2 = st.beta_columns(2)
	with col1:
		login_name = st.text_input('登录账号')
	with col2:
		placeholder = st.empty()
		login_password = placeholder.text_input('登录密码')
		true_pass = login_table[login_table['login_name']==login_name]['password']
	
	# 判断登录者是否有权限、密码是否正确
	if login_name == '' or login_password == '':
		st.warning('请输入账号密码登录。')
		st.stop()
	elif login_table[login_table['login_name']==login_name].shape[0] == 0:
		st.warning('非常抱歉，你还没有登入的权限，请按照流程申请才能使用该系统！！！')
		st.stop()
	elif (login_password != true_pass).all():
		st.warning('密码错误，请重新输入。若忘记密码，请联系管理员')
		st.stop()
	
	st.success('登入成功！！！欢迎使用')
	placeholder.empty() # 清空密码窗口

2、多行多列循环展示
	1）范例1：
	fail_id = st.multiselect('请选择不予审批通过的项目：',list(action_log['id']))
	fail_reason = []
	for i in range(0,math.ceil(len(fail_id)/2)):
		fail_id_tmp1 = fail_id[i*2+0]
		try:
			fail_id_tmp2 = fail_id[i*2+1]
		except:
			fail_id_tmp2 = '其他'
		col1, col2 = st.beta_columns(2)
		with col1:
			fail_temp1 = st.text_input(f'{fail_id_tmp1} 审批不通过原因')
			fail_reason.append(fail_temp1)
		if fail_id_tmp2 != '其他':
			with col2:
				fail_temp2 = st.text_input(f'{fail_id_tmp2} 审批不通过原因')
				fail_reason.append(fail_temp2)

	2）范例2：
	# 自定义产品粒度勾选
	def product_select():
		product_var = ['医院等级','yy_id','处方性质','通用名','品名','商品名','品牌'
						,'包装单位','规格','给药途径','大类剂型','小类剂型','厂家','集团权益','企业性质','ATC1'
						,'ATC2','ATC3','ATC4','ATC编码','功效主治','药品属性','招标品种','中标品种'
						,'医保分类','基药分类','品名(属性)','对象','日服用量','原研药','是否一致性评价','是否专利药','是否创新药','零售分类编码']
		var_list = ['level','yy_id','otc_rx','tym','drug_name','spm','brand'
					,'dosage_name','spec','vrote_name','big_jx','small_jx','company','group_rights','is_local','atc1'
					,'atc2','atc3','atc4','atc_code','gongxiao_zhuzhi','drug_type','zhaobiao_47','zhongbiao_47'
					,'yibaofenlei','jiyao','pm_sx','dx','vpd','is_yuanyan','yizhixing_pingjia','zhuangliyao','chuangxinyao','sort_code']	
		product_list = ''
		for i in range(0,7):
			if i < 6:
				configurations = [dict(text = product_var[i*5+0], var = var_list[i*5+0]),
	    		dict(text = product_var[i*5+1], var = var_list[i*5+1]),
	            dict(text = product_var[i*5+2], var = var_list[i*5+2]),
	            dict(text = product_var[i*5+3], var = var_list[i*5+3]),
	            dict(text = product_var[i*5+4], var = var_list[i*5+4])]
				columns = st.beta_columns(len(configurations))
	
				for column, configuration in zip(columns, configurations):
					with column:
						if st.checkbox(configuration["text"]):
							product_list = product_list + "," + configuration["var"] + ' "' + configuration["text"] + '"'
	
			if i >= 6:
				configurations = [dict(text = product_var[i*4+6], var = var_list[i*4+6]),
				dict(text = product_var[i*4+7], var = var_list[i*4+7]),
				dict(text = product_var[i*4+8], var = var_list[i*4+8]),
				dict(text = product_var[i*4+9], var = var_list[i*4+9])]
				columns = st.beta_columns(len(configurations))
	
				for column, configuration in zip(columns, configurations):
					if configuration["text"] != '其他':
						with column:
							if st.checkbox(configuration["text"]):
								product_list = product_list + "," + configuration["var"] + ' "' + configuration["text"] + '"'
	
		return product_list

3、文件下载
	def get_binary_file_downloader_html(bin_file, file_label='File'):
	    with open(bin_file, 'rb') as f:
	    	data = f.read()
	    bin_str = base64.b64encode(data).decode()
	    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">点击下载 {file_label}</a>'
	    return href

	# 需求汇总表明细下载
	if st.checkbox('是否下载需求汇总表'):
		col1, col2 = st.beta_columns(2)
		with col1:
			time_start = st.text_input(
				"开始时间",
				datetime.date(2021, 1, 1))
		with col2:
			time_end = st.date_input(
				"结束时间",
				datetime.date.today())
		state_table = pd.read_sql("select * from dpc.yy_vivian_dim_common_project where create_time between '" + str(time_start) + "' and '" + str(time_end) + "';",conn)
		state_table.to_csv('item_detail.csv',encoding='utf_8_sig')
		text_tmp = f'时间段 {str(time_start)} 到 {str(time_end)} 的需求汇总表'
		st.markdown(get_binary_file_downloader_html('item_detail.csv', text_tmp),unsafe_allow_html=True)

4、多种文字样式表现（成功、警告、提示等）

5、邮件发送


框架：
1、登录模块
2、前期调研（兴趣调研--单选/滑动打分（分别针对python、streamlit、知乎热门话题爬虫、邮件发送）、是否接触过python、认为难易程度）
2、即时爬取知乎热门话题（开始按钮）
3、是否显示结果（复选框、自主选择显示多少个话题、结果展示形式）
4、下载结果链接
5、热门话题互动（选择感兴趣的话题，表达自己的见解？）
6、源码获取（下载链接、邮件发送）
