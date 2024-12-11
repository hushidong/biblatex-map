@echo off


call makeclear

copy ..\*.py . /y

start cmd /c "call d:\Anaconda3\Scripts\activate.bat && call activate base && python bibmap.py testbib.bib -m bibmaptitlecases.py --nofmt"

pause






