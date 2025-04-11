%{
#include <ctype.h>
#include <stdlib.h> 
#include <string.h> 
#include <stdio.h>
#define YYSTYPE double
int yylex();               // Prototype for yylex()
void yyerror(char *s);     // Prototype for yyerror()

%}

%token num
%left '+' '-'
%left '*' '/'

%%

st: st expr '\n' { printf("VALID\n"); }
 | st '\n'
 |
 | error '\n' { printf("INVALID\n"); yyerrok; }
 ;

expr: num
    | expr '+' expr
    | expr '-' expr
    | expr '*' expr
    | expr '/' expr
    ;

%%

int main() {
    printf("ENTER AN EXPRESSION TO VALIDATE:\n");
    yyparse();
    return 0;
}

int yylex() {
    int ch;
    
    while ((ch = getchar()) == ' ' || ch == '\t'); // Ignore whitespace

    if (isdigit(ch) || ch == '.') {
        ungetc(ch, stdin);
        scanf("%lf", &yylval);
        return num;
    }

    return ch; // Return operators and newline
}

void yyerror(char *s) {
    printf("%s\n", s);
}


//bison -d parser.y  # Generates y.tab.c and y.tab.h  
//gcc y.tab.c   
//./a