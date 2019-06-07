
#
#数据修改的设置
#
#
# 为数据map设置参数
# 选项的逻辑与biblatex基本一致，
# 差别包括:overwrite选项可以放到step步中表示
#[]=maps
#[[],[]]=map in maps
#[[{optionkey:optionval},{optionkey:optionval}],[]]=step in map in mpas
#注意python正则表达方式与perl的略有不同，比如unicode表示
#python用\xHH,\uHHHH,\UHHHHHHHH表示，而perl直接用\x{HHHH}表示。
sourcemaps=[#maps
	[#map1:将ELECTRONIC类型转换为online类型
		{"typesource":"ELECTRONIC","typetarget":"online"}#step1
	],
	[#map2:将source域转换为url域
		{"fieldsource":"source","fieldtarget":"url"}#step1
	],
	[#map3:将urldate域的信息“yyyy-m-d”转换为“yyyy-mm-dd”,注意正则表达式直接写不用在外面套""
		{"fieldsource":"urldate","match":r'(\d\d\d\d)\-(\d)\-(\d)',"replace":r'\1-0\2-0\3'}#step1
	],
	[#map4:将urldate域的信息“yyyy-m-d”转换为“yyyy-mm-dd”,注意正则表达式直接写不用在外面套""
		{"fieldsource":"date","match":r'(\d\d\d\d)\-(\d)\-(\d)',"replace":r'\1-0\2-0\3',"overwrite":True}#step1
	],
	[#map5:将refdate域转换为urldate域
		{"fieldsource":"refdate","fieldtarget":"urldate"}#step1
	],
	[#map6:对于newspaper类型，设置note为news
		{"pertype":"newspaper"},#step1
		{"fieldset":"note","fieldvalue":"news","overwrite":True}#step2
	],
	[#map7:设置edition域等于version
		{"fieldsource":"version","final":True},#step1
		{"fieldset":"edition","origfieldval":True}#step2
	],
	[#map8:设置entrykey域设置给keywords
		{"fieldsource":"entrykey"},#step1
		{"fieldset":"keywords","origfieldval":True}#step2
	],
	[#map9:对于存在note域的情况，将其值添加到keywords
		{"fieldsource":"note","final":True},#step1
		{"fieldset":"keywords","origfieldval":True,"overwrite":True,"append":True}#step2
	],
	 [#map10:根据标题的字符编码范围确定标题的语言类型
		{"fieldsource":"title","match":r'[\u2FF0-\u9FA5]',"final":True},#step1
		{"fieldset":"userd","fieldvalue":"chinese"}#step2
	],
]

#重设新的任务处理
sourcemaps=[
	[#map1:设置entrykey域设置给keywords
		{"fieldsource":"entrykey"},#step1
		{"fieldset":"keywords","origfieldval":True,"overwrite":True}#step2
	],
]


#重设新的任务
sourcemaps=[
	[#map1:取消note域
		{"fieldsource":"note","final":True},#step1
		{"fieldset":"note","null":True,"overwrite":True}#step2
	],
	[#map2:取消abstract域
		{"fieldsource":"abstract","final":True},#step1
		{"fieldset":"abstract","null":True,"overwrite":True}#step2
	],
	[#map3:取消keywords域
		{"fieldsource":"keywords","final":True},#step1
		{"fieldset":"keywords","null":True,"overwrite":True}#step2
	],
	[#map4:取消keywords-plus域
		{"fieldsource":"keywords-plus","final":True},#step1
		{"fieldset":"keywords-plus","null":True,"overwrite":True}#step2
	],
	[#map5:取消affiliation域
		{"fieldsource":"affiliation","final":True},#step1
		{"fieldset":"affiliation","null":True,"overwrite":True}#step2
	],
	[#map6:取消funding-acknowledgement域
		{"fieldsource":"funding-acknowledgement","final":True},#step1
		{"fieldset":"funding-acknowledgement","null":True,"overwrite":True}#step2
	],
	[#map7:取消funding-text域
		{"fieldsource":"funding-text","final":True},#step1
		{"fieldset":"funding-text","null":True,"overwrite":True}#step2
	],
	]

#重设不处理
sourcemaps=[]