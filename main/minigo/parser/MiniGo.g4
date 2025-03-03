// 2213860
grammar MiniGo;

@lexer::header {
from lexererr import *
from antlr4.Token import CommonToken

}
@lexer::members {
prevTokenType = -1
comma_signal = False

def nextToken(self):
    # Lấy token tiếp theo
    next_token = super().nextToken()
    print(  " PREVIOUS self.prevTokenType: " + str(self.prevTokenType) + 
            " TYPE: " + str(type(next_token)) + 
            "string: " + str(next_token.text) + 
            " / type: " + str(next_token.type) +
            " self.comma_signal: " + str(self.comma_signal))  # Kiểm tra kiểu của next_token
    if self.prevTokenType == -1 and next_token.type in {self.NL, self.MULTI_NEWLINE}:
        # print("tin hieu 201")
        self._type = self.SKIP
        next_token = super().nextToken()
        return next_token
    self.prevTokenType = next_token.type
    if self.prevTokenType in {self.IDENTIFIER, self.DECIMAL_INT, self.FLOAT_LITERAL, 
                          self.TRUE, self.FALSE, self.STRING_LITERAL, 
                          self.RETURN, self.CONTINUE, self.BREAK, 
                          self.RPAREN, self.RBRACE, self.RBRACK, self.NIL,
                          self.INT, self.FLOAT, self.STRING, self.BOOLEAN}:
        self.comma_signal = True
    print(  " AFTER    self.prevTokenType: " + str(self.prevTokenType) + 
            " TYPE: " + str(type(next_token)) + 
            "string: " + str(next_token.text) + 
            " / type: " + str(next_token.type) +
            " self.comma_signal: " + str(self.comma_signal))
    print("====================================================")
    return next_token
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit()
        raise UncloseString(result.text)
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit()
        raise IllegalEscape(result.text)
    elif tk == self.ERROR_CHAR:
        result = super().emit()
        raise ErrorToken(result.text)
    elif tk == self.NL:
        result = super().emit()
        if self.comma_signal:
            result.text = ";"
            result.type = self.SEMI
            
            self.comma_signal = False
            #print("TYPE_IN_NL: " + str(type(result)))
            return result
        else:
            self._type = self.SKIP
            next_token = super().nextToken()
            return next_token

    elif tk == self.MULTI_NEWLINE:
        result = super().emit()
        if self.comma_signal:
            result.text = ";"
            result.type = self.SEMI
            
            self.comma_signal = False
            #print("TYPE_IN_NL: " + str(type(result)))
            return result
        else:
            self._type = self.SKIP
            next_token = super().nextToken()
            return next_token
    else:
        self.comma_signal = False
        return super().emit()
}


options{
	language=Python3;
}

// A program in MiniGo consists of a single file that includes various declarations without strict
// ordering. The file may contain constant declarations, variable declarations, type declarations
// (such as structs and interfaces), and function declarations, all of which can appear in any order.
// The program is structured around a mandatory ‘main‘ function, which serves as the entry point
// of execution. The ‘main‘ function does not take parameters or return values, and it is where
// the program’s execution begins.
// program  : decl+ EOF ;

// decl: funcdecl | vardecl ;

// vardecl: 'var' IDENTIFIER 'int' ';' ;

