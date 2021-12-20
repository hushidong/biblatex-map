@echo off


xelatex.exe -no-pdf test-sort.tex

python bibmap.py testc.bib -m bibmapaddpinyinkey.py

biber test-sort

xelatex.exe --synctex=-1 test-sort.tex



