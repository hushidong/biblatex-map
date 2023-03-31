@echo off

del /q *.aux *.bbl *.blg *.log *.out *.toc *.bcf *.xml *.synctex *.nlo *.nls *.bak *.ind *.idx *.ilg *.lof *.lot *.ent-x *.tmp *.ltx *.los *.lol *.loc *.listing *.gz *.userbak *.nav *.snm *.vrb


del /q *.nav *.snm *.vrb *.fls *.xdv *.fdb_latexmk *.json *.html *.txt *.pdf *.py new*.bib *.exe 

copy ..\*.py . /y

start cmd /c "call d:\Anaconda3\Scripts\activate.bat && call activate base && pyinstaller -F bibmap.py  && copy .\dist\bibmap.exe . /y &&  RD /S /Q __pycache__  build   dist &&  del /q *.spec"

copy ..\readme.md . /y

copy ..\*.sty . /y

pause



