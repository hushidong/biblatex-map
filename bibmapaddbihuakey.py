
#
#数据修改的设置
#
#

#重设新的任务处理
sourcemaps=[
	[#map1:设置author域的字符串的拼音字符串设置给域key
		{"fieldsource":"author"},#step1
		{"fieldset":"key","origfieldval":True,"fieldfunction":'sethzstroke'}#step2
	],
	[#map1:设置editor域的字符串的拼音字符串设置给域key
		{"fieldsource":"editor"},#step1
		{"fieldset":"key","origfieldval":True,"fieldfunction":'sethzstroke'}#step2
	],
]


