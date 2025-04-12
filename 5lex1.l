

%{
#include<stdio.h>
int k,c,d,i,s,o;
%}

%%
include|void|main|int|float|double|scanf|char|printf {printf("keyword"); k++;}
[a-z][a-zA-Z0-9]* {printf("Identifier"); i++;}
[0-9]* {printf("digit"); d++;}
[+|-||/|=] {printf("operator"); o++;}
[;|:|(|)|{|}|"|'|,|\n|\t]* {printf("delimeter"); c++;}
[#|<|>|%]* {printf("symbols"); s++;}
%%

int main(void)
{
yyin=fopen("input.txt","r");
yylex();
printf("\nidentifier %d\n",i);
printf("Symbols %d\n",s);
printf("digits %d\n",d);
printf(" Operator %d\n",o);
printf(" keywords %d\n",k);
printf("delimeter %d\n",c);
return 1;
}
int yywrap()
{
return 1;
}



// terminal ->
// flex lex1.l
// gcc lex.yy.c -o lex1 -lfl
//  ./lex1