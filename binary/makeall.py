#!/usr/bin/env python3
#_∗_coding: utf-8 _∗_

import os
import shutil
import pathlib
import re
import subprocess


def compileall(task='all'): #'all','compare'
    print(os.linesep)#这些都是字符串
    print(os.sep)
    print(os.pathsep)
    print(os.curdir)
    print(os.pardir)
    print(os.getcwd())
    print(os.listdir(path='.'))

    if task=='all':
        pwd=os.getcwd()
        filesneedcopy=["bibmap.sty",
            "bibmap.py",
            "bibmapaddauthoran.py",
            "bibmapaddbihuakey.py",
            "bibmapaddkw.py",
            "bibmapaddpinyinkey.py",
            "bibmapdefault.py",
            "bibmapsomeset.py",
            "bibmaptitlecase.py",
            "bibmaptitlecases.py",
            "bibmaptobibtex.py",
            "bibstyleauthoryear.py",
            "bibstyleexample.py",
            "bibstylenumeric.py",
            "bibstyletabthreecols.py",
            "bibstyletabtwocols.py",
            "hanzicollationpinyin.py",
            "hanzicollationstroke.py",
            "hanzipinyindatabase.py"]


        filelatexext=[".aux", ".bbl", ".blg", ".log", ".out", ".toc", ".bcf", 
        ".xml", ".synctex", ".nlo", ".nls", ".bak", ".ind", ".idx", 
        ".ilg", ".lof", ".lot", ".ent-x", ".tmp", ".ltx", ".los", 
        ".lol", ".loc", ".listing", ".gz", ".userbak", ".nav", ".snm", ".vrb",
        ".fls", ".xdv", ".fdb_latexmk"]

        
        #复制相关文件
        dirlst=os.listdir()
        subdirlst=[]
        for elem in dirlst:
            #print('elem=',elem)
            if os.path.isdir(elem) and elem != ".git" and elem not in  ["bibfiles"]:
                subdir=pwd+os.sep+elem
                subdirlst.append(subdir)
                for file in filesneedcopy:
                    shutil.copyfile(pwd+os.sep+file,subdir+os.sep+file)
                    print(subdir+os.sep+file+' ... copied')
        

        
        '''
        #进入相关文件夹进行编译
        for dirname in ["backendtest","backendtest-tabbib","backendtest-lanparal"]: #
            subdir=pwd+os.sep+dirname
            os.chdir(subdir)
            pwd=os.getcwd()
            print('pwd=',pwd)
            print(os.listdir())

            #--------编译latex---------
            

            fileuniset=["eg*.tex","test*.tex"]

            for fileuni in fileuniset:
                pf1=pathlib.Path('.').glob(fileuni)
                pf=[str(x) for x in pf1]
                print('pf=',pf)
                if pf:
                    for file in pf:
                        print('---------compile new file:---------')
                        print('file=',file)
                        print('file=',os.path.splitext(file))
                        jobname=os.path.splitext(file)[0]
                        #删除辅助文件
                        for fileext in filelatexext:
                            fileaux=pwd+os.sep+jobname+fileext
                            if os.path.exists(fileaux):
                                os.remove(fileaux)
                        #latex编译
                        latexcmd="xelatex"
                        subprocess.run([latexcmd,"-no-pdf",file],check=True)
                        subprocess.run("python bibmap.py "+jobname,shell=True)
                        subprocess.run([latexcmd,file],check=True)

            #--------编译latex结束---------
            os.chdir(os.pardir)
            pwd=os.getcwd()
            print('pwd=',pwd)
        

        #进入相关文件夹进行测试
        for dirname in ["mapbibtest","mapbibtest-authoran","mapbibtest-casetransfer","mapbibtest-tobibtex"]: #
            subdir=pwd+os.sep+dirname
            os.chdir(subdir)
            pwd=os.getcwd()
            print('pwd=',pwd)
            print(os.listdir())


            fileuniset=["*.bib"]

            for fileuni in fileuniset:
                pf1=pathlib.Path('.').glob(fileuni)
                pf=[str(x) for x in pf1]
                print('pf=',pf)
                if pf:
                    for file in pf:
                        print('---------compile new file:---------')
                        print('file=',file)
                        print('file=',os.path.split(file))
                        jobname=os.path.split(file)[1]

                        if dirname == "mapbibtest":
                            #python bibmap.py test.bib -m bibmapaddpinyinkey.py --nofmt
                            subprocess.run(["python", "bibmap.py",jobname,'-m', 'bibmapaddpinyinkey.py', '--nofmt'],check=True) 
                        elif dirname == "mapbibtest-authoran":
                            subprocess.run(["python", "bibmap.py",jobname,'-m', 'bibmapaddauthoran.py', '--nofmt'],check=True) 
                        elif dirname == "mapbibtest-casetransfer":
                            subprocess.run(["python", "bibmap.py",jobname,'-m', 'bibmaptitlecases.py','--nofmt'],check=True) 
                        elif dirname == "mapbibtest-tobibtex":
                            subprocess.run(["python", "bibmap.py",jobname,'-m', 'bibmaptobibtex.py','--nofmt'],check=True) 

                        

            #返回上级目录
            os.chdir(os.pardir)
            pwd=os.getcwd()
            print('pwd=',pwd)
        '''

        #进入相关文件夹进行测试
        for dirname in ["binary"]: #
            subdir=pwd+os.sep+dirname
            os.chdir(subdir)
            pwd=os.getcwd()
            print('pwd=',pwd)
            print(os.listdir())


            subprocess.run(["makeexefile.bat"])

            #返回上级目录
            os.chdir(os.pardir)
            pwd=os.getcwd()
            print('pwd=',pwd)


        #主目录文档编译
        jobname="bibmap"
        subprocess.run(["xelatex","-no-pdf",jobname],check=True)
        subprocess.run(["xelatex","--synctex=-1",jobname],check=True)
        



        #删除相关文件
        dirlst=os.listdir()
        subdirlst=[]
        for elem in dirlst:
            
            #print('elem=',elem)
            if os.path.isdir(elem) and elem != ".git" and elem not in  ["bibfiles","binary",'__pycache__']:
                subdir=pwd+os.sep+elem
                os.chdir(subdir)
                pwd=os.getcwd()
                print('pwd=',pwd)

                subprocess.run(["makeclear.bat"])

                
                os.chdir(os.pardir)
                pwd=os.getcwd()
                print('pwd=',pwd)
        
        
        print("test all ended!")


if __name__ == '__main__':
    compileall()
    #compileall('all')
    #compileall('compare')