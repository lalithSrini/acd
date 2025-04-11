%{
#include <stdio.h>
%}

%%
[0-9]+         { printf("Number: %s\n", yytext); }
[a-zA-Z]+      { printf("Identifier: %s\n", yytext); }
[ \t\n]+       { /* Ignore whitespace */ }
.              { printf("Other character: %s\n", yytext); }
%%

int main() {
    yylex();
    return 0;
}

// flex meow.l
// gcc lex.yy.c -o meow -lfl
//  ./meow