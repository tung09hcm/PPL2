from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *

class ASTGeneration(MiniGoVisitor):
    def visitProgram(self, ctx: MiniGoParser.ProgramContext):
        decl_list = self.visit(ctx.declist())
        return Program(decl_list)

    def visitDeclist(self, ctx: MiniGoParser.DeclistContext):
        #declist: decl declist | decl;
        if ctx.getChildCount() == 1:  # decl
            return [self.visit(ctx.decl())]
        else:  # decl declist
            return [self.visit(ctx.decl())] + self.visit(ctx.declist())
    
    def visitDecl(self, ctx: MiniGoParser.DeclContext):
        #decl: vardecl | constdecl | structdecl | interfacedecl | funcdecl | simplemethod;
        if ctx.vardecl():
            return self.visit(ctx.vardecl())
        elif ctx.constdecl():
            return self.visit(ctx.constdecl())
        elif ctx.structdecl():
            return self.visit(ctx.structdecl())
        elif ctx.interfacedecl():       
            return self.visit(ctx.interfacedecl())
        elif ctx.funcdecl():
            return self.visit(ctx.funcdecl())
        elif ctx.simplemethod():
            return self.visit(ctx.simplemethod())
        else:
            raise Exception("UNKNOWN DECLARATION")
    
    def visitVardecl(self, ctx: MiniGoParser.VardeclContext):
        #vardecl: normal_vardecl | arr_vardecl ;
        if ctx.normal_vardecl():
            return self.visit(ctx.normal_vardecl())
        elif ctx.arr_vardecl():
            return self.visit(ctx.arr_vardecl())
        else:
            raise Exception("UNKNOWN VARDECL")
        
    def visitNormal_vardecl(self, ctx: MiniGoParser.Normal_vardeclContext):
        # normal_vardecl: normal_vardecl_without_init | normal_vardecl_with_init;
        if ctx.normal_vardecl_without_init():
            return self.visit(ctx.normal_vardecl_without_init())
        elif ctx.normal_vardecl_with_init():
            return self.visit(ctx.normal_vardecl_with_init())
        else:
            raise Exception("UNKNOWN NORMAL_VARDECL")
        
    def visitNormal_vardecl_without_init(self, ctx: MiniGoParser.Normal_vardecl_without_initContext):
        # normal_vardecl_without_init:  VAR IDENTIFIER typedecl SEMI;

        return VarDecl((ctx.IDENTIFIER().getText()), self.visit(ctx.typedecl()), None)
    
    def visitNormal_vardecl_with_init(self, ctx: MiniGoParser.Normal_vardecl_with_initContext):
        # normal_vardecl_with_init: VAR IDENTIFIER (typedecl | ) ASSIGN expr SEMI;
        if ctx.typedecl():
            return VarDecl((ctx.IDENTIFIER().getText()), self.visit(ctx.typedecl()), self.visit(ctx.expr()))
        else:
            return VarDecl((ctx.IDENTIFIER().getText()), None, self.visit(ctx.expr()))
        
    def visitTypedecl(self, ctx: MiniGoParser.TypedeclContext):
        #typedecl: INT | FLOAT | STRING | BOOLEAN | IDENTIFIER;
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.STRING():
            return StringType()
        elif ctx.BOOLEAN():
            return BoolType()
        elif ctx.IDENTIFIER():
            return Id(ctx.IDENTIFIER().getText())
        else:
            raise Exception("UNKNOWN TYPEDECL")
        
    def visitArr_vardecl(self, ctx: MiniGoParser.Arr_vardeclContext):
        # arr_vardecl: arr_vardecl_without_init | arr_vardecl_with_init;
        if ctx.arr_vardecl_without_init():
            return self.visit(ctx.arr_vardecl_without_init())
        elif ctx.arr_vardecl_with_init():
            return self.visit(ctx.arr_vardecl_with_init())
        else:
            raise Exception("UNKNOWN ARR_VARDECL")
        
    def visitArr_vardecl_without_init(self, ctx: MiniGoParser.Arr_vardecl_without_initContext):
        # arr_vardecl_without_init: VAR IDENTIFIER arr_dimension_list typedecl SEMI;
        return VarDecl(ctx.IDENTIFIER().getText(), ArrayType(self.visit(ctx.arr_dimension_list()), self.visit(ctx.typedecl())), None)
    
    def visitArr_dimension_list(self, ctx: MiniGoParser.Arr_dimension_listContext):
        #arr_dimension_list: arr_dimension arr_dimension_list | arr_dimension;
        if ctx.arr_dimension_list():
            return [self.visit(ctx.arr_dimension())] + self.visit(ctx.arr_dimension_list())
        else:
            return [self.visit(ctx.arr_dimension())]
        
    def visitArr_dimension(self, ctx: MiniGoParser.Arr_dimensionContext):
        #arr_dimension: LBRACK (DECIMAL_INT | IDENTIFIER) RBRACK;
        if ctx.DECIMAL_INT():
            return IntLiteral(int(ctx.DECIMAL_INT().getText()))
        elif ctx.IDENTIFIER():
            return Id(ctx.IDENTIFIER().getText())
        else:
            raise Exception("UNKNOWN ARR_DIMENSION")
        
    def visitArr_vardecl_with_init(self, ctx: MiniGoParser.Arr_vardecl_with_initContext):
        # arr_vardecl_with_init: VAR IDENTIFIER (arr_dimension_list typedecl | ) ASSIGN arrliteral SEMI;
        if ctx.arr_dimension_list():
            return VarDecl((ctx.IDENTIFIER().getText()), ArrayType(self.visit(ctx.arr_dimension_list()), self.visit(ctx.typedecl())), self.visit(ctx.arrliteral()))
        else:
            return VarDecl((ctx.IDENTIFIER().getText()), None, self.visit(ctx.arrliteral()))
    

    def visitArrliteral(self, ctx: MiniGoParser.ArrliteralContext):
        #arrliteral: arr_dimension_list typedecl arrlistvalue;
        return ArrayLiteral(self.visit(ctx.arr_dimension_list()), self.visit(ctx.typedecl()), self.visit(ctx.arrlistvalue()))
    
    def visitArray_list_value(self, ctx: MiniGoParser.ArrlistvalueContext):
        #arrlistvalue: LBRACE listvalue RBRACE;
        return self.visit(ctx.listvalue())
    
    def visitListvalue(self, ctx: MiniGoParser.ListvalueContext):
        #listvalue: value_for_arr COMMA listvalue | value_for_arr;
        if ctx.listvalue():
            return [self.visit(ctx.value_for_arr())] + self.visit(ctx.listvalue())
        else:
            return [self.visit(ctx.value_for_arr())]
    
    def visitValue_for_arr(self, ctx: MiniGoParser.Value_for_arrContext):
        #value_for_arr: literalvalue_for_arr | arrlistvalue;
        if ctx.expr():
            return self.visit(ctx.literalvalue_for_arr())
        elif ctx.arrliteral():
            return self.visit(ctx.arrliteral())
        else:
            raise Exception("UNKNOWN VALUE_FOR_ARR")
        
    def visitLiteralvalue_for_arr(self, ctx: MiniGoParser.Literalvalue_for_arrContext):
        #literalvalue_for_arr: DECIMAL_INT | BINARY_INT | OCTAL_INT 
        # | HEXADECIMAL_INT | FLOAT_LITERAL| STRING_LITERAL | TRUE | FALSE | NIL | structinst;
        if ctx.DECIMAL_INT():
            return IntLiteral(int(ctx.DECIMAL_INT().getText()))
        elif ctx.BINARY_INT():
            return IntLiteral(int(ctx.BINARY_INT().getText(), 2))
        elif ctx.OCTAL_INT():
            return IntLiteral(int(ctx.OCTAL_INT().getText(), 8))
        elif ctx.HEXADECIMAL_INT():
            return IntLiteral(int(ctx.HEXADECIMAL_INT().getText(), 16))
        elif ctx.FLOAT_LITERAL():
            return FloatLiteral(float(ctx.FLOAT_LITERAL().getText()))
        elif ctx.STRING_LITERAL():
            return StringLiteral(ctx.STRING_LITERAL().getText())
        elif ctx.TRUE():
            return BooleanLiteral(True)
        elif ctx.FALSE():
            return BooleanLiteral(False)
        elif ctx.NIL():
            return NilLiteral()
        elif ctx.structinst():
            return self.visit(ctx.structinst())
        else:
            raise Exception("UNKNOWN LITERALVALUE_FOR_ARR")
        
    def visitStructinst(self, ctx: MiniGoParser.StructinstContext):
        #structinst: IDENTIFIER structinst_body;
        return StructLiteral((ctx.IDENTIFIER().getText()), self.visit(ctx.structinst_body()))
    
    def visitStructinst_body(self, ctx: MiniGoParser.Structinst_bodyContext):
        #structinst_body: LBRACE structinst_field_list RBRACE;
        return self.visit(ctx.structinst_field_list())
    
    def visitStructinst_field_list(self, ctx: MiniGoParser.Structinst_field_listContext):
        #structinst_field_list: structinst_field_prime | ;
        if ctx.structinst_field_prime():
            return self.visit(ctx.structinst_field_prime())
        else:
            return []
        
    def visitStructinst_field_prime(self, ctx: MiniGoParser.Structinst_field_primeContext):
        #structinst_field_prime: structinst_field COMMA structinst_field_prime | structinst_field;
        if ctx.structinst_field_prime():
            return [self.visit(ctx.structinst_field())] + self.visit(ctx.structinst_field_prime())
        else:
            return [self.visit(ctx.structinst_field())]
        
    def visitStructinst_field(self, ctx):
        #structinst_field: IDENTIFIER COLON expr;
        return (Id(ctx.IDENTIFIER().getText()), self.visit(ctx.expr()))
    
    def visitConstdecl(self, ctx: MiniGoParser.ConstdeclContext):
        #constdecl: CONST IDENTIFIER ASSIGN expr SEMI;
        return ConstDecl((ctx.IDENTIFIER().getText()), None, self.visit(ctx.expr()))
    
    def visitStructdecl(self, ctx: MiniGoParser.StructdeclContext):
        #structdecl: TYPE IDENTIFIER STRUCT structbody SEMI;
        return StructType((ctx.IDENTIFIER().getText()), self.visit(ctx.structbody()), [])
    
    def visitStructbody(self, ctx: MiniGoParser.StructbodyContext):
        #structbody: LBRACE fieldlist RBRACE;
        return self.visit(ctx.fieldlist())
    
    def visitFieldlist(self, ctx: MiniGoParser.FieldlistContext):
        #fieldlist: field fieldlist | ;
        if ctx.fieldlist():
            return [self.visit(ctx.field())] + self.visit(ctx.fieldlist())
        else:
            return []
        
    def visitField(self, ctx: MiniGoParser.FieldContext):
        #field: IDENTIFIER (arr_dimension_list | ) typedecl SEMI;
        if ctx.arr_dimension_list():
            return (Id(ctx.IDENTIFIER().getText()), ArrayType(self.visit(ctx.arr_dimension_list()), self.visit(ctx.typedecl())))
        else:
            return (Id(ctx.IDENTIFIER().getText()), self.visit(ctx.typedecl()))
    
    def visitInterfacedecl(self, ctx: MiniGoParser.InterfacedeclContext):
        #interfacedecl: TYPE IDENTIFIER INTERFACE interface_body SEMI;
        return InterfaceType((ctx.IDENTIFIER().getText()), self.visit(ctx.interface_body()))
    
    def visitInterface_body(self, ctx: MiniGoParser.Interface_bodyContext):
        #interface_body: LBRACE methodlist RBRACE;
        return self.visit(ctx.methodlist())
    
    def visitMethodlist(self, ctx: MiniGoParser.MethodlistContext):
        #methodlist: method methodlist | ;
        if ctx.methodlist():
            return [self.visit(ctx.method())] + self.visit(ctx.methodlist())
        else:
            return []
        
    def visitMethod(self, ctx: MiniGoParser.MethodContext): #??????
        #method: IDENTIFIER LPAREN paramlist RPAREN (returntype | ) SEMI;
        if ctx.returntype():
            return Prototype((ctx.IDENTIFIER().getText()), self.visit(ctx.paramlist()), self.visit(ctx.returntype()))
        else:
            return Prototype((ctx.IDENTIFIER().getText()), self.visit(ctx.paramlist()), VoidType())
        
    def visitFuncdecl(self, ctx: MiniGoParser.FuncdeclContext):
        #funcdecl: FUNC IDENTIFIER LPAREN paramlist RPAREN (returntype | ) funcbody SEMI;
        if ctx.returntype():
            return FuncDecl((ctx.IDENTIFIER().getText()), self.visit(ctx.paramlist()), self.visit(ctx.returntype()), self.visit(ctx.funcbody()))
        else:
            return FuncDecl((ctx.IDENTIFIER().getText()), self.visit(ctx.paramlist()), VoidType(), self.visit(ctx.funcbody()))
    
    def visitParamlist(self, ctx: MiniGoParser.ParamlistContext):
        # paramlist: param_group COMMA paramlist | param_group |;
        if ctx.paramlist():
            return self.visit(ctx.param_group()) + self.visit(ctx.paramlist())
        elif ctx.param_group():
            return self.visit(ctx.param_group())
        else:
            return []
    
    def visitParam_group(self, ctx: MiniGoParser.Param_groupContext):
        # param_group: param_mem_list (arr_dimension_list | ) typedecl;
        param_names = self.visit(ctx.param_mem_list())
        param_type = self.visit(ctx.typedecl())
        print("param_names", param_names)
        print("param_type:", param_type)
        print("param_type type:", type(param_type))
        print("param_type class name:", param_type.__class__.__name__)

        # nếu có arr_dimension_list thì nó là mảng
        if ctx.arr_dimension_list():
            param_type = ArrayType(self.visit(ctx.arr_dimension_list()), param_type)

        param_decl_list = []
        for name in param_names:
            param_decl = ParamDecl(str(name), (param_type))
            param_decl_list.append(param_decl)

        return param_decl_list


    
    def visitParam_mem_list(self, ctx: MiniGoParser.Param_mem_listContext):
        # param_mem_list: IDENTIFIER COMMA param_mem_list | IDENTIFIER;
        if ctx.param_mem_list():
            return [(ctx.IDENTIFIER().getText())] + self.visit(ctx.param_mem_list())
        else:
            return [(ctx.IDENTIFIER().getText())]
        
    def visitFuncbody(self, ctx: MiniGoParser.FuncbodyContext):
        #funcbody: LBRACE stmtlist RBRACE;
        return Block(self.visit(ctx.stmtlist()))
    
    def visitStmtlist(self, ctx: MiniGoParser.StmtlistContext):
        #stmtlist: stmt stmtlist | ;
        if ctx.stmtlist():
            return ([self.visit(ctx.stmt())] + self.visit(ctx.stmtlist()))
        else:
            return ([])
        
    def visitReturntype(self, ctx: MiniGoParser.ReturntypeContext):
        #returntype: (arr_dimension_list | ) typedecl;
        if ctx.arr_dimension_list():
            return ArrayType(self.visit(ctx.arr_dimension_list()), self.visit(ctx.typedecl()))
        else:
            return self.visit(ctx.typedecl())
    
    def visitSimplemethod(self, ctx: MiniGoParser.SimplemethodContext):
        # simplemethod:
        # FUNC LPAREN IDENTIFIER IDENTIFIER RPAREN IDENTIFIER LPAREN paramlist RPAREN (returntype | ) simplemethod_body SEMI;

        receiver_name = ctx.IDENTIFIER(0).getText()  
        receiver_type = Id(ctx.IDENTIFIER(1).getText())  

        method_name = ctx.IDENTIFIER(2).getText()  

        params = self.visit(ctx.paramlist()) if ctx.paramlist() else [] 

        if ctx.returntype(): 
            retType = self.visit(ctx.returntype())
        else:
            retType = VoidType()  

        body = self.visit(ctx.simplemethod_body())  

        func = FuncDecl(method_name, params, retType, body) 
        return MethodDecl(receiver_name, receiver_type, func) 

    def visitSimplemethod_body(self, ctx: MiniGoParser.Simplemethod_bodyContext):
        #simplemethod_body: LBRACE stmtlist RBRACE;
        return Block(self.visit(ctx.stmtlist()))
    
    def visitExpr(self, ctx: MiniGoParser.ExprContext):
        #expr: expr OR expr0 | expr0;
        if ctx.OR():
            return BinaryOp("||", self.visit(ctx.expr()), self.visit(ctx.expr0()))
        else:
            return self.visit(ctx.expr0())
        
    def visitExpr0(self, ctx: MiniGoParser.Expr0Context):
        #expr0: expr0 AND expr1 | expr1; 
        if ctx.AND():
            return BinaryOp("&&", self.visit(ctx.expr0()), self.visit(ctx.expr1()))
        else:
            return self.visit(ctx.expr1())
        
    def visitExpr1(self, ctx: MiniGoParser.Expr1Context):
        #expr1: expr1 (EQUAL | NOT_EQUAL | LESS | GREATER | LESS_EQUAL | GREATER_EQUAL) expr2 | expr2;
        if ctx.EQUAL():
            return BinaryOp("==", self.visit(ctx.expr1()), self.visit(ctx.expr2()))
        elif ctx.NOT_EQUAL():
            return BinaryOp("!=", self.visit(ctx.expr1()), self.visit(ctx.expr2()))
        elif ctx.LESS():
            return BinaryOp("<", self.visit(ctx.expr1()), self.visit(ctx.expr2()))
        elif ctx.GREATER():
            return BinaryOp(">", self.visit(ctx.expr1()), self.visit(ctx.expr2()))
        elif ctx.LESS_EQUAL():
            return BinaryOp("<=", self.visit(ctx.expr1()), self.visit(ctx.expr2()))
        elif ctx.GREATER_EQUAL():
            return BinaryOp(">=", self.visit(ctx.expr1()), self.visit(ctx.expr2()))
        else:
            return self.visit(ctx.expr2())
        
    def visitExpr2(self, ctx: MiniGoParser.Expr2Context):
        #expr2: expr2 (PLUS | MINUS) expr3 | expr3;
        if ctx.PLUS():
            return BinaryOp("+", self.visit(ctx.expr2()), self.visit(ctx.expr3()))
        elif ctx.MINUS():
            return BinaryOp("-", self.visit(ctx.expr2()), self.visit(ctx.expr3()))
        else:
            return self.visit(ctx.expr3())
        
    def visitExpr3(self, ctx: MiniGoParser.Expr3Context):
        #expr3: expr3 (MULTIPLY | DIVIDE | MODULUS) expr4 | expr4;
        if ctx.MULTIPLY():
            return BinaryOp("*", self.visit(ctx.expr3()), self.visit(ctx.expr4()))
        elif ctx.DIVIDE():
            return BinaryOp("/", self.visit(ctx.expr3()), self.visit(ctx.expr4()))
        elif ctx.MODULUS():
            return BinaryOp("%", self.visit(ctx.expr3()), self.visit(ctx.expr4()))
        else:
            return self.visit(ctx.expr4())
    
    def visitExpr4(self, ctx: MiniGoParser.Expr4Context):
        #expr4: (MINUS | NOT) expr4 | expr5;
        if ctx.MINUS():
            return UnaryOp("-", self.visit(ctx.expr4()))
        elif ctx.NOT():
            return UnaryOp("!", self.visit(ctx.expr4()))
        else:
            return self.visit(ctx.expr5())
        
    def visitExpr5(self, ctx: MiniGoParser.Expr5Context):
        #expr5: expr5 DOT IDENTIFIER | expr5 LBRACK expr RBRACK | expr6;
        if ctx.DOT():
            return FieldAccess(self.visit(ctx.expr5()), (ctx.IDENTIFIER().getText()))
        elif ctx.LBRACK():
            return ArrayCell(self.visit(ctx.expr5()), [self.visit(ctx.expr())])
        else:
            return self.visit(ctx.expr6())
        
    def visitExpr6(self, ctx: MiniGoParser.Expr6Context):
        #expr6: subexpr | value;
        if ctx.subexpr():
            return self.visit(ctx.subexpr())
        else:
            return self.visit(ctx.value())
        
    def visitSubexpr(self, ctx: MiniGoParser.SubexprContext):
        #subexpr: LPAREN expr RPAREN;
        return self.visit(ctx.expr())
    
    def visitValue(self, ctx: MiniGoParser.ValueContext):
        #value: literalvalue | IDENTIFIER | funccall;
        if ctx.literalvalue():
            return self.visit(ctx.literalvalue())
        elif ctx.IDENTIFIER():
            return Id(ctx.IDENTIFIER().getText())
        elif ctx.funccall():
            return self.visit(ctx.funccall())
        else:
            raise Exception("UNKNOWN VALUE")
        
    def visitLiteralvalue(self, ctx: MiniGoParser.LiteralvalueContext):
        #literalvalue: literalvalue_for_arr | arrliteral;
        if ctx.literalvalue_for_arr():
            return self.visit(ctx.literalvalue_for_arr())
        elif ctx.arrliteral():
            return self.visit(ctx.arrliteral())
        else:
            raise Exception("UNKNOWN LITERALVALUE")
        
    def visitFunccall(self, ctx: MiniGoParser.FunccallContext):
        #funccall: IDENTIFIER LPAREN (arglist | ) RPAREN;
        return FuncCall((ctx.IDENTIFIER().getText()), self.visit(ctx.arglist()) if ctx.arglist() else [])
    
    def visitArglist(self, ctx: MiniGoParser.ArglistContext):
        #arglist: expr COMMA arglist | expr |;
        if ctx.arglist():
            return [self.visit(ctx.expr())] + self.visit(ctx.arglist())
        elif ctx.expr():
            return [self.visit(ctx.expr())]
        else:
            return []
        
    def visitMethodcall(self, ctx: MiniGoParser.MethodcallContext):
        #methodcall: expr accesslist LPAREN arglist RPAREN;
        return MethCall(self.visit(ctx.expr()), ctx.IDENTIFIER().getText(), self.visit(ctx.arglist()))
        
    def visitStmt(self, ctx: MiniGoParser.StmtContext):
        #stmt: vardecl | constdecl | assignstmt | returnstmt | ifstmt | forstmt | breakstmt | continuestmt | callstmt;
        if ctx.vardecl():
            return self.visit(ctx.vardecl())
        elif ctx.constdecl():
            return self.visit(ctx.constdecl())
        elif ctx.assignstmt():
            return self.visit(ctx.assignstmt())
        elif ctx.returnstmt():
            return self.visit(ctx.returnstmt())
        elif ctx.ifstmt():
            return self.visit(ctx.ifstmt())
        elif ctx.forstmt():
            return self.visit(ctx.forstmt())
        elif ctx.breakstmt():
            return self.visit(ctx.breakstmt())
        elif ctx.continuestmt():
            return self.visit(ctx.continuestmt())
        elif ctx.callstmt():
            return self.visit(ctx.callstmt())
        else:
            raise Exception("UNKNOWN STATEMENT")
        
    def visitAssignstmt(self, ctx: MiniGoParser.AssignstmtContext):
        #assignstmt: var assignop expr SEMI;
        return Assign(self.visit(ctx.var()), self.visit(ctx.expr()))
    
    def visitVar(self, ctx: MiniGoParser.VarContext):
        #var: IDENTIFIER accesslist | IDENTIFIER;
        if ctx.accesslist():
            return ArrayCell(Id(ctx.IDENTIFIER().getText()), self.visit(ctx.accesslist()))
        else:
            return Id(ctx.IDENTIFIER().getText())
    
    def visitAccesslist(self, ctx: MiniGoParser.AccesslistContext):
        #accesslist: access accesslist | access;
        if ctx.accesslist():
            return [self.visit(ctx.access())] + self.visit(ctx.accesslist())
        else:
            return [self.visit(ctx.access())]
        
    def visitAccess(self, ctx: MiniGoParser.AccessContext):
        #access: arrayaccess | structaccess;
        if ctx.arrayaccess():
            return self.visit(ctx.arrayaccess())
        elif ctx.structaccess():
            return self.visit(ctx.structaccess())
        else:
            raise Exception("UNKNOWN ACCESS")
        
    def visitArrayaccess(self, ctx: MiniGoParser.ArrayaccessContext):
        #arrayaccess: LBRACK expr RBRACK;
        return self.visit(ctx.expr())
    
    def visitStructaccess(self, ctx: MiniGoParser.StructaccessContext):
        #structaccess: DOT IDENTIFIER;
        return Id(ctx.IDENTIFIER().getText())
    
    def visitAssignop(self, ctx: MiniGoParser.AssignopContext):
        #assignop: ASSIGN_DECLARE | PLUS_ASSIGN | MINUS_ASSIGN | MULTIPLY_ASSIGN| DIVIDE_ASSIGN | MODULUS_ASSIGN;
        if ctx.ASSIGN_DECLARE():
            return ":="
        elif ctx.PLUS_ASSIGN():
            return "+="
        elif ctx.MINUS_ASSIGN():
            return "-="
        elif ctx.MULTIPLY_ASSIGN():
            return "*="
        elif ctx.DIVIDE_ASSIGN():
            return "/="
        elif ctx.MODULUS_ASSIGN():
            return "%="
        else:
            raise Exception("UNKNOWN ASSIGNOP")
        
    def visitReturnstmt(self, ctx: MiniGoParser.ReturnstmtContext):
        #returnstmt: RETURN (expr | ) SEMI ;
        if ctx.expr():
            return Return(self.visit(ctx.expr()))
        else:
            return Return(None)
        
    def visitCallstmt(self, ctx: MiniGoParser.CallstmtContext):
        #callstmt: ( funccall |  methodcall) SEMI;
        if ctx.funccall():
            return self.visit(ctx.funccall())
        elif ctx.methodcall():
            return self.visit(ctx.methodcall())
        else:
            raise Exception("UNKNOWN CALLSTMT")
        
    def visitIfstmt(self, ctx: MiniGoParser.IfstmtContext):
        # ifstmt: firstifstmt elseifstmtlist (elsestmt | ) SEMI;

        first_if = self.visit(ctx.firstifstmt())
        elseif_list = self.visit(ctx.elseifstmtlist())
        else_stmt = self.visit(ctx.elsestmt()) if ctx.elsestmt() else None

        # Nếu không có elseif, thì else_stmt thuộc về first_if
        if len(elseif_list) == 0:
            first_if.elseStmt = else_stmt
            return first_if

        # Gắn elseif đầu tiên vào else của first_if
        first_if.elseStmt = elseif_list[0]

        # Chuỗi nối các elseif lại với nhau
        for i in range(len(elseif_list) - 1):
            elseif_list[i].elseStmt = elseif_list[i + 1]

        # Gán else_stmt vào cuối cùng của elseif_list
        elseif_list[-1].elseStmt = else_stmt

        return first_if
        # cái if cuối cùng của mảng ms bỏ else_stmt vào
    
    def visitFirstifstmt(self, ctx: MiniGoParser.FirstifstmtContext):
        # firstifstmt: IF LPAREN expr RPAREN ifstmtbody;
        expr = self.visit(ctx.expr())
        then_stmt = Block(self.visit(ctx.ifstmtbody()))
        return If(expr, then_stmt, None)
    def visitIfstmtbody(self, ctx: MiniGoParser.IfstmtbodyContext):
        # ifstmtbody: LBRACE stmtlist RBRACE;
        return self.visit(ctx.stmtlist())

    def visitElseifstmtlist(self, ctx: MiniGoParser.ElseifstmtlistContext):
        # elseifstmtlist: elseifstmt elseifstmtlist | ;
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.elseifstmt())] + self.visit(ctx.elseifstmtlist())
    def visitElseifstmt(self, ctx: MiniGoParser.ElseifstmtContext):
        # elseifstmt: ELSE IF LPAREN expr RPAREN ifstmtbody;
        expr = self.visit(ctx.expr())
        then_stmt = Block(self.visit(ctx.ifstmtbody()))
        return If(expr, then_stmt, None)
    def visitElsestmt(self, ctx: MiniGoParser.ElsestmtContext):
        # elsestmt: ELSE ifstmtbody;
        return Block(self.visit(ctx.ifstmtbody()))
    
    def visitForstmt(self, ctx: MiniGoParser.ForstmtContext):
        #forstmt: basicforstmt | init_cond_update_forstmt | rangeforstmt;
        if ctx.basicforstmt():
            return self.visit(ctx.basicforstmt())
        elif ctx.init_cond_update_forstmt():
            return self.visit(ctx.init_cond_update_forstmt())
        elif ctx.rangeforstmt():
            return self.visit(ctx.rangeforstmt())
        else:
            raise Exception("UNKNOWN FORSTMT")
    
    def visitBasicforstmt(self, ctx: MiniGoParser.BasicforstmtContext):
        #basicforstmt: FOR expr forstmtbody SEMI;
        expr = self.visit(ctx.expr())
        body = self.visit(ctx.forstmtbody())
        return ForBasic(expr, body)
    
    def visitForstmtbody(self, ctx: MiniGoParser.ForstmtbodyContext):
        #forstmtbody: LBRACE stmtlist RBRACE;
        return Block(self.visit(ctx.stmtlist()))
    
    def visitInit_cond_update_forstmt(self, ctx):
        #init_cond_update_forstmt: FOR init_for SEMI expr SEMI assign forstmtbody SEMI;
        return ForStep(self.visit(ctx.init_for()), self.visit(ctx.expr()), self.visit(ctx.assign()), self.visit(ctx.forstmtbody()))

    def visitInit_for(self, ctx: MiniGoParser.Init_forContext):
        #init_for: assign | VAR IDENTIFIER (typedecl | ) ASSIGN expr; trick lỏ ????
        if ctx.assign():
            return self.visit(ctx.assign())
        elif ctx.VAR():
            if ctx.typedecl():
                return VarDecl(ctx.IDENTIFIER().getText(), self.visit(ctx.typedecl()), self.visit(ctx.expr()))
            else:
                return VarDecl(ctx.IDENTIFIER().getText(), None, self.visit(ctx.expr()))
        else:
            raise Exception("UNKNOWN INIT_FOR")

    def visitAssign(self, ctx: MiniGoParser.AssignContext):
        #assign: var assignop expr;
        return Assign(self.visit(ctx.var()), 
                      BinaryOp(str(self.visit(ctx.assignop()))[0], self.visit(ctx.var()), self.visit(ctx.expr())))
        
    def visitRangeforstmt(self, ctx: MiniGoParser.RangeforstmtContext):
        #rangeforstmt: FOR IDENTIFIER COMMA IDENTIFIER ASSIGN_DECLARE RANGE expr forstmtbody SEMI;
        idx = Id(ctx.IDENTIFIER(0).getText())
        value = Id(ctx.IDENTIFIER(1).getText())
        arr = self.visit(ctx.expr())
        loop = self.visit(ctx.forstmtbody())
        return ForEach(idx, value, arr, loop)
    
    def visitBreakstmt(self, ctx: MiniGoParser.BreakstmtContext):
        #breakstmt: BREAK SEMI;
        return Break()
    
    def visitContinuestmt(self, ctx: MiniGoParser.ContinuestmtContext):
        #continuestmt: CONTINUE SEMI;
        return Continue()
    