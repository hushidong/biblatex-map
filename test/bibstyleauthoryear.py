
#
#文献格式化的设置
#
#全局选项
formatoptions={
"style":'authoryear',#写bbl信息的设置选项,authoryear,'numeric'
"nameformat":'uppercase',#姓名处理选项：uppercase,lowercase,given-family,family-given,pinyin
"giveninits":'space',#使用名的缩写，space表示名见用空格分隔，dotspace用点加空格，dot用点，terse无分隔，false不使用缩写
"maxbibnames":3,#
"minbibnames":3,#
"morenames":True,#
"maxbibitems":1,#
"minbibitems":1,#
"moreitems":False,#
"date":'year',#'日期处理选项'：year，iso，等
"urldate":'iso',#'日期处理选项'：year，iso，等
}

#本地化字符串
localstrings={
'andothers':{'english':'et al.','chinese':'等'},
'and':{'english':' and ','chinese':'和'},
'edition':{'english':'th ed','chinese':'版'},#th ed. 中的点不要，为方便标点处理
'in':{'english':'in: ','chinese':'见: '},
'nolocation':{'english':'[S.l.]','chinese':'[出版地不详]'},
'nopublisher':{'english':'[s.n.]','chinese':'[出版者不详]'},
'bytranslator':{'english':'trans by','chinese':'译'},
}

#标点
localpuncts={
'multinamedelim':', ',
'finalnamedelim':', ',
'andothorsdelim':', ',
'finalitemdelim':', ',
'multiitemdelim':', ',
}

#替换字符串
replacestrings={
'[出版地不详]: [出版者不详]':'[出版地不详 : 出版者不详]',
'[S.l.]: [s.n.]':'[S.l. : s.n.]',
'..':'.',
}

#类型和载体字符串
typestrings={
'book':'[M]',
'inbook':'[M]',
'standard':'[S]',
'periodical':'[J]',
'article':'[J]',
'newspaper':'[N]',
'patent':'[P]',
'online':'[EB]',
'www':'[EB]',
'electronic':'[EB]',
'proceedings':'[C]',
'inproceedings':'[C]',
'conference':'[C]',
'collection':'[G]',
'incollection':'[G]',
'thesis':'[D]',
'mastersthsis':'[D]',
'phdthesis':'[D]',
'report':'[R]',
'techreport':'[R]',
'manual':'[A]',
'archive/manual':'[A]',
'database':'[DB]',
'dataset':'[DS]',
'software':'[CP]',
'map':'[CM]',
'unpublished':'[Z]',
'misc':'[Z]',
}

#数据类型
datatypeinfo={
'namelist':['author','editor','translator','bookauthor'],
'literallist':['location','address','publisher','institution','organization','school','language','keywords'],
'literalfield':['title','journaltitle','journal','booktitle','subtitle','titleaddon','edition','version','url',
                'volume','number','endvolume','endnumber','type','note','labelnumber'],
'datefield':['date','year','urldate','enddate','origdate','eventdate'],
'rangefield':['pages']
}

