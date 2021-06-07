@echo off



setlocal enabledelayedexpansion
for  %%a in ( test*.tex ) do (
call makeclearthesis
set jobfile=%%a
set jobname=!jobfile:~0,-4!
echo %%a
echo !jobfile!
echo !jobname!
xelatex.exe -no-pdf !jobfile!
biber !jobname!
xelatex.exe --synctex=-1 !jobfile!
)
setlocal DISABLEDELAYEDEXPANSION


