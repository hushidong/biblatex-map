#!/usr/bin/env python

"""
A python script to modify bib data and 
to display references with specific bibliography standard

two key features：

两大核心功能
1. bib文件抽取，bib文件内容的自定义修改
2. 格式化文献表输出，包括json，bib，text，html，bbl文件，其中bbl文件可以在tex源代码中直接使用，利用natbib、bibmap宏包可以实现不同的标注样式。


"""

__author__ = "Hu zhenzhen"
__version__ = "1.0"
__license__ = "MIT"
__email__ = "hzzmail@163.com"

import os
import string
import re
import sys
import datetime
import copy
import json
import operator #数学计算操作符
import argparse #命令行解析
import locale #用locale的方法来进行中文排序，windows下是gbk，一级汉字按拼音排，二级按笔画数排

#引入拼音和笔画顺序的排序数据
import hanzicollationpinyin
import hanzicollationstroke
import hanzipinyindatabase

sqpinyindata=hanzicollationpinyin.sqpinyindata
sqstrokedata=hanzicollationstroke.sqstrokedata
hzpinyindata=hanzipinyindatabase.pinyindatabase

#
#bib数据修改所用的选项数据库
#用于检查用户设置的选项
bibmapoptiondatabase={
'typesource':'entrytype', #对应的值为 entrytype名
'typetarget':'entrytype', #对应的值为 entrytype名
'fieldsource':'entryfield', #对应的值为 entryfield名
'fieldtarget':'entryfield', #对应的值为 entryfield名
'match':'regexp', #对应的值为 regexp(正则表达式)
'notmatch':'regexp', #对应的值为 regexp(正则表达式)
'replace':'regexp', #对应的值为 regexp(正则表达式)
'notfield':'entryfield', #对应的值为 entryfield名
'final':[True,False], #对应的值为 true和false(bool值)
'origfieldval':[True,False], #对应的值为 true, false(bool值)
'append':[True,False], #对应的值为 true, false(bool值)
'appdelim':'string', #添加信息时使用的分隔符，用string(字符串)
'pertype':'entrytype', #对应的值为 entrytype名即条目类型
'pernottype':'entrytype', #对应的值为 entrytype名即条目类型
'fieldset':'entryfield', #对应的值为 entryfield名
'fieldvalue':'string', #对应的值为 string(字符串)
'null':[True,False], #对应的值为 true, false(bool值)
'origfield':[True,False], #对应的值为 true, false(bool值)
'origentrytype':[True,False], #对应的值为 true, false(bool值)
'origfieldval':[True,False], #对应的值为 true, false(bool值)
'overwrite':[True,False],#对应的值为 true, false(bool值)
'fieldfunction':['sethzpinyin','sethzstroke','setsentencecase','settitlecase','setuppercase',
'setlowercase','setsmallcaps','setalltitlecase','setauthoran'], #对应的值为用户指定的函数名，目前提供的函数主要是:sethzpinyin。
#在域内容处理时，当给出'fieldfunction':'sethzpinyin'选项时，程序会调用sethzpinyin函数以域内容为参数，输出其对应的拼音。'sethzstroke'设置用于排序的笔画顺序字符串。
}




#
#格式化参考文献所用的全局选项数据库
#用于检查用户设置的选项
formatoptiondatabase={
"style":['numeric','authoryear'],#这个选项目前暂无功能
"nameformat":['uppercase','lowercase','givenahead','familyahead','pinyin','reverseorder'],#姓名处理选项：uppercase,lowercase,given-family,family-given,pinyin
"citenameformat":['titlecase','uppercase'],#标注中的姓名处理选项：uppercase,titlecase
"giveninits":['space','dotspace','dot','terse','false'],#使用名的缩写，space表示名见用空格分隔，dotspace用点加空格，dot用点，terse无分隔，false不使用缩写
"useprefix":[True,False],#使用前缀名
"usesuffix":[True,False],#使用后缀名
"maxbibnames":3,#
"minbibnames":3,#
"maxcitenames":1,#
"mincitenames":1,#
"morenames":[True,False],#
"labelname":"author",#作者年制中作者标签的域的选择设置，比如['author','editor','translator','bookauthor','title'],实际是一个随意设置的列表，这里为了检查机制正常则不设为列表，因为若设为列表，就会检查值是否在database设置的范围内
"labelyear":"year",#作者年制中作者标签的域的选择设置，比如['year','endyear','urlyear']
"labelextrayear":[True,False],#是否使用bibextrayear，citeextrayear来消除姓名列表的歧义
"uniquename":['false','init','true'],#false 不对姓名消除歧义，init则仅使用名的首字母来消除，true则首先使用首字母，不行则使用全名
"uniquelist":['false','minyear','true'],#false 不对姓名消除歧义，minyear则判断时加入labelyear，true不使用year直接对列表消除歧义
"maxbibitems":1,#
"minbibitems":1,#
"moreitems":[True,False],#
"lanorder":'none',#文种排序，指定语言全面的顺序['chinese','japanese','korean','english','french','russian']
"sorting":'none',#排序，或者指定一个域列表比如['key','author','year','title']
"sortlocale":['none','pinyin','stroke','system'],#本地化排序:'none'，'pinyin'，'stroke'，'system'，none不使用，system是操作系统提供的的locale，pinyin，stroke是bibmap根据unicode-cldr实现的排序
'sortascending':[True,False],#排序使用升序还是降序，默认是升序，设置为False则为降序
"date":['year','iso','ymd'],#'日期处理选项'：year，iso，等
"urldate":['year','iso','ymd'],#'日期处理选项'：year，iso，等
"origdate":['year','iso','ymd'],#'日期处理选项'：year，iso，等
"eventdate":['year','iso','ymd'],#'日期处理选项'：year，iso，等
'caseformat':['none','sentencecase','titlecase','uppercase','lowercase','smallcaps'],#设计'none','sentencecase','titlecase','uppercase','lowercase','smallcaps'
'numberformat':['ordinal','arabic'],#设计'ordinal','arabic'
}


#
#格式化参考文献所用的域格式设置时的关键词数据库
#用于检查用户对域格式进行设置的问题
keyoptiondatabase=[
"fieldsource",
'options',
'prepunct',
'prepunctifnolastfield',
'prestringifnumber',
'posstringifnumber',
'replstring',
"posstring",
"prestring",
"omitifnofield",
"omitiffield",
'pospunct',
]

#输入文件信息的全局变量
inputbibfile=''
inputauxfile=''
inputstyfile=''
inputmapfile=''
bibliotableflag='false' #输出表格形式的参考文献表的内容的标识


#
#
#打印格式化后的全部文献条目文本
def printbibliography():
	global inputbibfile,inputauxfile,inputstyfile,inputmapfile,bibliotableflag
	global subauxfilelist,subbibfilelist,substyfilelist,submapfilelist #主文档包含的子文档的aux文件

	#md文件输出,直接用write写
	mdoutfile="newformatted"+inputbibfile.replace('.bib','.txt')
	fout = open(mdoutfile, 'w', encoding="utf8")
	print("INFO: writing cited references to '" + mdoutfile + "'")
	
	biblabelnumber=0
	newbibliographytext=copy.deepcopy(bibliographytext)
	for entrykey,prtbibentry in newbibliographytext.items():
		if len(prtbibentry)>0:
			#print(prtbibentry)
			#\allowbreak字符串的替换
			if r'\allowbreak' in prtbibentry:
				prtbibentry=re.sub(r'\\allowbreak','',prtbibentry)
			
			#\newblock字符串的替换
			if r'\newblock' in prtbibentry:
				prtbibentry=re.sub(r'\\newblock','',prtbibentry)
				
			#\url字符串的替换
			if r'\url' in prtbibentry:
				prtbibentry=re.sub(r'\\url','',prtbibentry)
				
			#\doi字符串的替换
			if r'\doi' in prtbibentry:
				prtbibentry=re.sub(r'\\doi','',prtbibentry)
			
			#print(prtbibentry)
			#sys.exit(-1)
			
			biblabelnumber=biblabelnumber+1
			fout.write('['+str(biblabelnumber)+'] '+prtbibentry+'\n')
	fout.close()
	
	#html文件输出,直接用write写
	mdoutfile="newformatted"+inputbibfile.replace('.bib','.html')
	fout = open(mdoutfile, 'w', encoding="utf8")
	print("INFO: writing cited references to '" + mdoutfile + "'")
	fout.write('<html><head><title>references</title></head>')
	fout.write('<body bgcolor="lightgray"><div align="top"><center>')
	fout.write('<font color="blue">')
	fout.write('<table border="0" cellPadding="10" cellSpacing="5" height="400" width="70%">')
	fout.write('<tr><td height="1" width="566" align="center" colspan="1" bgcolor="teal"></td></tr>')
	
	biblabelnumber=0
	for entrykey,prtbibentry in newbibliographytext.items():

		if len(prtbibentry)>0:
			
			#\allowbreak字符串的替换
			if r'\allowbreak' in prtbibentry:
				prtbibentry=re.sub(r'\\allowbreak','',prtbibentry)
			
			#\newblock字符串的替换
			if r'\newblock' in prtbibentry:
				prtbibentry=re.sub(r'\\newblock','',prtbibentry)
				
			#\url字符串的替换
			if r'\url' in prtbibentry:
				prtbibentry=re.sub(r'\\url','',prtbibentry)
				
			#\doi字符串的替换
			if r'\doi' in prtbibentry:
				prtbibentry=re.sub(r'\\doi','',prtbibentry)
			
			biblabelnumber=biblabelnumber+1
			fout.write('<tr> <td width="480" height="15" colspan="6"><font color="blue">')
			fout.write('<span style="font-family: 宋体; font-size: 14">')
			fout.write('['+str(biblabelnumber)+'] '+prtbibentry)
			fout.write('</span></font></td> </tr>')
	
	fout.write('<tr><td height="1" width="566" align="center" colspan="1" bgcolor="teal"></td></tr>')
	fout.write('</table></div></body></html>')
	fout.close()
	
	#bbl文件输出,直接用write写
	if inputauxfile:
		bblfile=inputauxfile.replace('.aux','.bbl')
	else:
		bblfile=inputbibfile.replace('.bib','.bbl')
		inputauxfile=inputbibfile.replace('.bib','.aux')
	bbloutfile=bblfile

	#写入bbl文件中
	fout = open(bbloutfile, 'w', encoding="utf8") #inputauxfile
	print("INFO: writing citation info to '" + bbloutfile + "'")
	
	entrynum=0
	for entrykey,prtbibentry in bibliographytext.items():
		entrynum+=1
		fout.write(r'\bibmapciteb{'+entrykey+'}{'+str(entrynum)+'}\n')
		#fout.write(r'\bibcite{'+entrykey+'}{'+str(entrynum)+'}\n')
	fout.close()

	
	fout = open(bbloutfile, 'a', encoding="utf8")
	print("INFO: writing cited references to '" + bbloutfile + "'")
	
	fout.write('\n'+r'\begin{thebibliography}{'+str(len(bibliographytext))+'}\n')
	
	biblabelnumber=0
	for entrykey,prtbibentry in bibliographytext.items():
		if len(prtbibentry)>0:
			biblabelnumber+=1
			
			entrykeystr=entrykey
			
			entrycitelabel=''
			#仅当'labelname'选项存在时处理
			if 'labelname' in formatoptions:
				for bibentry in bibentries:
					if bibentry['entrykey']==entrykey:
						entryciteauthor=formatlabelauthor(bibentry)
						if 'labelyear' in bibentry:
							entryciteyear=bibentry['labelyear']
						else:
							entryciteyear='N.d.'
						if 'labelextrayear' in bibentry: #formatlabelyear(bibentry)
							entryciteyear=entryciteyear+bibentry['labelextrayear']
						entrycitelabel=entryciteauthor[0]+'('+entryciteyear+')'+entryciteauthor[1]
						#Baker et~al.(1995) Baker and Jackson
						break
			
			if bibliotableflag!="false":
				#表格形式
				if 'labelname' in formatoptions:
					fout.write(r'\bibitem['+entrycitelabel+']{'+entrykeystr+r'} & '+prtbibentry+r'\\ \hline'+'\n')
				else:
					fout.write(r'\bibitem['+str(biblabelnumber)+']{'+entrykeystr+r'} & '+prtbibentry+r'\\ \hline'+'\n')
			else:	
				if 'labelname' in formatoptions:
					fout.write(r'\bibitem['+entrycitelabel+']{'+entrykeystr+'}'+prtbibentry+'\n')
				else:
					fout.write(r'\bibitem['+str(biblabelnumber)+']{'+entrykeystr+'}'+prtbibentry+'\n')
		
	fout.write(r'\end{thebibliography}')
	fout.close()



	
	





#
#authoryear样式提供标注标签的作者信息
#
def formatlabelauthor(bibentry):
	
	#从formatoptions["labelname"]获取备选域
	fieldexistflag=False
	for field in formatoptions["labelname"]:
		if field in bibentry:
			namelist=bibentry[field]
			fieldexistflag=True
			break
	if not fieldexistflag:#citation尽管使用Anon并不合适，但作为最后的手段
		return ['Anon','Anon']

	citenamelist=bibentry['labelname']
	
	#自定义标点的处理
	while r'\printdelim' in citenamelist:
		m = re.search(r'\\printdelim{([^\}]*)}',citenamelist)#注意贪婪算法的影响，所以要排除\}字符
		citenamelist=re.sub(r'\\printdelim{[^\}]*}',localpuncts[m.group(1)],citenamelist,count=1)
	
	
	#本地化字符串的处理
	while r'\bibstring' in citenamelist:
		language=languagejudgement(bibentry,citenamelist)
		m = re.search(r'\\bibstring{([^\}]*)}',citenamelist)#注意\字符的匹配，即便是在r''中也需要用\\表示
		citenamelist=re.sub(r'\\bibstring{[^\}]*}',localstrings[m.group(1)][language],citenamelist,count=1)
		
	return [citenamelist,namelist]

#
#authoryear样式提供标注标签的年份信息
#
def formatlabelyear(bibentry):
	
	#从formatoptions["labelyear"]获取备选域
	fieldexistflag=False
	for field in formatoptions["labelyear"]:
		if field in bibentry:
			yearlist=bibentry[field]
			fieldexistflag=True
			break
	if not fieldexistflag:#
		return 'N.d'
		
	return yearlist


