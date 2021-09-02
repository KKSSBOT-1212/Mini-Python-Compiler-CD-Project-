a.o: lex.yy.c y.tab.c y.tab.h 
	gcc lex.yy.c y.tab.c -g -ll -o a.o

y.tab.c : grammar.y
	yacc -dv grammar.y

lex.yy.c : grammar.l
	lex grammar.l

clean :
	rm lex.yy.c y.tab.c y.tab.h Test.out