// funcdecl: 'func' IDENTIFIER '(' ')' '{' '}' ';' ;
program: declist EOF;
declist: decl declist | decl;
decl: vardecl | constdecl | structdecl | interfacedecl | funcdecl | simplemethod;
    vardecl: normal_vardecl | arr_vardecl ;
        normal_vardecl: normal_vardecl_without_init | normal_vardecl_with_init;
            normal_vardecl_without_init: VAR IDENTIFIER typedecl SEMI;
            normal_vardecl_with_init: VAR IDENTIFIER (typedecl | ) ASSIGN expr SEMI;
                typedecl: INT | FLOAT | STRING | BOOLEAN | IDENTIFIER;
        arr_vardecl: arr_vardecl_without_init | arr_vardecl_with_init;
            arr_vardecl_without_init: VAR IDENTIFIER arr_dimension_list typedecl SEMI;
                arr_dimension_list: arr_dimension arr_dimension_list | arr_dimension;
                    arr_dimension: LBRACK (DECIMAL_INT | IDENTIFIER) RBRACK;
            arr_vardecl_with_init: VAR IDENTIFIER (arr_dimension_list typedecl | ) ASSIGN arrliteral SEMI;
                arrliteral: arr_dimension_list typedecl arrlistvalue;
                arrlistvalue: LBRACE listvalue RBRACE;
                listvalue: value_for_arr COMMA listvalue | value_for_arr;
                value_for_arr: literalvalue_for_arr | arrlistvalue;
                    literalvalue_for_arr: DECIMAL_INT | BINARY_INT | OCTAL_INT | HEXADECIMAL_INT | FLOAT_LITERAL
                                        | STRING_LITERAL | TRUE | FALSE | NIL | structinst;
                    structinst: IDENTIFIER structinst_body;
                    structinst_body: LBRACE structinst_field_list RBRACE;
                    structinst_field_list: structinst_field_prime | ;
                    structinst_field_prime: structinst_field COMMA structinst_field_prime | structinst_field;
                    structinst_field: IDENTIFIER COLON expr;
    constdecl: CONST IDENTIFIER ASSIGN expr SEMI;
    structdecl: TYPE IDENTIFIER STRUCT structbody SEMI;
        structbody: LBRACE fieldlist RBRACE;
            fieldlist: field fieldlist | ;
                field: IDENTIFIER (arr_dimension_list | ) typedecl SEMI;
    interfacedecl: TYPE IDENTIFIER INTERFACE interface_body SEMI;
        interface_body: LBRACE methodlist RBRACE;
            methodlist: method methodlist | ;
                method: IDENTIFIER LPAREN paramlist RPAREN (returntype | ) SEMI;
    funcdecl: FUNC IDENTIFIER LPAREN paramlist RPAREN (returntype | ) funcbody SEMI;
        paramlist: param_group COMMA paramlist | param_group |;
        param_group: param_mem_list (arr_dimension_list | ) typedecl;
        param_mem_list: IDENTIFIER COMMA param_mem_list | IDENTIFIER;
        funcbody: LBRACE stmtlist RBRACE;
        stmtlist: stmt stmtlist | ;
        returntype: (arr_dimension_list | ) typedecl;
    simplemethod: FUNC LPAREN IDENTIFIER IDENTIFIER RPAREN IDENTIFIER LPAREN paramlist RPAREN (returntype | ) simplemethod_body SEMI;
        simplemethod_body: LBRACE stmtlist RBRACE;
expr: expr OR expr0 | expr0;
    expr0: expr0 AND expr1 | expr1; 
    expr1: expr1 (EQUAL | NOT_EQUAL | LESS | GREATER | LESS_EQUAL | GREATER_EQUAL) expr2 | expr2;
    expr2: expr2 (PLUS | MINUS) expr3 | expr3;
    expr3: expr3 (MULTIPLY | DIVIDE | MODULUS) expr4 | expr4;
    expr4: (MINUS | NOT) expr4 | expr5;
    expr5: expr5 DOT IDENTIFIER | expr5 LBRACK expr RBRACK | expr6;
    expr6: subexpr | value;
        subexpr: LPAREN expr RPAREN;
        value: literalvalue | IDENTIFIER | funccall;
            literalvalue: literalvalue_for_arr | arrliteral;
            funccall: IDENTIFIER LPAREN (arglist | ) RPAREN;
                arglist: expr COMMA arglist | expr |;   
methodcall: expr accesslist LPAREN arglist RPAREN;
stmt: vardecl | constdecl | assignstmt | returnstmt | ifstmt | forstmt | breakstmt | continuestmt | callstmt;
    assignstmt: var assignop expr SEMI;
        var: IDENTIFIER accesslist | IDENTIFIER;
        accesslist: access accesslist | access;
        access: arrayaccess | structaccess;
            arrayaccess: LBRACK expr RBRACK;
            structaccess: DOT IDENTIFIER;
        assignop: ASSIGN_DECLARE | PLUS_ASSIGN | MINUS_ASSIGN | MULTIPLY_ASSIGN
                    | DIVIDE_ASSIGN | MODULUS_ASSIGN;
    returnstmt: RETURN (expr|) SEMI ;
    callstmt:( funccall |  methodcall) SEMI;
    ifstmt: firstifstmt elseifstmtlist (elsestmt | ) SEMI;
        firstifstmt: IF LPAREN expr RPAREN ifstmtbody;
            ifstmtbody:  LBRACE stmtlist RBRACE;
        elseifstmtlist: elseifstmt elseifstmtlist | ;
            elseifstmt: ELSE IF LPAREN expr RPAREN ifstmtbody;
        elsestmt: ELSE ifstmtbody;
    forstmt: basicforstmt | init_cond_update_forstmt | rangeforstmt;
        basicforstmt: FOR expr forstmtbody SEMI;
        forstmtbody: LBRACE stmtlist RBRACE;
        init_cond_update_forstmt: FOR init_for SEMI expr SEMI assign forstmtbody SEMI;
            init_for: assign | VAR VAR (typedecl | ) ASSIGN expr;
            assign: var assignop expr;
        rangeforstmt: FOR IDENTIFIER COMMA IDENTIFIER ASSIGN_DECLARE RANGE expr forstmtbody SEMI;
        breakstmt: BREAK SEMI;
        continuestmt: CONTINUE SEMI;


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Lexer PART
// 3.1 Characters set


MULTI_LINE_COMMENT_2: '/*' (MULTI_LINE_COMMENT_2 | .)*? '*/' -> skip;
MULTI_LINE_COMMENT
    :   '/*' .*? '*/' -> skip
    ;