#条目的著录格式
bibliographystyle={
"book":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','editor','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'caseformat':'sentencecase','prepunct':". ",'prepunctifnolastfield':'','posstring':r"\typestring"},
{"fieldsource":['translator'],'options':{'nameformat':'uppercase'},'prepunct':". ",'posstring':r', \bibstring{bytranslator}'},
{"fieldsource":['edition'],'numerformat':'arabic','prepunct':". ","posstringifnumber":r'\bibstring{edition}'},
{"fieldsource":['location','address'],'prepunct':". ",'replstring':r"\bibstring{nolocation}"},
{"fieldsource":['publisher'],'prepunct':": ",'replstring':r"\bibstring{nopublisher}",'prepunctifnolastfield':'. '},
{"fieldsource":['date','year'],'prepunct':", "},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':". ",'prestring':r'\url{','posstring':'}'},
{"fieldsource":['doi'],'prepunct':". "},
{"fieldsource":['endpunct'],'replstring':"."}
],
"article":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','editor','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'caseformat':'sentencecase','prepunct':". ",'prepunctifnolastfield':'','posstring':r"\typestring"},
{"fieldsource":['journaltitle','journal'],'prepunct':". "},
{"fieldsource":['year','date'],'prepunct':", "},
{"fieldsource":['volume'],'prepunct':", "},
{"fieldsource":['number'],'prestring':"(",'posstring':")"},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':". "},
{"fieldsource":['doi'],'prepunct':". "},
{"fieldsource":['endpunct'],'replstring':"."}
],
"newspaper":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','editor','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'caseformat':'sentencecase','prepunct':". ",'prepunctifnolastfield':'','posstring':r"\typestring"},
{"fieldsource":['journaltitle','journal'],'prepunct':". "},
{"fieldsource":['date','year'],'prepunct':", ",'options':{'date':'iso'}},
{"fieldsource":['number'],'prestring':"(",'posstring':")"},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':". "},
{"fieldsource":['doi'],'prepunct':". "},
{"fieldsource":['endpunct'],'replstring':"."}
],
"inbook":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'caseformat':'sentencecase','prepunct':". ",'prepunctifnolastfield':'','posstring':r"\typestring"},
{"fieldsource":['in'],'replstring':"//",'omitifnofield':['bookauthor','editor','booktitle']},
{"fieldsource":['bookauthor','editor'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['booktitle'],'caseformat':'sentencecase','prepunct':". ",'prepunctifnolastfield':''},
{"fieldsource":['edition'],'numerformat':'arabic','prepunct':". ","posstring":r'\bibstring{edition}'},
{"fieldsource":['location','address'],'prepunct':". ",'replstring':r"\bibstring{nolocation}"},
{"fieldsource":['publisher'],'prepunct':": ",'replstring':r"\bibstring{nopublisher}",'prepunctifnolastfield':'. '},
{"fieldsource":['date','year'],'prepunct':", "},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':". "},
{"fieldsource":['doi'],'prepunct':". "},
{"fieldsource":['endpunct'],'replstring':"."}
],
"inproceedings":"inbook",
"incollection":"inbook",
"standard":"inbook",
"proceedings":"book",
"collection":"book",
"patent":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'caseformat':'sentencecase','prepunct':". ",'prepunctifnolastfield':'','posstring':r"\typestring"},
{"fieldsource":['number'],'prepunct':": "},
{"fieldsource":['date','year'],'prepunct':", "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':". "},
{"fieldsource":['doi'],'prepunct':". "},
{"fieldsource":['endpunct'],'replstring':"."}
],
"online":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','editor','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'caseformat':'sentencecase','prepunct':". ",'prepunctifnolastfield':'','posstring':r"\typestring"},
{"fieldsource":['organization','instiution'],'prepunct':". "},
{"fieldsource":['date','year'],'prepunct':", ",'prepunctifnolastfield':'. ','omitifnofield':['enddate','eventdate']},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['date','enddate','eventdate'],'prepunct':". ",'options':{"date":"iso",'eventdate':'iso'},'prestring':"(","posstring":")"},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]",'prepunctifnolastfield':'. '},
{"fieldsource":['url'],'prepunct':". ",'prepunctifnolastfield':''},
{"fieldsource":['doi'],'prepunct':". "},
{"fieldsource":['endpunct'],'replstring':"."}
],
"www":"online",
"electronic":"online",
"report":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','editor','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'caseformat':'sentencecase','prepunct':". ",'prepunctifnolastfield':'','posstring':r"\typestring"},
{"fieldsource":['translator'],'options':{'nameformat':'uppercase'},'prepunct':". "},
{"fieldsource":['type'],'prepunct':". "},
{"fieldsource":['number'],'prepunct':"",'prepunctifnolastfield':'. '},
{"fieldsource":['version'],'prepunct':". "},
{"fieldsource":['location','address'],'prepunct':". ",'replstring':r"\bibstring{nolocation}"},
{"fieldsource":['institution','publisher'],'prepunct':": ",'replstring':r"\bibstring{nopublisher}",'prepunctifnolastfield':'. '},
{"fieldsource":['date','year'],'prepunct':", ",'omitifnofield':['location','address','institution','publisher'],'omitiffield':['url']},
{"fieldsource":['date','year'],'prepunct':". ",'prestring':'(','posstring':')','omitiffield':['location','address','institution','publisher']},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':". "},
{"fieldsource":['doi'],'prepunct':". "},
{"fieldsource":['endpunct'],'replstring':"."}
],
"techreport":"report",
"periodical":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['editor','author'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'caseformat':'sentencecase','prepunct':". ",'prepunctifnolastfield':'','posstring':r"\typestring"},
{"fieldsource":['year','date'],'prepunct':", "},
{"fieldsource":['volume'],'prepunct':", "},
{"fieldsource":['number'],'prestring':"(",'posstring':")-"},
{"fieldsource":['endyear','enddate'],'prepunct':", "},
{"fieldsource":['endvolume'],'prepunct':", "},
{"fieldsource":['endnumber'],'prestring':"(",'posstring':")"},
{"fieldsource":['location','address'],'prepunct':". ",'replstring':r"\bibstring{nolocation}"},
{"fieldsource":['institution','publisher'],'prepunct':": ",'replstring':r"\bibstring{nopublisher}",'prepunctifnolastfield':'. '},
{"fieldsource":['year','date'],'prepunct':", ",'posstring':'-'},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':". "},
{"fieldsource":['doi'],'prepunct':". "},
{"fieldsource":['endpunct'],'replstring':"."}
],
#omitifnofield:必须所有的域都不存在才为true
#omitiffield:只要存在一个域就为true
"thesis":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','editor','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'caseformat':'sentencecase','prepunct':". ",'prepunctifnolastfield':'','posstring':r"\typestring"},
{"fieldsource":['translator'],'options':{'nameformat':'uppercase'},'prepunct':". "},
{"fieldsource":['location','address'],'prepunct':". "},
{"fieldsource":['institution','publisher','school'],'prepunct':": ",'prepunctifnolastfield':'. '},
{"fieldsource":['date','year'],'prepunct':", ",'omitifnofield':['location','address','institution','publisher'],'omitiffield':['url']},
{"fieldsource":['date','year'],'prepunct':". ",'prestring':'(','posstring':')','omitiffield':['location','address','institution','publisher']},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':". ",'prestring':r'\url{','posstring':'}'},
{"fieldsource":['doi'],'prepunct':". "},
{"fieldsource":['endpunct'],'replstring':"."}
],
"manual":"thesis",
"unpublished":"thesis",
"database":"thesis",
"dataset":"thesis",
"software":"thesis",
"map":"thesis",
"archive":"thesis",
"misc":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','editor','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'caseformat':'sentencecase','prepunct':". ",'prepunctifnolastfield':'','posstring':r"\typestring"},
{"fieldsource":['howpublished'],'prepunct':". "},
{"fieldsource":['location','address'],'prepunct':". "},
{"fieldsource":['institution','publisher'],'prepunct':": ",'prepunctifnolastfield':'. '},
{"fieldsource":['date','year'],'prepunct':", "},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':". "},
{"fieldsource":['doi'],'prepunct':". "},
{"fieldsource":['endpunct'],'replstring':"."}
],
"phdthesis":"thesis",
"mastersthesis":"thesis",
}
