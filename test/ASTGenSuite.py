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
        
    