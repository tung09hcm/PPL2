import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    
    def test_in_single_ast(self):
        input ="""func main(){
            car.wheel[0][b].brand[1] := "Michelin";
        };"""
        expect = str(Program(
            [
                FuncDecl(
                    "main",
                    [],
                    VoidType(),
                    Block(
                        [
                            Assign(
                                ArrayCell(
                                    FieldAccess(
                                        ArrayCell(
                                            FieldAccess(Id("car"),"wheel"),
                                            [IntLiteral(0), Id("b")]),
                                        "brand"),
                                    [IntLiteral(1)]),
                                StringLiteral("\"Michelin\"")
                            )
                        ]
                    )
                )
            ]
        ))
        print("expect: " + expect)
        self.assertTrue(TestAST.checkASTGen(input,expect,0))