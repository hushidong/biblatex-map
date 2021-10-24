<b>Date of last change: 2021-10-23 to version v1.0d</b>


# bibmap 宏包

bibmap 是一个参考文献宏包，包含一个 sty 文件，用于设置参考文献处理时的选项;
一个 bibmap 程序，用于在后端处理参考文献数据。

bibmap 宏包加载了 natbib等宏包，用于 latex 参考文献标注和文献表的生成。
可以通过几个选项指定需要的标注样式、文献表著录样式、以及bib数据修改的样式。

bibmap 后端程序类似 bibtex/biber 程序用于处理参考文献数据，其输出类似于
bibtex， 为 bbl 文件，用于tex编译器读取后编译生成文献表。


## bibmap 宏包两大核心功能

### 参考文献表格式化

bibmap 宏包的标注样式基于natbbib宏包实现，而著录样式采用极简单的python代码来设置。

该功能主要特点包括:

* bibmap使用的样式文件为python代码构成的文本文件，设置极为方便，避免用户使用复杂的bst语法

* 根据样式文件输出格式化后的 bbl 文件，便于 latex 文档直接使用。

* 转存格式化的参考文献表文本为文本文件和网页文件，便于在其它文档中直
接使用。

* 除了 bibmap 程序内部处理逻辑外，样式文件可以全面控制参考文献的格式
化。

* bibmap 实现的内部处理: 根据选项进行排序，根据选项对姓名列表域、文本
列表域、日期域、文本域、范围域格式化，根据选项对条目输出项进行组织和格式化。

### bib 数据修改

bib 文件修改功能，借鉴 biblatex 的设计，逻辑基本一致，可以说是一套python 的重新实现，
可以对 bib 文件的条目和域做非常细致的处理和修改。

该功能主要特点包括:

* bib 文件的读取和解析

* bib 文件的转存，包括从大的 bib 文件抽取引用的文献保存为一个小的 bib 文
件，将 bib 文件的内容存储为 json 格式的问题。

* 参考文献条目的修改，包括条目类型的修改，条目内部的域的修改等，包括
删除、变化、转换等等。



## 用法：

### bibmap宏包

* 最小工作示例MWE

```
\documentclass{article}
    \usepackage{ctex}
    \usepackage{xcolor}
    \usepackage{toolbox}
    \usepackage{hyperref}
    \usepackage{lipsum}
    \usepackage[paperwidth=16cm,paperheight=10cm,top=10pt,bottom=10pt,left=1cm,right=1cm,showframe,showcrop]{geometry}
\usepackage[citestyle=numeric,bibstyle=gb7714-2015]{bibmap}
\usepackage{filecontents}
\begin{filecontents}{\jobname.bib}
@techreport{calkin,
  author       = {Calkin, D and Ager, A and Thompson, M},
  title        = {A Comparative Risk Assessment Framework for Wildland Fire
                 Management: the 2010 Cohesive Strategy Science Report},
  number       = {RMRS-GTR-262},
  year         = {2011},
  pages        = {8--9},
}
\end{filecontents}

    \begin{document}

    文献\cite{calkin}

    \bibliography{\jobname}

    \end{document} 
```

* 编译方式

四步编译:
```
xelatex jobname
bibmap.py jobname
xelatex jobname
xelatex jobname
```


### bibmap程序

bibmap程序，若直接使用py程序，那么需要python环境的支持。若在windows下可以直接使用打包成的bibmap.EXE。

bibmap程序的命令行参数如下:

```
bibmap.py
或
bibmap.exe

filename 单个输入文件的文件名，可带后缀名如bib或aux，无后缀名时默认为辅助文件.aux

[-h] 输出帮助

[-a AUXFILE] 辅助文件的文件名，可带后缀名.aux，如果filename已经设置aux文件则无效

[-b BIBFILE] 文献数据库文件名，可带后缀名.bib，如果filename已经设置bib文件则无效

[-s STYFILE] 设置文献样式文件的文件名，可带后缀名.py，不给出则使用默认样式文件

[-m MAPFILE] 数据库修改设置文件文件名，可带后缀名.py，不给出则使用默认设置文件

[--addpinyin] 给出该选项则将为每个文献条目增加带有拼音的key域。

[--nofmt] 给出该选项则不做格式化输出

[--nobdm] 给出该选项则不做bib数据修改
```

其中涉及到三种文件：

一是aux文件，如果是要得到格式化的文献表，那么这是最重要的文件，由tex编译生成，当使用bibmap宏包时，可以通过宏包选项设置样式文件，而bib文件通过bibliography命令也会在该文件中指出。

