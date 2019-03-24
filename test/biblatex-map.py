#!/usr/bin/env python

"""
A python script to modify bib data and 
to display references with specific bibliography standard

two key features：

两大核心功能
1. bib文件抽取，bib文件内容的自定义修改
2. 格式化文献表输出，包括json，bib，text，html，bbl文件，其中bbl文件可以在tex源代码中直接使用，利用natbib宏包可以实现不同的标注样式。


"""

__author__ = "Hu zhenzhen"
__version__ = "1.0"
__license__ = "MIT"
__email__ = "hzzmail@163.com"

import string
import re
import sys
import datetime
import copy
import json
import operator #数学计算操作符
import argparse #命令行解析


#
#
#打印格式化后的全部文献条目文本
def printbibliography():
	
	
	#md文件输出,直接用write写
	mdoutfile="newformatted"+inputbibfile.replace('.bib','.md')
	fout = open(mdoutfile, 'w', encoding="utf8")
	print("INFO: writing cited references to '" + mdoutfile + "'")
	
	biblabelnumber=0
	for entrykey,prtbibentry in bibliographytext.items():
		if len(prtbibentry)>0:
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
	for entrykey,prtbibentry in bibliographytext.items():
		if len(prtbibentry)>0:
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
	bbloutfile=bblfile
	fout = open(bbloutfile, 'w', encoding="utf8")
	print("INFO: writing cited references to '" + bbloutfile + "'")
	
	fout.write(r'\begin{thebibliography}{'+str(len(bibentries))+'}\n')
	
	biblabelnumber=0
	for entrykey,prtbibentry in bibliographytext.items():
		if len(prtbibentry)>0:
			biblabelnumber=biblabelnumber+1
			
			entrykeystr=entrykey
			
			for bibentry in bibentries:
				if bibentry['entrykey']==entrykey:
					entryciteauthor=formatlabelauthor(bibentry)
					entryciteyear=formatlabelyear(bibentry)
					entrycitelabel=entryciteauthor[0]+'('+entryciteyear+')'+entryciteauthor[1]
					#Baker et~al.(1995)Baker and Jackson
					break
			
			if formatoptions['style']=='authoryear':
				fout.write(r'\bibitem['+entrycitelabel+']{'+entrykeystr+'}'+prtbibentry+'\n')
			else:
				fout.write(r'\bibitem['+str(biblabelnumber)+']{'+entrykeystr+'}'+prtbibentry+'\n')
			
	fout.write(r'\end{thebibliography}')
	fout.close()



#
#authoryear样式提供标注标签的作者信息
#
def formatlabelauthor(bibentry):
	
	if 'author' in bibentry:
		namelist=bibentry['author']
	elif 'editor' in bibentry:
		namelist=bibentry['editor']
	elif 'translator' in bibentry:
		namelist=bibentry['translator']
	else:
		namelist='Anon'
		
	return [namelist,namelist]

#
#authoryear样式提供标注标签的年份信息
#
def formatlabelyear(bibentry):
	
	if 'year' in bibentry:
		yearlist=bibentry['year']
	elif 'eventyear' in bibentry:
		yearlist=bibentry['eventyear']
	elif 'origyear' in bibentry:
		yearlist=bibentry['origyear']
	elif 'urlyear' in bibentry:
		yearlist=bibentry['urlyear']
	else:
		yearlist='N.D.'
		
	return yearlist


#
#
#格式化全部文献条目文本
def formatallbibliography():
	labelnumber=0
	global bibliographytext
	bibliographytext={}
	for bibentry in bibentries:
		if bibentry["entrykey"] in usedIds or not usedIds:
			labelnumber=labelnumber+1
			bibentry['labelnumber']=labelnumber
			bibentrytext=''
			bibentrytext=formatbibentry(bibentry)
			bibliographytext[bibentry["entrykey"]]=bibentrytext
		
	print('\nreferecences')
	print(bibliographytext)

