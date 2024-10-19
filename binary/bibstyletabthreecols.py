

#
#文献格式化的设置
#
#全局选项
formatoptions={
"style":'authoryear',##这个选项目前暂无功能
"nameformat":'lowercase',#姓名处理选项：uppercase,lowercase,given-family,family-given,pinyin
"citenameformat":'titlecase',#标注中的姓名处理选项：uppercase,titlecase
"giveninits":'dotspace',#使用名的缩写，space表示名见用空格分隔，dotspace用点加空格，dot用点，terse无分隔，false不使用缩写
"useprefix":False,#使用前缀名
"usesuffix":True,#使用后缀名
"maxbibnames":3,#
"minbibnames":3,#
"maxcitenames":1,#
"mincitenames":1,#
"morenames":True,#
"labelname":['author','editor','translator','bookauthor','title'],#作者年制中作者标签的域的选择设置，比如['author','editor','translator','bookauthor','title'],
"labelyear":['year','endyear','urlyear'],#作者年制中作者标签的域的选择设置，比如['year','endyear','urlyear']
"labelextrayear":True,#是否使用bibextrayear，citeextrayear来消除姓名列表的歧义
"uniquename":'true',#false 不对姓名消除歧义，init则仅使用名的首字母来消除，true则首先使用首字母，不行则使用全名['false','init','true']
"uniquelist":'true',#false 不对姓名消除歧义，minyear则判断时加入labelyear，true不使用year直接对列表消除歧义['false','minyear','true']
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
"sorting":['author','year','title'],#排序，或者指定一个域列表比如['author','year','title']，'none'。注意key域时默认要使用的当存在的时候'key'它在lanorder后面
"sortlocale":'stroke',#本地化排序:'none'，'pinyin'，'stroke'，'system'，none不使用，system是操作系统提供的的locale，pinyin，stroke是bibmap根据unicode-cldr实现的排序
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
'backref':{'english':'Cited on ','chinese':'引用页: '}
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
'otherfield':['in','typeid','endpunct'],#虚设的用于替换的域
'labelfield':['labelnumber','sortlabelnumber','labelname','biblabelname','labelyear','biblabelextrayear','citelabelname','citelabelextrayear'],#用于消除作者列表歧义的域，也用于作者年制中的citation和bibliography中
}


#文献表的环境，包括表格环境
bibliographyenv={
"default":r'''
\renewcommand\bibitem[2][]{\item}
    \setlength{\biblabelsep}{1em}
    \setlength{\bibitemindent}{0pt}
    \setlength{\biblabelextend}{0pt}
    \renewenvironment{thebibliography}[1]
    {\bibheading\list%
     {\mkbibbracket{\arabic{biblabelnumber}}}
     {\usecounter{biblabelnumber}%
     \settowidth{\labelnumberwidth}{\mkbibbracket{#1}}%
     \addtolength{\labelnumberwidth}{\biblabelextend}%
      \setlength{\labelwidth}{\labelnumberwidth}%
      \setlength{\labelsep}{\biblabelsep}%
      \setlength{\bibhang}{\biblabelsep}%
      \addtolength{\bibhang}{\labelnumberwidth}%
      \setlength{\leftmargin}{\bibhang}%
      \setlength{\itemindent}{\bibitemindent}%
      \setlength{\itemsep}{\bibitemsep}%
      \setlength{\parsep}{\bibparsep}}%
      \renewcommand*{\makelabel}[1]{\hss##1}}
  {\endlist}
''',
"longtable":{
    "cmd":r"\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}",  # 需定义的命令
    "env":"longtable",
    "colspec":"{|C{1cm}|C{3cm}|p{11cm}|}",
    "head":"序号 & 作者 & 信息"
},
"tabularray":{
    "cmd":"",  # 需定义的命令
    "env":"longtblr",
    "colspec":"[label=none]{colspec={|Q[c,m,1cm]|Q[c,m,3cm]|Q[l,m,11cm]|},cell{1}{3}={c,m}, rowhead = 1,rows={ht=1cm}}",
    "head":"序号 & 作者 & 信息"
}
}


#数据注解的样式设置
#"default"是默认的注解名
annotestyle={"default":
             {"thesisauthor":{'prestring':r"\textcolor{red}{\textbf{","posstring":"}}"},
              "important":{'prestring':r"\textbf{","posstring":"}"}
              }}



