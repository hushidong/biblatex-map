@echo off


call makecleareg

copy ..\*.py . /y

copy ..\*.sty . /y



setlocal enabledelayedexpansion
for  %%a in ( eg*.tex ) do (
set jobfile=%%a
set jobname=!jobfile:~0,-4!
echo %%a
echo !jobfile!
echo !jobname!
xelatex.exe -no-pdf !jobfile!
python bibmap.py !jobname!
xelatex.exe -no-pdf !jobfile!
xelatex.exe --synctex=-1 !jobfile!
)
setlocal DISABLEDELAYEDEXPANSION

call makecleareg

del eg*.bib /Q

del *.sty /q



::pause