二是bib文件，这是参考文献数据源文件，可以由通过bibliography命令在aux文件内给出，也可以直接利用选项给出。

三是py文件，这是用于设置数据修改和文献格式化的文件，是python代码。宏包自带的样式，通常bibmap*.py是用于bib文件数据修改的，而bibstyle*.py是用于格式化文献表的。


使用方式为:



### bib文件修改

直接在命令行输入脚本及其参数：

`bibmap.py biblatex-map-test.bib`

或

`bibmap.exe biblatex-map-test.bib`

此时，bibmap读取biblatex-map-test.bib文件，并根据默认的数据修改设置bibmapdefault.py做修改，此时还会自动的做格式化后的文献表输出。

`bibmap.py biblatex-map-test.bib --nofmt`

或

`bibmap.exe biblatex-map-test.bib --nofmt`

此时不再输出格式化后的文献表。

`bibmap.py biblatex-map-test.bib --nofmt -m bibmapaddkw.py`

或

`bibmap.exe biblatex-map-test.bib --nofmt -m bibmapaddkw.py`

此时使用指定的数据修改设置bibmapaddkw.py代替默认的bibmapdefault.py对数据库bib文件做修改。


* 增加用于按拼音排序的key域

`python bibmap.py biblatex-map-test.bib --nofmt -m bibmapaddpinyinkey.py`


* 增加用于按笔画顺序排序的key域

`python bibmap.py biblatex-map-test.bib --nofmt -m bibmapaddbihuakey.py`


* 将期刊和会议名改成英文字母的titlecase模式

`python bibmap.py c.bib -m bibmaptitlecase.py --nofmt`

需要注意的是bibmap中大小写的保护与bibtex的方法一致，就是要把需要保护大小写的字符串包围在花括号中，比如{UBRS}，那么在进行字符串转换的时候就不会发生变化。


值得说明的是：我们只要知道bibmap.py或bibmap.exe位置，就可以使用它，而无需把bib文件放到相同目录下。
比如：bib文件在`D:\work-latex\bibmap\biblatex-map-master\mapbibtest>`目录下。
而bibmap.py和bibmap.exe在`D:\work-latex\bibmap\biblatex-map-master\binary`目录下。
那么我们在bib文件所在目录打开终端使用bibmap时指定其路径即可，比如：
`python D:\work-latex\bibmap\biblatex-map-master\binary\bibmap.py testc.bib --addpinyin`
就可以添加拼音域。
`python D:\work-latex\bibmap\biblatex-map-master\binary\bibmap.py testc.bib -m bibmaptitlecase.py`
就可以调整booktitle等域的字母大小写为titlecase。
因此我们只要把bibmap.py和bibmap.exe所在目录设置到系统path中，那么就可以直接使用它们而无需指定绝对路径了。



### 参考文献格式化

直接在命令行输入脚本及其参数：

`bibmap.py egtest`

或

`bibmap.exe egtest`

此时输入一个辅助文件egtest.aux，其它所有的参数根据对egtest.aux的解析来获取，如果没有解析到，若存在默认的设置，则使用默认的设置文件。
若没有默认设置，则可以通过可选参数来指定：

`bibmap.py egtest -b biblatex-map-test.bib`

或

`bibmap.exe egtest -b biblatex-map-test.bib`

当aux文件未给出格式化设置文件时，也可以用-s选项给出，格式化设置文件(即文献样式文件)，比如

`bibmap.py egtest -s bibstyleauthoryear.py`

或

`bibmap.exe egtest -s bibstyleauthoryear.py`


## 文件夹说明

backendtest 是作为后端程序时的测试

mapbibtest 是作为bib文件修改工具时的测试

bibfiles 放了一些bib文件

binary 用于生成一个可以带走的绿色工具（整个文件夹作为工具）


# bibmap Package : A bibliography Package

-------------------------------
 
bibmap is a bibliography Package, contains a `.sty` used to config bibliography generation and 
a bibmap.py program used to deal bib file at backend.

package bibmap loads natbib to generate the citation and bibliography list.
citestyle, bibstyle, mapstyle(bib file modification style) can be set with package options.

backend program bibmap is like bibtex/biber used to deal bibfile, the output is bbl file 
which can be loaded directly by latex to generate a bibliography.

-------------------------------

Maintainer: huzhenzhen <hzzmail@163.com>

Homepage: <https://github.com/hushidong/biblatex-map>

License：MIT license

--------------------------------------

## tow key functions of bibmap pacakge

### bibliography generation

the citation generation is based on natbib loaded by bibmap, and the bibliography generation is based on 
bibmap.py with a bibstyle file which is a very simple python code file.

features :

* bibstyle file is python code file which contains some coefficients can be easily set. more simpler than bst. 