#
#
#格式化全部文献条目文本
def formatallbibliography():
	
	global bibliographytext
	bibliographytext={}
	
	#
	#1. 将引用的文献存到一个新的列表中，便于排序
	labelnumber=0
	newbibentries=[]
	bibentrynotsame=set()
	for bibentry in bibentries:
		if bibentry["entrykey"] in usedIds or not usedIds:
			if bibentry["entrykey"] not in bibentrynotsame:
				labelnumber=labelnumber+1
				bibentry['labelnumber']=labelnumber
				bibentrynotsame.add(bibentry["entrykey"])
				newbibentries.append(bibentry)
	
	print('INFO: '+str(labelnumber)+'s references to be outputed')
	
	#
	#2. 格式化之前先处理完需要解析的范围域和日期域
	#             先处理完文献语言以及排序问题
	#
	#sortfieldlist用于保存排序的域
	sortfieldlist=[]#
	
	if formatoptions['lanorder']=='none':
		pass
	else:
		print('INFO: sorting with language as the first key')
		sortfieldlist.append('sortlang')#第一个排序域是文种，这里用sortlang来进行文种的排序
		sortlangdict={}#用于设置对应的语言的排序数字
		tempserialno=1
		for lan in formatoptions['lanorder']:
			sortlangdict[lan]=tempserialno
			tempserialno+=1
			
	sortfieldlist.append('sortkey')#第二个排序域是key/sortkey，用sortkey表示用key/sortkey进行排序
	print('INFO: sorting with sortkey as the second key')
	
	sortingflag=True #标记一下便于后面判断
	if formatoptions['sorting']=='none':#如果sorting选项不为none，那么将其设置的域作为接下来的排序域来排序
		sortingflag=False
	else:
		print('INFO: sorting with fields',formatoptions['sorting'])
		for field in formatoptions['sorting']:
			sortfieldlist.append('sort'+field)
	
	for bibentry in newbibentries:
		#
		# 由于volume和number域可能存在范围的特殊情况，首先做特殊处理
		#
		if 'volume' in bibentry:
			if '-' in bibentry['volume']:
				multivolume=bibentry['volume'].split("-")
				bibentry['volume']=multivolume[0]
				bibentry['endvolume']=multivolume[1]
		if 'number' in bibentry:
			if '-' in bibentry['number']:
				multinumber=bibentry['number'].split("-")
				bibentry['number']=multinumber[0]
				bibentry['endnumber']=multinumber[1]
		#
		#四种日期域也做范围解析
		#year本来作为不可解析的日期存放的域
		#但有时老的bib文件会把year和date混用，因此仅存在year域时也需要解析
		#将[datetype]date域解析以后，则删除这些域，仅保留[datetype]year|month|day
		if 'year' in bibentry:
			if '/' in bibentry['year']:
				datestring=bibentry['year'].split('/')
				bibentry['year']=datestring[0]
				bibentry['endyear']=datestring[1]
				#print('year=',bibentry['year'])
				#print('endyear=',bibentry['endyear'])
				
				dateparts,datetype=datetoymd(bibentry,'year')
				for k,v in dateparts.items():
					bibentry[k]=v
					
				dateparts,datetype=datetoymd(bibentry,'endyear')
				for k,v in dateparts.items():
					bibentry[k]=v
			else:
				dateparts,datetype=datetoymd(bibentry,'year')
				for k,v in dateparts.items():
					bibentry[k]=v
		
		
		if 'date' in bibentry:
			if '/' in bibentry['date']:
				datestring=bibentry['date'].split('/')
				bibentry['date']=datestring[0]
				bibentry['enddate']=datestring[1]
				#print('date=',bibentry['date'])
				#print('enddate=',bibentry['enddate'])
				
				dateparts,datetype=datetoymd(bibentry,'date')
				for k,v in dateparts.items():
					bibentry[k]=v
				dateparts,datetype=datetoymd(bibentry,'enddate')
				for k,v in dateparts.items():
					bibentry[k]=v
				del bibentry['date']
				del bibentry['enddate']
			else:
				dateparts,datetype=datetoymd(bibentry,'date')
				for k,v in dateparts.items():
					bibentry[k]=v
				del bibentry['date']
		
		if 'urldate' in bibentry:
			if '/' in bibentry['urldate']:
				datestring=bibentry['urldate'].split('/')
				bibentry['urldate']=datestring[0]
				bibentry['endurldate']=datestring[1]
				dateparts,datetype=datetoymd(bibentry,'urldate')
				for k,v in dateparts.items():
					bibentry[k]=v
				dateparts,datetype=datetoymd(bibentry,'endurldate')
				for k,v in dateparts.items():
					bibentry[k]=v
				del bibentry['urldate']
				del bibentry['endurldate']
			else:
				dateparts,datetype=datetoymd(bibentry,'urldate')
				for k,v in dateparts.items():
					bibentry[k]=v
				del bibentry['urldate']
		
		if 'eventdate' in bibentry:
			if '/' in bibentry['eventdate']:
				datestring=bibentry['eventdate'].split('/')
				bibentry['eventdate']=datestring[0]
				bibentry['endeventdate']=datestring[1]
				
				dateparts,datetype=datetoymd(bibentry,'eventdate')
				for k,v in dateparts.items():
					bibentry[k]=v
				dateparts,datetype=datetoymd(bibentry,'endeventdate')
				for k,v in dateparts.items():
					bibentry[k]=v
				del bibentry['eventdate']
				del bibentry['endeventdate']
			else:
				dateparts,datetype=datetoymd(bibentry,'eventdate')
				for k,v in dateparts.items():
					bibentry[k]=v
				del bibentry['eventdate']
		
		if 'origdate' in bibentry:
			if '/' in bibentry['origdate']:
				datestring=bibentry['origdate'].split('/')
				bibentry['origdate']=datestring[0]
				bibentry['endorigdate']=datestring[1]
				
				dateparts,datetype=datetoymd(bibentry,'origdate')
				for k,v in dateparts.items():
					bibentry[k]=v
				dateparts,datetype=datetoymd(bibentry,'endorigdate')
				for k,v in dateparts.items():
					bibentry[k]=v
				del bibentry['origdate']
				del bibentry['endorigdate']
			else:
				dateparts,datetype=datetoymd(bibentry,'origdate')
				for k,v in dateparts.items():
					bibentry[k]=v
				del bibentry['origdate']
				
		#
		#接着判断一下文献的整体语言情况，方便后面一些域格式化时的处理，当然有些域比如作者还需要根据域本身进行判断
		#
		if 'language' in bibentry:#存在language域则不做处理
			pass
		elif 'title' in bibentry:#若不存在则首先title域做判断
			language=languagejudgement(bibentry,'title')
			bibentry['language']=language
		print('language of bibentry: ',bibentry['entrykey'],' is: ',bibentry['language'])
		
	#
	#2.1 姓名列表的歧义的处理，先于排序
	#仅当'labelname'选项存在时处理
	if 'labelname' in formatoptions:
		for bibentry in newbibentries:
			
			#姓名列表标签备选域处理
			fieldlabelname=''
			for field in formatoptions['labelname']:
				if field in bibentry:
					fieldlabelname=field
					break
			if not fieldlabelname:
				print('INFO: warning label name field is not defined')
				bibentry['noauthor']='Anon'
				fieldlabelname='noauthor'
				
			#年份标签备选域处理
			fieldlabelyear=''
			for field in formatoptions['labelyear']:
				if field in bibentry:
					fieldlabelyear=field
					break
			if not fieldlabelyear:
				print('INFO: warning label name field is not defined')
				bibentry['noyear']='N.D.'
				fieldlabelyear='noyear'
				
			#先把姓名列表解析处理存储起来，便于后面处理
			bibentry['labelnameraw']=labelnamelistparser(bibentry,fieldlabelname)
			bibentry['labelyearraw']=bibentry[fieldlabelyear]
		
		#处理姓名列表的模糊问题
		newbibentries=dealambiguity(newbibentries)
		
		for bibentry in newbibentries:
			#格式化labelname，labelyear。而labelextrayear还得等排序以后才能得到
			bibentry['labelname']=labelnameformat(bibentry)
			bibentry['labelyear']=bibentry['labelyearraw']
			print('entry:',bibentry['entrykey'])
			print('labelname=',bibentry['labelname'])
			print('labelyear=',bibentry['labelyear'])
		
	
	#
	#2.2 排序的域的信息的准备
	for bibentry in newbibentries:
		#
		#接着处理排序的前期准备工作，根据全局的排序设置选项，在条目中保存排序需要的信息
		#
		if sortingflag:
			#首先处理sortlan域的信息
			if 'sortlang' in sortfieldlist:
				bibentry['sortlang']=sortlangdict[bibentry['language']]
				
			#接着处理sortkey域的信息
			if 'key' in bibentry:
				bibentry['sortkey']=bibentry['key']
			else:
				bibentry['sortkey']=''
			
			#接着处理各个排序域的信息
			for fieldsource in formatoptions['sorting']:
				if fieldsource in bibentry:
					#bibentry['sort'+field]=bibentry[field]
					
					#当域为姓名列表域时：
					if fieldsource in  datatypeinfo['namelist']:
						if 'options' in bibentry:
							options=bibentry['options']#如果条目本身具有选项
						else:
							options={}
						fieldcontents=namelistparser(bibentry,fieldsource,options)
						#自定义标点的处理
						while r'\printdelim' in fieldcontents:
							m = re.search(r'\\printdelim{([^\}]*)}',fieldcontents)#注意贪婪算法的影响，所以要排除\}字符
							fieldcontents=re.sub(r'\\printdelim{[^\}]*}',localpuncts[m.group(1)],fieldcontents,count=1)
						
					#当域为文本列表域时：
					elif fieldsource in datatypeinfo['literallist']:
						fieldcontents=literallistparser(bibentry,fieldsource)
							
					#当域为文本域时：
					elif fieldsource in  datatypeinfo['literalfield']:
						if 'options' in bibentry:
							options=bibentry['options']#如果条目本身具有选项
						else:
							options={}
						fieldcontents=literalfieldparser(bibentry,fieldsource,options)
					
					#当域为日期域时：
					elif fieldsource in  datatypeinfo['datefield']:
						fieldcontents=bibentry[fieldsource]
							
					#当域为范围域时：
					elif fieldsource in  datatypeinfo['rangefield']:
						fieldcontents=rangefieldparser(bibentry,fieldsource)
						
					else:
						fieldcontents=bibentry[fieldsource]
					
					bibentry['sort'+fieldsource]=fieldcontents
					
				else:
					bibentry['sort'+fieldsource]=''
			
	#
	#3. 接着根据排序信息对条目进行排序
	if sortingflag:
		tempsna=0
		#print('sortfieldlist=',sortfieldlist)
		sortfieldlist.reverse()#reverse()变换位置但不返回新的list
		#print('sortfieldlist=',sortfieldlist)
		#print('-------------')
		#for bibentry in newbibentries:
		#	print(tempsna,bibentry)
		
		
		#输出一下升降序信息
		if formatoptions['sortascending']:
			print('INFO: sorting in ascending order')
		else:
			print('INFO: sorting in descending order')
		
		print('INFO: sorting with locale:'+formatoptions['sortlocale'])
		if formatoptions['sortlocale']=='none':
			for sortfield in sortfieldlist:
				#print('-------------sort with',sortfield,'----------')
				#tempsna+=1
				if formatoptions['sortascending']:#升序排列
					newbibentries=sorted(newbibentries,key=lambda dict: str(dict[sortfield]))
				else:#降序排列
					newbibentries=sorted(newbibentries,key=lambda dict: str(dict[sortfield]),reverse=True)
					
		elif formatoptions['sortlocale']=='system':
			#设置locale排序
			locale.setlocale(locale.LC_COLLATE,'')
			print('INFO: sorting with local:',locale.getdefaultlocale())
			for sortfield in sortfieldlist:
				#print('-------------sort with',sortfield,'----------')
				#tempsna+=1
				if formatoptions['sortascending']:#升序排列
					newbibentries=sorted(newbibentries,key=lambda dict: locale.strxfrm(str(dict[sortfield])))
				else:#降序排列
					newbibentries=sorted(newbibentries,key=lambda dict: locale.strxfrm(str(dict[sortfield])),reverse=True)
				
				#for bibentry in newbibentries:
				#	print(tempsna,bibentry)
				
		elif formatoptions['sortlocale']=='pinyin':
			for sortfield in sortfieldlist:
				#print('-------------sort with',sortfield,'----------')
				#tempsna+=1
				if formatoptions['sortascending']:#升序排列
					newbibentries=sorted(newbibentries,key=lambda dict: comparepinyin(str(dict[sortfield])))
				else:#降序排列
					newbibentries=sorted(newbibentries,key=lambda dict: comparepinyin(str(dict[sortfield])),reverse=True)
				#for bibentry in newbibentries:
				#	print(tempsna,bibentry)
					
		elif formatoptions['sortlocale']=='stroke':
			for sortfield in sortfieldlist:
				if formatoptions['sortascending']:#升序排列
					newbibentries=sorted(newbibentries,key=lambda dict: comparestroke(str(dict[sortfield])))
				else:#降序排列
					newbibentries=sorted(newbibentries,key=lambda dict: comparestroke(str(dict[sortfield])),reverse=True)
		else:
			print('WARNING: sortlocale is not defined!')
			
	#
	#3.1 接着根据排序条目处理labelextrayear
	#仅当'labelname'选项存在时处理
	if 'labelname' in formatoptions:
		extrayearrawdict={}
		for bibentry in newbibentries:
			if 'labelextrayearraw' in bibentry:
				extrayearkey=str(bibentry['labelextrayearraw'])
				if extrayearkey not in extrayearrawdict:
					extrayearrawdict[extrayearkey]=1
					bibentry['labelextrayearraw']=1
				else:
					extrayearrawdict[extrayearkey]+=1
					bibentry['labelextrayearraw']=extrayearrawdict[extrayearkey]
		for bibentry in newbibentries:
			if 'labelextrayearraw' in bibentry:
				if isinstance(bibentry['labelextrayearraw'],int):
					bibentry['labelextrayear']=setnumberalpha(bibentry['labelextrayearraw'])
				print('labelextrayear=',bibentry['labelextrayear'])
	
	#sys.exit(-1)
		
	#
	#4. 将所有需要输出的文献进行格式化
	for bibentry in newbibentries:
		bibentrytext=''
		bibentrytext=formatbibentry(bibentry)
		bibliographytext[bibentry["entrykey"]]=bibentrytext
		
	print('\nReferecences:','\n'+'-'.center(50,'-'))
	entryidtemp=0
	for k,v in bibliographytext.items():
		entryidtemp+=1
		print('entry id=',entryidtemp,' bibtexkey="'+k+'"\n'+v,'\n'+'-'.center(50,'-'))
		
	return None

	
#
#处理uniquename=true即full选项非歧义，与dealambiguity中给出的=init的处理不同，采用另一种思路
#
def dealuniquename(sameentryset,truncnamenum,checkstart):
	'''
	返回处理过的sameentryset，如果能够处理完成，那么带有labelusedparts项
	checkstart表示从第几个姓名开始比较，一般情况下是0
	'''
	usedpartslist=[]
	labelusedparts=[]
	#几个姓名那么就有几个family
	for i in range(truncnamenum):
		labelusedparts.append(['family'])
	
	#truncnamenum*4中可能的情况
	#一个姓名一个姓名的判断，如果一个姓名足够了，那么就已经完成
	#如果一个姓名的所有情况都无法实现，那么只要比较第二个姓名即可
	for i in range(truncnamenum):
		if i>=checkstart:
			for j in range(4):
				if j==0:
					lableusedpartstemp=copy.deepcopy(labelusedparts)
					lableusedpartstemp[i].append('giveni')
					usedpartslist.append(lableusedpartstemp)
				elif j==1:
					lableusedpartstemp=copy.deepcopy(labelusedparts)
					lableusedpartstemp[i].append('giveni')
					lableusedpartstemp[i].append('middlei')
					usedpartslist.append(lableusedpartstemp)
				elif j==2:
					lableusedpartstemp=copy.deepcopy(labelusedparts)
					lableusedpartstemp[i].append('given')
					lableusedpartstemp[i].append('middlei')
					usedpartslist.append(lableusedpartstemp)
				elif j==3:
					lableusedpartstemp=copy.deepcopy(labelusedparts)
					lableusedpartstemp[i].append('given')
					lableusedpartstemp[i].append('middle')
					usedpartslist.append(lableusedpartstemp)
	print(usedpartslist)
	
	
	#
	#遍历所有的labelusedparts情况，生成label字符串，然后判断能否消除歧义
	sameentrysetnum=len(sameentryset)
	unambiguityflag=False
	for labelusedparts in usedpartslist:
		
		#
		labelnamerawstrs={}
		for bibentry in sameentryset:
		
			rawlabelnames=bibentry['labelnameraw']
			rawnamenumber=bibentry['rawnamenumber'] #labelauthor的姓名数量
			trunamenumber=truncnamenum #labelauthor的截断后姓名数量
			rawnameothers=bibentry['rawnameothers'] #labelauthor是否含有and others
			
			labelnamerawstr=''
			nameliststop=trunamenumber
			nameliststart=1
			namelistcount=0
			
			for namepartsinfo in rawlabelnames[:nameliststop]:
				namelistcount=namelistcount+1
				if namelistcount==nameliststop and namelistcount>1:#当没有others时最后一个姓名前加的标点
					
					#最后一个姓名的处理
					singlenamefmtstr=namepartsinfo['family'].lower()
					
					nameinfo=labelusedparts[-1]
					if 'giveni' in nameinfo and 'giveni' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['giveni'].lower()
					elif 'given' in nameinfo and 'given' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['given'].lower()
						
					if 'middlei' in nameinfo and 'middlei' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['middlei'].lower()
					elif 'middle' in nameinfo and 'middle' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['middle'].lower()
					
					#加入到姓名列表字符串中
					labelnamerawstr=labelnamerawstr+' '+singlenamefmtstr
					
				elif namelistcount==nameliststart:#第一个姓名

					singlenamefmtstr=namepartsinfo['family'].lower()
					
					nameinfo=labelusedparts[0]
					if 'giveni' in nameinfo and 'giveni' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['giveni'].lower()
					elif 'given' in nameinfo and 'given' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['given'].lower()
						
					if 'middlei' in nameinfo and 'middlei' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['middlei'].lower()
					elif 'middle' in nameinfo and 'middle' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['middle'].lower()
					
					#加入到姓名列表字符串中
					labelnamerawstr=labelnamerawstr+singlenamefmtstr
					
				else:
					
					singlenamefmtstr=namepartsinfo['family'].lower()
					nameinfo=labelusedparts[namelistcount-1]
					if 'giveni' in nameinfo and 'giveni' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['giveni'].lower()
					elif 'given' in nameinfo and 'given' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['given'].lower()
						
					if 'middlei' in nameinfo and 'middlei' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['middlei'].lower()
					elif 'middle' in nameinfo and 'middle' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['middle'].lower()
					
					#加入到姓名列表字符串中
					labelnamerawstr=labelnamerawstr+singlenamefmtstr
			
			#print('---1--',nameformattedstr)
			if trunamenumber < rawnamenumber or rawnameothers:
				if formatoptions['morenames']:#只有设置morenames为true是才输出other的相关信息
					labelnamerawstr=labelnamerawstr+' others'
					#print('---2--',nameformattedstr)
			
			#默认的姓名字符串保存到字典中便于判断和后面处理
			if labelnamerawstr not in labelnamerawstrs:
				labelnamerawstrs[labelnamerawstr]=[bibentry['entrykey']]
			else:
				labelnamerawstrs[labelnamerawstr].append(bibentry['entrykey'])
		
		print('labelusedparts=',labelusedparts)
		print('labelnamerawstrs=',labelnamerawstrs)
		if len(labelnamerawstrs)==sameentrysetnum:#当歧义消除时，则退出
			unambiguityflag=True
			
			for bibentry in sameentryset:
				bibentry['labelusedparts']=labelusedparts

			break
	
	return sameentryset,unambiguityflag
	

#
#处理uniquename=init选项非歧义，与dealambiguity中给出的=init的处理不同，采用另一种思路
#
def dealuniquenameinit(sameentryset,truncnamenum,checkstart):
	'''
	返回处理过的sameentryset，如果能够处理完成，那么带有labelusedparts项
	checkstart表示从第几个姓名开始比较，一般情况下是0
	'''
	usedpartslist=[]
	labelusedparts=[]
	#几个姓名那么就有几个family
	for i in range(truncnamenum):
		labelusedparts.append(['family'])
	
	#truncnamenum*4中可能的情况
	#一个姓名一个姓名的判断，如果一个姓名足够了，那么就已经完成
	#如果一个姓名的所有情况都无法实现，那么只要比较第二个姓名即可
	for i in range(truncnamenum):
		if i>= checkstart:
			for j in range(2):
				if j==0:
					lableusedpartstemp=copy.deepcopy(labelusedparts)
					lableusedpartstemp[i].append('giveni')
					usedpartslist.append(lableusedpartstemp)
				elif j==1:
					lableusedpartstemp=copy.deepcopy(labelusedparts)
					lableusedpartstemp[i].append('giveni')
					lableusedpartstemp[i].append('middlei')
					usedpartslist.append(lableusedpartstemp)
	print(usedpartslist)
	
	
	#
	#遍历所有的labelusedparts情况，生成label字符串，然后判断能否消除歧义
	sameentrysetnum=len(sameentryset)
	unambiguityflag=False
	for labelusedparts in usedpartslist:
		
		#
		labelnamerawstrs={}
		for bibentry in sameentryset:
		
			rawlabelnames=bibentry['labelnameraw']
			rawnamenumber=bibentry['rawnamenumber'] #labelauthor的姓名数量
			trunamenumber=truncnamenum #labelauthor的截断后姓名数量
			rawnameothers=bibentry['rawnameothers'] #labelauthor是否含有and others
			
			labelnamerawstr=''
			nameliststop=trunamenumber
			nameliststart=1
			namelistcount=0
			
			for namepartsinfo in rawlabelnames[:nameliststop]:
				namelistcount=namelistcount+1
				if namelistcount==nameliststop and namelistcount>1:#当没有others时最后一个姓名前加的标点
					
					#最后一个姓名的处理
					singlenamefmtstr=namepartsinfo['family'].lower()
					
					nameinfo=labelusedparts[-1]
					if 'giveni' in nameinfo and 'giveni' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['giveni'].lower()
						
					if 'middlei' in nameinfo and 'middlei' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['middlei'].lower()
					
					#加入到姓名列表字符串中
					labelnamerawstr=labelnamerawstr+' '+singlenamefmtstr
					
				elif namelistcount==nameliststart:#第一个姓名

					singlenamefmtstr=namepartsinfo['family'].lower()
					
					nameinfo=labelusedparts[0]
					if 'giveni' in nameinfo and 'giveni' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['giveni'].lower()
						
					if 'middlei' in nameinfo and 'middlei' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['middlei'].lower()
					
					#加入到姓名列表字符串中
					labelnamerawstr=labelnamerawstr+singlenamefmtstr
					
				else:
					
					singlenamefmtstr=namepartsinfo['family'].lower()
					nameinfo=labelusedparts[namelistcount-1]
					if 'giveni' in nameinfo and 'giveni' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['giveni'].lower()
						
					if 'middlei' in nameinfo and 'middlei' in namepartsinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['middlei'].lower()
					
					#加入到姓名列表字符串中
					labelnamerawstr=labelnamerawstr+singlenamefmtstr
			
			#print('---1--',nameformattedstr)
			if trunamenumber < rawnamenumber or rawnameothers:
				if formatoptions['morenames']:#只有设置morenames为true是才输出other的相关信息
					labelnamerawstr=labelnamerawstr+' others'
					#print('---2--',nameformattedstr)
			
			#默认的姓名字符串保存到字典中便于判断和后面处理
			if labelnamerawstr not in labelnamerawstrs:
				labelnamerawstrs[labelnamerawstr]=[bibentry['entrykey']]
			else:
				labelnamerawstrs[labelnamerawstr].append(bibentry['entrykey'])
				
		if len(labelnamerawstrs)==sameentrysetnum:#当歧义消除时，则退出
			unambiguityflag=True
			
			for bibentry in sameentryset:
				bibentry['labelusedparts']=labelusedparts

			break
	
	return sameentryset,unambiguityflag
	
#
#处理uniquelist即无论是minyear，还是true都是一样的逻辑
#
def dealuniquelist(sameentryset,truncnamenum):
	'''
	返回处理过的sameentryset，如果能够处理完成，那么带有labelusedparts项，以及增加的truncnamenum数
	'''
	
	labelusedparts=[]
	#几个姓名那么就有几个family
	for i in range(truncnamenum):
		labelusedparts.append(['family'])
		
	print('truncnamenum=',truncnamenum)
	
	unambiguityflag=False
	sameentrysetnum=len(sameentryset)
	while truncnamenum<sameentryset[0]['rawnamenumber']:
		truncnamenum=truncnamenum+1
			
		if formatoptions['uniquename']=='init':
			sameentryset,unambiguityflag=dealuniquenameinit(sameentryset,truncnamenum,truncnamenum-1)
			
		elif formatoptions['uniquename']=='true':
			print('truncnamenum=',truncnamenum)
			sameentryset,unambiguityflag=dealuniquename(sameentryset,truncnamenum,truncnamenum-1)
			
		else: 
			labelnamerawstrs={}
			labelusedparts.append(['family'])
			for bibentry in sameentryset:
				labelnamerawstr=namepartsinfo['family'].lower()
				#默认的姓名字符串保存到字典中便于判断和后面处理
				if labelnamerawstr not in labelnamerawstrs:
					labelnamerawstrs[labelnamerawstr]=[bibentry['entrykey']]
				else:
					labelnamerawstrs[labelnamerawstr].append(bibentry['entrykey'])
					
				if len(labelnamerawstrs)==sameentrysetnum:#当歧义消除时，则退出
					unambiguityflag=True
					
					for bibentry in sameentryset:
						bibentry['labelusedparts']=labelusedparts
					break
		
		if unambiguityflag:
			for bibentry in sameentryset:
				bibentry['trunamenumber']=truncnamenum
			break
	
	return sameentryset,unambiguityflag
	
