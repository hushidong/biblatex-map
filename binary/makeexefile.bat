@echo off

copy ..\*.py . /y

start cmd /c "call d:\Anaconda3\Scripts\activate.bat && call activate base && pyinstaller -F bibmap.py  && copy .\dist\bibmap.exe . /y &&  RD /S /Q __pycache__  build   dist &&  del /q *.spec"

copy ..\readme.md . /y

copy ..\*.sty . /y

pause



