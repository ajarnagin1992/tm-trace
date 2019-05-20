grammar tm;

/*
 * Parser Rules
 */
alphalist : alphasymbol (SEP alphasymbol)* ;
alphasymbol : (CHAR | ALPHACHAR | INIL | INIR | COL | SEP) ;
inittitle : (STATES | START | ACCEPT | REJECT | ALPHA | TALPHA) ;
rl : (RRL | RLL) statename alphasymbol ';' ;
rt : (RRT | RLT) statename alphasymbol statename ';' ;
rwt : (RWRT | RWLT) statename alphasymbol alphasymbol statename ';' ;
statelist : statename (SEP statename)* ;
statename : (NAME | ALPHACHAR | inittitle | transtitle) ;
transfunc : (rl | rt | rwt) ;
translist : transfunc* ;
transtitle : (RWRT | RWLT | RRL | RLL | RRT | RLT) ;

init : states start accept reject alpha talpha transition;
states : INIL STATES COL statelist INIR ;
start : INIL START COL (NAME | CHAR) INIR ;
accept : INIL ACCEPT COL statelist INIR ;
reject : INIL REJECT COL statelist INIR ;
alpha : INIL ALPHA COL alphalist INIR ;
talpha : INIL TALPHA COL alphalist INIR ;
transition : translist ;

/*
 * Lexer Rules
 */

COMMENT : '--' ~('\r' | '\n')* -> skip;
WS : [ \t\r\n]+ -> skip;
INIL : '{' ;
INIR : '}' ;
COL : ':' ;
SEP : ',' ; 
STATES : 'states' ;
START : 'start' ;
ACCEPT : 'accept' ;
REJECT : 'reject' ;
ALPHA : 'alpha' ;
TALPHA : 'tape-alpha' ;
RWRT : 'rwRt' ;
RWLT : 'rwLt' ;
RRL : 'rRl' ;
RLL : 'rLl' ;
RRT : 'rRt' ;
RLT : 'rLt' ;
NAME : ALPHANUM ALPHANUM+;
ALPHACHAR : ALPHANUM ;
CHAR : . ;
fragment ALPHANUM : [a-zA-Z0-9] ;