#
#处理姓名列表的模糊问题
def dealambiguity(newbibentries):

	#1. 先citation中的处理，bib中是类似的处理
	#1.1 根据基本选项判断原始状态下是否需要存在有歧义的文献
	labelnamerawstrs={}
	for bibentry in newbibentries:
		
		#1. 计算姓名原始总数和截断后的总数
		rawlabelnames=bibentry['labelnameraw']
		rawnameothers=False
		if 'morename' in rawlabelnames[-1]:
			rawnamenumber=len(rawlabelnames)-1
			rawnameothers=True
		else:
			rawnamenumber=len(rawlabelnames)
		if rawnamenumber > formatoptions['maxcitenames']:
			trunamenumber=formatoptions['mincitenames']
		else:
			trunamenumber=rawnamenumber
		
		#记录一下信息
		bibentry['rawnamenumber']=rawnamenumber #记录labelauthor的姓名数量
		bibentry['trunamenumber']=trunamenumber #记录labelauthor的截断后姓名数量
		bibentry['rawnameothers']=rawnameothers #记录labelauthor是否含有and others

		#截断后的姓名列表构成一个字符串，用于相同判断	
		labelnamerawstr=''		
		j=0
		for namepartsinfo in rawlabelnames:
			if j<trunamenumber:#在截断的范围内
				labelnamerawstr=labelnamerawstr+namepartsinfo['family'].lower()+" "
			else:#之外，则判断一下是否还有姓名，有的话加上others
				if rawnameothers or rawnamenumber>trunamenumber:
					labelnamerawstr=labelnamerawstr+'other'
				break #仅做一次就够了
			j=j+1
				
		
		#默认的姓名字符串保存到字典中便于判断和后面处理
		if labelnamerawstr not in labelnamerawstrs:
			labelnamerawstrs[labelnamerawstr]=[bibentry['entrykey']]
		else:
			labelnamerawstrs[labelnamerawstr].append(bibentry['entrykey'])
	
	#
	#1.2 对产生歧义的文献进行处理
	labelnamerawstrsb=labelnamerawstrs #labelnamerawstrs后面要用到，因为直接复制的代码，所以这里换一个存一下
	for k,v in labelnamerawstrsb.items():
		if len(v)>1:#当list>1，那么存在相同的
		
			#显示一下信息
			print(v)
			print(k)
			
			#记录有歧义的条目，放到一起，便于处理
			samenamestring=k
			sameentrysetnum=len(v)
			sameentryset=[]
			for entrykeya in v:
				for bibentry in newbibentries:
					if entrykeya==bibentry['entrykey']:
						print(bibentry['labelnameraw'])
						sameentryset.append(bibentry)
			
			unambiguityflag=False
			
			#
			#1.2.1 处理非歧义:首先根据uniquename选项考虑
			if formatoptions['uniquename']=='false':
				pass
			elif formatoptions['uniquename']=='init':
				
				#用list来记录可以消除歧义时，使用的姓名成分
				labelusedparts=[]
				truncnamenum=sameentryset[0]['trunamenumber']
				for i in range(truncnamenum):
					labelusedparts.append(['family'])
				print('labelusedparts=',labelusedparts)
				
				#根据截断姓名的数量逐个处理姓名使其非歧义
				for i in range(truncnamenum):
					#print('i=',i)
					labelnamerawstrs={}
					labelusedparts[i].append('giveni')
					for bibentry in sameentryset:
						rawnamenumber=bibentry['rawnamenumber']
						trunamenumber=bibentry['trunamenumber']
						rawnameothers=bibentry['rawnameothers']
						rawlabelnames=bibentry['labelnameraw']
						
						labelnamerawstr=''
						j=0
						for namepartsinfo in rawlabelnames:
							if j<trunamenumber:#在截断的范围内
								labelnamerawstr=labelnamerawstr+namepartsinfo['family'].lower()+" "
								if 'giveni' in namepartsinfo:
									labelnamerawstr=labelnamerawstr+namepartsinfo['giveni'].lower()+" "
							else:#之外，则判断一下是否还有姓名，有的话加上others
								if rawnameothers or rawnamenumber>trunamenumber:
									labelnamerawstr=labelnamerawstr+'other'
								break #仅做一次就够了
							j=j+1
						
						#默认的姓名字符串保存到字典中便于判断和后面处理
						if labelnamerawstr not in labelnamerawstrs:
							labelnamerawstrs[labelnamerawstr]=[bibentry['entrykey']]
						else:
							labelnamerawstrs[labelnamerawstr].append(bibentry['entrykey'])
						
					if len(labelnamerawstrs)==sameentrysetnum:#当歧义消除时，则退出
						unambiguityflag=True
						break
					else:
						labelnamerawstrs={}
						labelusedparts[i].append('middlei')
						for bibentry in sameentryset:
							rawnamenumber=bibentry['rawnamenumber']
							trunamenumber=bibentry['trunamenumber']
							rawnameothers=bibentry['rawnameothers']
							rawlabelnames=bibentry['labelnameraw']
							
							labelnamerawstr=''
							j=0
							for namepartsinfo in rawlabelnames:
								if j<trunamenumber:#在截断的范围内
									labelnamerawstr=labelnamerawstr+namepartsinfo['family'].lower()+" "
									if 'giveni' in namepartsinfo:
										labelnamerawstr=labelnamerawstr+namepartsinfo['giveni'].lower()+" "
									if 'middlei' in namepartsinfo:
										labelnamerawstr=labelnamerawstr+namepartsinfo['middlei'].lower()+' '
								else:#之外，则判断一下是否还有姓名，有的话加上others
									if rawnameothers or rawnamenumber>trunamenumber:
										labelnamerawstr=labelnamerawstr+'other'
									break #仅做一次就够了
								j=j+1
							
							#默认的姓名字符串保存到字典中便于判断和后面处理
							if labelnamerawstr not in labelnamerawstrs:
								labelnamerawstrs[labelnamerawstr]=[bibentry['entrykey']]
							else:
								labelnamerawstrs[labelnamerawstr].append(bibentry['entrykey'])
						
						if len(labelnamerawstrs)==sameentrysetnum:#当歧义消除时，则退出
							unambiguityflag=True
							break
						
					print('unambiguityflag=',unambiguityflag)
					print('labelusedparts=',labelusedparts)
				
				if unambiguityflag:
					for bibentry in sameentryset:
						bibentry['labelusedparts']=labelusedparts
					
					#替换处理完的条目，用于返回
					for bibentry in sameentryset:
						k=0
						for bibentrya in newbibentries:
							if bibentrya["entrykey"]==bibentry["entrykey"]:
								del newbibentries[k]
								newbibentries.insert(k,bibentry)
							k=k+1
					print('INFO: uniquename based unambiguity seceed!!')
					continue
					
			elif formatoptions['uniquename']=='true':
				
				#与前一个选项的实现逻辑略有不同，使用dealuniquename函数实现
				#前一个选项也可以用dealuniquename实现，只是之前已经调试完毕，那种逻辑也就留下来
				truncnamenum=sameentryset[0]['trunamenumber']
				sameentryset,unambiguityflag=dealuniquename(sameentryset,truncnamenum,0)
				
				if unambiguityflag:
					#替换处理完的条目，用于返回
					for bibentry in sameentryset:
						k=0
						for bibentrya in newbibentries:
							if bibentrya["entrykey"]==bibentry["entrykey"]:
								del newbibentries[k]
								newbibentries.insert(k,bibentry)
							k=k+1
					print('INFO: uniquename based unambiguity seceed!!')
					continue
					
				#print(sameentryset)
				#sys.exit(-1)
		
			#
			#1.2.2 处理非歧义: 接着根据uniquelist选项考虑
			if formatoptions['uniquelist']=='false':
				
				if not unambiguityflag:#使用uniquelist无法消除歧义
					for bibentry in sameentryset:
						bibentry['labelextrayearraw']=v #将相同作者的条目记录下来，便于后面排序的时候处理处合适的extrayear值，比如a，b，c等。
				else:
					pass
				
				#替换处理完的条目，用于返回
				for bibentry in sameentryset:
					k=0
					for bibentrya in newbibentries:
						if bibentrya["entrykey"]==bibentry["entrykey"]:
							del newbibentries[k]
							newbibentries.insert(k,bibentry)
						k=k+1
				
				
				
			elif formatoptions['uniquelist']=='minyear':
				labelnamerawstrs={}
				for bibentry in sameentryset:
					labelnamerawstr=''
					labelnamerawstr=samenamestring+bibentry['labelyearraw']
					
					#默认的姓名字符串保存到字典中便于判断和后面处理
					if labelnamerawstr not in labelnamerawstrs:
						labelnamerawstrs[labelnamerawstr]=[bibentry['entrykey']]
					else:
						labelnamerawstrs[labelnamerawstr].append(bibentry['entrykey'])
				
				if len(labelnamerawstrs)==sameentrysetnum:#当歧义消除时，则退出
					unambiguityflag=True
					print('INFO: uniquelist minyear based unambiguity seceed!!')
					continue
				
				sameentryset,unambiguityflag=dealuniquelist(sameentryset,truncnamenum)
				
				if not unambiguityflag:#使用uniquelist无法消除歧义
					for bibentry in sameentryset:
						bibentry['labelextrayearraw']=v #将相同作者的条目记录下来，便于后面排序的时候处理处合适的extrayear值，比如a，b，c等。
				else:
					print('INFO: uniquelist based unambiguity seceed!!')
					
				#替换处理完的条目，用于返回
				for bibentry in sameentryset:
					k=0
					for bibentrya in newbibentries:
						if bibentrya["entrykey"]==bibentry["entrykey"]:
							del newbibentries[k]
							newbibentries.insert(k,bibentry)
						k=k+1
				
			elif formatoptions['uniquelist']=='true':
			
				sameentryset,unambiguityflag=dealuniquelist(sameentryset,truncnamenum)
				
				print('unambiguityflag=',unambiguityflag)
				print(sameentryset)
				
				#sys.exit(-1)
				
				if not unambiguityflag:#使用uniquelist无法消除歧义
					for bibentry in sameentryset:
						bibentry['labelextrayearraw']=v #将相同作者的条目记录下来，便于后面排序的时候处理处合适的extrayear值，比如a，b，c等。
				else:
					print('INFO: uniquelist based unambiguity seceed!!')
					
				#替换处理完的条目，用于返回
				for bibentry in sameentryset:
					k=0
					for bibentrya in newbibentries:
						if bibentrya["entrykey"]==bibentry["entrykey"]:
							del newbibentries[k]
							newbibentries.insert(k,bibentry)
						k=k+1
				
			else:
				print("INFO: option value for uniquelist is not defined!")
	
	
	for bibentryc in newbibentries:
		print(bibentryc,'\n')
	
	return newbibentries
	
#
#将数字顺序转换为字母顺序
def setnumberalpha(number):
	numa=ord('a')
	if number >= 0:
		numb=numa+number-1
		numalpha=chr(numb)
	elif number > 25:
		print('WARNING: number is too big')
	else:
		print('WARNING: number is negtive')
	return numalpha
	
	
#
#
#label姓名列表解析
#label姓名列表的选项仅使用全局选项
def labelnamelistparser(bibentry,fieldsource):
	fieldcontents=bibentry[fieldsource]
	
	#首先做针对{}保护的处理
	#{}有可能保护一部分，有可能保护全部
	#首先判断{}是否存在，若存在，那么可以确定需要做保护处理，否则用常规处理
	#当然这些事情可以在一个函数中处理

	#首先姓名列表进行分解，包括用' and '和' AND '做分解
	#利用safetysplit函数实现安全的分解
	seps=[' and ',' AND ']
	fieldcontents=fieldcontents.strip()
	fieldauthors=safetysplit(fieldcontents,seps)

	#print('fieldauthors:',fieldauthors)
	
	#接着从各个姓名得到更详细的分解信息
	fieldnames=[]
	for name in fieldauthors:
		if name.lower() == 'others':
			nameinfo={'morename':True}
		else:
			if fieldlanguage(name)=='chinese':#当中文姓名中存在逗号先去除
				if ', ' in name:
					name=name.replace(', ','')
			else:
				pass
			nameinfo=singlenameparser(name)
		fieldnames.append(nameinfo)
	
	return fieldnames


	
#
#
#格式化labelname
def labelnameformat(bibentry):
	'''
	逻辑如下:
	1. 首先根据trunnamenumber确定所要使用的姓名数
	2. 根据labelusedparts给出使用的姓名成分
	3. 最后根据trunnamenumber和rawnnamenumber以及rawnameothers来给出etal或等
	'''
		
	if 'citenameformat' in formatoptions:#label仅使用全局的选项
		nameformat=formatoptions['citenameformat']
	else:#最后使用默认的选项
		nameformat='titlecase'
		
	if 'giveninits' in formatoptions:#label仅使用全局的选项
		giveninits=formatoptions['giveninits']
	else:#最后使用默认的选项
		giveninits='space'
	
	rawlabelnames=bibentry['labelnameraw']
	rawnamenumber=bibentry['rawnamenumber'] #labelauthor的姓名数量
	trunamenumber=bibentry['trunamenumber'] #labelauthor的截断后姓名数量
	rawnameothers=bibentry['rawnameothers'] #labelauthor是否含有and others
	if 'labelusedparts' in bibentry:
		labelusedparts=bibentry['labelusedparts']
	else:
		labelusedparts=False
		
	
	nameformattedstr=''
	nameliststop=trunamenumber
	nameliststart=1
	namelistcount=0
	
	for namepartsinfo in rawlabelnames[:nameliststop]:
		namelistcount=namelistcount+1
		if namelistcount==nameliststop and namelistcount>1:#当没有others时最后一个姓名前加的标点
			
			#单个姓名的处理
			if nameformat=='uppercase':
				singlenamefmtstr=namepartsinfo['family'].upper()
			else:
				singlenamefmtstr=namepartsinfo['family'].title()
			
			#labelusedparts的存在表示处理过歧义问题
			if labelusedparts:
				#根据选项确定使用名的缩写
				nameinfo=labelusedparts[-1]
				if giveninits=='space':#space表示名见用空格分隔，
					if 'giveni' in nameinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['giveni'].upper()
				elif giveninits=='dotspace':#dotspace用点加空格，
					if 'giveni' in nameinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['giveni'].upper()+'.'
				elif giveninits=='dot':#dot用点，
					if 'giveni' in nameinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['giveni'].upper()+'.'
				elif giveninits=='terse':#terse无分隔，
					if 'giveni' in nameinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['giveni'].upper()
				elif giveninits=='false' or giveninits==False:#false不使用缩写
					if 'given' in nameinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['given'].upper()
						
				#根据选项确定使用名的缩写
				if giveninits=='space':#space表示名见用空格分隔，
					if 'middlei' in nameinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['middlei'].upper()
				elif giveninits=='dotspace':#dotspace用点加空格，
					if 'middlei' in nameinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['middlei'].upper()+'.'
				elif giveninits=='dot':#dot用点，
					if 'middlei' in nameinfo:
						singlenamefmtstr=singlenamefmtstr+namepartsinfo['middlei'].upper()+'.'
				elif giveninits=='terse':#terse无分隔，
					if 'middlei' in nameinfo:
						singlenamefmtstr=singlenamefmtstr+namepartsinfo['middlei'].upper()
				elif giveninits=='false' or giveninits==False:#false不使用缩写
					if 'middle' in nameinfo:
						singlenamefmtstr=singlenamefmtstr+' '+namepartsinfo['middle'].upper()
			
			#加入到姓名列表字符串中
			nameformattedstr=nameformattedstr+r'\printdelim{finalnamedelim}'+singlenamefmtstr
			
		elif namelistcount==nameliststart:#第一个姓名
			#单个姓名的处理
			if nameformat=='uppercase':
				labelnamerawstr=namepartsinfo['family'].upper()
			else:
				labelnamerawstr=namepartsinfo['family'].title()
			#加入到姓名列表字符串中
			nameformattedstr=nameformattedstr+labelnamerawstr
		else:
			#单个姓名的处理
			if nameformat=='uppercase':
				labelnamerawstr=namepartsinfo['family'].upper()
			else:
				labelnamerawstr=namepartsinfo['family'].title()
			#加入到姓名列表字符串中
			nameformattedstr=nameformattedstr+r'\printdelim{multinamedelim}'+labelnamerawstr
	
	#print('---1--',nameformattedstr)
	if trunamenumber < rawnamenumber or rawnameothers:
		if formatoptions['morenames']:#只有设置morenames为true是才输出other的相关信息
			nameformattedstr=nameformattedstr+r'\printdelim{andothorsdelim}\bibstring{andothers}'
			#print('---2--',nameformattedstr)
		
	return nameformattedstr
	

#
#
#用于输出字符串对应拼音顺序的字符串
def comparepinyin(stra):
	strb=''
	for chari in stra:
		if chari in sqpinyindata:
			strb=strb+'字'+str(hex(sqpinyindata.index(chari)+4096))#加字是为了避免与西文字符混淆
		else:
			strb=strb+chari
	return strb

#
#
#用于输出字符串对应笔画顺序的字符串	
def comparestroke(stra):
	strb=''
	for chari in stra:
		if chari in sqstrokedata:
			strb=strb+'字'+str(hex(sqstrokedata.index(chari)+4096)) #用一个统一的16进制数来表示一个子的顺序是巧妙的设计
		else:
			strb=strb+chari
	return strb

#
#
#用于设置字符串的拼音字符串		
def sethzpinyin(stra):
	strb=''
	for chari in stra:
		if chari in hzpinyindata:
			strb=strb+str(hzpinyindata[chari])
			#print(strb)
		else:
			strb=strb+str(chari)
			#print(strb)
	return strb

#
#
#用于设置字符串的笔画顺序字符串		
def sethzstroke(stra):
	strb=''
	for chari in stra:
		if str(chari) in sqstrokedata:
			strb=strb+str(hex(sqstrokedata.index(chari)+4096))
		else:
			strb=strb+str(chari)
	return strb
	
#
#
#格式化一个文献条目文本
def formatbibentry(bibentry):
	
	#print('--------------new entry---------')
	#print('\nbibentry:',bibentry)
	#bibentrytext='entry:'
	
	#
	#1. 首先处理所有域到一个条目文本
	#
	bibentrytext=''
	
	if bibentry['entrytype'] in bibliographystyle:
		print('INFO: format style of entrytype "'+bibentry['entrytype']+'" is defined.')
		if isinstance(bibliographystyle[bibentry['entrytype']],str):
			formattype=bibliographystyle[bibentry['entrytype']]
		else:
			formattype=bibentry['entrytype']
		
		lastfield=True #前一域存在
		
		for fieldinfo in bibliographystyle[formattype]:
			
			rtnfield=formatfield(bibentry,fieldinfo,lastfield)
			fieldtext=rtnfield[0]
			lastfield=rtnfield[1]
			
			bibentrytext=bibentrytext+fieldtext
	
	#2. 对替换字符串做处理
	#	包括对重复的标点做处理比如：..变为.
	for k,v in replacestrings.items():
		#print(k,v)
		#m=re.search(k,bibentrytext)
		#print(m)
		#bibentrytext=re.sub(k,v,bibentrytext)
		#利用正则反而不行，直接用字符串替换
		bibentrytext=bibentrytext.replace(k,v)
	
	#print(bibentrytext)
	return bibentrytext



