@echo off


call makeclearall

start cmd /c "call d:\Anaconda3\Scripts\activate.bat && call activate base && call makecompile.bat"

pause






