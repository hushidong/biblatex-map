import re

#
#
#对{}做保护的字符串分割
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
	
a='{Research Group of Shanghai Food and Drug Administration} and {ABC} AND {CDE and edf}'
seps=[' and ',' AND ']
print(safetysplit(a,seps))

a='{昂温, G} and {昂温, P S}'
seps=[' and ']
print(safetysplit(a,seps))

a='{昂温, G}'
seps=[',']
print(safetysplit(a,seps))

a='{昂温, P S}'
seps=[',']
print(safetysplit(a,seps))

a='昂温, G'
seps=[',']
print(safetysplit(a,seps))

a='昂温, P S'
seps=[',']
print(safetysplit(a,seps))

a='{LI Jiangning}'
seps=[' ']
print(safetysplit(a,seps))

a='LI {Jiang ning}'
seps=[' ']
print(safetysplit(a,seps))