.refresh :
	touch .refresh

all : main.tex target
	latexmk -pdf -jobname=target/$(subst .tex,,$<) -halt-on-error $<

watch : main.tex target
	latexmk -pdf -jobname=target/$(subst .tex,,$<) -pvc -halt-on-error $<

target :
	mkdir target

