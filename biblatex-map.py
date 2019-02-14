﻿#!/usr/bin/env python

"""
python script to modify bib data

features：
1. souce map of biblatex
2. generalize date

history：
v1.0 2019/02/09

biblatex source map opts：

已实现的选项：
typesource=?entrytype?
typetarget=?entrytype?
fieldsource=?entryfield?
fieldtarget=?entryfield?
match=?regexp?
matchi=?regexp?
notmatch=?regexp?
notmatchi=?regexp?
replace=?regexp?

notfield=?entryfield?
final=true, false default: false
origfieldval=true, false default: false
append=true, false default: false
pertype
pernottype

fieldset=?entryfield?
fieldvalue=?string?
null=true, false default: false
origfield=true, false default: false
origentrytype=true, false default: false
origfieldval=true, false default: false



未实现的选项

entryclone=?clonekey?
entrynew=?entrynewkey?
entrynewtype=?string?
entrytarget=?string?
entrynocite=true, false default: false
entrynull=true, false default: false

1. match 大小写区分的match

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


#
# 为数据map设置参数
# 选项的逻辑与biblatex基本一致，
# 差别包括:overwrite选项可以放到step步中表示
#[]=maps
#[[],[]]=map in maps
#[[[]],[]]=step in map in mpas
#[[[{optionkey: }]],[]]=step in map in mpas
#注意python正则表达方式与perl的略有不同，比如unicode表示
#python用\xHH,\uHHHH,\UHHHHHHHH表示，而perl直接用\x{HHHH}表示。
sourcemaps=[#maps
	[#map1:将ELECTRONIC类型转换为online类型
		[{"typesource":"ELECTRONIC","typetarget":"online"}]#step1
	],
	[#map2:将source域转换为url域
		[{"fieldsource":"source","fieldtarget":"url"}]#step1
	],
	[#map3:将urldate域的信息“yyyy-m-d”转换为“yyyy-mm-dd”,注意正则表达式直接写不用在外面套""
		[{"fieldsource":"urldate","match":r'(\d\d\d\d)\-(\d)\-(\d)',"replace":r'\1-0\2-0\3'}]#step1
	],
	[#map4:将urldate域的信息“yyyy-m-d”转换为“yyyy-mm-dd”,注意正则表达式直接写不用在外面套""
		[{"fieldsource":"date","match":r'(\d\d\d\d)\-(\d)\-(\d)',"replace":r'\1-0\2-0\3',"overwrite":True}]#step1
	],
	[#map5:将refdate域转换为urldate域
		[{"fieldsource":"refdate","fieldtarget":"urldate"}]#step1
	],
	[#map6:对于newspaper类型，设置note为news
		[{"pertype":"newspaper"}],#step1
		[{"fieldset":"note","fieldvalue":"news","overwrite":True}]#step2
	],
	[#map7:设置edition域等于version
		[{"fieldsource":"version","final":True}],#step1
		[{"fieldset":"edition","origfieldval":True}]#step2
	],
	[#map8:设置entrykey域设置给keywords
		[{"fieldsource":"entrykey"}],#step1
		[{"fieldset":"keywords","origfieldval":True}]#step2
	],
	[#map9:对于存在note域的情况，将其值添加到keywords
		[{"fieldsource":"note","final":True}],#step1
		[{"fieldset":"keywords","origfieldval":True,"overwrite":True,"append":True}]#step2
	],
	 [#map10:根据标题的字符编码范围确定标题的语言类型
		 [{"fieldsource":"title","match":r'[\u2FF0-\u9FA5]',"final":True}],#step1
		 [{"fieldset":"userd","fieldvalue":"chinese"}]#step2
	 ],
]



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
	biboutfile="new"+bibFile
	print("INFO: writing references from '" + biboutfile + "'")
	try:
		fout = open(biboutfile, 'w', encoding="utf8")
		fout.write("%% \n")
		fout.write("%% bib file modified by bibmap.py\n")
		print(datetime.datetime.now().isoformat(timespec='seconds'))
		fout.write("%% "+datetime.datetime.now().isoformat(timespec='seconds')+"\n")
		fout.write("%% \n\n\n")
		for bibentry in bibentries:
			fout.write('@'+bibentry["entrytype"]+'{'+bibentry["entrykey"]+',\n')
			for k,v in bibentry.items():
				if k=="entrytype" or k=="entrykey" or v=='""' or v==None:
					pass
				else:
					fout.write('\t'+k+' = {'+v+'},\n')
			fout.write('}\n\n')
		
		fout.close()
	except IOError:
		print("ERROR: Input bib file '" + bibFile +
				"' doesn't exist or is not readable")
		sys.exit(-1)
		
#
#将条目解析放到bibentries列表中
#每个条目是一个dict字典
def bibentryparsing():
	global bibentries
	bibentries=[]
	bibentry={}
	entrysn=0
	for line in bibfilecontents:
		#print(line)
		if line.startswith("@"):#条目开始行
			entrysn=entrysn+1
			entrynow=line.lstrip('@').split(sep='{', maxsplit=1)
			#print(entrynow)
			entrytype=entrynow[0]
			bibentry['entrytype']=entrytype.lower()#条目类型小写，方便比较
			entrykey=entrynow[1].split(sep=',', maxsplit=1)[0]
			bibentry['entrykey']=entrykey
		else:
			if '=' in line:#条目域信息行
				entryline=line.lstrip()
				entrynow=entryline.split(sep='=', maxsplit=1)
				#print(entrynow)
				entryfield=entrynow[0].strip().lstrip().lower()#域名小写，方便比较
				#print(entrynow[1])
				entryfieldline=entrynow[1].split(sep=',', maxsplit=1)
				entryfieldvalue=entryfieldline[0].lstrip()
				if entryfieldvalue=='':
					pass
				else:
					entryfieldvaluenew=entryfieldvalue.strip()
					if entryfieldvaluenew.startswith("{"):
						entryfieldvalue=entryfieldvaluenew.lstrip('{').strip('}')
					else:
						entryfieldvalue=entryfieldvaluenew.lstrip('"').strip('"')
					bibentry[entryfield]=entryfieldvalue
				
					
			elif '}' in line:#条目结束行
				print('entrysn=',entrysn)
				global bibentryglobal
				bibentryglobal=copy.deepcopy(bibentry) 
				bibentries.append(bibentryglobal)
				bibentry={}
			else:
				pass
	bibentrycounter=len(bibentries)
	print('entrytotal=',bibentrycounter)
	for bibentryi in bibentries:
		print(bibentryi)
			
def printbibentries():
	for bibentryi in bibentries:
		print(bibentryi)	
			

		
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
			
			print("map info=",map)
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
	
					
				

		
#运行脚本测试
if __name__=="__main__":
    
    #设置需要修改的bib文件
	inputbibfile='biblatex-map-test.bib'
    
    
	readfilecontents(inputbibfile)
	
	printfilecontents()

	bibentryparsing()
	
	printbibentries()
	
	execsourcemap()
	
	printbibentries()
	
	writefilenewbib(inputbibfile)
    
    
		