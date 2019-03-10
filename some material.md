⃝1 prefix lastname, suffix, firstname middlename
⃝2 firstname middlename lastname or firstname prefix lastname

\meaning\finalandcomma

尽然是在english.LBX中定义了。
biblatex.STY
BIBLATEX.DEF
STANDARD.BBX
等一堆文件中没有找到，那么对他进行定义也类似于
\bibrangedash的定义了。
当然也可以直接对该命令进行定义，这样可能会破坏其它语言的定义。