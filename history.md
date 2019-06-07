


1. 目前读取文件的bib文件应该是utf-8 无bom格式。

2. 著录表中的extrayear是否要处理？目前暂无需求


5. 一些biblatex的map选项需要实现，包括
		entryclone=?clonekey?
		entrynew=?entrynewkey?
		entrynewtype=?string?
		entrytarget=?string?
		entrynocite=true, false default: false
		entrynull=true, false default: false
		match 大小写区分的matchi
		
		
		
#### 20190607

1. pyinstaller打包成exe文件

	方法：
	
		1. 安装pyinstaller

		下载，解压，进入目录，然后使用命令：

		python setup.py install

		连网会自动处理依赖问题。
		(不连网处理起来估计会比较麻烦，但可以查看一下怎么在anaconda下安装pyinstaller)


		2. 打包程序：

		1、使用下载安装的方式安装的Pyinstaller打包方式

		将需要打包的文件放在解压得到的Pyinstaller文件夹中，打开cmd窗口，把路径切换到当前路径打开命令提示行，输入以下内容（最后的是文件名）：

		python pyinstaller.py -F myfile.py

		2、使用pip方式安装的Pyinstaller打包方式

		打开cmd窗口，把路径切换到文件所在路径(文件随便放在哪里都行)打开命令提示行，输入以下内容（最后的是文件名）：

		pyinstaller -F myfile.py
		
#### 20190419

* bibmap宏包的完善
		
* 文档内的多个文献表的解决用chapterbib，兼容性测试完成

* natbib报错的排除，当采用上标标签时，引用前面应该有内容，否则第一个会包unskip不能再垂直环境中使用的问题。


* 文本输出替换，bbl输出的替换，HTML不同的替换，三者不同的替换要考虑

文本中{}的忽略，而输出到tex的文本中的{}不忽略
到正常文本中的利用符号追踪方法成对的消除{}，或者也不消除，
而是在html文件中做类似于tex中的编组操作，保护大小写的作用要体现。
保护大小写的{}在域处理中必须要处理完成，而用于格式的编组{}必须要保留。
输出给bbl的保留，对于tex和html关键是\url等命令可能需要的替换

		
#### 20190418

1. uniquename和uniquelist完善。

从遍历的角度重新设计了uniquename选项下的比较，uniquelist只是利用uniquename，因为它只是姓名数量的扩张，没有其它的变化。
		

#### 20190416

1. 当需要对标题等域做大小写转换是，要把命令进行保护，比如\LaTeX等

* 标注姓名的歧义处理。初步实现uniquename，uniquelist等选项。

* 姓名的前后缀

* 标注中的姓名处理

* Anon可以在著录格式设置中，用替代字符串实现。或者在bib数据修改时增加域的处理。		

* natbib 做标注样式的修改，测试。
		
#### 20190415

* 借鉴xpinyin的方式实现拼音输出，借鉴perl模块和unicodecldr的实现拼音和笔画排序。

* readme 英文版的更新。

#### 20190413
		
* 姓名格式的其它选项实现，比如拼音
		
#### 20190412
		
*  py不再同目录下怎么处理？？

通过加载当前目录到sys.PATH中的方法解决当前目录下模块的导入。


#### 20190411

* 文献的排序及序号,已实现。


* 用法说明文档：
{包括设置的方式，其中的选项}，完成整个逻辑的过程中完善代码
		
		
#### 20190410

* 检查格式是否写正确
	1. 即用选项是否在设定范围内来进行检查
	比如有时会笔误，posstring写出postring

	2. 一些设置参数的检查，
	比如datatypeinfo={}的内部设置中缺少了都好，导致的问题。一般情况下无法发现？
	
	完成了检查机制。

* 改名为bibmap，并做了bibmap宏包

* 可以设置不做格式化。利用nofmt选项

* 作者年制的标签和thebibliography环境中的参数设置，从egtest编译开始全套走

* 文献表中空格导致的间距扩大问题如何解决？？
利用allowbreak去掉中英文之间的空格
其它正常处理，利用newblock，空格等处理，
其中url的内容进行了特别的处理。

* 一些格式的处理时用prestring和posstring呢还是其他？

