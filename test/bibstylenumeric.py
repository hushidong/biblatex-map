

#
#文献格式化的设置
#
#全局选项
formatoptions={
"style":'numeric',#写bbl信息的设置选项,authoryear,'numeric'
"nameformat":'uppercase',#姓名处理选项：uppercase,lowercase,given-family,family-given,pinyin
"giveninits":'space',#使用名的缩写，space表示名见用空格分隔，dotspace用点加空格，dot用点，terse无分隔，false不使用缩写
"usesuffix":True,#使用后缀名
"maxbibnames":3,#
"minbibnames":3,#
"morenames":True,#
"maxbibitems":1,#
"minbibitems":1,#
"moreitems":False,#
"date":'year',#'日期处理选项'：year，iso，等
"urldate":'iso',#'日期处理选项'：year，iso，等
"origdate":'year',#'日期处理选项'：year，iso，等
"eventdate":'year',#'日期处理选项'：year，iso，等
'caseformat':'none',#设计'none','sentencecase','titlecase','uppercase','lowercase','smallcaps'
#'numberformat':'ordinal',#设计'ordinal','arabic'
"lanorder":['chinese','japanese','korean','english','french','russian'],#文种排序，指定语言全面的顺序['chinese','japanese','korean','english','french','russian'],'none'
'sortascending':True,#排序使用升序还是降序，默认是升序，设置为False则为降序
"sorting":['author','year','title'],#排序，或者指定一个域列表比如['key','author','year','title']，'none'
}

#本地化字符串
localstrings={
'andothers':{'english':'et al.','chinese':'等'},
'and':{'english':' and ','chinese':'和'},
'edition':{'english':' ed','chinese':'版'},#ed. 中的点不要，为方便标点处理
'in':{'english':'in: ','chinese':'见: '},
'nolocation':{'english':'[S.l.]','chinese':'[出版地不详]'},
'nopublisher':{'english':'[s.n.]','chinese':'[出版者不详]'},
'bytranslator':{'english':'trans by','chinese':'译'},
'volsn':{'english':'Vol.','chinese':'第'},
'volume':{'english':'','chinese':'卷'},
'numsn':{'english':'No.','chinese':'第'},
'number':{'english':'','chinese':'册'},
}

#标点
localpuncts={
'multinamedelim':', ',
'finalnamedelim':', ',
'andothorsdelim':', ',
'finalitemdelim':', ',
'multiitemdelim':', ',
'pagerangedelim':'-',
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
'mastersthesis':'[D]',
'phdthesis':'[D]',
'report':'[R]',
'techreport':'[R]',
'manual':'[A]',
'archive':'[A]',
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
'literalfield':['title','journaltitle','journal','booktitle','subtitle','titleaddon','url','doi','edition','version',
                'volume','number','endvolume','endnumber','type','note','labelnumber','series'],
'datefield':['date','enddate','year','endyear','urldate','origdate','eventdate','endurldate','endorigdate','endeventdate'],
'rangefield':['pages'],
'otherfield':['in','typeid','endpunct']#虚设的用于替换的域
}




