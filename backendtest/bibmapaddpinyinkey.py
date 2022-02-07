
#
#数据修改的设置
#
#

#设置多音字的首读音
multiplepinyin={
'曾':'zeng1',
'沈':'shen3',
'翟':'zhai2'
}

#重设新的任务处理
sourcemaps=[
	[#map1:设置author域的字符串的拼音字符串设置给域key
		{"fieldsource":"author"},#step1
		{"fieldset":"key","origfieldval":True,"fieldfunction":'sethzpinyin'}#step2
	],
	[#map1:设置editor域的字符串的拼音字符串设置给域key
		{"fieldsource":"editor"},#step1
		{"fieldset":"key","origfieldval":True,"fieldfunction":'sethzpinyin'}#step2
	],
]


