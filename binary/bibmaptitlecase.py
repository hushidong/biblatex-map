
#
#数据修改的设置
#
#注意：域如果不存在且需要终止，应加上"final":True
sourcemaps=[
	[#map1:将设置title为sentencecase
		{"fieldsource":"title","final":True},#
		{"fieldset":"title","origfieldval":True,"fieldfunction":'settitlecase',"overwrite":True}#step1
	],
	[#map2:将设置booktitle为titlecase
		{"fieldsource":"booktitle","final":True},#
		{"fieldset":"booktitle","origfieldval":True,"fieldfunction":'settitlecase',"overwrite":True}#step1
	],
	[#map3:将设置journal为titlecase
		{"fieldsource":"journal","final":True},#
		{"fieldset":"journal","origfieldval":True,"fieldfunction":'settitlecase',"overwrite":True}#step1
	],
	[#map3:将设置journaltitle为titlecase
		{"fieldsource":"journaltitle","final":True},#
		{"fieldset":"journaltitle","origfieldval":True,"fieldfunction":'settitlecase',"overwrite":True}#step1
	]
]

#默认不做修改
#sourcemaps=[]