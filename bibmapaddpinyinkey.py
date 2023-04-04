
#
#数据修改的设置
#
#

#设置多音字的首读音
multiplepinyin={
'曾':'zeng1',
'沈':'shen3',
'汤':'tang1', #姓不读shāng
'仇':'qiu2', #不读chóu。如明代著名画家仇英。4EC7
'朴':'piao2', #不读pǔ。此姓朝鲜族多见，如韩国前总统朴槿惠。6734
'单':'shan4', #不读dān。如《说唐》中的单雄信。5355
'解':'xie4', #不读jiě。如明代才子解缙。89E3
'区':'ou1', #不读qū。如柳宗元《童区寄传》中的区寄。533A
'查':'zha1',#不读chá。如作家金庸原名查良镛。67E5 
'繁':'po2', #不读fán。如写《定情诗》的汉末诗人繁钦。7E41 
'瞿':'qu2', #不读jù。如革命家瞿秋白。77BF 
'员':'yun4',#员，读【yùn】，不读yuán。如唐代诗人员半千。5458 
'能':'nai4',#能读【nài】，不读néng。如宋代名医能自宣。80FD
'阚':'kan4',#阚，读【kàn】，不读hǎn。如三国时吴国学者阚泽。961A 
'都':'du1',#都，读【dū】，不读dōu。如明代进士都穆。90FD 
'乜':'nie4',#乜，读【niè】，不读miē。如民国时国军少将乜子彬。4E5C 
'缪':'miao4',#缪，读【miào】，不读móu。7F2A
'句':'gou1',#句，读【gōu】，不读jù。如宋代进士句克俭。复姓句龙，也读gōu。53E5 
'阿':'e1',  #阿，读【ē】，不读ā。963F 
'谌':'chen2',#谌，读【chén】，不读shèn。如羽毛球运动员谌龙。8C0C
'尉':'yu4',#尉迟，读【yù chí】，不读wèi chí。如唐初大将尉迟恭；5C09 尉单独作姓时读wèi，如战国时著名军事理论家尉缭。
'澹':'tan2'#澹台，读【tán tái】，不读dàn tái。如孔子弟子澹台灭明。6FB9
#'翟':'zhai2',7FDF
# 折，一读【shé】，一读【zhé】。
# 盖，一读【gě】，一读【gài】。一般念【gě】，如现代京剧表演艺术家盖叫天。
# 隗，一读【kuí】，一读【wěi】。
# 种，一读【chóng】，一读【zhǒng】。一般念【chóng】，如北宋末年名将种师道。
# 覃，一读【tán】，一读【qín】；一般读【qín】。
# 召，一读【shào】，得姓始祖为周武王之弟召公姬奭（shì）。一读【zhào】，为傣族姓。
# 相，一读【xiāng】，一读【xiàng】。
# 曲，读【qū】，不读qǔ。如唐代司空曲环。
# 訾，读【zī】，不读zǐ。如元代有名孝子訾汝道。
# 哈，读【hǎ】，不读hā。如央视春晚总导演哈文。
# 钻，读【zuān】，不读zuàn。
# 任，读【rén】，不读rèn。如《笑傲江湖》女主角任盈盈。
# 要，读【yāo】，不读yào。如春秋时著名刺客要离。
# 华，读【huà】，不读huá。如数学家华罗庚。
# 过，读【guō】，不读guò。
# 皇甫，读【huáng fǔ】，不读huáng pǔ。如晚唐诗人皇甫松。
# 长孙，读【zhǎng sūn】，不读cháng sūn。如唐初名臣长孙无忌。
# 宰父，读【zǎi fǔ】，不读zǎi fù。如孔子弟子宰父黑。
# 亓官，读【qí guān】。如孔子的妻子亓官氏。
# 毌丘，读【guàn qiū】，不要读作 wú qiū 或 mǔqiū，也不要写作“毋丘”或“母丘”。
# 逄，读【páng】。
# 桓，读【huán】。如东晋大将桓温。
# 蒯，读【kuǎi】。如汉初谋士蒯通。
# 殳，读【shū】。
# 厍，读【shè】。如北周大臣厍狄峙。
# 靳，读【jìn】。如演员“老干部”靳东。
# 郄，读【qiè】。
# 昝，读【zǎn】。如清代书画家昝茹颖。
# 逯，读【lù】。如汉代大臣逯普。
# 郦，读【lì】。如汉初名臣郦食其（lì yì jī）。
# 麹，读【qū】。如隋代高昌国国王麴伯稚。
# 璩，读【qú】。
# 郗，读【xī】。但古籍中也有读chī的。
# 妫，读【guī】，不读wěi。
# 郏，读【jiá】。如清代著名画家郏伦逵。
# 郜，读【gào】。如国足运动员郜林。
}

#重设新的任务处理
sourcemaps=[
    [#map3:author中中文作者的逗号去掉
		{"fieldsource":"author","match":r'[\u2FF0-\u9FA5]',"final":True},#step1
		{"fieldsource":"author","match":r'\,\s',"replace":'',"overwrite":True}#step1
	],
    [#map3:author中中文作者的逗号去掉
		{"fieldsource":"author","match":r'[\u2FF0-\u9FA5]',"final":True},#step1
		{"fieldsource":"author","match":r'\{',"replace":'',"overwrite":True}#step1
	],
    [#map3:author中中文作者的逗号去掉
		{"fieldsource":"author","match":r'[\u2FF0-\u9FA5]',"final":True},#step1
		{"fieldsource":"author","match":r'\}',"replace":'',"overwrite":True}#step1
	],
    [#map3:author中中文作者的逗号去掉
		{"fieldsource":"editor","match":r'[\u2FF0-\u9FA5]',"final":True},#step1
		{"fieldsource":"editor","match":r'\,\s',"replace":'',"overwrite":True}#step1
	],
	[#map1:设置author域的字符串的拼音字符串设置给域key
		{"fieldsource":"author","match":r'[\u2FF0-\u9FA5]',"final":True},#step1
        {"fieldsource":"author"},#step1
		{"fieldset":"key","origfieldval":True,"fieldfunction":'sethzpinyin'}#step2
	],
	[#map1:设置editor域的字符串的拼音字符串设置给域key
		{"fieldsource":"editor","match":r'[\u2FF0-\u9FA5]',"final":True},#step1
        {"fieldsource":"author"},#step1
		{"fieldset":"key","origfieldval":True,"fieldfunction":'sethzpinyin'}#step2
	],
]


