import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    def test_simple_program(self):
        """Simple program: int main() {} """
        input = """func main() {};"""
        expect = str(Program([FuncDecl("main",[],VoidType(),Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,300))

    def test_more_complex_program(self):
        """More complex program"""
        input = """var x int ;"""
        expect = str(Program([VarDecl("x",IntType(),None)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,301))
    
    def test_call_without_parameter(self):
        """More complex program"""
        input = """func main () {}; var x int ;"""
        expect = str(Program([FuncDecl("main",[],VoidType(),Block([])),VarDecl("x",IntType(),None)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,302))
   
    def test_function_with_one_param(self):
        """Function with 1 parameter"""
        input = """func sum(a int) {};"""
        expect = str(Program([
            FuncDecl("sum",[
                ParamDecl("a","IntType")
            ],VoidType(),Block([]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input,expect,303))
    def test_function_with_params(self):
        """Function with 1 parameter"""
        input = """func sum(a int, b float) {};"""
        expect = str(Program([
            FuncDecl("sum",[
                ParamDecl("a","IntType"),
                ParamDecl("b","FloatType")
            ],VoidType(),Block([]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input,expect,304))
        
    def test_variable_initialization(self):
        """Variable with initialization"""
        input = """var x int = 5;"""
        expect = str(Program([
            VarDecl("x",IntType(),IntLiteral(5))
        ]))
        self.assertTrue(TestAST.checkASTGen(input,expect,305))
        
    def test_block_with_statements(self):
        """Function with block containing variable declaration"""
        input = """func main() {var x int; var y float;};"""
        expect = str(Program([
            FuncDecl("main",[],VoidType(),Block([
                VarDecl("x",IntType(),None),
                VarDecl("y",FloatType(),None)
            ]))
        ]))
        self.assertTrue(TestAST.checkASTGen(input,expect,306))
        
    def test_block_with_statements_params(self):
        """Function with array type parameters block containing variable declaration"""
        input = """func vitinhtu(x [5] int, y [5] float, z [5] string){};"""
        expect = str(Program([
            FuncDecl("vitinhtu",[
                ParamDecl("x",ArrayType([IntLiteral(5)],IntType())),
                ParamDecl("y",ArrayType([IntLiteral(5)],FloatType())),
                ParamDecl("z",ArrayType([IntLiteral(5)],StringType()))
                ],VoidType(),Block([]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,307))
        
    def test_scalar_variable_with_init(self):
        input = """var i int = 1;"""
        expect = str(Program([VarDecl("i",IntType(),IntLiteral(1))]))
        print("expect: ",expect)
        self.assertTrue(TestAST.checkASTGen(input,expect,308))
        
    def test_scalar_variable_without_init(self):
        input = """var i int;"""
        expect = str(Program([VarDecl("i",IntType(),None)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,309))
        
    def test_scalar_variable_struct_type_without_init(self):
        input = """var i tung;"""
        expect = str(Program([VarDecl("i",Id("tung"),None)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,310))
        
    def test_scalar_variable_missing_type_integer(self):
        input = """var i = 2;"""
        expect = str(Program([VarDecl("i",None,IntLiteral(2))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,311))
        
    def test_scalar_variable_missing_type_float(self):
        input = """var i = 2.4;"""
        expect = str(Program([VarDecl("i",None,FloatLiteral(2.4))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,312))
        
    def test_scalar_variable_missing_type_boolean(self):
        input = """var i = true;"""
        expect = str(Program([VarDecl("i",None,BooleanLiteral(True))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,313))
        
    def test_scalar_variable_missing_type_boolean_nil(self):
        input = """var i = "tung"; var a = nil;"""
        expect = str(Program([VarDecl("i",None,StringLiteral("\"tung\"")), VarDecl("a",None,NilLiteral())]))
        print("EXPECT: " + expect)
        self.assertTrue(TestAST.checkASTGen(input,expect,314))
        
    def test_const_decl_int_value(self):
        input = """const i = 2;"""
        expect = str(
            Program([
                ConstDecl("i",None,IntLiteral(2))
                ]))
        self.assertTrue(TestAST.checkASTGen(input,expect,315))
        
    def test_const_decl_id_value(self):
        input = """const Pi = i;"""
        expect = str(
            Program([
                ConstDecl("Pi",None,Id("i"))
                ]))
        self.assertTrue(TestAST.checkASTGen(input,expect,316))
        
    def test_array_decl_without_init(self):
        input = """var a [2] int; var b [1][3][2][10] string;"""
        expect = str(Program([
            VarDecl("a",ArrayType([IntLiteral(2)],IntType()),None),
            VarDecl("b",ArrayType([IntLiteral(1),IntLiteral(3),IntLiteral(2),IntLiteral(10)],StringType()),None)
        ]))
        self.assertTrue(TestAST.checkASTGen(input,expect,317))
        
    def test_array_decl_with_init(self):
        input= """var a [5] int = [5] int{1,2,3,4};"""
        expect = str(Program(
            [
                VarDecl("a",ArrayType([IntLiteral(5)],IntType()),
                        ArrayLiteral([IntLiteral(5)], IntType(), [IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4)]))
            ]
        ))
        self.assertTrue(TestAST.checkASTGen(input,expect,318))
        
    def test_matrix_decl_with_init(self):
        input = """var a [1][2] int = [2][1]int{{1},{2}};"""
        expect = str(Program(
            [
                VarDecl("a",ArrayType([IntLiteral(1), IntLiteral(2)],IntType()),
                        ArrayLiteral([IntLiteral(2), IntLiteral(1)], IntType(), [[IntLiteral(1)],[IntLiteral(2)]]))
            ]
        ))
        self.assertTrue(TestAST.checkASTGen(input,expect,319))
        
    def test_struct_decl(self):
        input = """type foo struct {
            a int;
            b float;
        };"""
        expect = str(Program([
            StructType(
                "foo",
                [
                    ("a", IntType()),
                    ("b", FloatType())
                ],
                []
            )
        ]))
        self.assertTrue(TestAST.checkASTGen(input, expect, 320))
        
    def test_declare_struct_method(self):
        input = """type foo struct {
            a int;
            b float;
        };
        func (f foo) getA() int {
            return f.a;
        };"""
        expect = str(Program([
            StructType(
                "foo",
                [
                    ("a", IntType()),
                    ("b", FloatType())
                ],[]),
            MethodDecl("f",Id("foo"),FuncDecl("getA", [], IntType(), Block([Return(FieldAccess(Id("f"), "a"))])))
                
        ]))
        print("EXPECT:", expect)
        self.assertTrue(TestAST.checkASTGen(input, expect, 321))

    def test_instance_struct(self):
        input = """var s student = student{name: "Nguyen Van A",age: 20, isAvailable: true};"""
        
        expect = str(Program([
            VarDecl("s", Id("student"),
                StructLiteral("student",
                   [
                          ("name", StringLiteral("\"Nguyen Van A\"")),
                          ("age", IntLiteral(20)),
                          ("isAvailable", BooleanLiteral(True))
                   ]
                )
            )
        ]))
        print("EXPECT:", expect)
        self.assertTrue(TestAST.checkASTGen(input, expect, 322))