#条目的著录格式
bibliographystyle={
"book":[
#{"fieldsource":["labelnumber"],'prestring':"[","posstring":"]","pospunct":"  "},
{"fieldsource":['author','editor','translator']},
{"fieldsource":['series'],'prepunct':"FunNotCondition{inentryset}{ & }",'prepunctifnolastfield':''},
{"fieldsource":['title'],'options':{'caseformat':'none'},'prepunct':": ",'prepunctifnolastfield':"FunNotCondition{inentryset}{ & }"},
{"fieldsource":['volume'],'prepunct':": ",'prestringifnumber':r'\bibstring{volsn}','posstringifnumber':r'\bibstring{volume}'},
{"fieldsource":['number'],'prepunct':": ",'prestringifnumber':r'\bibstring{numsn}','posstringifnumber':r'\bibstring{number}'},
{"fieldsource":['typeid'],'replstring':r"\allowbreak\typestring"},
{"fieldsource":['translator'],'prepunct':". ",'posstring':r', \bibstring{bytranslator}'},
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
{"fieldsource":['author','editor','translator']},
{"fieldsource":['title'],'options':{'caseformat':'none'},'prepunct':"FunNotCondition{inentryset}{ & }",
 'prepunctifnolastfield':"FunNotCondition{inentryset}{ & }",'posstring':r"\allowbreak\typestring"},
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
{"fieldsource":['author','editor','translator']},
{"fieldsource":['title'],'options':{'caseformat':'none'},'prepunct':"FunNotCondition{inentryset}{ & }",
 'prepunctifnolastfield':"FunNotCondition{inentryset}{ & }",'posstring':r"\allowbreak\typestring"},
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
{"fieldsource":['author','translator']},
{"fieldsource":['title'],'options':{'caseformat':'none'},'prepunct':"FunNotCondition{inentryset}{ & }",
 'prepunctifnolastfield':"FunNotCondition{inentryset}{ & }",'posstring':r"\allowbreak\typestring"},
{"fieldsource":['in'],'replstring':"//",'omitifnofield':['bookauthor','editor','booktitle']},
{"fieldsource":['bookauthor','editor'],'options':{'nameformat':'uppercase'}},
{"fieldsource":['booktitle'],'options':{'caseformat':'none'},'prepunct':". ",'prepunctifnolastfield':''},
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
{"fieldsource":['author','translator']},
{"fieldsource":['series'],'prepunct':"FunNotCondition{inentryset}{ & }",'prepunctifnolastfield':''},
{"fieldsource":['title'],'options':{'caseformat':'none'},'prepunct':": ",'prepunctifnolastfield':"FunNotCondition{inentryset}{ & }"},
{"fieldsource":['number'],'prepunct':" "},
{"fieldsource":['typeid'],'replstring':r"\allowbreak\typestring"},
{"fieldsource":['in'],'replstring':"//",'omitifnofield':['bookauthor','editor','booktitle']},
{"fieldsource":['bookauthor','editor']},
{"fieldsource":['booktitle'],'options':{'caseformat':'none'},'prepunct':". ",'prepunctifnolastfield':''},
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
{"fieldsource":['author']},
{"fieldsource":['title'],'options':{'caseformat':'none'},'prepunct':"FunNotCondition{inentryset}{ & }",'prepunctifnolastfield':"FunNotCondition{inentryset}{ & }"},
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
{"fieldsource":['author','editor','translator']},
{"fieldsource":['title'],'options':{'caseformat':'none'},'prepunct':"FunNotCondition{inentryset}{ & }",
 'prepunctifnolastfield':"FunNotCondition{inentryset}{ & }",'posstring':r"\allowbreak\typestring"},
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
{"fieldsource":['author','editor','translator']},
{"fieldsource":['title'],'options':{'caseformat':'none'},'prepunct':"FunNotCondition{inentryset}{ & }",
 'prepunctifnolastfield':"FunNotCondition{inentryset}{ & }",'posstring':r"\allowbreak\typestring"},
{"fieldsource":['translator'],'prepunct':". "},
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
{"fieldsource":['editor','author']},
{"fieldsource":['title'],'options':{'caseformat':'none'},'prepunct':"FunNotCondition{inentryset}{ & }",
 'prepunctifnolastfield':"FunNotCondition{inentryset}{ & }",'posstring':r"\allowbreak\typestring"},
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
{"fieldsource":['author','editor','translator']},
{"fieldsource":['title'],'options':{'caseformat':'none'},'prepunct':"FunNotCondition{inentryset}{ & }",
 'prepunctifnolastfield':"FunNotCondition{inentryset}{ & }",'posstring':r"\allowbreak\typestring"},
{"fieldsource":['translator'],'prepunct':". "},
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
{"fieldsource":['author','editor','translator']},
{"fieldsource":['title'],'options':{'caseformat':'none'},'prepunct':"FunNotCondition{inentryset}{ & }",
 'prepunctifnolastfield':"FunNotCondition{inentryset}{ & }",'posstring':r"\allowbreak\typestring"},
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



#标注样式
#要指明每个命令需要的信息内容和格式要求
citationstyle={
    "numeric":{
        "cite":[{"fieldsource":['labelnumber'],'prestring':"[","posstring":"]","position":"superscript"}],#即用在文献表中的序号
        "parencite":[{"fieldsource":['labelnumber'],'prestring':"[","posstring":"]"}],
        "textcite":[{"fieldsource":['labelname']}, #用全局选项
                    {"fieldsource":['labelnumber'],'prestring':"[","posstring":"]","position":"superscript"}],
        "fullcite":[{"fieldsource":['styletext']}],#即用完整的格式化后的条目文本
        "footfullcite":[{"fieldsource":['styletext'],"position":"footnote"}],#即用完整的格式化后的条目文本
        "citep":"cite", #表示citep命令与cite等同
        "citet":"textcite"
    },
    "authoryear":{
        "cite":[{"fieldsource":['labelname'],'prestring':"(","posstring":", "},
                {"fieldsource":['labelyear']},
                {"fieldsource":['labelextrayear']},
                {"fieldsource":['endpunct'],'replstring':")"}],#即用在文献表中的序号
        "textcite":[{"fieldsource":['labelname']}, #用全局选项
                    {"fieldsource":['labelyear'],'prestring':"("},
                    {"fieldsource":['labelextrayear']},
                {"fieldsource":['endpunct'],'replstring':")"}],
        "fullcite":[{"fieldsource":['styletext']}],#即用完整的格式化后的条目文本
        "footfullcite":[{"fieldsource":['styletext'],"position":"footnote"}],#即用完整的格式化后的条目文本
        "parencite":"cite",
        "citep":"cite", #表示citep命令与cite等同
        "citet":"textcite"
    }
}