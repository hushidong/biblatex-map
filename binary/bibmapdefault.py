
#
#数据修改的设置
#
#默认不做修改
sourcemaps=[
	# [#map1:将source域转换为url域
		# {"fieldsource":"year","fieldtarget":"date"}#step1
	# ],
	[#map2:将urldate域的信息“yyyy-m-d”转换为“yyyy-mm-dd”,注意正则表达式直接写不用在外面套""
		{"fieldsource":"date","match":r'(\d\d\d\d)\-(\d)\-(\d)',"replace":r'\1-0\2-0\3',"overwrite":True}#step1
	],
]

sourcemaps=[]