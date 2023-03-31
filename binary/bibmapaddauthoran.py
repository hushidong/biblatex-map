
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
	[#map1:在作者信息中找到Zhao, Mou Mou并添加相应的注释信息为thesisauthor
		{"fieldsource":"author","match":'Zhao, Mou Mou',"final":True},#step1
		{"fieldset":"AUTHOR+an","fieldfunction":'setauthoran','fieldvalue':'thesisauthor'}#step2
	],
	[#map1:在作者信息中找到Chiani, M.并添加相应的注释信息为corresponding
		{"fieldsource":"author","match":'Chiani, M.',"final":True},#step1
		{"fieldset":"AUTHOR+an","fieldfunction":'setauthoran','fieldvalue':'corresponding','overwrite':True,'append':True,'appdelim':";"}#step2
	],
]