#
#
#格式化文献条目的域
#不同类型的域不同处理
#分5类：姓名列表，文本列表，文本域，日期域，范围域
#其中姓名列表，文本列表，日期域，日期域，范围域，都需要进行特殊的解析
#而volume，number如果需要特殊解析则在文件域的格式处理时增加新的处理逻辑。
def formatfield(bibentry,fieldinfo,lastfield):

	#print('fieldinfo:',fieldinfo)
	
	#首先把域的内容先解析处理
	fieldcontents=''
	
	fieldsource=None

	#首先判断域是否忽略
	#false表示不忽略
	#首先假设为不忽略
	#omitifnofield:必须所有的域都不存在才为true
	#omitiffield:只要存在一个域就为true
	fieldomit=False
	
	if 'omitifnofield' in fieldinfo and 'omitiffield' in fieldinfo:

		fieldomita=True#假设忽略的条件满足,即需要不存在的域都不能存在
		for field in fieldinfo['omitifnofield']:
			if field in bibentry:#只要需要不存在的域有一个存在，那么条件就不满足
				fieldomita=False
				break
		#print('fieldomita=',fieldomita)

		fieldomitb=False#假设忽略的条件不满足
		for field in fieldinfo['omitiffield']:
			if field in bibentry:#只要需要存在的域中有一个存在，那么条件就满足
				fieldomitb=True
				break
		#print('fieldomitb=',fieldomitb)

		fieldomit=fieldomita and fieldomitb
		
	elif 'omitifnofield' in fieldinfo:
		
		fieldomit=True#假设忽略的条件满足
		for field in fieldinfo['omitifnofield']:
			if field in bibentry:#只要需要不存在的域有一个存在，那么条件就不满足
				fieldomit=False
				break
		#print('fieldomitc=',fieldomit)
		
	elif 'omitiffield' in fieldinfo:
		
		fieldomit=False#假设忽略的条件不满足
		for field in fieldinfo['omitiffield']:
			if field in bibentry:#只要需要存在的域中有一个存在，那么条件就满足
				fieldomit=True
				break
		#print('fieldomitd=',fieldomit)
	
	#print('fieldomit=',fieldomit)
	
	
	#如果不忽略该域那么：
	if not fieldomit:
		
		#当域为姓名列表域时：
		if fieldinfo['fieldsource'][0] in  datatypeinfo['namelist']:
			#print('0',fieldinfo['fieldsource'][0])
			#print('author' in bibentry)
			for field in fieldinfo['fieldsource']:#
				#print(fieldinfo['fieldsource'])
				#print('namelist:',field)
				if field in bibentry:#当域存在于条目中时，确定要处理的域
					fieldsource=field
					break
			if fieldsource:
				#传递条目给出的一些控制选项
				if 'options' in fieldinfo:
					options=fieldinfo['options']
				else:
					options={}
				fieldcontents=namelistparser(bibentry,fieldsource,options)
			
		
		#当域为文本列表域时：
		elif fieldinfo['fieldsource'][0] in  datatypeinfo['literallist']:

			for field in fieldinfo['fieldsource']:#
				if field in bibentry:#当域存在于条目中时，确定要处理的域
					fieldsource=field
					break
			if fieldsource:
				fieldcontents=literallistparser(bibentry,fieldsource)
				
		#当域为文本域时：
		
		elif fieldinfo['fieldsource'][0] in  datatypeinfo['literalfield']:
			#print('fieldinfo=',fieldinfo)
			#print('bibentry=',bibentry)
			for field in fieldinfo['fieldsource']:#
				#print('field=',field)
				if field in bibentry:#当域存在于条目中时，确定要处理的域
					fieldsource=field
					break
			#print('fieldsource=',fieldsource)
			if fieldsource:
				#传递条目给出的一些控制选项
				if 'options' in fieldinfo:
					options=fieldinfo['options']
				else:
					options={}
				fieldcontents=literalfieldparser(bibentry,fieldsource,options)
				
		
		#当域为日期域时：
		elif fieldinfo['fieldsource'][0] in  datatypeinfo['datefield']:

			for field in fieldinfo['fieldsource']:#
				datetype=field.replace('date','')
			
				if datetype+'year' in bibentry:#当datetype+'year'存在于条目中时则跳出处理
					fieldsource=field
					break
					
			if fieldsource:#这里因为给出的选项时datetype+date的所以，仍然用filedsource传递信息。
				#传递条目给出的一些控制选项
				if 'options' in fieldinfo:
					options=fieldinfo['options']
				else:
					options={}
				fieldcontents=datefieldparser(bibentry,fieldsource,datetype,options)
				
				
		#当域为范围域时：
		elif fieldinfo['fieldsource'][0] in  datatypeinfo['rangefield']:

			for field in fieldinfo['fieldsource']:#
				if field in bibentry:#当域存在域条目中时，确定要处理的域
					fieldsource=field
					break
			if fieldsource:
				fieldcontents=rangefieldparser(bibentry,fieldsource)
				
		#当域为其它类型时，通常是虚设的域
		else:
			#print('this filed is used to replace')
			fieldsource=None
			
	
	#当所需的域不存在，且当前著录项不应忽略时，那么做替换处理
	if not fieldsource and not fieldomit:
		if 'replstring' in fieldinfo and fieldinfo['replstring']:
			#print('replstring')
			fieldsource=True
			fieldcontents=fieldinfo['replstring']
			
	
	#接着做进一步的格式化，包括标点，格式，字体等
	fieldtext=''
	
	#print(fieldsource)
	if fieldsource:
		#前置标点输出
		if lastfield:#当前一个著录项存在，则正常输出
			if 'prepunct' in fieldinfo:
				fieldtext=fieldtext+fieldinfo['prepunct']
		else:#当前一个著录项不存在，则首先输出'prepunctifnolastfield'
			if 'prepunctifnolastfield' in fieldinfo:
				fieldtext=fieldtext+fieldinfo['prepunctifnolastfield']
			elif 'prepunct' in fieldinfo:
				fieldtext=fieldtext+fieldinfo['prepunct']
		
		#前置字符串输出
		if 'prestringifnumber' in fieldinfo:
			try:
				numtemp=int(bibentry[fieldsource])#这里仅对域本身的内容判断
				if  isinstance(numtemp,int):
					fieldtext=fieldtext+fieldinfo['prestringifnumber']
			except:
				print('INFO: the field value can not convert to integer when deal prestringifnumber')
		
		if 'prestring' in fieldinfo:
			fieldtext=fieldtext+fieldinfo['prestring']
		
		#域格式加入
		if 'fieldformat' in fieldinfo:
			fieldtext=fieldtext+'{'+fieldinfo['fieldformat']+'{'+fieldcontents+'}}'
		else:
			fieldtext=fieldtext+str(fieldcontents)
		
		#后置字符串输出
		if 'posstring' in fieldinfo:
			fieldtext=fieldtext+fieldinfo['posstring']
			
		if 'posstringifnumber' in fieldinfo:
			try:
				numtemp=int(bibentry[fieldsource])#这里仅对域本身的内容判断
				if  isinstance(numtemp,int):
					fieldtext=fieldtext+fieldinfo['posstringifnumber']
			except:
				print('INFO: the field value can not convert to integer when deal posstringifnumber')
		
		#后置标点输出
		if 'pospunct' in fieldinfo:
			fieldtext=fieldtext+fieldinfo['pospunct']
			
		#更新lastfiled
		lastfield=True
	else:
		lastfield=False
	
	
	#自定义标点的处理
	#print('fieldtext:',fieldtext)
	while r'\printdelim' in fieldtext:
		m = re.search(r'\\printdelim{([^\}]*)}',fieldtext)#注意贪婪算法的影响，所以要排除\}字符
		#print('m.group(1):',m.group(1))
		fieldtext=re.sub(r'\\printdelim{[^\}]*}',localpuncts[m.group(1)],fieldtext,count=1)
		#print('fieldtext:',fieldtext)
	
	
	#本地化字符串的处理
	#print('fieldtext:',fieldtext)
	while r'\bibstring' in fieldtext:
		language=languagejudgement(bibentry,fieldsource)
		m = re.search(r'\\bibstring{([^\}]*)}',fieldtext)#注意\字符的匹配，即便是在r''中也需要用\\表示
		fieldtext=re.sub(r'\\bibstring{[^\}]*}',localstrings[m.group(1)][language],fieldtext,count=1)
		#print('fieldtext:',fieldtext)
		#下面这句不行因为，在字典取值是，不支持\1这样的正则表达式
		#fieldtext=re.sub(r'\\bibstring{(.*)}',localstrings[r'\1'][language],fieldtext,count=1)
	
	#标题的类型和载体标识符的处理
	if r'\typestring' in fieldtext:#当需要处理类型和载体时
		if bibentry['entrytype'] in typestrings:#当条目对应的类型存在时
			#print(r'\typestring in',fieldtext)
			typestring=typestrings[bibentry['entrytype']]
			if 'url' in bibentry:
				typestring=typestring.replace(']','/OL]')
			elif 'medium' in bibentry:
				rplctypestring=bibentry['medium']+']'
				typestring=typestring.replace(']',rplctypestring)
		else:#当条目对应的类型不存在时，当做其它类型处理
			typestring='[Z]'

		#print(typestring)
		fieldtext=fieldtext.replace(r'\typestring',typestring)
		
	return [fieldtext,lastfield]





#
#根据作者域或者标题域确定条目的语言
#
def languagejudgement(bibentry,fieldsource):

	if fieldsource in datatypeinfo['namelist']:#当域是作者类时，利用作者域本身信息做判断
	
		language=fieldlanguage(bibentry[fieldsource])
		
	else:#其它情况，利用title域做判断
		if 'title' in bibentry:
			language=fieldlanguage(bibentry['title'])
		elif 'author' in bibentry:
			language=fieldlanguage(bibentry['author'])
		else:
			language='english'
		
	return language
	

#
#根据域值所在的字符范围确定域的语言
#
def fieldlanguage(fieldvalueinfo):
	
	#要特别注意re中match，fullmatch，search之间的差异
	#match是只匹配从头开始的内容，若头不匹配，则不匹配
	#fullmatch则是全部字符串匹配，若有一处不匹配，则不匹配
	#search则是搜索匹配的字符串的位置，若有匹配，则范围位置，否则返回None
	if re.search(r'[\u2FF0-\u9FA5]', fieldvalueinfo):
		language='chinese'
	elif re.search(r'[\u3040-\u30FF\u31F0-\u31FF]', fieldvalueinfo):
		language='japanese'
	elif re.search(r'[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7AF]', fieldvalueinfo):
		language='korean'
	elif re.search(r'[\u0400-\u052F]', fieldvalueinfo):
		language='russian'
	elif re.search(r'[\u0100-\u017F]', fieldvalueinfo):
		language='french'
	else:
		language='english'
	
	return language


#
#
#对存在{}做保护的字符串进行分割
def safetysplit(strtosplt,seps):
	
	#首先查找{}保护的所有字符串
	s1=re.findall('\{.*?\}',strtosplt)
	
	#接着确定保护字符串中是否存在分割用字符串
	sepinbrace=False
	for s1a in s1:
		for sep in seps:
			if sep in s1a:
				sepinbrace=True
				break
		if sepinbrace:
			break
	#print(sepinbrace)
			
	#若保护字符串中存在分割字符串那么做特殊处理		
	a=strtosplt
	if sepinbrace:
		
		#保护字符串用特殊字符串代替，特殊字符串与分割字符串没有任何关联
		strsn=0
		for stra1 in s1:
			strsn=strsn+1
			a=a.replace(stra1,'$'+str(strsn)+'$')
		#print(a)
		
		#处理原字符串为只需要一个分隔字符串就能分隔
		if len(seps)>1:
			for i in range(1,len(seps)):
				a=a.replace(seps[i],seps[0])
			#print(a)
		
		#接着做分割
		names=a.split(seps[0])
		#print(names)
		
		#对分割后的字符串做还原，即把特殊字符串还原回保护字符串
		namesnew=[]
		for name in names:#去掉因为分割而产生的空字符
			if name.strip():
				strsn=0
				for stra1 in s1:
					strsn=strsn+1
					name=name.replace('$'+str(strsn)+'$',stra1)
				#print(name)
				namesnew.append(name.strip())
		
	else:
		#处理原字符串为只需要一个分隔字符串就能分隔
		if len(seps)>1:
			for i in range(1,len(seps)):
				a=a.replace(seps[i],seps[0])
			#print(a)
		
		#直接分割
		names=a.split(seps[0])
		namesnew=[]
		for name in names:
			if name.strip():#去掉因为分割而产生的空字符
				namesnew.append(name.strip())
		
	#print(namesnew)
	return namesnew

	
#
#
#姓名列表解析:用于标注
#增加条目给出的选项
def citenamelistparser(bibentry,fieldsource,options):
	fieldcontents=bibentry[fieldsource]
	
	#首先做针对{}保护的处理
	#{}有可能保护一部分，有可能保护全部
	#首先判断{}是否存在，若存在，那么可以确定需要做保护处理，否则用常规处理
	#当然这些事情可以在一个函数中处理

	#首先姓名列表进行分解，包括用' and '和' AND '做分解
	#利用safetysplit函数实现安全的分解
	seps=[' and ',' AND ']
	fieldcontents=fieldcontents.strip()
	fieldauthors=safetysplit(fieldcontents,seps)

	#print('fieldauthors:',fieldauthors)
	
	#接着从各个姓名得到更详细的分解信息
	fieldnames=[]
	for name in fieldauthors:
		if name.lower() == 'others':
			nameinfo={'morename':True}
		else:
			if fieldlanguage(name)=='chinese':#当中文姓名中存在逗号先去除
				if ', ' in name:
					name=name.replace(', ','')
			else:
				pass
			nameinfo=singlenameparser(name)
		fieldnames.append(nameinfo)
	
	#最后根据全局和局部选项进行格式化
	nameformattedstr=''
	
	#根据'maxcitenames'和'mincitenames'截短
	if 'maxcitenames' in options:#首先使用条目中的选项
		if len(fieldnames)>options['maxcitenames']:
			fieldnamestrunc=fieldnames[:options['mincitenames']]
			nameinfo={'morename':True}
			fieldnamestrunc.append(nameinfo)
		else:
			fieldnamestrunc=fieldnames
	elif 'maxcitenames' in formatoptions:#接着使用全局选项
		if len(fieldnames)>formatoptions['maxcitenames']:
			fieldnamestrunc=fieldnames[:formatoptions['mincitenames']]
			nameinfo={'morename':True}
			fieldnamestrunc.append(nameinfo)
		else:
			fieldnamestrunc=fieldnames
	else:
		fieldnamestrunc=fieldnames
	
	
	#这里根据条目本身的信息，以及条目类型的格式设置中的信息来确定姓名的格式选项
	#姓名四个选项：nameformat，giveninits作为主要的设置选项，可以在文献条目内容中设置，也可以在类型选项中设置，也可以全局设置
	#usesuffix和morenames则仅做全局设置
	if 'citenameformat' in bibentry:#当bib中条目本身存在存在域'nameformat'
		option={'citenameformat':bibentry['citenameformat']}
	elif 'citenameformat' in options:#当条目类型选项中存在域'nameformat'
		option={'citenameformat':options['citenameformat']}
	else:
		option={}
		
	
	#print('fieldnamestrunc:',fieldnamestrunc)
	nameliststop=len(fieldnamestrunc)
	nameliststart=1
	namelistcount=0
	for nameinfo in fieldnamestrunc:
		namelistcount=namelistcount+1
		if 'morename' in nameinfo:
			if formatoptions['morenames']:#只有设置morenames为true是才输出other的相关信息
				nameformattedstr=nameformattedstr+r'\printdelim{andothorsdelim}\bibstring{andothers}'
		else:
			if namelistcount==nameliststop and namelistcount>1:#当没有others时最后一个姓名前加的标点
				nameformattedstr=nameformattedstr+r'\printdelim{finalnamedelim}'+citesinglenameformat(nameinfo,option)
			elif namelistcount==nameliststart:
				nameformattedstr=singlenameformat(nameinfo,option)
			else:
				nameformattedstr=nameformattedstr+r'\printdelim{multinamedelim}'+citesinglenameformat(nameinfo,option)
	
	return nameformattedstr
	
	
	
#
#
#单个姓名格式化
def citesinglenameformat(nameinfo,option):
	
	singlenamefmtstr=''
		
	if 'citenameformat' in option:#首先使用bib中条目本身和条目类型给出的选项
		nameformat=option['citenameformat']
	elif 'citenameformat' in formatoptions:#接着使用全局的选项
		nameformat=formatoptions['citenameformat']
	else:#最后使用默认的选项
		nameformat='titlecase'
	

	#根据单个姓名格式化选项来实现具体的格式
	if nameformat=='uppercase':
		
		if 'prefix' in nameinfo:
			singlenamefmtstr=nameinfo['prefix'].title()
		else:
			singlenamefmtstr=''
		
		if nameinfo['family'].startswith('{'):
			singlenamefmtstr=singlenamefmtstr+nameinfo['family']
		else:
			singlenamefmtstr=singlenamefmtstr+nameinfo['family'].upper()
				
		#根据选项确定使用后缀
		if formatoptions["usesuffix"]:#
			if 'suffix' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+', '+nameinfo['suffix']

	elif nameformat=='titlecase':
	
		if 'prefix' in nameinfo:
			singlenamefmtstr=nameinfo['prefix'].title()
		else:
			singlenamefmtstr=''
		
		#
		if nameinfo['family'].startswith('{'):
			singlenamefmtstr=singlenamefmtstr+nameinfo['family']
		else:
			singlenamefmtstr=singlenamefmtstr+nameinfo['family'].title()
			
		#根据选项确定使用后缀
		if formatoptions["usesuffix"]:#
			if 'suffix' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+', '+nameinfo['suffix'].title()
		
	else:
		print('WARNING: value of option citenameformat: '+nameformat+' is not defined!!')
	
	return singlenamefmtstr

	
	
#
#
#姓名列表解析
#增加条目给出的选项
def namelistparser(bibentry,fieldsource,options):
	fieldcontents=bibentry[fieldsource]
	
	#首先做针对{}保护的处理
	#{}有可能保护一部分，有可能保护全部
	#首先判断{}是否存在，若存在，那么可以确定需要做保护处理，否则用常规处理
	#当然这些事情可以在一个函数中处理

	#首先姓名列表进行分解，包括用' and '和' AND '做分解
	#利用safetysplit函数实现安全的分解
	seps=[' and ',' AND ']
	fieldcontents=fieldcontents.strip()
	fieldauthors=safetysplit(fieldcontents,seps)

	#print('fieldauthors:',fieldauthors)
	
	#接着从各个姓名得到更详细的分解信息
	fieldnames=[]
	for name in fieldauthors:
		if name.lower() == 'others':
			nameinfo={'morename':True}
		else:
			if fieldlanguage(name)=='chinese':#当中文姓名中存在逗号先去除
				if ', ' in name:
					name=name.replace(', ','')
			else:
				pass
			nameinfo=singlenameparser(name)
		fieldnames.append(nameinfo)
	
	#最后根据全局和局部选项进行格式化
	nameformattedstr=''
	
	#根据'maxbibnames'和'minbibnames'截短
	if 'maxbibnames' in options:#首先使用条目中的选项
		if len(fieldnames)>options['maxbibnames']:
			fieldnamestrunc=fieldnames[:options['minbibnames']]
			nameinfo={'morename':True}
			fieldnamestrunc.append(nameinfo)
		else:
			fieldnamestrunc=fieldnames
	elif 'maxbibnames' in formatoptions:#接着使用全局选项
		if len(fieldnames)>formatoptions['maxbibnames']:
			fieldnamestrunc=fieldnames[:formatoptions['minbibnames']]
			nameinfo={'morename':True}
			fieldnamestrunc.append(nameinfo)
		else:
			fieldnamestrunc=fieldnames
	else:
		fieldnamestrunc=fieldnames
	
	
	#这里根据条目本身的信息，以及条目类型的格式设置中的信息来确定姓名的格式选项
	#姓名四个选项：nameformat，giveninits作为主要的设置选项，可以在文献条目内容中设置，也可以在类型选项中设置，也可以全局设置
	#usesuffix和morenames则仅做全局设置
	if 'nameformat' in bibentry:#当bib中条目本身存在存在域'nameformat'
		option={'nameformat':bibentry['nameformat']}
	elif 'nameformat' in options:#当条目类型选项中存在域'nameformat'
		option={'nameformat':options['nameformat']}
	else:
		option={}
		
	if 'giveninits' in bibentry:#当bib中条目本身存在存在域'nameformat'
		option['giveninits']=bibentry['giveninits']
	elif 'giveninits' in options:#当条目类型选项中存在域'nameformat'
		option['giveninits']=options['giveninits']
	else:
		pass
	
	#print('fieldnamestrunc:',fieldnamestrunc)
	nameliststop=len(fieldnamestrunc)
	nameliststart=1
	namelistcount=0
	for nameinfo in fieldnamestrunc:
		namelistcount=namelistcount+1
		if 'morename' in nameinfo:
			if formatoptions['morenames']:#只有设置morenames为true是才输出other的相关信息
				nameformattedstr=nameformattedstr+r'\printdelim{andothorsdelim}\bibstring{andothers}'
		else:
			if namelistcount==nameliststop and namelistcount>1:#当没有others时最后一个姓名前加的标点
				nameformattedstr=nameformattedstr+r'\printdelim{finalnamedelim}'+singlenameformat(nameinfo,option)
			elif namelistcount==nameliststart:
				nameformattedstr=singlenameformat(nameinfo,option)
			else:
				nameformattedstr=nameformattedstr+r'\printdelim{multinamedelim}'+singlenameformat(nameinfo,option)
	
	return nameformattedstr