NL 
    : ('\r'? '\n'+);
MULTI_NEWLINE: ('\r'? '\n') ('\r'? '\n')+ ;
WS: [ \t\r]+ -> skip; // skip spaces, tabs 

// 3.2 Program comment

SINGLE_LINE_COMMENT
    :   '//' ~[\r\n]* -> skip 
    ;


// 3.3 Tokens set
// 3.3.2 Keywords
IF: 'if';
ELSE: 'else';
FOR: 'for';
RETURN: 'return';
FUNC: 'func';
TYPE: 'type';
STRUCT: 'struct';
INTERFACE: 'interface';
STRING: 'string';
INT: 'int';
FLOAT: 'float';
BOOLEAN: 'boolean';
CONST: 'const';
VAR: 'var';
CONTINUE: 'continue';
BREAK: 'break';
RANGE: 'range';
NIL: 'nil';
TRUE: 'true';
FALSE: 'false';



// 3.3.3 Operators
// Arithmetic Operators
PLUS: '+';
MINUS: '-';
MULTIPLY: '*';
DIVIDE: '/';
MODULUS: '%';

// Relational Operators
EQUAL: '==';
NOT_EQUAL: '!=';
LESS: '<';
LESS_EQUAL: '<=';
GREATER: '>';
GREATER_EQUAL: '>=';

// Logical Operators
AND: '&&';
OR: '||';
NOT: '!';

// Assignment Operators
ASSIGN_DECLARE: ':=';
ASSIGN: '=';
PLUS_ASSIGN: '+=';
MINUS_ASSIGN: '-=';
MULTIPLY_ASSIGN: '*=';
DIVIDE_ASSIGN: '/=';
MODULUS_ASSIGN: '%=';

// Other Operators
// DOT: '.';
// ARITHMETIC_OPERATOR: '+' | '-' | '*' | '/' | '%';
// RELATIONAL_OPERATOR: '==' | '!=' | '<' | '<=' | '>' | '>=';
// LOGICAL_OPERATOR: '&&' | '||' | '!';
// ASSIGNMENT_OPERATOR: '=' | '+=' | '-=' | '*=' | '/=' | '%=';
// OTHER_OPERATOR: '.';

// 3.3.4 Separators

// Parentheses
LPAREN: '(';
RPAREN: ')';

// Curly Braces
LBRACE: '{';
RBRACE: '}';

// Square Brackets
LBRACK: '[';
RBRACK: ']';

// Comma
COMMA: ',';
// Dot
DOT: '.';
// Semicolon
SEMI: ';';
COLON: ':';
// SEPARATOR: '(' | ')' | '{' | '}' | '[' | ']' | ',' | ';';

// 3.3.5 Literals
// Integer Literals
// Decimal Integers
DECIMAL_INT
    : '0'                      // Số 0
    | [1-9] [0-9]*             // Số thập phân bắt đầu từ 1-9, không có số 0 đứng đầu
    ;

// Binary Integers
BINARY_INT
    : ('0b' | '0B') [01]+      // Số nhị phân bắt đầu bằng 0b hoặc 0B, theo sau là 0 hoặc 1
    ;

// Octal Integers
OCTAL_INT
    : ('0o' | '0O') [0-7]+     // Số bát phân bắt đầu bằng 0o hoặc 0O, theo sau là các chữ số từ 0 đến 7
    ;

// Hexadecimal Integers
HEXADECIMAL_INT
    : ('0x' | '0X') [0-9a-fA-F]+ // Số thập lục phân bắt đầu bằng 0x hoặc 0X, theo sau là 0-9 hoặc a-f/A-F
    ;

// Float Literals
FLOAT_LITERAL
    : [0-9]+ '.' [0-9]* ([eE] [+-]? [0-9]+)?    // Có phần nguyên, dấu chấm, và tùy chọn phần mũ
    | [0-9]+ '.' ([eE] [+-]? [0-9]+)?           // Có phần nguyên và dấu chấm, không cần phần thập phân
    ;
// String Literals
STRING_LITERAL
    : '"' (ESC | ~["\\\r\n])* '"' 
    ;

fragment ESC
    : '\\' [ntr"\\]
    ;



// bỏ này vô auto semi
// RAW_STRING_LIT         : '`' ~'`'* '`' ;
// end - bỏ này vô auto semi


// 3.3.1 Identifiers
IDENTIFIER
    : [a-zA-Z_] [a-zA-Z0-9_]*
    ;

ILLEGAL_ESCAPE
    : '"' (~["\r\n\\] | '\\' [btnfr"'\\])* '\\' (~[btnfr"'\\]) 
    ;

UNCLOSE_STRING
    : '"' (~["\r\n\\] | '\\' [btnfr"'\\])* 
    ;

ERROR_CHAR: .;