#
#
#格式化一个文献条目文本
def formatbibentry(bibentry):
	
	print('--------------new entry---------')
	print('\nbibentry:',bibentry)
	#bibentrytext='entry:'
	
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
	
	#四种日期域也做范围解析
	if 'date' in bibentry:
		if '/' in bibentry['date']:
			datestring=bibentry['date'].split('/')
			bibentry['date']=datestring[0]
			bibentry['enddate']=datestring[1]
	
	if 'urldate' in bibentry:
		if '/' in bibentry['urldate']:
			datestring=bibentry['urldate'].split('/')
			bibentry['urldate']=datestring[0]
			bibentry['endurldate']=datestring[1]
	
	if 'eventdate' in bibentry:
		if '/' in bibentry['eventdate']:
			datestring=bibentry['eventdate'].split('/')
			bibentry['eventdate']=datestring[0]
			bibentry['endeventdate']=datestring[1]
	
	if 'origdate' in bibentry:
		if '/' in bibentry['origdate']:
			datestring=bibentry['origdate'].split('/')
			bibentry['origdate']=datestring[0]
			bibentry['endorigdate']=datestring[1]
	
	#
	#接着处理所有域到一个条目文本
	#
	bibentrytext=''
	
	if bibentry['entrytype'] in bibliographystyle:
		print('INFO: format style of entrytype',bibentry['entrytype'],'is defined.')
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
	
	#对替换字符串做处理
	#包括对重复的标点做处理比如：..变为.
	for k,v in replacestrings.items():
		print(k,v)
		#m=re.search(k,bibentrytext)
		#print(m)
		#bibentrytext=re.sub(k,v,bibentrytext)
		#利用正则反而不行，直接用字符串替换
		bibentrytext=bibentrytext.replace(k,v)
	
	print(bibentrytext)
	return bibentrytext



