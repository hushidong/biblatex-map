


#### 20190320

* 完善对article的测试
测试其它类型，比如periodical等

* 姓名格式的其它选项实现，比如拼音

* 文本输出的内容中去掉{}
输出给bbl的保留

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