
#
#数据修改的设置
#
#默认不做修改
#sourcemaps=[]
#重设新的任务处理
sourcemaps=[
	[#map1:设置entrykey域设置给keywords
		[{"fieldsource":"entrykey"}],#step1
		[{"fieldset":"keywords","origfieldval":True,"overwrite":True}]#step2
	],
]