* 检查一下格式处理后，解析出的信息比如year，month等是否已经存储到bibentry中

* 两大主要功能的处理逻辑
	1. 对bib文件的直接处理？
	2. 对tex文件的辅助bib处理？

* 完善对article的测试，测试其它类型，比如periodical等

* 基本样式测试完毕，基本已经够用。

* literal类型的格式选项：sentencecase，5中case已经完成

* range类型的格式选项

* edition中的英文的序号问题？？ordinal的问题，ordinal不能简单的替换，因为它与数值有关，
那么怎么做处理？？同时还要中英文区分，所以怎么处理？
'numberformat':'ordinal'，'arabic'，'alpha'等？？
最后选择用传递选项来处理域。
		
#### 20190324

* 文件的输入改为命令输入，而不在脚本内指定

* bbl配合natbib文件使用时的处理
		

#### 20190321

* 初步完成bbl文件的输出，便于在tex文件中直接应用

* 初步完成bibitem的[]中的信息的处理，需要进一步完善


#### 20190315

* 日期的条目内选项控制
增加options选项的传递

* 姓名的条目内选项控制
增加options选项的传递




#### 20190314

* 保护字符串不做分割，但出于不同的位置时可能逻辑是不同的。
比如整个姓名做了保护字符串，那么带花括号的整个命名仅都作为family，和familyi
比如仅对名做保护，那么仅做given和giveni，giveni不再抽取，因为已经保护了，所以是一个整体。

* 文本项的列表也采用同样的逻辑处理

#### 20190313

* 测试大多数的文献适应性
思考花括号的保护作用实现？？
在姓名列表中，在文本列表中，在文本域，在日期域，在范围域


#### 20190312


* 增加选项可以去除姓名列表中的others情况，用morenames选项
* 处理文本的列表，others用moreitems选项设置
* 处理日期的解析和格式，日期与卷一样先把范围解析完毕，然后对当个日期做解析



#### 20190311

* 姓名处理进一步完善
中文作者中存在‘, ’的处理
是否使用名的首字母处理

* 格式化文本的输出
输出文本文件，用md为后缀
输出网页文件，用html为后缀


#### 20190310 

* 姓名处理初步考虑：把姓名列表分解为单个姓名，然后把单个姓名再分解为姓名成分
格式化时，单个姓名根据选项格式化
姓名间的标点用localpuncts来替换
姓名内的本地化字符串用localstrings来替换
字符串导致的多重点用直接替换的方式解决。

* 完善了bib文件解析，包括无包围符号的域值的解析，comment，string类型的解析。

#### 20190309及以前

1. souce map of biblatex like: generalize date
bib文件数据修改，比如对日期进行规范化等

2. bib file parsing, bib file out, json formatted file out
bib文件解析，输出新的bib文件，或json格式的文件

3. display the bib info with specific standard like GB/T 7714-2015
将bib文件信息格式化显示，比如以GB/T 7714-2015格式显示

4. 当某些项缺失时，后面跟着的项前标点可能会变化的问题，要处理。
利用prepunctifnolastfield选项处理

5. newspaper,与aritcle的关系
不像biblatex中需要用note来标记，而直接用newpaper类型，使用article类型的格式，但是年份需要修改。
同样是date，newspaper需要写全，而article不需要，这利用dateformat选项处理

6. standard,与book和inbook的关系
直接用inbook代替，但利用omitifnofield选项，处理好//

7. [S.l.]: [s.n.]合并
利用replacestrings单独做替换

8. 当存在载体域时加上载体
在title域中对\typestring做处理

9. 使用了@string字符串的输出要处理，可以采用全局选项控制的方式实施。
这将在开始格式化之前对域值进行替换
这时还进行
date范围解析，年月日的解析放到域格式处理中
volume和number的范围解析
pages中的间隔符替换

10. 当出版项不存在，而url存在是，日期格式从普通的year变为iso格式带()
利用omitifnofield，omitiffield做两次date处理

11. 本地化字符串处理
在域格式处理时，利用\bibstring做不同语言的替换

12. 需要整数做的处理
用的 posstringifnumber 选项


#### 20190209及以前

实现map功能，biblatex source map opts：

biblatex中数据处理已实现的选项：
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