#
#
#单个姓名格式化
def singlenameformat(nameinfo,option):
	
	singlenamefmtstr=''
		
	if 'nameformat' in option:#首先使用bib中条目本身和条目类型给出的选项
		nameformat=option['nameformat']
	elif 'nameformat' in formatoptions:#接着使用全局的选项
		nameformat=formatoptions['nameformat']
	else:#最后使用默认的选项
		nameformat='uppercase'
	
	if 'giveninits' in option:#首先使用bib中条目本身和条目类型给出的选项
		giveninits=option['giveninits']
	elif 'giveninits' in formatoptions:#接着使用全局的选项
		giveninits=formatoptions['giveninits']
	else:#最后使用默认的选项
		giveninits='space'
	
	
	#根据单个姓名格式化选项来实现具体的格式
	if nameformat=='uppercase':
		
		if 'prefix' in nameinfo and formatoptions["useprefix"]:
			singlenamefmtstr=nameinfo['prefix'].title()+' '
		else:
			singlenamefmtstr=''
		
		if nameinfo['family'].startswith('{'):
			singlenamefmtstr=singlenamefmtstr+nameinfo['family']
		else:
			singlenamefmtstr=singlenamefmtstr+nameinfo['family'].upper()
		
		#根据选项确定使用名的缩写
		if giveninits=='space':#space表示名见用空格分隔，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middlei'].upper()
		elif giveninits=='dotspace':#dotspace用点加空格，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+'. '+nameinfo['middlei'].upper()+'.'
		elif giveninits=='dot':#dot用点，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+'.'+nameinfo['middlei'].upper()+'.'
		elif giveninits=='terse':#terse无分隔，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+nameinfo['middlei'].upper()
		elif giveninits=='false' or giveninits==False:#false不使用缩写
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['given'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middle'].upper()
				
		#根据选项确定使用后缀
		if formatoptions["usesuffix"]:#
			if 'suffix' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+', '+nameinfo['suffix']

	elif nameformat=='lowercase':
	
		if 'prefix' in nameinfo and formatoptions["useprefix"]:
			singlenamefmtstr=nameinfo['prefix'].title()+' '
		else:
			singlenamefmtstr=''
		
		#不管有没有保护，都不做字母大小写修改
		singlenamefmtstr=singlenamefmtstr+nameinfo['family']
		
		#根据选项确定使用名的缩写
		#当使用名的首字母缩写时大写
		#否则不做字母大小写变化
		if giveninits=='space':#space表示名见用空格分隔，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middlei'].upper()
		elif giveninits=='dotspace':#dotspace用点加空格，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+'. '+nameinfo['middlei'].upper()+'.'
		elif giveninits=='dot':#dot用点，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+'.'+nameinfo['middlei'].upper()+'.'
		elif giveninits=='terse':#terse无分隔，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+nameinfo['middlei'].upper()
		elif giveninits=='false' or giveninits==False:#false不使用缩写
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['given']
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middle']
				
		#根据选项确定使用后缀
		if formatoptions["usesuffix"]:#
			if 'suffix' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+', '+nameinfo['suffix']
	
		
	elif nameformat=='given-family':
		
		#given在前的不使用前缀
		
		#根据选项确定使用名的缩写
		#当使用名的首字母缩写时大写
		#否则不做字母大小写变化
		if giveninits=='space':#space表示名见用空格分隔，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middlei'].upper()
		elif giveninits=='dotspace':#dotspace用点加空格，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+nameinfo['giveni'].upper()+'.'
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middlei'].upper()+'.'
		elif giveninits=='dot':#dot用点，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+nameinfo['giveni'].upper()+'.'
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+nameinfo['middlei'].upper()+'.'
		elif giveninits=='terse':#terse无分隔，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+nameinfo['middlei'].upper()
		elif giveninits=='false' or giveninits==False:#false不使用缩写
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+nameinfo['given']
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middle']
				
		#不管有没有保护，都不做字母大小写修改
		singlenamefmtstr=singlenamefmtstr+' '+nameinfo['family']
		
		#根据选项确定使用后缀
		if formatoptions["usesuffix"]:#
			if 'suffix' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+', '+nameinfo['suffix']
		
	elif nameformat=='family-given':
	
		if 'prefix' in nameinfo and formatoptions["useprefix"]:
			singlenamefmtstr=nameinfo['prefix'].title()+' '
		else:
			singlenamefmtstr=''
		
		#不管有没有保护，都把姓设置为titlecase模式
		singlenamefmtstr=singlenamefmtstr+nameinfo['family'].title()
		
		#根据选项确定使用名的缩写
		#当使用名的首字母缩写时大写
		#否则不做字母大小写变化
		if giveninits=='space':#space表示名见用空格分隔，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middlei'].upper()
		elif giveninits=='dotspace':#dotspace用点加空格，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+'. '+nameinfo['middlei'].upper()+'.'
		elif giveninits=='dot':#dot用点，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+'.'+nameinfo['middlei'].upper()+'.'
		elif giveninits=='terse':#terse无分隔，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+nameinfo['middlei'].upper()
		elif giveninits=='false' or giveninits==False:#false不使用缩写
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['given']
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middle']
		
		#根据选项确定使用后缀
		if formatoptions["usesuffix"]:#
			if 'suffix' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+', '+nameinfo['suffix']
		
	elif nameformat=='pinyin':
	
		#pinyin不使用前缀、后缀
		
		#不管有没有保护，都把姓设置为uppercase模式
		singlenamefmtstr=nameinfo['family'].upper()
		
		#拼音模式不考虑姓名的缩写，直接使用全名
		#given用titlecase，middle用lowercase，中间加-
		if 'given' in nameinfo:
			singlenamefmtstr=singlenamefmtstr+' '+nameinfo['given'].title()
		if 'middle' in nameinfo:
			singlenamefmtstr=singlenamefmtstr+'-'+nameinfo['middle'].lower()
		
	elif nameformat=='reverseorder':
		
		if namelistcount==1:#第一个姓名用family-given
		
			if 'prefix' in nameinfo and formatoptions["useprefix"]:
				singlenamefmtstr=nameinfo['prefix'].title()+' '
			else:
				singlenamefmtstr=''
			
			#不管有没有保护，都把姓设置为titlecase模式
			singlenamefmtstr=singlenamefmtstr+nameinfo['family'].title()
			
			#根据选项确定使用名的缩写
			#当使用名的首字母缩写时大写
			#否则不做字母大小写变化
			if giveninits=='space':#space表示名见用空格分隔，
				if 'given' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
				if 'middle' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middlei'].upper()
			elif giveninits=='dotspace':#dotspace用点加空格，
				if 'given' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
				if 'middle' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+'. '+nameinfo['middlei'].upper()+'.'
			elif giveninits=='dot':#dot用点，
				if 'given' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
				if 'middle' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+'.'+nameinfo['middlei'].upper()+'.'
			elif giveninits=='terse':#terse无分隔，
				if 'given' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
				if 'middle' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+nameinfo['middlei'].upper()
			elif giveninits=='false' or giveninits==False:#false不使用缩写
				if 'given' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+' '+nameinfo['given']
				if 'middle' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middle']
					
			#根据选项确定使用后缀
			if formatoptions["usesuffix"]:#
				if 'suffix' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+', '+nameinfo['suffix']
			
		else:#后面的姓名全部用given-family
			#根据选项确定使用名的缩写
			#当使用名的首字母缩写时大写
			#否则不做字母大小写变化
			if giveninits=='space':#space表示名见用空格分隔，
				if 'given' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+nameinfo['giveni'].upper()
				if 'middle' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middlei'].upper()
			elif giveninits=='dotspace':#dotspace用点加空格，
				if 'given' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+nameinfo['giveni'].upper()+'.'
				if 'middle' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middlei'].upper()+'.'
			elif giveninits=='dot':#dot用点，
				if 'given' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+nameinfo['giveni'].upper()+'.'
				if 'middle' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+nameinfo['middlei'].upper()+'.'
			elif giveninits=='terse':#terse无分隔，
				if 'given' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+nameinfo['giveni'].upper()
				if 'middle' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+nameinfo['middlei'].upper()
			elif giveninits=='false' or giveninits==False:#false不使用缩写
				if 'given' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+nameinfo['given']
				if 'middle' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middle']
					
			#不管有没有保护，都不做字母大小写修改
			singlenamefmtstr=singlenamefmtstr+' '+nameinfo['family']
			
			#根据选项确定使用后缀
			if formatoptions["usesuffix"]:#
				if 'suffix' in nameinfo:
					singlenamefmtstr=singlenamefmtstr+', '+nameinfo['suffix']

	else:
		print('WARNING: value of option nameformat: '+nameformat+' is not defined!!')
	
	return singlenamefmtstr


#
#
#单个姓名解析
def singlenameparser(name):
	
	singlename=name
	
	#print('name:',name)
	
	#字典用于存储所有的姓名成分信息
	namepartsinfo={}
	
	nameparts=safetysplit(singlename,[','])
	
	if len(nameparts)==3:#两个逗号的情况，表示存在family和suffix
		
		prefixfamily=safetysplit(nameparts[0].strip(),[' '])
		if len(prefixfamily)>1:
			namepartsinfo['prefix']=prefixfamily[0].strip()
			namepartsinfo['family']=prefixfamily[1].strip()
		else:
			namepartsinfo['family']=prefixfamily[0].strip()
			
		namepartsinfo['suffix']=nameparts[1].strip()
		
		
		givenmiddle=safetysplit(nameparts[2].strip(),[' '])
		if len(givenmiddle)>1:
			namepartsinfo['given']=givenmiddle[0].strip()
			namepartsinfo['middle']=givenmiddle[1].strip()
		else:
			namepartsinfo['given']=givenmiddle[0].strip()
		
	elif len(nameparts)==2:#1个逗号的情况，表示存在family
		
		prefixfamily=safetysplit(nameparts[0].strip(),[' '])
		if len(prefixfamily)>1:
			namepartsinfo['prefix']=prefixfamily[0].strip()
			namepartsinfo['family']=prefixfamily[1].strip()
		else:
			namepartsinfo['family']=prefixfamily[0].strip()
			
		
		givenmiddle=safetysplit(nameparts[1].strip(),[' '])
		if len(givenmiddle)>1:
			namepartsinfo['given']=givenmiddle[0].strip()
			namepartsinfo['middle']=givenmiddle[1].strip()
		else:
			namepartsinfo['given']=givenmiddle[0].strip()
		
	else:
		givenmiddlefamily=safetysplit(nameparts[0].strip(),[' '])
		if len(givenmiddlefamily)==3:
			namepartsinfo['given']=givenmiddlefamily[0].strip()
			namepartsinfo['middle']=givenmiddlefamily[1].strip()
			namepartsinfo['family']=givenmiddlefamily[2].strip()
		elif len(givenmiddlefamily)==2:
			namepartsinfo['given']=givenmiddlefamily[0].strip()
			namepartsinfo['family']=givenmiddlefamily[1].strip()
		elif len(givenmiddlefamily)==1:
			namepartsinfo['family']=givenmiddlefamily[0].strip()
	
	
	#print('nameparts:',namepartsinfo)
	
	if 'family' in namepartsinfo:
		if namepartsinfo['family'].startswith('{'):
			namepartsinfo['familyi']=namepartsinfo['family']
		else:
			namepartsinfo['familyi']=namepartsinfo['family'][0].upper()
	
	if 'given' in namepartsinfo:
		#print(namepartsinfo['given'])
		if namepartsinfo['given'].startswith('{'):
			namepartsinfo['giveni']=namepartsinfo['given']
		else:
			namepartsinfo['giveni']=namepartsinfo['given'][0].upper()
		
	if 'middle' in namepartsinfo:
		if namepartsinfo['middle'].startswith('{'):
			namepartsinfo['middle']=namepartsinfo['middle']
		else:
			namepartsinfo['middlei']=namepartsinfo['middle'][0].upper()
		
	return namepartsinfo

#
#
#文本列表解析
def literallistparser(bibentry,fieldsource):
	fieldcontents=bibentry[fieldsource]
	
	
	#首先从文本列表分解出各个项，包括用' and '和' AND '做分解
	#利用safetysplit函数实现安全的分解
	seps=[' and ',' AND ']
	fieldcontents=fieldcontents.strip()
	fielditems=safetysplit(fieldcontents,seps)
	
	#print('fielditems:',fielditems)
	
	#根据'maxbibitems'和'minbibitems'截短
	fielditemstrunc=[]
	
	if len(fielditems)>formatoptions['maxbibitems']:
		fielditemstrunc=fielditems[:formatoptions['minbibitems']]
		fielditemstrunc.append('others')
	else:
		fielditemstrunc=fielditems
	
	#重设一下others的大小写，因为可能输入的时大写的
	if fielditems[-1].lower() == 'others':
		fielditems[-1]='others'
	
	#最后根据全局和局部选项进行格式化
	itemliststop=len(fielditemstrunc)
	itemliststart=1
	itemlistcount=0
	itemformattedstr=''
	for iteminfo in fielditemstrunc:
		itemlistcount=itemlistcount+1
		if iteminfo == 'others':
			if formatoptions['moreitems']:#只有设置moreitems为true是才输出other的相关信息
				itemformattedstr=itemformattedstr+r'\printdelim{andothorsdelim}\bibstring{andothers}'
		else:
			if itemlistcount==itemliststop and itemlistcount>1:#当没有others时最后一个项前加标点
				itemformattedstr=itemformattedstr+r'\printdelim{finalitemdelim}'+iteminfo
			elif itemlistcount==itemliststart:
				itemformattedstr=iteminfo
			else:
				itemformattedstr=itemformattedstr+r'\printdelim{multiitemdelim}'+iteminfo
	
	return itemformattedstr

#
#
#文本域解析
def literalfieldparser(bibentry,fieldsource,options):
	
	#主要是要处理options选项
	#numberformat
	numberformat=''
	if 'numberformat' in bibentry:#首先使用bib中条目信息给出的选项
		numberformat=bibentry['numberformat']
	elif 'numberformat' in options:#接着使用条目类型格式化设置给出的选项
		numberformat=options['numberformat']
	elif 'numberformat' in formatoptions:#接着使用全局的选项
		numberformat=formatoptions['numberformat']
	
	#caseformat
	caseformat='none'
	if 'caseformat' in bibentry:#首先使用bib中条目信息给出的选项
		caseformat=bibentry['caseformat']
	elif 'caseformat' in options:#接着使用条目类型格式化设置给出的选项
		caseformat=options['caseformat']
	elif 'caseformat' in formatoptions:#接着使用全局的选项
		caseformat=formatoptions['caseformat']
	
	
	if numberformat:#当存在数字选项时处理
		fieldstring=bibentry[fieldsource]
		#print('fieldstring=',fieldstring)
		
		fieldisint=False
		try:
			fieldisint=isinstance(int(fieldstring),int)
		except:
			print('INFO: WARNING '+fieldsource+' is not a number')
		
		if fieldisint:#如果域信息是数字，那么做处理
			if numberformat=='arabic':
				fieldcontents=str(int(fieldstring))
			elif numberformat=='ordinal':
				if bibentry['language']=='english':#英文需要注意序号的表示问题0th，1st，2nd，3rd，4-都是th
					remainder=int(fieldstring)%10
					if remainder==1:
						fieldcontents=str(int(fieldstring))+'st'
					elif remainder==2:
						fieldcontents=str(int(fieldstring))+'nd'
					elif remainder==3:
						fieldcontents=str(int(fieldstring))+'rd'
					else:
						fieldcontents=str(int(fieldstring))+'th'
				else:
					fieldcontents=str(int(fieldstring))
				
		
		else:#否则原样输出
			fieldcontents=bibentry[fieldsource]
	else:#否则原样输出
		fieldcontents=bibentry[fieldsource]
	
	#大小写模式处理
	if caseformat:
		if caseformat=='none':
			pass
		elif caseformat=='sentencecase':
			fieldcontents=mkstrsetencecase(fieldcontents)
		elif caseformat=='titlecase':
			fieldcontents=mkstrtitlecase(fieldcontents)
		elif caseformat=='uppercase':
			fieldcontents=mkstruppercase(fieldcontents)
		elif caseformat=='lowercase':
			fieldcontents=mkstrlowercase(fieldcontents)
		elif caseformat=='smallcaps':
			fieldcontents=mkstrsmallcaps(fieldcontents)

	return fieldcontents


#2021-05-27,v1.0c,hzz
#为"fieldfunction"增加字符串的case变换的函数
def setsentencecase(fieldstring):
	return mkstrsetencecase(fieldstring)

def setalltitlecase(fieldstring):
	return mkstrtitlecase(fieldstring)

def settitlecase(fieldstring):
	return mkstrtitlecasestd(fieldstring)

def setuppercase(fieldstring):
	return mkstruppercase(fieldstring)

def setlowercase(fieldstring):
	return mkstrlowercase(fieldstring)

def setsmallcaps(fieldstring):
	return mkstrsmallcaps(fieldstring)	


def setauthoran(fieldvtoset,fieldstring,matchstring):
	return mkstrauthoran(fieldvtoset,fieldstring,matchstring)

#
#功能是根据matchstring判断其在fieldstring中作者的序号，然后设置annotation信息
def mkstrauthoran(fieldvtoset,fieldstring,matchstring):
	print("mkstrauthoran:",fieldvtoset,fieldstring,matchstring)
	sall=fieldstring.lower().split(" and ")
	print('sall:',sall)
	sm=matchstring.lower()
	idx=0
	for s in sall:
		idx+=1
		if sm==s:
			sout="{}=".format(idx)+fieldvtoset
			break
	return sout


#
#处理字符串的大小写的函数:
#其中对{}做了保护
#对\和{之间的字符做了保护
def mkstrsetencecase(fieldstring):
	#首先查找{}保护的所有字符串
	s0=re.findall(r'\\.*?\{.*?\}',fieldstring)
	
	a=fieldstring
	if s0:
		strsn=0
		for stra1 in s0:
			strsn=strsn+1
			a=a.replace(stra1,'$'+str(strsn)+'$')

	s1=re.findall('\{.*?\}',a)
	
	if s1:
		#保护字符串用特殊字符串代替，特殊字符串与分割字符串没有任何关联
		strsn=len(s0)
		for stra1 in s1:
			strsn=strsn+1
			a=a.replace(stra1,'$'+str(strsn)+'$')
	
	#对字符串做大小写变换:
	a1=a[0].upper()
	a2=a[1:].lower()
	a=a1+a2
      
	#对字符串做还原	  
	if s1:
		strsn=len(s0)
		for stra1 in s1:
			strsn=strsn+1
			a=a.replace('$'+str(strsn)+'$',stra1)
	
	if s0:
		strsn=0
		for stra1 in s0:
			strsn=strsn+1
			a=a.replace('$'+str(strsn)+'$',stra1)

	strtoreturn=a
	return strtoreturn


#
#增加对介词等进行保护
def mkstrtitlecasestd(fieldstring):
	#查找命令和{}保护的所有字符串
	#思路是存储信息并利用替换进行保护

	#保护:命令
	s0=re.findall(r'\\.*?\{.*?\}',fieldstring)
	
	a=fieldstring
	if s0:
		strsn=0
		for stra1 in s0:
			strsn=strsn+1
			a=a.replace(stra1,'$'+str(strsn)+'$')

	#保护:{}内容
	s1=re.findall('\{.*?\}',a)
	
	if s1:
		#保护字符串用特殊字符串代替，特殊字符串与分割字符串没有任何关联
		strsn=len(s0)
		for stra1 in s1:
			strsn=strsn+1
			a=a.replace(stra1,'$'+str(strsn)+'$')
	
	#需要保护的字符串，如介词、连词等
	#主要是：不在句首的冠词、介词、连词和作为不定式的to
	protectstr=['a','an','the', 'for', 'and', 'nor', 'but', 'or', 'yet', 'so', 'on','in','of','and','to', 'at','around','by','after','along','for','from','with','without']
	ndtransstr=['A','An','The', 'For', 'And', 'Nor', 'But', 'Or', 'Yet', 'So', 'On','In','Of','And','To', 'At','Around','By','After','Along','For','From','With','Without']


	#对字符串做大小写变换:
	b=a.split(" ")
	c=[]
	for s2 in b:
		if s2 in protectstr:
			c.append(s2)
		elif s2 in ndtransstr:
			c.append(s2.lower())
		else:
			c.append(s2.title())
	c[0]=c[0].title()
	a=" ".join(c)
	#a=a.title()
      
	#对字符串做还原	  
	if s1:
		strsn=len(s0)
		for stra1 in s1:
			strsn=strsn+1
			a=a.replace('$'+str(strsn)+'$',stra1)
	
	if s0:
		strsn=0
		for stra1 in s0:
			strsn=strsn+1
			a=a.replace('$'+str(strsn)+'$',stra1)
			
	strtoreturn=a
	return strtoreturn

#
#没有对介词等进行保护
def mkstrtitlecase(fieldstring):
	#首先查找{}保护的所有字符串
	s0=re.findall(r'\\.*?\{.*?\}',fieldstring)
	
	a=fieldstring
	if s0:
		strsn=0
		for stra1 in s0:
			strsn=strsn+1
			a=a.replace(stra1,'$'+str(strsn)+'$')

	s1=re.findall('\{.*?\}',a)
	
	if s1:
		#保护字符串用特殊字符串代替，特殊字符串与分割字符串没有任何关联
		strsn=len(s0)
		for stra1 in s1:
			strsn=strsn+1
			a=a.replace(stra1,'$'+str(strsn)+'$')
	
	#对字符串做大小写变换:
	a=a.title()
      
	#对字符串做还原	  
	if s1:
		strsn=len(s0)
		for stra1 in s1:
			strsn=strsn+1
			a=a.replace('$'+str(strsn)+'$',stra1)
	
	if s0:
		strsn=0
		for stra1 in s0:
			strsn=strsn+1
			a=a.replace('$'+str(strsn)+'$',stra1)
			
	strtoreturn=a
	return strtoreturn

def mkstruppercase(fieldstring):

	#首先查找{}保护的所有字符串
	s0=re.findall(r'\\.*?\{.*?\}',fieldstring)
	
	a=fieldstring
	if s0:
		strsn=0
		for stra1 in s0:
			strsn=strsn+1
			a=a.replace(stra1,'$'+str(strsn)+'$')

	s1=re.findall('\{.*?\}',a)
	
	if s1:
		#保护字符串用特殊字符串代替，特殊字符串与分割字符串没有任何关联
		strsn=len(s0)
		for stra1 in s1:
			strsn=strsn+1
			a=a.replace(stra1,'$'+str(strsn)+'$')
	
	#对字符串做大小写变换:
	a=a.upper()
      
	#对字符串做还原	  
	if s1:
		strsn=len(s0)
		for stra1 in s1:
			strsn=strsn+1
			a=a.replace('$'+str(strsn)+'$',stra1)
	
	if s0:
		strsn=0
		for stra1 in s0:
			strsn=strsn+1
			a=a.replace('$'+str(strsn)+'$',stra1)
			
	strtoreturn=a
	return strtoreturn	

def mkstrlowercase(fieldstring):
	#首先查找{}保护的所有字符串
	s0=re.findall(r'\\.*?\{.*?\}',fieldstring)
	
	a=fieldstring
	if s0:
		strsn=0
		for stra1 in s0:
			strsn=strsn+1
			a=a.replace(stra1,'$'+str(strsn)+'$')

	s1=re.findall('\{.*?\}',a)
	
	if s1:
		#保护字符串用特殊字符串代替，特殊字符串与分割字符串没有任何关联
		strsn=len(s0)
		for stra1 in s1:
			strsn=strsn+1
			a=a.replace(stra1,'$'+str(strsn)+'$')
	
	#对字符串做大小写变换:
	a=a.lower()
      
	#对字符串做还原	  
	if s1:
		strsn=len(s0)
		for stra1 in s1:
			strsn=strsn+1
			a=a.replace('$'+str(strsn)+'$',stra1)
	
	if s0:
		strsn=0
		for stra1 in s0:
			strsn=strsn+1
			a=a.replace('$'+str(strsn)+'$',stra1)
	
	strtoreturn=a
	return strtoreturn	

def mkstrsmallcaps(fieldstring):
	#首先查找{}保护的所有字符串
	s0=re.findall(r'\\.*?\{.*?\}',fieldstring)
	
	a=fieldstring
	if s0:
		strsn=0
		for stra1 in s0:
			strsn=strsn+1
			a=a.replace(stra1,'$'+str(strsn)+'$')

	s1=re.findall('\{.*?\}',a)
	
	if s1:
		#保护字符串用特殊字符串代替，特殊字符串与分割字符串没有任何关联
		strsn=len(s0)
		for stra1 in s1:
			strsn=strsn+1
			a=a.replace(stra1,'$'+str(strsn)+'$')
	
	#对字符串做大小写变换:
	a1=a[0].upper()
	a2=a[1:]
	a=a1+r'\textsc{'+a2+'}'
      
	#对字符串做还原	  
	if s1:
		strsn=len(s0)
		for stra1 in s1:
			strsn=strsn+1
			a=a.replace('$'+str(strsn)+'$',stra1)
	
	if s0:
		strsn=0
		for stra1 in s0:
			strsn=strsn+1
			a=a.replace('$'+str(strsn)+'$',stra1)
		
	strtoreturn=a
	return strtoreturn	
		

#
#
#日期域解析
#条目设置的选项options:
def datefieldparser(bibentry,fieldsource,datetype,options):
	
	#print('bibentry=',bibentry)
	#print('fieldsource=',fieldsource)
	#print('datetype=',datetype)
	#print('options=',options)
	
	#获取日期信息：
	#因为所有的date都已经解析为y，m，d
	dateparts={}
	dtyear=datetype+'year'
	if dtyear in bibentry:
		dateparts[dtyear]=bibentry[dtyear]
	dtmonth=datetype+'month'
	if dtmonth in bibentry:
		dateparts[dtmonth]=bibentry[dtmonth]
	dtday=datetype+'day'
	if dtday in bibentry:
		dateparts[dtday]=bibentry[dtday]
	#print(dateparts)
	
	#判断解析的年月日是不是整数，若不是则表示日期不可解析
	#做此判断便于后面原样输出不可解析的year
	datecanbeparse=True
	for k,v in dateparts.items():
		try:
			datepartisint=isinstance(int(v),int)
		except:
			print('INFO: WARNING '+fieldsource+' of entry "'+bibentry['entrykey']+'" can not be parsed')
			datecanbeparse=False
			break
		
	
	#然后根据全局选项进行格式化：
	#如果解析的年月日不是整数，那么对于date域则忽略，对于year域则直接输出
	if datecanbeparse:
		if datetype+'date' in options:#首先使用条目给出的选项
			fieldcontents=singledateformat(dateparts,datetype,options[datetype+'date'])
		elif datetype+'date' in formatoptions:#接着使用全局给出的选项
			fieldcontents=singledateformat(dateparts,datetype,formatoptions[datetype+'date'])
		else:#否则使用默认选项
			fieldcontents=singledateformat(dateparts,datetype,'default')
	else:
		#如果日期无法解析，那么日期信息仅可能存在datetype+year域中
		fieldcontents=bibentry[dtyear]
			
	return fieldcontents

	
#
#将单个日期解析到year，month，day中
#
def datetoymd(bibentry,fieldsource):
	
	#首先从日期域，解析日期类型：
	dateparts={}
	if fieldsource=='year':
		datestring=bibentry[fieldsource]
		datetype=''
	elif fieldsource=='endyear':
		datestring=bibentry[fieldsource]
		datetype='end'
	else:
		datetype=fieldsource.replace('date','')
		datestring=bibentry[fieldsource]
	#print('datetype=',datetype)	
		
	#日期的年月日解析
	#日期一般很少用{}进行保护，当保护的时候通常是整个进行包括，所以通常{}会出现在域的起始和末尾
	#所以当出现{字符时通常不用再做解析
	if '{' in datestring:
		datepartinfo=[datestring]
	else:
		datepartinfo=datestring.split('-')
	
	if len(datepartinfo)==3:
		dateparts[datetype+'year']=datepartinfo[0].strip()
		dateparts[datetype+'month']=datepartinfo[1].strip()
		dateparts[datetype+'day']=datepartinfo[2].strip()
	elif len(datepartinfo)==2:
		dateparts[datetype+'year']=datepartinfo[0].strip()
		dateparts[datetype+'month']=datepartinfo[1].strip()
	else:
		dateparts[datetype+'year']=datepartinfo[0].strip()
	
	return dateparts,datetype
#
#
# 根据日期的设置选项格式化单个日期
def singledateformat(dateparts,datetype,formatoption):
	if formatoption=='year':
		dateformatstr=dateparts[datetype+'year']
		
	elif formatoption=='iso':
		dateformatstr=dateparts[datetype+'year']
		
		if datetype+'month' in dateparts:#得保证存在month
			if len(dateparts[datetype+'month'])<2:
				dateformatstr=dateformatstr+'-0'+dateparts[datetype+'month']
			else:
				dateformatstr=dateformatstr+'-'+dateparts[datetype+'month']
		if datetype+'day' in dateparts:#得保证存在day
			if len(dateparts[datetype+'day'])<2:
				dateformatstr=dateformatstr+'-0'+dateparts[datetype+'day']
			else:
				dateformatstr=dateformatstr+'-'+dateparts[datetype+'day']
			
	elif formatoption=='ymd':
		dateformatstr=dateparts[datetype+'year']
		if datetype+'month' in dateparts:#得保证存在month
			dateformatstr=dateformatstr+'-'+dateparts[datetype+'month']
		if datetype+'day' in dateparts:#得保证存在day
			dateformatstr=dateformatstr+'-'+dateparts[datetype+'day']
		
	elif formatoption=='default':
		dateformatstr=dateparts[datetype+'year']
	else:
		pass
	
	return dateformatstr





#
#
#范围域解析
def rangefieldparser(bibentry,fieldsource):

	fieldcontents=bibentry[fieldsource]
	
	#将一个-或多个-，替换为pagerangedelim
	fieldcontents=re.sub(r'-+',localpuncts['pagerangedelim'],fieldcontents)
	
	return fieldcontents


#
#
#打开bib文件
def readfilecontents(bibFile):

	global bibfilecontents
	global usedIds
	
	print("INFO: Reading references from '" + bibFile + "'")
	try:
		fIn = open(bibFile, 'r', encoding="utf8")
		bibfilecontents=fIn.readlines()
		fIn.close()
		
		#当使用nocite{*}引用全部文献时做的标记，全部引用则设置setemptyflag=True
		#便于后面处理，比如将usedIds直接置空，表示引用全部的文献。
		setemptyflag=False
		usedIds = set()
		if inputauxfile:
			fInAux = open(inputauxfile, 'r', encoding="utf8")
			for line in fInAux:
				if line.startswith("\\citation") or line.startswith("\\abx@aux@cite"):
					ids = line.split("{")[1].rstrip("} \n").split(",")
					for id in ids:
						if (id != ""):
							usedIds.add(id.strip()) #使用add方法，自动会判断set中是否已存在，若存在则不会添加
						if (id == "*"):
							setemptyflag=True
							break
					if setemptyflag:
						break
			if setemptyflag:#当存在*时，表示引用所有文献，因此直接设置usedIds为空即可
				usedIds = set()
			fInAux.close()
		print('references:',usedIds)
		
	except IOError:
		print("ERROR: Input bib file '" + bibFile +
				"' doesn't exist or is not readable")
		sys.exit(-1)

#
#打印bib文件内容
def printfilecontents():
	for line in bibfilecontents:
		print(line)



#
#输出修改后的bib文件
def writefilenewbib(bibFile):

	print(datetime.datetime.now().isoformat(timespec='seconds'))
	
	#json文件输出,用dump方法
	jsonoutfile="new"+bibFile.replace('.bib','.json')
	print("INFO: writing all references to '" + jsonoutfile + "'")
	fout = open(jsonoutfile, 'w', encoding="utf8")
	json.dump(bibentries, fout)
	fout.close()
	
	#json文件输出，仅输出被引用的文献,直接用write写
	jsonoutfile="new"+bibFile.replace('.bib','cited.json')
	fout = open(jsonoutfile, 'w', encoding="utf8")
	print("INFO: writing cited references to '" + jsonoutfile + "'")
	fout.write('[\n')
	for bibentry in bibentries:
		if bibentry["entrykey"] in usedIds or not usedIds:
			fout.write(repr(bibentry)+',\n')
	fout.write(']\n')
	fout.close()

	#bib文件输出
	biboutfile="new"+bibFile
	
	try:
		fout = open(biboutfile, 'w', encoding="utf8")
		fout.write("%% \n")
		fout.write("%% bib file modified by bibmap.py\n")
		
		fout.write("%% "+datetime.datetime.now().isoformat(timespec='seconds')+"\n")
		fout.write("%% \n\n\n")
		
		for bibcomment in bibcomments:
			for k,v in bibcomment.items():
				if k=="entrytype":
					fout.write('@'+bibcomment["entrytype"]+'{')
				else:
					fout.write(str(v))
			fout.write('}\n\n')
			
		for bibstring in bibstrings:
			for k,v in bibstring.items():
				if k=="entrytype":
					fout.write('@'+bibstring["entrytype"]+'{')
				else:
					fout.write(str(v))
			fout.write('}\n\n')
		
		writebibentrycounter=0
		if inputauxfile:
			print("INFO: writing cited references in aux to '" + biboutfile + "'")
			
			for bibentry in bibentries:
				if bibentry["entrykey"] in usedIds or not usedIds:
					writebibentrycounter=writebibentrycounter+1
					fout.write('@'+bibentry["entrytype"]+'{'+bibentry["entrykey"]+',\n')
					for k,v in bibentry.items():
						if k=="entrytype" or k=="entrykey" or v=='""' or v==None or k=='entrysn':
							pass
						else:
							fout.write('\t'+str(k)+' = {'+str(v)+'},\n')
					fout.write('}\n\n')
		else:
			print("INFO: writing all references to '" + biboutfile + "'")
			for bibentry in bibentries:
				writebibentrycounter=writebibentrycounter+1
				fout.write('@'+bibentry["entrytype"]+'{'+bibentry["entrykey"]+',\n')
				for k,v in bibentry.items():
					if k=="entrytype" or k=="entrykey" or v=='""' or k=='entrysn' or v==None:
						pass
					else:
						fout.write('\t'+k+' = {'+v+'},\n')
				fout.write('}\n\n')
		
		fout.close()
		print("INFO: " + str(writebibentrycounter) + " references writed")
	except IOError:
		print("ERROR: Input bib file '" + bibFile +
				"' doesn't exist or is not readable")
		sys.exit(-1)
		



#
#将条目解析放到bibentries列表中
#每个条目是一个dict字典
def bibentryparsing():
	global bibentries
	global bibcomments
	global bibstrings
	bibentries=[]#用于记录所有条目
	bibentry={}#用于记录当前条目
	
	bibcomments=[]#用于记录所有@comment条目
	bibcomment={}#用于记录当前@comment条目
	
	bibstrings=[]#用于记录所有@stirng条目
	bibstring={}#用于记录当前@stirng条目
	
	entrysn=0 #用于标记条目序号
	bibentrycounter=0##用于标记条目总数
	commentsn=0 #用于标记@comment条目序号
	bibcommentcounter=0#用于标记@comment条目总数
	stringsn=0 #用于标记@stirng条目序号
	bibstringcounter=0#用于标记@stirng条目总数
	
	entrystated=False #用于标记条目开始
	fieldvalended=True #用于标记域的值当前行是否已经结束
	fieldvalue="" #用于记录当前域的值
	counterbracket=0 #用于追踪{}符号
	counterquotes=0  #用于追踪“”符号
	enclosebracket=True #用于记录是用{}还是用“”做为域的值的包围符号
	enclosenone=False #用于记录域的值无包围符号的情况
	
	for line in bibfilecontents:#遍历所有行
		#print(line)
		
		if line.startswith("@") and not "@comment" in line.lower() and not "@string" in line.lower():#判断条目开始行
			entrysn=entrysn+1
			entrystated=True #新条目开始
			#print('entry No.=',entrysn)
			entrynow=line.lstrip('@').split(sep='{', maxsplit=1)
			#print(entrynow)
			entrytype=entrynow[0]
			bibentry['entrytype']=entrytype.lower()#条目类型小写，方便比较
			entrykey=entrynow[1].split(sep=',', maxsplit=1)[0]
			bibentry['entrykey']=entrykey
			bibentry['entrysn']=entrysn
		elif entrystated: #只有新条目开始了才有意义

			if fieldvalended: #当前行不是前面的未结束域的值
				if '=' in line and not line.lstrip().startswith("}"):
					#排除以'}'开头的行后根据=号判断条目域信息行，不可能出现=号无法判断信息行的问题，
					#因为是域值中存在=的特殊情况已经在未结束逻辑处理
					entryline=line.lstrip()
					entrynow=entryline.split(sep='=', maxsplit=1)
					#print(entrynow)
					entryfield=entrynow[0].strip().lower()#域名小写，方便比较
					entryfieldline=entrynow[1].lstrip()
					
					if entryfieldline.startswith("{"):
						enclosebracket=True
					elif entryfieldline.startswith('"'):
						enclosebracket=False
					else:#当没有符号包围是设置enclosenone以便特殊处理
						enclosenone=True
					
					fieldvalcontinued=True #临时标记，用于记录域值是否还未结束，先假设未结束
					for chari in entryfieldline.strip():#遍历域值中的每个字符
						fieldvalue=fieldvalue+chari
						#print('chari=',chari)
						if chari =='{':#对{符号进行追踪
							counterbracket=counterbracket+1
						elif chari =='}':#对}符号进行追踪
							counterbracket=counterbracket-1
							if enclosebracket:
								if counterbracket==0:#当}与域开始的{配对，那么说明域值已经结束
									bibentry[entryfield]=fieldvalue[1:-1]#利用strip可能会消多次，因此用list的方式处理
									fieldvalue=""
									counterbracket=0
									counterquotes=0
									fieldvalended=True
									fieldvalcontinued=False
									break #直接跳出循环
						elif chari =='"':
							counterquotes=counterquotes+1
							if not enclosebracket:
								if operator.mod(counterquotes,2)==0:
									bibentry[entryfield]=fieldvalue[1:-1]
									fieldvalue=""
									counterbracket=0
									counterquotes=0
									fieldvalended=True
									fieldvalcontinued=False
									break
						elif chari ==',':#若域值没有包围符号那么遇到,号即为域值结束
							if enclosenone:
								bibentry[entryfield]=fieldvalue[:-1]
								fieldvalue=""
								counterbracket=0
								counterquotes=0
								fieldvalended=True
								fieldvalcontinued=False
								enclosenone=False
						
						#测试：输出看是否正确
						#if entryfield=='abstract':
						#	print('val=',fieldvalue)
						#	print('counterbracket=',counterbracket)
						
					if fieldvalcontinued:
						fieldvalended=False
				
				elif '}' in line:#条目结束行

					#global bibentryglobal
					#bibentryglobal=copy.deepcopy(bibentry) 
					#print('entry:',bibentryglobal)
					#bibentries.append(bibentryglobal)
					
					#print('entry:',bibentry)
					bibentries.append(bibentry)
					bibentry={}
					entrystated=False
					
			else: #当前行是前面的未结束域的值，因此直接往前面的域值添加即可
				fieldvalcontinued=True

				entryfieldline=line
				
				if enclosenone:#当域没有包围符号时，接续的行可能是用逗号结束的域，也可能没有逗号，而用}直接结束条目信息
					for chari in entryfieldline.strip():
						fieldvalue=fieldvalue+chari
						if chari ==',':
							bibentry[entryfield]=fieldvalue[:-1]
							fieldvalue=""
							counterbracket=0
							counterquotes=0
							fieldvalended=True
							fieldvalcontinued=False
							enclosenone=False
						elif chari =='}':
							bibentry[entryfield]=fieldvalue[:-1]
							fieldvalue=""
							counterbracket=0
							counterquotes=0
							fieldvalended=True
							fieldvalcontinued=False
							enclosenone=False
							print('entry:',bibentry)
							bibentries.append(bibentry)
							bibentry={}
							entrystated=False
				
				else:
					#接续的行可能存在大量的空格，所以先进行处理使得多个空格或tab转换成一个空格
					#只要做strip后不存在在字符，那么该字符必然是空格
					#2019.04.09，hzz
					if not entryfieldline[0].strip():
						entryfieldline=' '+entryfieldline.strip()
					
					for chari in entryfieldline:#这里strip可能会把接续行前面的空格去掉，所以考虑不做strip  .strip()
						fieldvalue=fieldvalue+chari
						#print('chari=',chari)
						if chari =='{':
							counterbracket=counterbracket+1
						elif chari =='}':
							counterbracket=counterbracket-1
							if enclosebracket:
								if counterbracket==0:
									bibentry[entryfield]=fieldvalue[1:-1]
									fieldvalue=""
									counterbracket=0
									counterquotes=0
									fieldvalended=True
									fieldvalcontinued=False
									break
						elif chari =='"':
							counterquotes=counterquotes+1
							if not enclosebracket:
								if mod(counterquotes,2)==0:
									bibentry[entryfield]=fieldvalue[1:-1]
									fieldvalue=""
									counterbracket=0
									counterquotes=0
									fieldvalended=True
									fieldvalcontinued=False
									break

								
				if fieldvalcontinued:
					fieldvalended=False
		elif line.startswith("@") and "@comment" in line.lower():#@comment的起始
			commentsn=commentsn+1
			entrynow=line.lstrip('@').split(sep='{', maxsplit=1)
			entrytype=entrynow[0]
			bibcomment['entrytype']=entrytype.lower()#条目类型小写，方便比较
			entrycontents=entrynow[1].strip()[:-1]
			bibcomment['entrycontents']=entrycontents
			#print(bibcomment)
			bibcomments.append(bibcomment)
			bibcomment={}
			
		elif line.startswith("@") and "@string" in line.lower():#@string的起始
			stringsn=stringsn+1
			entrynow=line.lstrip('@').split(sep='{', maxsplit=1)
			entrytype=entrynow[0]
			bibstring['entrytype']=entrytype.lower()#条目类型小写，方便比较
			entrycontents=entrynow[1].strip()[:-1]
			bibstring['entrycontents']=entrycontents
			#print(bibstring)
			bibstrings.append(bibstring)
			bibstring={}

	
	bibentrycounter=len(bibentries)
	bibcommentcounter=len(bibcomments)
	bibstringcounter=len(bibstrings)

	if not bibentrycounter==entrysn or not bibcommentcounter==commentsn or not bibstringcounter==stringsn:
		try:
			print('entrysn=',entrysn,' commentsn=',commentsn,' stringsn=',stringsn)
			print('entryct=',bibentrycounter,' commentct=',bibcommentcounter,' stringct=',bibstringcounter)
			raise BibParsingError('bib file parsing went wrong!')
		except BibParsingError as e:
			raise BibParsingError(e.message)
	print('total entries=',bibentrycounter)
	
	#输出解析后的bib文件信息
	#for bibentryi in bibentries:
		#print(bibentryi)


#
#打印bibentries列表中的所有条目
def printbibentries():
	for bibentryi in bibentries:
		print(bibentryi)	
			

#
#自定义异常类
class BibParsingError(Exception):
	def __init__(self,message):
		Exception.__init__(self)
		self.message=message 
		
#
# 执行数据映射操作
# 还有一些选项没有实现，20190209
# 实现的选项中也需要和未实现的选项进行数据传递
def execsourcemap():
	for map in sourcemaps:#every map in maps，每个map逐步开始
		for bibentry in bibentries:#每个映射都需要遍历所有条目，对每个条目做map
	
			mapcontinue=1#大于0表示正常，继续当前条目的map
			typesrcinfo={}#用于记录typesource相关处理结果
			fieldsrcinfo={}#用于记录fieldsource相关处理的结果
			constraintinfo={}#用于记录类型等限制信息记录
			constraintinfo['pertype']=[]
			constraintinfo['pernottype']=[]
			
			#print("map info=",map)
			for step in map:#every step in map
				if mapcontinue>0:#对前面已经final完成的情况做限制
					keyvals=step #step is a key-vals dict 
					for k,v in keyvals.items():#step 是有迹可循的，每个step总是存在一些东西，找到这些做其中的逻辑即可
						#print(k,v)
						
						if k=="typesource":#条目类型设置
							mapcontinue=maptypesource(keyvals,bibentry,typesrcinfo)#coef is dict
							
						elif k=="fieldsource":#域查找或设置
							mapcontinue=mapfieldsource(keyvals,bibentry,fieldsrcinfo,constraintinfo)#
							#print("fieldsource step:",fieldsrcinfo)
							
						elif k=="fieldset":#域设置-添加的话使用append选项就可以了。
							mapcontinue=mapfieldset(keyvals,bibentry,typesrcinfo,fieldsrcinfo,constraintinfo)#

						elif k=="pertype": #类型限制
							mapcontinue=mappertype(keyvals,constraintinfo)
							
						elif k=="pernottype":#类型限制
							mapcontinue=mappernottype(keyvals,constraintinfo)
							
						elif k=="notfield":#域限制
							mapcontinue=mapnotfield(keyvals,bibentry,fieldsrcinfo,constraintinfo)#
						else:
							pass

								
#
#域限制,若域确定不存在则终止map				
def mapnotfield(keyvals,bibentry,fieldsrcinfo,constraintinfo):

	setcontinue=True
	print(setcontinue)
	if len(constraintinfo['pertype'])>0:
		if bibentry['entrytype'] not in constraintinfo['pertype']:#
			setcontinue=False
	if len(constraintinfo['pernottype'])>0:
		if bibentry['entrytype'] in constraintinfo['pernottype']:#
			setcontinue=False
	print(setcontinue)

	
	print("constraints:notfield")
	if setcontinue:
		for k,v in keyvals.items():
			#print(k,v)
			if k=='notfield':
				notfield=v.lower()
			elif k=='final':
				fieldfinal=v
			else:
				pass
				
		if notfield not in bibentry:#当notfield不存在，则判断为true，若存在final则终止，否则继续
			if fieldfinal:
				return 0
			else:
				return 1
		else:
			return 1
			
	else:
		return 0
	

	
#
#
#条目类型限制,将类型限制信息放入字典				
def mappertype(keyvals,constraintinfo):
	
	print("constraints:pertype")
	for k,v in keyvals.items():
		#print(k,v)
		if k=='pertype':
			pertype=v.lower()#因为大小写区分，所以全部小写方便比较
		else:
			pass
	print('pertype=',pertype)
	
	constraintinfo['pertype'].append(pertype)
	return 1
	
#
#
#条目类型限制,将类型限制信息放入字典				
def mappernottype(keyvals,constraintinfo):
	
	print("constraints:pernottype")
	for k,v in keyvals.items():
		#print(k,v)
		if k=='pernottype':
			pernottype=v.lower()#因为大小写区分，所以全部小写方便比较
		else:
			pass
	print('pertype=',pertype)
	
	constraintinfo['pernottype'].append(pernottype)
	return 1
 
								
#
#条目类型转换				
def maptypesource(keyvals,bibentry,typesrcinfo):
	retrunval=1
	for k,v in keyvals.items():
		#print(k,v)
		if k=='typesource':
			typesource=v.lower()
		elif k=='typetarget':
			typetarget=v.lower()
		elif k=='final':
			retrunval=0
		else:
			pass
		
	typesrcinfo
	if typetarget:
		if bibentry['entrytype']==typesource:
			bibentry['entrytype']=typetarget
			typesrcinfo['typesource']=typesource
			return 1
		else:
			return retrunval #存在final时，且不匹配则终止map
	else:
		if bibentry['entrytype']==typesource:
			typesrcinfo['typesource']=typesource
		else:
			typesrcinfo['typesource']=None
		return retrunval



#
#
# 域信息设置
def mapfieldset(keyvals,bibentry,typesrcinfo,fieldsrcinfo,constraintinfo):
	overwrite=False
	append=False
	
	setcontinue=True
	print(setcontinue)
	if len(constraintinfo['pertype'])>0:
		if bibentry['entrytype'] not in constraintinfo['pertype']:#
			setcontinue=False
	if len(constraintinfo['pernottype'])>0:
		if bibentry['entrytype'] in constraintinfo['pernottype']:#
			setcontinue=False
	print(setcontinue)
	
	if setcontinue:
		
		appdelim=',' #设置一个默认的添加信息前面的分隔符
		for k,v in keyvals.items():
			#print(k,v)
			if k=='fieldset':
				fieldset=v.lower()
			elif k=='fieldvalue':
				fieldvalue=v
			elif k=='origfieldval':
				fieldvalue=fieldsrcinfo[fieldsrcinfo['fieldsource']]
				print(fieldvalue)
			elif k=='origentrytype':
				fieldvalue=typesrcinfo['typesource']
				print(fieldvalue)
			elif k=='origfield':
				fieldvalue=fieldsrcinfo['fieldsource']
				print(fieldvalue)
			elif k=="fieldfunction":
				fieldfunction=v
			elif k=='null':
				fieldvalue=None
				print(fieldvalue)
			elif k=='append':
				append=v
			elif k=='appdelim':
				appdelim=v
			elif k=='overwrite':
				overwrite=v
			else:
				pass
		
		#print("\nfieldvalue=",fieldvalue,"\n")
		#只有当fieldvalue存在时才需要设置:两种情况：一种要求不是[None]，另一种是直接的字符串
		if (type(fieldvalue)==list and fieldvalue[0]) or (type(fieldvalue)!=list and fieldvalue):
			if fieldfunction:
				if fieldfunction=='sethzpinyin':
					fieldvalue=sethzpinyin(fieldvalue)
				elif fieldfunction=='sethzstroke':
					fieldvalue=sethzstroke(fieldvalue)
				elif fieldfunction=='setsentencecase':
					fieldvalue=setsentencecase(fieldvalue)
				elif fieldfunction=='settitlecase':
					fieldvalue=settitlecase(fieldvalue)
				elif fieldfunction=='setalltitlecase':
					fieldvalue=setalltitlecase(fieldvalue)
				elif fieldfunction=='setuppercase':
					fieldvalue=setuppercase(fieldvalue)
				elif fieldfunction=='setlowercase':
					fieldvalue=setlowercase(fieldvalue)
				elif fieldfunction=='setsmallcaps':
					fieldvalue=setsmallcaps(fieldvalue)
				elif fieldfunction=='setauthoran':#给作者添加annotaion信息
					#参数：要设置的说明信息，作者域的内容，需要设置说明的作者名
					fieldvalue=setauthoran(fieldvalue,fieldsrcinfo['fieldsrcraw'],fieldsrcinfo['fieldmatch'])
				else:
					print('WARNING: field function "'+fieldfunction+'" for mapping is not defined!')
			
			print("fieldset=",fieldset)
			if overwrite:
				if append:
					oldvalue=""
					if fieldset in bibentry:
						oldvalue=bibentry[fieldset]
					if oldvalue:
						newvalue=oldvalue+appdelim+fieldvalue
					else:
						newvalue=fieldvalue
					bibentry[fieldset]=newvalue
				else:
					bibentry[fieldset]=fieldvalue
			else:
				if fieldset in bibentry:
					pass
				else:
					bibentry[fieldset]=fieldvalue
			return 1
		
	else:
		return 1
	
#
#域名转换或判断域是否存在或match
def mapfieldsource(keyvals,bibentry,fieldsrcinfo,constraintinfo):
	mapfieldtype=0 #域名map的类型设置
	fieldmatch=''#匹配模式默认为空
	fieldmatchi=''#匹配模式默认为空
	
	
	#首先根据pertype和notpertype设置约束
	#先假设无约束，即setcontinue=True
	setcontinue=True
	print(setcontinue)
	if len(constraintinfo['pertype'])>0:
		if bibentry['entrytype'] not in constraintinfo['pertype']:#
			setcontinue=False
	if len(constraintinfo['pernottype'])>0:
		if bibentry['entrytype'] in constraintinfo['pernottype']:#
			setcontinue=False
	print(setcontinue)
	
	
	overwrite=False
	for k,v in keyvals.items():
		#print(k,v)
		if k=='fieldsource':
			fieldsource=v.lower()
		elif k=='fieldtarget':
			fieldtarget=v.lower()
			mapfieldtype=1 #域map类型1，直接做域名转换
		elif k=='replace':
			fieldreplace=v
			mapfieldtype=2 #域map类型2，直接做域信息转换
		elif k=='final':
			fieldfinal=v #final要么选项不给出，要么选项给出为true
			if fieldfinal and mapfieldtype==0:#当为true时则做终止判断，当mapfieldtype已经设置，则不再设置新的map类型
				mapfieldtype=3 #域map类型3，做final判断可以终止map
		elif k=='overwrite':#
			overwrite=v
		elif k=='match':#不区分大小写的match
			fieldmatch=v
			fieldsrcinfo['fieldmatch']=v
		elif k=='matchi':#区分大小写的match
			fieldmatchi=v
			fieldsrcinfo['fieldmatchi']=v
		elif k=='notmatch':#不区分大小写的notmatch，下面这两个选项的逻辑没有实现
			fieldnotmatch=v
		elif k=='notmatchi':#区分大小写的notmatch
			fieldnotmatch=v
		else:
			pass
	
	
	if setcontinue:

		#返回字典的第一项是fieldsource信息
		fieldsrcinfo['fieldsource']=fieldsource
		if fieldsource in bibentry:
			fieldsrcinfo['fieldsrcraw']=bibentry[fieldsource]
		
		if mapfieldtype==0:#第0中情况即，不做信息转换，也不终止map，仅返回一些信息
		
			if fieldsource in bibentry:
				if fieldmatch:
					m = re.search(fieldmatch, bibentry[fieldsource])
					if m:
						fieldsrcinfo[fieldsource]=[bibentry[fieldsource],fieldmatch]
					else:
						fieldsrcinfo[fieldsource]=[None] #正则不匹配，则返回为None

				elif fieldmatchi:
					m = re.search(fieldmatchi, bibentry[fieldsource])
					if m:
						fieldsrcinfo[fieldsource]=[bibentry[fieldsource],fieldmatchi]
					else:
						fieldsrcinfo[fieldsource]=[None] #正则不匹配，则返回为None
					
				else:
					fieldsrcinfo[fieldsource]=bibentry[fieldsource]#将域的值记录下来，用于下一step
			
			else:
				fieldsrcinfo[fieldsource]=[None] #域不存在则返回为None
			return 1
			
		
		elif mapfieldtype==1:#第1种情况即，做域名转换
			print('fieldsource=',fieldsource,'fieldtarget=',fieldtarget)
			if overwrite or fieldtarget not in bibentry:#当overwite选项启用，或者fieldtarget不存在时，直接做转换
				if fieldsource in bibentry:
					bibentry[fieldtarget]=bibentry[fieldsource]
					del bibentry[fieldsource]
					fieldsrcinfo[fieldsource]=bibentry[fieldtarget]
				else:
					fieldsrcinfo[fieldsource]=[None]
			else:#否则不做转换
				pass
			return 1
			
			
		
		
		elif mapfieldtype==2:#域map类型2，直接做域信息转换，真正操作需要overwrite选项支持
			print('fieldsource=',fieldsource)
			print('fieldmatch=',fieldmatch)
			print('fieldreplace=',fieldreplace)
			if overwrite:
				if fieldsource in bibentry:
					if fieldmatch:
						#strafrpl=re.sub(r'(\d\d\d\d)\-(\d)\-(\d)',r'\1-0\2-0\3','2015-1-3')
						#strafrpl=re.sub(r'(\d\d\d\d)\-(\d)\-(\d)',r'\1-0\2-0\3',bibentry[fieldsource])
						strafrpl=re.sub(fieldmatch,fieldreplace,bibentry[fieldsource]) #执行替换
						print('strafterreplace=',strafrpl)
						bibentry[fieldsource]=strafrpl
					elif fieldmatchi:
						strafrpl=re.sub(fieldmatchi, fieldreplace,bibentry[fieldsource]) 
						bibentry[fieldsource]=strafrpl
					else:
						fieldsrcinfo[fieldsource]=[None]
				else:
					fieldsrcinfo[fieldsource]=[None]
			else:
				fieldsrcinfo[fieldsource]=[None]
			return 1

		
		elif mapfieldtype==3:#域map类型3，当没有匹配则终止map
			if fieldsource in bibentry:
				if fieldmatch:
					m = re.search(fieldmatch, bibentry[fieldsource])
					#print('fieldmatch=',fieldmatch, 'bibentry[fieldsource]=', bibentry[fieldsource])
					#print('\nmatch=',m,"\n")
					if m:
						fieldsrcinfo[fieldsource]=[bibentry[fieldsource],fieldmatch]
						return 1
					else:
						return 0

				elif fieldmatchi:
					if m:
						fieldsrcinfo[fieldsource]=[bibentry[fieldsource],fieldmatchi]
						return 1
					else:
						return 0
					
				else:
					fieldsrcinfo[fieldsource]=bibentry[fieldsource]#将域的值记录下来，用于下一step
					return 1
			
			else:
				return 0
	
	else:
		fieldsrcinfo[fieldsource]=[None]
		return 1


#
#自定义异常类
class BibFileinputError(Exception):
	def __init__(self,message):
		Exception.__init__(self)
		self.message=message 
		
		

#输入命令行解析
#
#命令行参数，输入文件处理，所有操作流程组织
#
def bibmapinput():
	#要使用全局变量先声明一下
	global inputbibfile,inputauxfile,inputstyfile,inputmapfile,bibliotableflag
	global subauxfilelist,subbibfilelist,substyfilelist,submapfilelist #主文档包含的子文档的aux文件


	#创建一个解析器
	parser = argparse.ArgumentParser(description='Process input files for bibmap')
	
	#添加命令行参数
	parser.add_argument('filename', type=str, help='单个输入文件的文件名，可带后缀名，无后缀名时默认为辅助文件.aux')
	parser.add_argument('-a', type=str, dest='auxfile',help='辅助文件的文件名，可带后缀名.aux')
	parser.add_argument('-b', type=str, dest='bibfile',help='文献数据库文件名，可带后缀名.bib')
	parser.add_argument('-s', type=str, dest='styfile',help='设置文献样式文件的文件名，可带后缀名.py')
	parser.add_argument('-m', type=str, dest='mapfile',help='数据库修改设置文件文件名，可带后缀名.py')
	
	parser.add_argument('--nofmt', action='store_true', help='不做格式化输出,no format')
	parser.add_argument('--nobdm', action='store_true', help='不做bib数据修改,no bib data modify')
	#
	#2021-05-24,hzz,v1.0c
	#增加：写拼音key域的功能
	#注意action='store_true'表示这个命令行选项会存储到命名空间内，可以在程序后面查看
	parser.add_argument('--addpinyin', action='store_true', help='为每个条目增加写拼音的key域, add pinyin for every bib entry')

	
	#解析命令行参数
	args=parser.parse_args()
	inputfiles=vars(args)
	print(inputfiles)
	#s = input('press any key to continue:')
	
	
	#根据输入的文件字典判断
	#1.首先判断必选参数
	if '.bib' in inputfiles['filename']:
		inputbibfile=inputfiles['filename']
	elif '.aux' in inputfiles['filename']:
		inputauxfile=inputfiles['filename']
	else:
		inputauxfile=inputfiles['filename']+'.aux'
		
	#2.接着判断可选参数
	#可选参数可以覆盖默认参数
	if inputfiles['auxfile'] and not inputauxfile:
		if '.aux' in inputfiles['auxfile']:
			inputauxfile=inputfiles['auxfile']
		else:
			inputauxfile=inputfiles['auxfile']+'.aux'
		
	if inputfiles['bibfile'] and not inputbibfile:
		if '.bib' in inputfiles['bibfile']:
			inputbibfile=inputfiles['bibfile']
		else:
			inputbibfile=inputfiles['bibfile']+'.bib'
			
	if inputfiles['styfile']:
		inputstyfile=inputfiles['styfile']
			
	if inputfiles['mapfile']:
		inputmapfile=inputfiles['mapfile']
		
	#把当前路径加入到sys.path中便于python加载当前目录下的模块
	print('sys.path=',sys.path)
	print('current path=',os.getcwd())
	pathtoadd=os.getcwd()
	sys.path.append(pathtoadd)
	print('sys.path=',sys.path)

	# print('aux:',inputauxfile)
	# print('bib:',inputbibfile)
	# print('sty:',inputstyfile)
	# print('map:',inputmapfile)
	
		
	#3.接着辅助文件aux中提供的参数
	#可能有多个bib文件的需求，这个问题等明确chapterbib使用确定
	#辅助文件aux中提供的参数可以覆盖前面设置的参数
	subauxfilelist=[]
	if inputauxfile:
		fInAux = open(inputauxfile, 'r', encoding="utf8")
		for line in fInAux:
			if line.startswith("\\bibdata"):
				m = re.search(r'\\bibdata{(.*)}',line)#注意贪婪算法的影响，所以要排除\}字符
				print('inputbibfile:m.group(1):',m.group(1))
				inputbibfile = m.group(1)
				if '.bib' not in inputbibfile:
					inputbibfile=inputbibfile+'.bib'

			if line.startswith("\\bibmap@tabflag"):
				m = re.search(r'\\bibmap@tabflag {(.*)}',line)
				bibliotableflag=m.group(1)
				print('bibliotableflag:m.group(1):',m.group(1))
					
			if line.startswith("\\bibmap@bibstyle"):
				m = re.search(r'\\bibmap@bibstyle {(.*)}',line)#注意贪婪算法的影响，所以要排除\}字符
				print('inputstyfile:m.group(1):',m.group(1))
				
				if not inputstyfile:#当命令行未指定styfile时
					inputstyfile = m.group(1)
				if '.py' not in inputstyfile:
					inputstyfile = inputstyfile+'.py'
					
			if line.startswith("\\bibmap@mapstyle"):
				m = re.search(r'\\bibmap@mapstyle {(.*)}',line)#注意贪婪算法的影响，所以要排除\}字符
				print('inputmapfile:m.group(1):',m.group(1))
				if not inputmapfile:#当命令行未指定mapfile时
					inputmapfile = m.group(1)
				if '.py' not in inputmapfile:
					inputmapfile = inputmapfile+'.py'
			
			if line.startswith("\\@input"):
				m = re.search(r'\\@input\s*{(.*).aux\s*}',line)#注意贪婪算法的影响，所以要排除\}字符
				print('m.group(1):',m.group(1))
				subauxfile = m.group(1)
				if '.aux' not in subauxfile:
					subauxfile+='.aux'
				if subauxfile not in subauxfilelist:
					subauxfilelist.append(subauxfile)
					
		fInAux.close()
	
	if not inputbibfile and not subauxfilelist:
		try:
			raise BibFileinputError('error：未指定bib文件，请用-b选项直接指定或者在aux文件内指定！')
		except BibFileinputError as e:
			raise BibFileinputError(e.message)
	
	if not inputstyfile:
		print('INFO：著录格式设置文件未指定，使用默认的样式bibstylenumeric.py！')
		inputstyfile='bibstylenumeric.py' #使用默认的设置
		
	if not inputmapfile:
		print('INFO：数据修改设置文件未指定，使用默认的样式bibmapdefault.py！')
		inputmapfile='bibmapdefault.py' #使用默认的设置
	
	print('aux:',inputauxfile)
	print('bib:',inputbibfile)
	print('sty:',inputstyfile)
	print('map:',inputmapfile)
	
	
	subbibfilelist=[]
	substyfilelist=[]
	submapfilelist=[]
	#读取子文档的信息
	if subauxfilelist:
		for subauxfile in subauxfilelist:
		
			subbibfile=''
			substyfile=''
			submapfile=''
			
			fInAux = open(subauxfile, 'r', encoding="utf8")
			
			for line in fInAux:
				if line.startswith("\\bibdata"):
					m = re.search(r'\\bibdata{(.*)}',line)#注意贪婪算法的影响，所以要排除\}字符
					print('m.group(1):',m.group(1))
					subbibfile = m.group(1)
					if '.bib' not in subbibfile:
						subbibfile=subbibfile+'.bib'
						
				if line.startswith("\\bibmap@bibstyle"):
					m = re.search(r'\\bibmap@bibstyle {(.*)}',line)#注意贪婪算法的影响，所以要排除\}字符
					print('m.group(1):',m.group(1))
					substyfile = m.group(1)
					if '.py' not in substyfile:
						substyfile = substyfile+'.py'
						
				if line.startswith("\\bibmap@mapstyle"):
					m = re.search(r'\\bibmap@mapstyle {(.*)}',line)#注意贪婪算法的影响，所以要排除\}字符
					print('m.group(1):',m.group(1))
					submapfile = m.group(1)
					if '.py' not in submapfile:
						submapfile = submapfile+'.py'

			fInAux.close()
			
			if subbibfile:#子文档内没有指定文件，那么使用主文档的信息
				subbibfilelist.append(subbibfile)
			else:
				subbibfilelist.append(inputbibfile)
			
			if substyfile:#子文档内没有指定文件，那么使用主文档的信息
				substyfilelist.append(substyfile)
			else:
				substyfilelist.append(inputstyfile)

			if submapfile:#子文档内没有指定文件，那么使用主文档的信息
				submapfilelist.append(submapfile)
			else:
				submapfilelist.append(inputmapfile)
			
	print('subaux:',subauxfilelist)
	print('subbib:',subbibfilelist)
	print('substy:',substyfilelist)
	print('submap:',submapfilelist)
	
	#sys.exit(-1)
	
	
	##------------------------------------------
	## 参考文献数据的修改，比如类似biblatex的sourcemap
	## 
	#重设不处理
	global sourcemaps

	##------------------------------------------
	## 参考文献表的制定格式设置，比如GB/T 7714-2015
	## 

	#全局选项
	global formatoptions
	#本地化字符串
	global localstrings
	#标点
	global localpuncts
	#替换字符串
	global replacestrings
	#类型和载体字符串
	global typestrings
	#数据类型
	global datatypeinfo
	#条目的著录格式
	global bibliographystyle
	
	
	#当主文档存在inputbibfile时，那么做主文档的处理
	if inputbibfile:
	
		#导入设置参数模块，导入设置数据
		#
		#bib数据修改模块导入
		if '.py' in inputmapfile:
			strmapmodule=inputmapfile.replace('.py','')
		else:
			strmapmodule=inputmapfile

		try:
			mapmodule=__import__(strmapmodule)
			print(mapmodule)
		except ImportError as e:
			print('error：数据修改设置文件出错，请重新指定！')
			raise BibFileinputError(e.message)
		
		if 'sourcemaps' in dir(mapmodule):#做sourcemaps参数设置检查
			sourcemaps=mapmodule.sourcemaps
		else:
			sourcemaps=[]

		print("1",sourcemaps)
		#2021-05-24,hzz,v1.0c
		#增加：写拼音key域的功能
		#对所有中文文献增加key域，该域包含拼音信息
		if inputfiles['addpinyin']:
			try:
				mapmodule=__import__("bibmapaddpinyinkey")
				print(mapmodule)
				sourcemapsaddkeypinyin=mapmodule.sourcemaps
				print('sourcemapsaddkeypinyin=',sourcemapsaddkeypinyin)
				sourcemaps.extend(sourcemapsaddkeypinyin)
			except ImportError as e:
				print('error：数据修改设置文件出错，请重新指定！')
				raise BibFileinputError(e.message)
		print("2",sourcemaps)
		
		#print(dir(mapmodule))
		if 'multiplepinyin' in dir(mapmodule):#做multiplepinyin参数设置检查
			if mapmodule.multiplepinyin:#如果map样式文件中有对多音字的首音设置，那么做处理
				for k,v in mapmodule.multiplepinyin.items():
					hzpinyindata[k]=v
		
		#
		#文献数据格式化模块导入
		if '.py' in inputstyfile:
			strsetmodule=inputstyfile.replace('.py','')
		else:
			strsetmodule=inputstyfile
			
		try:
			setmodule=__import__(strsetmodule)
			print(setmodule)
		except ImportError as e:
			print('error：著录格式设置文件出错，请重新指定！')
			raise BibFileinputError(e.message)
		
		print(setmodule)
		
		formatoptions=setmodule.formatoptions
		
		localstrings=setmodule.localstrings
		localpuncts=setmodule.localpuncts
		replacestrings=setmodule.replacestrings
		typestrings=setmodule.typestrings
		
		datatypeinfo=setmodule.datatypeinfo
		
		bibliographystyle=setmodule.bibliographystyle
		
		#检查输入的信息是否正确，并给出错误提示信息
		#
		#检查map样式文件设置是否正确
		checkbibdatamapstyle()
		
		#检查bib样式全局选项信息
		checkformatoptions()
		
		#检查bib样式格式设置信息
		checkbibliographystyle()
		
		#读取bib和aux文件信息
		readfilecontents(inputbibfile)
		
		#bib文件解析
		bibentryparsing()
		
		if inputfiles['nobdm']:
			pass
		else:
			#根据map的信息执行bib文件map
			execsourcemap()
			#输出map后的bib文件
			writefilenewbib(inputbibfile)
		
		
		if inputfiles['nofmt']:
			pass
		else:
			#根据输入的设置参数对文献进行格式化
			formatallbibliography()
			
			#输出格式化后的文献数据
			printbibliography()
	
	
	#当子文档存在subbibfile时，那么做子文档的处理
	if subbibfilelist:
		
		for i in range(len(subbibfilelist)):
		
			inputmapfile=submapfilelist[i]
			inputstyfile=substyfilelist[i]
			inputbibfile=subbibfilelist[i]
			inputauxfile=subauxfilelist[i]
			
			print('aux:',inputauxfile)
			print('bib:',inputbibfile)
			print('sty:',inputstyfile)
			print('map:',inputmapfile)
			
			
			if inputbibfile[i]:
		
				#导入设置参数模块，导入设置数据
				#
				#bib数据修改模块导入
				if '.py' in inputmapfile:
					strmapmodule=inputmapfile.replace('.py','')
				else:
					strmapmodule=inputmapfile

				try:
					mapmodule=__import__(strmapmodule)
					print(mapmodule)
				except ImportError as e:
					print('error：数据修改设置文件出错，请重新指定！')
					raise BibFileinputError(e.message)
				
				if 'sourcemaps' in dir(mapmodule):#做sourcemaps参数设置检查
					sourcemaps=mapmodule.sourcemaps
				else:
					sourcemaps=[]

				#2021-05-24,hzz,v1.0c
				#增加：写拼音key域的功能
				#对所有中文文献增加key域，该域包含拼音信息
				if inputfiles['addpinyin']:
					try:
						mapmodule=__import__("bibmapaddpinyinkey")
						print(mapmodule)
						sourcemapsaddkeypinyin=mapmodule.sourcemaps
						sourcemaps=sourcemaps.extend(sourcemapsaddkeypinyin)
					except ImportError as e:
						print('error：数据修改设置文件出错，请重新指定！')
						raise BibFileinputError(e.message)
				
				#print(dir(mapmodule))
				if 'multiplepinyin' in dir(mapmodule):#做multiplepinyin参数设置检查
					if mapmodule.multiplepinyin:#如果map样式文件中有对多音字的首音设置，那么做处理
						for k,v in mapmodule.multiplepinyin.items():
							hzpinyindata[k]=v
				
				#
				#文献数据格式化模块导入
				if '.py' in inputstyfile:
					strsetmodule=inputstyfile.replace('.py','')
				else:
					strsetmodule=inputstyfile
					
				try:
					setmodule=__import__(strsetmodule)
					print(setmodule)
				except ImportError as e:
					print('error：著录格式设置文件出错，请重新指定！')
					raise BibFileinputError(e.message)
				
				print(setmodule)
				
				formatoptions=setmodule.formatoptions
				
				localstrings=setmodule.localstrings
				localpuncts=setmodule.localpuncts
				replacestrings=setmodule.replacestrings
				typestrings=setmodule.typestrings
				
				datatypeinfo=setmodule.datatypeinfo
				
				bibliographystyle=setmodule.bibliographystyle
				
				#检查输入的信息是否正确，并给出错误提示信息
				#
				#检查map样式文件设置是否正确
				checkbibdatamapstyle()
				
				#检查bib样式全局选项信息
				checkformatoptions()
				
				#检查bib样式格式设置信息
				checkbibliographystyle()
				
				#读取bib和aux文件信息
				readfilecontents(inputbibfile)
				
				#bib文件解析
				bibentryparsing()
				
				#continue
				
				if inputfiles['nobdm']:
					pass
				else:
					#根据map的信息执行bib文件map
					execsourcemap()
					#输出map后的bib文件
					writefilenewbib(inputbibfile)

				if inputfiles['nofmt']:
					pass
				else:
					#根据输入的设置参数对文献进行格式化
					formatallbibliography()
					
					#输出格式化后的文献数据
					printbibliography()
		
		sys.exit(-1)

#
#自定义异常类
class MapStyleSetError(Exception):
	def __init__(self,message):
		Exception.__init__(self)
		self.message=message 
		
#
#
#检查bib数据修改的选项设置是否正确
def checkbibdatamapstyle():
	print("sourcemaps:",sourcemaps)
	for map in sourcemaps:
		for step in map:
			for k,v in step.items():
				if k in bibmapoptiondatabase:
					if isinstance(bibmapoptiondatabase[k],list):
						if v in bibmapoptiondatabase[k]:
							pass
						else:
							try:
								print('Error: mapstyle option value "'+v+'" for option "'+k+'" is not in bibmapoptiondatabase!\n')
								raise MapStyleSetError('Error: mapstyle option value "'+v+'" for option "'+k+'" is not in bibmapoptiondatabase!')
							except MapStyleSetError as e:
								raise MapStyleSetError(e.message)
				else:
					try:
						print('Error: mapstyle option"'+k+'" is not defined and not in bibmapoptiondatabase!\n')
						raise MapStyleSetError('Error: mapstyle option"'+k+'" is not defined and not in bibmapoptiondatabase!')
					except MapStyleSetError as e:
						raise MapStyleSetError(e.message)
	return None
				
				
	
			
#
#
#检查bibliography格式的全局选项设置是否正确	
def checkformatoptions():#formatoptions等是全局的不用传递

	for k,v in formatoptions.items():
		if k in formatoptiondatabase:
			if isinstance(formatoptiondatabase[k],list):
				if v in formatoptiondatabase[k]:
					pass
				else:
					try:
						print('Error: global option value "'+str(v)+'" for option "'+str(k)+'" is not in formatoptions!\n')
						raise MapStyleSetError('Error: global option value "'+str(v)+'" for option "'+str(k)+'" is not in formatoptions!')
					except MapStyleSetError as e:
						raise MapStyleSetError(e.message)
		else:
			try:
				print('Error: global option"'+k+'" is not in formatoptions!\n')
				raise MapStyleSetError('Error: global option"'+k+'" is not in formatoptions!')
			except MapStyleSetError as e:
				raise MapStyleSetError(e.message)
	return None
		
#
#
#检查bibliography格式的条目著录格式设置是否正确			
def checkbibliographystyle():#bibliographystyle,typestrings等是全局的不用传递
	
	for entrytype,entryfmt in bibliographystyle.items():#对每个条目类型检查
		if entrytype not in typestrings:
			print('Warning: entrytype "',entrytype,'" has no typestring!!!')
			
		if isinstance(entryfmt,list):
			for fieldfmt in entryfmt:#对条目中的每个域设置进行检查
				for opt,optval in fieldfmt.items():#对每个域的设置选项进行检查:
					if opt not in keyoptiondatabase:
						try:
							print('Error: style set option "'+opt+'" is not defined!\n')
							raise MapStyleSetError('Error: style set option is not defined!')
						except MapStyleSetError as e:
							raise MapStyleSetError(e.message)
							
					if opt=='options':
						for k,v in optval.items():
							if k not in formatoptiondatabase:
								try:
									print('Error: style set option "'+k+'" is not defined!\n')
									raise MapStyleSetError('Error: style set option "'+k+'" is not defined!\n')
								except MapStyleSetError as e:
									raise MapStyleSetError(e.message)
							else:
								if v not in formatoptiondatabase[k]:
									try:
										print('Error: style set option value"'+v+'" of option"'+k+'" is not defined!\n')
										raise MapStyleSetError('Error: style set option value"'+v+'" of option"'+k+'" is not defined!\n')
									except MapStyleSetError as e:
										raise MapStyleSetError(e.message)
	return None				
	
	

			
#运行脚本测试
if __name__=="__main__":


	#biblatex-map或bibmap的逻辑如下：
	#输入由命令行参数确定，输出由设置参数确定，输出类型是固定的
	#输入最主要的时aux文件，程序从其中读取指定的bib文件和饮用的文献关键词
	#输入的aux文件没有指定bib文件时将会报错，这时可以用-b选项指定bib文件，
	#当给出-b选项指定bib文件时，aux文件中也存在指定的bib文件，此时以aux文件指定为准。
	#aux文件指定可以用-a选项，也可以直接给出，
	#当给出一个文件时，如果指定后缀名为bib，那么处理的时bib文件
	#如果指定后缀名为aux，那么处理的时aux文件的逻辑，
	#如果没有指定后缀名，那么默认是aux文件
	#如果没有获取bib文件信息，那么会报错
	bibmapinput()
	
	if False:
		a=r'Food {Irradiation} Research \LaTeX{} and \textbf{Technology} paper II'
		print(a)
		print(mkstrsetencecase(a))
		print(mkstrtitlecase(a))
		print(mkstruppercase(a))
		print(mkstrlowercase(a))
		print(mkstrsmallcaps(a))

	
	
	if False:
		#设置需要修改的bib文件
		#inputbibfile='example.bib'
		#inputbibfile='biblatex-map-test.bib'
		inputbibfile='eg-thesis.bib'
		
		#auxfile="opt-gbpub-true.aux"
		#set the aux file
		#this is not necessary
		auxfile=''
		#auxfile="opt-gbpub-true.aux"
		
		readfilecontents(inputbibfile)
		
		#printfilecontents()

		bibentryparsing()
		
		#printbibentries()
		
		execsourcemap()
		
		#printbibentries()
		
		writefilenewbib(inputbibfile)
		
		#print(bibentries[0])

		#print(formatbibentry(bibentries[0]))
		
		formatallbibliography()
		printbibliography()
		