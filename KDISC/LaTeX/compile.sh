echo "Compiling latex document"
pdflatex main.tex
bibtex main.aux
pdflatex main.tex
pdflatex main.tex
