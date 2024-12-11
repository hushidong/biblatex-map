
#
#数据修改的设置
#
#注意：域如果不存在且需要终止，应加上"final":True

# 大小写字母保护的字符串
CaseProtect=['AIAA','IEEE','AAAI',"GECCO\'18","ACML","SAR",'BVR','UAV','UCAV','UAVs','PSO','AI','IJCAI','WIC','ACM',
             'CICAI','CDC','CoRR','IT','CAA','PSO','CAC','ICLR','II','III','IV','NIPS','arXiv','VI','VII',
             'VIII','IJCNN','AAMAS','ICGNC','CIG','ICUS','ACC','ICMA','MATEC','ACTA'] 
#其他情况请在bib文件中修改做保护，比如用{}包起来，NIPS-12这种用带数字的单词会自动保护
#平时积累的时候就要做保护

'''
sourcemaps=[
	[#map1:将设置title为sentencecase
		{"fieldsource":"title","final":True},#
		{"fieldset":"title","origfieldval":True,"fieldfunction":'setuppercase',"overwrite":True}#step1
	],
    [#map2:将设置booktitle为titlecase
		{"fieldsource":"booktitle","final":True},#
		{"fieldset":"booktitle","origfieldval":True,"fieldfunction":'setuppercase',"overwrite":True}#step1
	],
	[#map3:将设置journal为titlecase
		{"fieldsource":"journal","final":True},#
		{"fieldset":"journal","origfieldval":True,"fieldfunction":'setuppercase',"overwrite":True}#step1
	],
	[#map3:将设置journaltitle为titlecase
		{"fieldsource":"journaltitle","final":True},#
		{"fieldset":"journaltitle","origfieldval":True,"fieldfunction":'setuppercase',"overwrite":True}#step1
	]
]
'''

sourcemaps=[
	[#map1:将设置title为sentencecase
		{"fieldsource":"title","final":True},#
		{"fieldset":"title","origfieldval":True,"fieldfunction":'setsentencecase',"overwrite":True}#step1
	],
    [#map2:将设置booktitle为titlecase
		{"fieldsource":"booktitle","final":True},#
		{"fieldset":"booktitle","origfieldval":True,"fieldfunction":'settitlecasestd',"overwrite":True}#step1
	],
	[#map3:将设置journal为titlecase
		{"fieldsource":"journal","final":True},#
		{"fieldset":"journal","origfieldval":True,"fieldfunction":'settitlecasestd',"overwrite":True}#step1
	],
	[#map3:将设置journaltitle为titlecase
		{"fieldsource":"journaltitle","final":True},#
		{"fieldset":"journaltitle","origfieldval":True,"fieldfunction":'settitlecasestd',"overwrite":True}#step1
	]
]


#默认不做修改
#sourcemaps=[]