#条目的著录格式
bibliographystyle={
"book":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','editor','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['series'],'prepunct':". ",'prepunctifnolastfield':''},
{"fieldsource":['title'],'options':{'caseformat':'sentencecase'},'prepunct':": ",'prepunctifnolastfield':'. '},
{"fieldsource":['volume'],'prepunct':": ",'prestringifnumber':r'\bibstring{volsn}','posstringifnumber':r'\bibstring{volume}'},
{"fieldsource":['number'],'prepunct':": ",'prestringifnumber':r'\bibstring{numsn}','posstringifnumber':r'\bibstring{number}'},
{"fieldsource":['typeid'],'replstring':r"\allowbreak\typestring"},
{"fieldsource":['translator'],'options':{'nameformat':'uppercase'},'prepunct':". ",'posstring':r', \bibstring{bytranslator}'},
{"fieldsource":['edition'],'options':{'numberformat':'ordinal'},'prepunct':". ","posstringifnumber":r'\bibstring{edition}'},
{"fieldsource":['location','address'],'prepunct':". ",'replstring':r"\bibstring{nolocation}"},
{"fieldsource":['publisher'],'prepunct':": ",'replstring':r"\bibstring{nopublisher}",'prepunctifnolastfield':'. '},
{"fieldsource":['date','year'],'prepunct':", "},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':r". ",'prestring':r'\newblock\url{','posstring':'}'},
{"fieldsource":['doi'],'prepunct':".",'prestring':r'\newblock DOI:\doi{','posstring':'}'},
{"fieldsource":['endpunct'],'replstring':"."}
],
"article":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','editor','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'options':{'caseformat':'sentencecase'},'prepunct':". ",'prepunctifnolastfield':'','posstring':r"\allowbreak\typestring"},
{"fieldsource":['journaltitle','journal'],'prepunct':". "},
{"fieldsource":['year','date'],'prepunct':", "},
{"fieldsource":['volume'],'prepunct':", "},
{"fieldsource":['number'],'prestring':"(",'posstring':")"},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':r". ",'prestring':r'\newblock\url{','posstring':'}'},
{"fieldsource":['doi'],'prepunct':".",'prestring':r'\newblock DOI:\doi{','posstring':'}'},
{"fieldsource":['endpunct'],'replstring':"."}
],
"newspaper":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','editor','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'options':{'caseformat':'sentencecase'},'prepunct':". ",'prepunctifnolastfield':'','posstring':r"\allowbreak\typestring"},
{"fieldsource":['journaltitle','journal'],'prepunct':". "},
{"fieldsource":['date','year'],'prepunct':", ",'options':{'date':'iso'}},
{"fieldsource":['number'],'prestring':"(",'posstring':")"},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':r". ",'prestring':r'\newblock\url{','posstring':'}'},
{"fieldsource":['doi'],'prepunct':".",'prestring':r'\newblock DOI:\doi{','posstring':'}'},
{"fieldsource":['endpunct'],'replstring':"."}
],
"inbook":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'options':{'caseformat':'sentencecase'},'prepunct':". ",'prepunctifnolastfield':'','posstring':r"\allowbreak\typestring"},
{"fieldsource":['in'],'replstring':"//",'omitifnofield':['bookauthor','editor','booktitle']},
{"fieldsource":['bookauthor','editor'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['booktitle'],'options':{'caseformat':'sentencecase'},'prepunct':". ",'prepunctifnolastfield':''},
{"fieldsource":['volume'],'prepunct':": ",'prestringifnumber':r'\bibstring{volsn}','posstringifnumber':r'\bibstring{volume}'},
{"fieldsource":['number'],'prepunct':": ",'prestringifnumber':r'\bibstring{numsn}','posstringifnumber':r'\bibstring{number}'},
{"fieldsource":['edition'],'options':{'numberformat':'ordinal'},'prepunct':". ","posstringifnumber":r'\bibstring{edition}'},
{"fieldsource":['location','address'],'prepunct':". ",'replstring':r"\bibstring{nolocation}"},
{"fieldsource":['publisher'],'prepunct':": ",'replstring':r"\bibstring{nopublisher}",'prepunctifnolastfield':'. '},
{"fieldsource":['date','year'],'prepunct':", "},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':r". ",'prestring':r'\newblock\url{','posstring':'}'},
{"fieldsource":['doi'],'prepunct':".",'prestring':r'\newblock DOI:\doi{','posstring':'}'},
{"fieldsource":['endpunct'],'replstring':"."}
],
"inproceedings":"inbook",
"incollection":"inbook",
#"standard":"inbook",
"proceedings":"book",
"collection":"book",
"standard":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['series'],'prepunct':". ",'prepunctifnolastfield':''},
{"fieldsource":['title'],'options':{'caseformat':'sentencecase'},'prepunct':" ",'prepunctifnolastfield':'. '},
{"fieldsource":['number'],'prepunct':" "},
{"fieldsource":['typeid'],'replstring':r"\allowbreak\typestring"},
{"fieldsource":['in'],'replstring':"//",'omitifnofield':['bookauthor','editor','booktitle']},
{"fieldsource":['bookauthor','editor'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['booktitle'],'options':{'caseformat':'sentencecase'},'prepunct':". ",'prepunctifnolastfield':''},
{"fieldsource":['edition'],'options':{'numberformat':'arabic'},'prepunct':". ","posstring":r'\bibstring{edition}'},
{"fieldsource":['location','address'],'prepunct':". ",'replstring':r"\bibstring{nolocation}"},
{"fieldsource":['publisher'],'prepunct':": ",'replstring':r"\bibstring{nopublisher}",'prepunctifnolastfield':'. '},
{"fieldsource":['date','year'],'prepunct':", "},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':r". ",'prestring':r'\newblock\url{','posstring':'}'},
{"fieldsource":['doi'],'prepunct':".",'prestring':r'\newblock DOI:\doi{','posstring':'}'},
{"fieldsource":['endpunct'],'replstring':"."}
],
"patent":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'options':{'caseformat':'sentencecase'},'prepunct':". ",'prepunctifnolastfield':''},
{"fieldsource":['number'],'prepunct':": "},
{"fieldsource":['typeid'],'replstring':r"\allowbreak\typestring"},
{"fieldsource":['date','year'],'prepunct':", ",'options':{"date":"iso"}},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':r". ",'prestring':r'\newblock\url{','posstring':'}'},
{"fieldsource":['doi'],'prepunct':".",'prestring':r'\newblock DOI:\doi{','posstring':'}'},
{"fieldsource":['endpunct'],'replstring':"."}
],
"online":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','editor','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'options':{'caseformat':'sentencecase'},'prepunct':". ",'prepunctifnolastfield':'','posstring':r"\allowbreak\typestring"},
{"fieldsource":['organization','instiution'],'prepunct':". "},
{"fieldsource":['date','year'],'prepunct':", ",'prepunctifnolastfield':'. ','omitifnofield':['enddate','eventdate']},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['date','enddate','eventdate'],'prepunct':". ",'options':{"date":"iso",'eventdate':'iso'},'prestring':"(","posstring":")"},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]",'prepunctifnolastfield':'. '},
{"fieldsource":['url'],'prepunct':". ",'prepunctifnolastfield':'','prestring':r'\url{','posstring':'}'},
{"fieldsource":['doi'],'prepunct':".",'prestring':r'\newblock DOI:\doi{','posstring':'}'},
{"fieldsource":['endpunct'],'replstring':"."}
],
"www":"online",
"electronic":"online",
"report":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','editor','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'options':{'caseformat':'sentencecase'},'prepunct':". ",'prepunctifnolastfield':'','posstring':r"\allowbreak\typestring"},
{"fieldsource":['translator'],'options':{'nameformat':'uppercase'},'prepunct':". "},
{"fieldsource":['type'],'prepunct':". "},
{"fieldsource":['number'],'prepunct':"",'prepunctifnolastfield':'. '},
{"fieldsource":['version'],'prepunct':". "},
{"fieldsource":['location','address'],'prepunct':". ",'replstring':r"\bibstring{nolocation}",'omitifnofield':['location','address','institution','publisher'],'omitiffield':['url']},
{"fieldsource":['institution','publisher'],'prepunct':": ",'replstring':r"\bibstring{nopublisher}",'prepunctifnolastfield':'. ','omitifnofield':['location','address','institution','publisher'],'omitiffield':['url']},
{"fieldsource":['date','year'],'prepunct':", ",'omitifnofield':['location','address','institution','publisher'],'omitiffield':['url']},
{"fieldsource":['date','year'],'prepunct':". ",'prestring':'(','posstring':')','options':{"date":"iso"},'omitifnofield':['url']},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':r". ",'prestring':r'\newblock\url{','posstring':'}'},
{"fieldsource":['doi'],'prepunct':".",'prestring':r'\newblock DOI:\doi{','posstring':'}'},
{"fieldsource":['endpunct'],'replstring':"."}
],
"techreport":"report",
"periodical":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['editor','author'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'options':{'caseformat':'sentencecase'},'prepunct':". ",'prepunctifnolastfield':'','posstring':r"\allowbreak\typestring"},
{"fieldsource":['year','date'],'prepunct':", "},
{"fieldsource":['volume'],'prepunct':", "},
{"fieldsource":['number'],'prestring':"(",'posstring':")-"},
{"fieldsource":['endyear','enddate']},
{"fieldsource":['endvolume'],'prepunct':", "},
{"fieldsource":['endnumber'],'prestring':"(",'posstring':")"},
{"fieldsource":['location','address'],'prepunct':". ",'replstring':r"\bibstring{nolocation}"},
{"fieldsource":['institution','publisher'],'prepunct':": ",'replstring':r"\bibstring{nopublisher}",'prepunctifnolastfield':'. '},
{"fieldsource":['year','date'],'prepunct':", ",'posstring':'-'},
{"fieldsource":['endyear','enddate']},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':r". ",'prestring':r'\newblock\url{','posstring':'}'},
{"fieldsource":['doi'],'prepunct':".",'prestring':r'\newblock DOI:\doi{','posstring':'}'},
{"fieldsource":['endpunct'],'replstring':"."}
],
#omitifnofield:必须所有的域都不存在才为true
#omitiffield:只要存在一个域就为true
"thesis":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','editor','translator'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['title'],'options':{'caseformat':'sentencecase'},'prepunct':". ",'prepunctifnolastfield':'','posstring':r"\allowbreak\typestring"},
{"fieldsource":['translator'],'options':{'nameformat':'uppercase'},'prepunct':". "},
{"fieldsource":['location','address'],'prepunct':". "},
{"fieldsource":['institution','publisher','school'],'prepunct':": ",'prepunctifnolastfield':'. '},
{"fieldsource":['date','year'],'prepunct':", ",'omitifnofield':['location','address','institution','publisher'],'omitiffield':['url']},
{"fieldsource":['date','year'],'prepunct':". ",'prestring':'(','posstring':')','omitiffield':['location','address','institution','publisher'],'options':{"date":"iso"}},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':r"\allowbreak[","posstring":"]"},
{"fieldsource":['url'],'prepunct':r". ",'prestring':r'\newblock\url{','posstring':'}'},
{"fieldsource":['doi'],'prepunct':".",'prestring':r'\newblock DOI:\doi{','posstring':'}'},
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
{"fieldsource":['title'],'options':{'caseformat':'sentencecase'},'prepunct':". ",'prepunctifnolastfield':'','posstring':r"\allowbreak\typestring"},
{"fieldsource":['howpublished'],'prepunct':". "},
{"fieldsource":['location','address'],'prepunct':". "},
{"fieldsource":['institution','publisher'],'prepunct':": ",'prepunctifnolastfield':'. '},
{"fieldsource":['date','year'],'prepunct':", "},
{"fieldsource":['pages'],'prepunct':": "},
{"fieldsource":['urldate'],'prestring':"[","posstring":"]"},
{"fieldsource":['url'],'prepunct':r". ",'prestring':r'\newblock\url{','posstring':'}'},
{"fieldsource":['doi'],'prepunct':".",'prestring':r'\newblock DOI:\doi{','posstring':'}'},
{"fieldsource":['endpunct'],'replstring':"."}
],
"phdthesis":"thesis",
"mastersthesis":"thesis",
}