* output contains a bbl file can be input by tex file.

* output contains a tex file and a html file can be used in other places.

* format of the bibliography is completedly controlled by the bibstyle file.

* internal logic implemented by bibmap includes: sorting by options, formation with options for namelist, literal list, date ,literal and range field, items in bib entry controlled by options.

### bib file modification

bib file modification function is very like biblatex's dynamic data modification, the logic is almost the same, to some extend it is a python reimplementation.
bib entries and fields can be deal and modified delicately.

features :

* bib file reading and parsing

* bib transient saving: save the cited references form a big database to a  small bib file, save bib file to json format file.

* bibentry modification: modification of entrytype, entry fields. 


## usage：

### bibmap package

* A MWE

```
\documentclass{article}
    \usepackage{ctex}
    \usepackage{xcolor}
    \usepackage{toolbox}
    \usepackage{hyperref}
    \usepackage{lipsum}
    \usepackage[paperwidth=16cm,paperheight=10cm,top=10pt,bottom=10pt,left=1cm,right=1cm,showframe,showcrop]{geometry}
\usepackage[citestyle=numeric,bibstyle=gb7714-2015]{bibmap}
\usepackage{filecontents}
\begin{filecontents}{\jobname.bib}
@techreport{calkin,
  author       = {Calkin, D and Ager, A and Thompson, M},
  title        = {A Comparative Risk Assessment Framework for Wildland Fire
                 Management: the 2010 Cohesive Strategy Science Report},
  number       = {RMRS-GTR-262},
  year         = {2011},
  pages        = {8--9},
}
\end{filecontents}

    \begin{document}

    REFERENCES\cite{calkin}

    \bibliography{\jobname}

    \end{document} 
```

* compiling method

four steps compiling:
```
xelatex jobname
bibmap.py jobname}
xelatex jobname
xelatex jobname
```

### bibmap.py

bibmap.py is a python script can be run directly with in the support of python environment, it can be easily downloaded and installed from the python website.


command in cmds for bibmap.py:


bibmap.py

`filename` a file name with or without an extension like .bib or .aux, if no extension was given, the file is treated as an aux file.

`[-h]` help

`[-a AUXFILE]` specify a aux file, invalid if the parameter filename is an aux file 

`[-b BIBFILE]` specify a bib file, invalid if the parameter filename is an bib file 

`[-s STYFILE]` specify a bibstyle file, using the default style file if not given.

`[-m MAPFILE]` specify a mapstyle file(data modification style file), using the default style file if not given.

`[--addpinyin]` add key of pinyin for every bib entry if given.

`[--nofmt]` do not format the bibliography if given

`[--nobdm]` do not modify the bibfile if given

where, three types of files may be used:

the first type is aux file

the seconde type is bib file 

the third type is py file，the bibstyle file and the mapstyle file are all the py file which contain python code.


### command for bib modification

run the following command in cmd：

`bibmap.py biblatex-map-test.bib`

the biblatex-map-test.bib will be read and parsed and modified with the config in the default mapstyle file bibmapdefault.py, then the bbl file with formatted bibliography will also be output.

`bibmap.py biblatex-map-test.bib --nofmt`

this command do not output bbl file.

`bibmap.py biblatex-map-test.bib --nofmt -m bibmapaddkw.py`

this command specify a user defined mapstyle file bibmapaddkw.py other than the default bibmapdefault.py



### command for bibliography formating

run the following command in cmd：

`bibmap.py egtest`

which specify a aux file egtest, all the setting will be read from the egtest.aux. if you want to set a bibfile, you can run:

`bibmap.py egtest -b biblatex-map-test.bib`

if  want to  set a bibstyle file , you  can run:

`bibmap.py egtest -s bibstyleauthoryear.py`



## history：

* v1.0 2019/02/09
* v1.0a 2019/04/12
* v1.0b 2019/04/19
* v1.0c 2021/05/24
* v1.0d 2021/10/23




--------------------------------------
## Related Links

* [Biblatex 宏包](https://github.com/plk/biblatex)
* [Beamer 文档类](https://github.com/josephwright/beamer)
* [biblatex 宏包中文手册 ](https://github.com/hushidong/biblatex-zh-cn)
* [biblatex 简明使用手册](https://github.com/hushidong/biblatex-solution-to-latex-bibliography)
* [biblatex-tutorial 摘译](https://github.com/hushidong/biblatex-tutorial-cn)
* [biblatex-map bib文件修改工具](https://github.com/hushidong/biblatex-map/)
* [biblatex-check bib文件检查工具](https://github.com/Pezmc/BibLatex-Check)



--------------------------------------