#
#
#格式化文献条目的域
#不同类型的域不同处理
#分5类：姓名列表，文本列表，文本域，日期域，范围域
#其中姓名列表，文本列表，日期域，日期域，范围域，都需要进行特殊的解析
#而volume，number如果需要特殊解析则在文件域的格式处理时增加新的处理逻辑。
def formatfield(bibentry,fieldinfo,lastfield):

	print('fieldinfo:',fieldinfo)
	#首先把域的内容先解析处理
	fieldcontents=''
	
	fieldsource=None

	#首先判断域是否忽略
	fieldomit=False
	
	if 'omitifnofield' in fieldinfo and 'omitiffield' in fieldinfo:

		fieldomita=True#假设忽略的条件满足
		for field in fieldinfo['omitifnofield']:#只要需要不存在的域有一个存在，那么条件就不满足
			if field in bibentry:
				fieldomita=False
				break

		fieldomitb=False#假设忽略的条件不满足
		for field in fieldinfo['omitiffield']:#只要需要存在的域中有一个存在，那么条件就满足
			if field not in bibentry:
				fieldomitb=True
				break

		fieldomit=fieldomita and fieldomitb
		
	elif 'omitifnofield' in fieldinfo:
		
		fieldomit=True#假设忽略的条件满足
		for field in fieldinfo['omitifnofield']:#只要需要不存在的域有一个存在，那么条件就不满足
			if field in bibentry:
				fieldomit=False
				break
		
	elif 'omitiffield' in fieldinfo:
		
		fieldomit=False#假设忽略的条件不满足
		for field in fieldinfo['omitiffield']:#只要需要存在的域中有一个存在，那么条件就满足
			if field not in bibentry:
				fieldomit=True
				break
	
	print(fieldomit)
	
	
	#如果不忽略该域那么：
	if not fieldomit:
		
		#当域为姓名列表域时：
		if fieldinfo['fieldsource'][0] in  datatypeinfo['namelist']:
			#print('0',fieldinfo['fieldsource'][0])
			#print('author' in bibentry)
			for field in fieldinfo['fieldsource']:#
				#print(fieldinfo['fieldsource'])
				#print('namelist:',field)
				if field in bibentry:#当域存在域条目中时，确定要处理的域
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
				if field in bibentry:#当域存在域条目中时，确定要处理的域
					fieldsource=field
					break
			if fieldsource:
				fieldcontents=literallistparser(bibentry,fieldsource)
				
		#当域为文本域时：
		elif fieldinfo['fieldsource'][0] in  datatypeinfo['literalfield']:

			for field in fieldinfo['fieldsource']:#
				if field in bibentry:#当域存在域条目中时，确定要处理的域
					fieldsource=field
					break
			if fieldsource:
				fieldcontents=literalfieldparser(bibentry,fieldsource)
				
		
		#当域为日期域时：
		elif fieldinfo['fieldsource'][0] in  datatypeinfo['datefield']:

			for field in fieldinfo['fieldsource']:#
				if field in bibentry:#当域存在域条目中时，确定要处理的域
					fieldsource=field
					break
			if fieldsource:
				#传递条目给出的一些控制选项
				if 'options' in fieldinfo:
					options=fieldinfo['options']
				else:
					options={}
				fieldcontents=datefieldparser(bibentry,fieldsource,options)
				
				
		#当域为范围域时：
		elif fieldinfo['fieldsource'][0] in  datatypeinfo['rangefield']:

			for field in fieldinfo['fieldsource']:#
				if field in bibentry:#当域存在域条目中时，确定要处理的域
					fieldsource=field
					break
			if fieldsource:
				fieldcontents=rangefieldparser(bibentry,fieldsource)
	
	if not fieldsource:
		if 'replstring' in fieldinfo and fieldinfo['replstring']:
			print('replstring')
			fieldsource=True
			fieldcontents=fieldinfo['replstring']
			
	
	#接着做进一步的格式化，包括标点，格式，字体等
	fieldtext=''
	
	print(fieldsource)
	if fieldsource:
		if lastfield:#当前一个著录项存在，则正常输出
			if 'prepunct' in fieldinfo:
				fieldtext=fieldtext+fieldinfo['prepunct']
		else:#当前一个著录项不存在，则首先输出'prepunctifnolastfield'
			if 'prepunctifnolastfield' in fieldinfo:
				fieldtext=fieldtext+fieldinfo['prepunctifnolastfield']
			elif 'prepunct' in fieldinfo:
				fieldtext=fieldtext+fieldinfo['prepunct']
		
		if 'prestring' in fieldinfo:
			fieldtext=fieldtext+fieldinfo['prestring']
		
		if 'fieldformat' in fieldinfo:
			fieldtext=fieldtext+'{'+fieldinfo['fieldformat']+'{'+fieldcontents+'}}'
		else:
			fieldtext=fieldtext+str(fieldcontents)
		
		if 'posstring' in fieldinfo:
			fieldtext=fieldtext+fieldinfo['posstring']
			
		if 'posstringifnumber' in fieldinfo:
			try:
				numtemp=int(fieldcontents)
				if  isinstance(numtemp,int):
					fieldtext=fieldtext+fieldinfo['posstringifnumber']
			except:
				print('info:waring the field value can not convert to integer')
		
		if 'pospunct' in fieldinfo:
			fieldtext=fieldtext+fieldinfo['pospunct']
			
		#更新lastfiled
		lastfield=True
	else:
		lastfield=False
	
	
	#自定义标点的处理
	print('fieldtext:',fieldtext)
	while r'\printdelim' in fieldtext:
		
		m = re.search(r'\\printdelim{([^\}]*)}',fieldtext)#注意贪婪算法的影响，所以要排除\}字符
		print('m.group(1):',m.group(1))
		fieldtext=re.sub(r'\\printdelim{[^\}]*}',localpuncts[m.group(1)],fieldtext,count=1)
		print('fieldtext:',fieldtext)
	
	
	#本地化字符串的处理
	print('fieldtext:',fieldtext)
	while r'\bibstring' in fieldtext:
		
		language=languagejudgement(bibentry,fieldinfo,fieldsource)
		m = re.search(r'\\bibstring{([^\}]*)}',fieldtext)#注意\字符的匹配，即便是在r''中也需要用\\表示
		fieldtext=re.sub(r'\\bibstring{[^\}]*}',localstrings[m.group(1)][language],fieldtext,count=1)
		print('fieldtext:',fieldtext)
		#下面这句不行因为，在字典取值是，不支持\1这样的正则表达式
		#fieldtext=re.sub(r'\\bibstring{(.*)}',localstrings[r'\1'][language],fieldtext,count=1)
	
	#标题的类型和载体标识符的处理
	if r'\typestring' in fieldtext:#当需要处理类型和载体时
		if bibentry['entrytype'] in typestrings:#当条目对应的类型存在时
			print(r'\typestring in',fieldtext)
			typestring=typestrings[bibentry['entrytype']]
			if 'url' in bibentry:
				typestring=typestring.replace(']','/OL]')
			elif 'medium' in bibentry:
				rplctypestring=bibentry['medium']+']'
				typestring=typestring.replace(']',rplctypestring)
		else:#当条目对应的类型不存在时，当做其它类型处理
			typestring='[Z]'

		print(typestring)
		fieldtext=fieldtext.replace(r'\typestring',typestring)
		
	return [fieldtext,lastfield]





