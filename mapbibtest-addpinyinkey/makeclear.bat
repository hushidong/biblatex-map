@echo off
del /q *.aux *.bbl *.blg *.log *.out *.toc *.bcf *.xml *.synctex *.nlo *.nls *.bak *.ind *.idx *.ilg *.lof *.lot *.ent-x *.tmp *.ltx *.los *.lol *.loc *.listing *.gz *.userbak *.nav *.snm *.vrb *.sty


del /q *.nav *.snm *.vrb *.fls *.xdv *.fdb_latexmk *.json *.html *.txt *.pdf *.py new*.bib

RD /S /Q __pycache__ 