#
#根据作者域或者标题域确定条目的语言
#
def languagejudgement(bibentry,fieldinfo,fieldsource):

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

	if re.match(r'[\u2FF0-\u9FA5]', fieldvalueinfo):
		language='chinese'
	elif re.match(r'[\u3040-\u30FF\u31F0}-\u31FF]', fieldvalueinfo):
		language='japanese'
	elif re.match(r'[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7AF]', fieldvalueinfo):
		language='korean'
	elif re.match(r'[\u0400-\u052F]', fieldvalueinfo):
		language='russian'
	elif re.match(r'[\u0100-\u017F]', fieldvalueinfo):
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
		for name in names:
			strsn=0
			for stra1 in s1:
				strsn=strsn+1
				name=name.replace('$'+str(strsn)+'$',stra1)
			#print(name)
			namesnew.append(name.strip().lstrip())
		
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
			namesnew.append(name.strip().lstrip())
		
	#print(namesnew)
	return namesnew

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
	fieldcontents=fieldcontents.lstrip().strip()
	fieldauthors=safetysplit(fieldcontents,seps)

	print('fieldauthors:',fieldauthors)
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
	
	#当条目选择中存在'nameformat'
	if 'nameformat' in options:
		option={'nameformat':options['nameformat']}
	else:
		option={}
	
	print('fieldnamestrunc:',fieldnamestrunc)
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
	
	
	if 'nameformat' in option:#首先使用条目给出的选项
		nameformat=option['nameformat']
	elif 'nameformat' in formatoptions:#接着使用全局的选项
		nameformat=formatoptions['nameformat']
	else:#最后使用默认的选项
		nameformat='uppercase'
	
	
	#根据单个姓名格式化选项来实现具体的格式
	if nameformat=='uppercase':
		
		if nameinfo['family'].startswith('{'):
			singlenamefmtstr=nameinfo['family']
		else:
			singlenamefmtstr=nameinfo['family'].upper()
		
		#根据选项确定使用名的缩写
		if formatoptions["giveninits"]=='space':#space表示名见用空格分隔，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middlei'].upper()
		elif formatoptions["giveninits"]=='dotspace':#dotspace用点加空格，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+'. '+nameinfo['middlei'].upper()+'.'
		elif formatoptions["giveninits"]=='dot':#dot用点，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+'.'+nameinfo['middlei'].upper()+'.'
		elif formatoptions["giveninits"]=='terse':#terse无分隔，
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['giveni'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+nameinfo['middlei'].upper()
		elif formatoptions["giveninits"]=='false':#false不使用缩写
			if 'given' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['given'].upper()
			if 'middle' in nameinfo:
				singlenamefmtstr=singlenamefmtstr+' '+nameinfo['middle'].upper()

		
	elif nameformat=='lowercase':
		pass
	elif nameformat=='given-family':
		pass
	elif nameformat=='family-given':
		pass
	elif nameformat=='pinyin':
		pass
	else:
		pass
	
	return singlenamefmtstr


#
#
#单个姓名解析
def singlenameparser(name):
	
	singlename=name
	
	print('name:',name)
	
	#字典用于存储所有的姓名成分信息
	namepartsinfo={}
	
	nameparts=safetysplit(singlename,[','])
	
	if len(nameparts)==3:#两个逗号的情况，表示存在family和suffix
		
		prefixfamily=safetysplit(nameparts[0].lstrip().strip(),[' '])
		if len(prefixfamily)>1:
			namepartsinfo['prefix']=prefixfamily[0].lstrip().strip()
			namepartsinfo['family']=prefixfamily[1].lstrip().strip()
		else:
			namepartsinfo['family']=prefixfamily[0].lstrip().strip()
			
		namepartsinfo['suffix']=nameparts[1].lstrip().strip()
		
		
		givenmiddle=safetysplit(nameparts[2].lstrip().strip(),[' '])
		if len(givenmiddle)>1:
			namepartsinfo['given']=givenmiddle[0].lstrip().strip()
			namepartsinfo['middle']=givenmiddle[1].lstrip().strip()
		else:
			namepartsinfo['given']=givenmiddle[0].lstrip().strip()
		
	elif len(nameparts)==2:
		
		prefixfamily=safetysplit(nameparts[0].lstrip().strip(),[' '])
		if len(prefixfamily)>1:
			namepartsinfo['prefix']=prefixfamily[0].lstrip().strip()
			namepartsinfo['family']=prefixfamily[1].lstrip().strip()
		else:
			namepartsinfo['family']=prefixfamily[0].lstrip().strip()
			
		
		givenmiddle=safetysplit(nameparts[1].lstrip().strip(),[' '])
		if len(givenmiddle)>1:
			namepartsinfo['given']=givenmiddle[0].lstrip().strip()
			namepartsinfo['middle']=givenmiddle[1].lstrip().strip()
		else:
			namepartsinfo['given']=givenmiddle[0].lstrip().strip()
		
	else:
		givenmiddlefamily=safetysplit(nameparts[0].lstrip().strip(),[' '])
		if len(givenmiddlefamily)==3:
			namepartsinfo['given']=givenmiddlefamily[0].lstrip().strip()
			namepartsinfo['middle']=givenmiddlefamily[1].lstrip().strip()
			namepartsinfo['family']=givenmiddlefamily[2].lstrip().strip()
		elif len(givenmiddlefamily)==2:
			namepartsinfo['given']=givenmiddlefamily[0].lstrip().strip()
			namepartsinfo['family']=givenmiddlefamily[1].lstrip().strip()
		elif len(givenmiddlefamily)==1:
			namepartsinfo['family']=givenmiddlefamily[0].lstrip().strip()
	
	
	print('nameparts:',namepartsinfo)
	
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
	fieldcontents=fieldcontents.lstrip().strip()
	fielditems=safetysplit(fieldcontents,seps)
	
	print('fielditems:',fielditems)
	
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
def literalfieldparser(bibentry,fieldsource):
	fieldcontents=bibentry[fieldsource]
	
	return fieldcontents

#
#
#日期域解析
#条目设置的选项options:
def datefieldparser(bibentry,fieldsource,options):
	fieldcontents=bibentry[fieldsource]
	
	#首先从日期域，解析日期类型：
	dateparts={}
	if fieldsource=='year':
		datestring=bibentry[fieldsource]
		datetype=''
	else:
		datetype=fieldsource.replace('date','')
		datestring=bibentry[fieldsource]
		
		
	#日期的年月日解析
	#日期一般很少用{}进行保护，当保护的时候通常是整个进行包括，所以通常{}会出现在域的起始和末尾
	#所以当出现{字符时通常不用再做解析
	if '{' in datestring:
		datepartinfo=[datestring]
	else:
		datepartinfo=datestring.split('-')
	
	if len(datepartinfo)==3:
		dateparts[datetype+'year']=datepartinfo[0].strip().lstrip()
		dateparts[datetype+'month']=datepartinfo[1].strip().lstrip()
		dateparts[datetype+'day']=datepartinfo[2].strip().lstrip()
	elif len(datepartinfo)==2:
		dateparts[datetype+'year']=datepartinfo[0].strip().lstrip()
		dateparts[datetype+'month']=datepartinfo[1].strip().lstrip()
	else:
		dateparts[datetype+'year']=datepartinfo[0].strip().lstrip()
	
	print(dateparts)
	
	#判断解析的年月日是不是整数，若不是则表示日期不可解析
	datecanbeparse=True
	for k,v in dateparts.items():
		try:
			datepartisint=isinstance(int(v),int)
		except:
			print('INFO: WARNING'+fieldsource+'can not be parsed')
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
		if fieldsource=='year':
			fieldcontents=bibentry[fieldsource]
		else:
			fieldcontents=''
			
	return fieldcontents


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
	
	return fieldcontents


#
#
#打开bib文件
def readfilecontents(bibFile):
	print("INFO: Reading references from '" + bibFile + "'")
	try:
		fIn = open(bibFile, 'r', encoding="utf8")
		global bibfilecontents
		bibfilecontents=fIn.readlines()
		fIn.close()
		
		global usedIds
		usedIds = set()
		if inputauxfile:
			fInAux = open(inputauxfile, 'r', encoding="utf8")
			for line in fInAux:
				if line.startswith("\\citation") or line.startswith("\\abx@aux@cite"):
					ids = line.split("{")[1].rstrip("} \n").split(", ")
					for id in ids:
						if (id != ""):
							usedIds.add(id) #使用add方法，自动会判断set中是否已存在，若存在则不会添加
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
		fout.write("%% bib file modified by biblatex-map.py\n")
		
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
			print('entrysn=',entrysn)
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
					entryfield=entrynow[0].strip().lstrip().lower()#域名小写，方便比较
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
					print('entry:',bibentry)
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
					for chari in entryfieldline.strip():
						fieldvalue=fieldvalue+chari
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
			print(bibcomment)
			bibcomments.append(bibcomment)
			bibcomment={}
			
		elif line.startswith("@") and "@string" in line.lower():#@string的起始
			stringsn=stringsn+1
			entrynow=line.lstrip('@').split(sep='{', maxsplit=1)
			entrytype=entrynow[0]
			bibstring['entrytype']=entrytype.lower()#条目类型小写，方便比较
			entrycontents=entrynow[1].strip()[:-1]
			bibstring['entrycontents']=entrycontents
			print(bibstring)
			bibstrings.append(bibstring)
			bibstring={}

	
	bibentrycounter=len(bibentries)
	bibcommentcounter=len(bibcomments)
	bibstringcounter=len(bibstrings)
	print('entrysn=',entrysn,' commentsn=',commentsn,' stringsn=',stringsn)
	print('entryct=',bibentrycounter,' commentct=',bibcommentcounter,' stringct=',bibstringcounter)
	
	if not bibentrycounter==entrysn or not bibcommentcounter==commentsn or not bibstringcounter==stringsn:
		try:
			raise BibParsingError('bib file parsing went wrong!')
		except BibParsingError as e:
			raise BibParsingError(e.message)
	print('entrytotal=',bibentrycounter)
	
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
# 还有很多选项没有实现，20190209
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
					for keyvals in step:#key-vals in step
						for k,v in keyvals.items():#step 是有迹可循的，每个step总是存在一些东西，找到这些做其中的逻辑即可
							#print(k,v)
							
							if k=="typesource":#条目类型设置
								mapcontinue=maptypesource(keyvals,bibentry,typesrcinfo)#coef is dict
								
							elif k=="fieldsource":#域查找或设置
								mapcontinue=mapfieldsource(keyvals,bibentry,fieldsrcinfo,constraintinfo)#
								#print("fieldsource step:",fieldsrcinfo)
								
							elif k=="fieldset":#域设置
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
			elif k=='null':
				fieldvalue=None
				print(fieldvalue)
			elif k=='append':
				append=v
			elif k=='overwrite':
				overwrite=v
			else:
				pass
				
		
		print("fieldset=",fieldset)
		if overwrite:
			if append:
				oldvalue=bibentry[fieldset]
				newvalue=oldvalue+","+fieldvalue
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
			if fieldfinal:#当为true时则做终止判断
				mapfieldtype=3 #域map类型3，做final判断可以终止map
		elif k=='overwrite':#
			overwrite=v
		elif k=='match':#不区分大小写的match
			fieldmatch=v
		elif k=='matchi':#区分大小写的match
			fieldmatchi=v
		elif k=='notmatch':#不区分大小写的notmatch，下面这两个选项的逻辑没有实现
			fieldnotmatch=v
		elif k=='notmatchi':#区分大小写的notmatch
			fieldnotmatch=v
		else:
			pass
	
	
	if setcontinue:

		#返回字典的第一项是fieldsource信息
		fieldsrcinfo['fieldsource']=fieldsource
		
		if mapfieldtype==0:#第0中情况即，不做信息转换，也不终止map，仅返回一些信息
		
			if fieldsource in bibentry:
				if fieldmatch:
					m = re.match(fieldmatch, bibentry[fieldsource])
					if m:
						fieldsrcinfo[fieldsource]=[bibentry[fieldsource],fieldmatch]
					else:
						fieldsrcinfo[fieldsource]=[None] #正则不匹配，则返回为None

				elif fieldmatchi:
					m = re.match(fieldmatchi, bibentry[fieldsource])
					if m:
						fieldsrcinfo[fieldsource]=[bibentry[fieldsource],fieldmatchi]
					else:
						fieldsrcinfo[fieldsource]=[None] #正则不匹配，则返回为None
					
				else:
					fieldsrcinfo[fieldsource]=bibentry[fieldsource]#将域的值记录下来，用于下一step
			
			else:
				fieldsrcinfo[fieldsource]=[None] #域不存在则返回为None
			return 1
			
		
		elif mapfieldtype==1:#第1中情况即，做域名转换
			print('fieldsource=',fieldsource,'fieldtarget=',fieldtarget)
			if fieldsource in bibentry:
				bibentry[fieldtarget]=bibentry[fieldsource]
				del bibentry[fieldsource]
				fieldsrcinfo[fieldsource]=bibentry[fieldtarget]
			else:
				fieldsrcinfo[fieldsource]=[None]
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
					m = re.match(fieldmatch, bibentry[fieldsource])
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
inputbibfile=''
inputauxfile=''
inputstyfile='bibstylenumeric.py'
inputmapfile='bibmapdefault.py'


#
#命令行参数，输入文件处理，所有操作流程组织
#
def bibmapinput():
	#要使用全局变量先声明一下
	global inputbibfile,inputauxfile,inputstyfile,inputmapfile

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
		inputstyfile=inputfiles['mapfile']

		
		
	#3.接着辅助文件aux中提供的参数
	#可能有多个bib文件的需求，这个问题等明确chapterbib使用确定
	#辅助文件aux中提供的参数可以覆盖前面设置的参数
	if inputauxfile:
		fInAux = open(inputauxfile, 'r', encoding="utf8")
		for line in fInAux:
			if line.startswith("\\bibdata"):
				m = re.search(r'\\bibdata{(.*)}',line)#注意贪婪算法的影响，所以要排除\}字符
				print('m.group(1):',m.group(1))
				inputbibfile = m.group(1)
			if line.startswith("\\bibmap@bibstyle"):
				m = re.search(r'\\bibmap@bibstyle {(.*)}',line)#注意贪婪算法的影响，所以要排除\}字符
				print('m.group(1):',m.group(1))
				inputstyfile = m.group(1)
			if line.startswith("\\bibmap@mapstyle"):
				m = re.search(r'\\bibmap@mapstyle {(.*)}',line)#注意贪婪算法的影响，所以要排除\}字符
				print('m.group(1):',m.group(1))
				inputmapfile = m.group(1)
		fInAux.close()
	
	if not inputbibfile:
		try:
			raise BibFileinputError('error：未指定bib文件，请用-b选项直接指定或者在aux文件内指定！')
		except BibFileinputError as e:
			raise BibFileinputError(e.message)
			
	if not inputstyfile:
		try:
			raise BibFileinputError('error：著录格式设置文件出错，请重新指定！')
		except BibFileinputError as e:
			raise BibFileinputError(e.message)
			
	if not inputmapfile:
		try:
			raise BibFileinputError('error：数据修改设置文件出错，请重新指定！')
		except BibFileinputError as e:
			raise BibFileinputError(e.message)
			
	print(inputauxfile)
	print(inputbibfile)
	print(inputstyfile)
	print(inputmapfile)
	
	
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
	
	
	#导入设置参数模块，导入设置数据
	if '.py' in inputmapfile:
		strmapmodule=inputmapfile.replace('.py','')
	else:
		strmapmodule=inputmapfile
	mapmodule=__import__(strmapmodule)
	print(mapmodule)
	sourcemaps=mapmodule.sourcemaps
	if '.py' in inputstyfile:
		strsetmodule=inputstyfile.replace('.py','')
	else:
		strsetmodule=inputstyfile
	setmodule=__import__(strsetmodule)
	print(setmodule)
	formatoptions=setmodule.formatoptions
	localstrings=setmodule.localstrings
	localpuncts=setmodule.localpuncts
	replacestrings=setmodule.replacestrings
	typestrings=setmodule.typestrings
	datatypeinfo=setmodule.datatypeinfo
	bibliographystyle=setmodule.bibliographystyle
	
	
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
		