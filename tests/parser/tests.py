import unittest

from typing import List, Dict

from langtools.lexer.token import Token
from langtools.parser.cfg import CFG
from langtools.ast.ast import ASTNode

from src.config.tokens import *
from src.config.parser import PRODUCTION_RULES, START


def parse(tokens: List[Token]) -> ASTNode:
    lara_grammar = CFG(
        production_rules=PRODUCTION_RULES,
        alphabet=[chr(i) for i in range(128)],
        start_symbol=START,
    )
    ast = lara_grammar.LL1_parse(tokens)
    ast.flatten(
        {
            "STATEMENTS": {"STATEMENTS"},
            "ARGUMENTS": {"ANOTHER_ARGUMENT", "ARGUMENTS"},
            "ANOTHER_ARGUMENT": {"ARGUMENTS"},
            # "EXPRESSION": {"TERM_OPERATOR"},
        }
    )
    return ast


def compare_ast(ast1: ASTNode, ast2: ASTNode) -> bool:
    if ast1.name != ast2.name:
        print(f"{ast1.name} != {ast2.name}")
        return False

    if len(ast1.children) != len(ast2.children):
        print(
            f"{ast1.name} : {len(ast1.children)} != {ast2.name} : {len(ast2.children)}"
        )
        return False

    for child1, child2 in zip(ast1.children, ast2.children):
        if not compare_ast(child1, child2):
            return False

    return True


def add_ast_boilerplate(literal: Dict) -> ASTNode:
    return ASTNode.from_dict_literal({"S-Prime": [{"BOF": []}, literal, {"EOF": []},]})


class ExpressionTests(unittest.TestCase):
    def test__LL1_parse_addition(self):
        tokens = [
            IntegerToken,
            PlusToken,
            IntegerToken,
            SemiColonToken,
        ]
        ast = parse(tokens)

        expected_ast = add_ast_boilerplate({"START": [],})

        # self.assertTrue(compare_ast(ast, expected_ast))


class FunctionDefinitionTests(unittest.TestCase):
    def test__LL1_parse__main(self):
        tokens = [
            FuncToken,
            IdentifierToken,
            LeftParenToken,
            RightParenToken,
            LeftCurlyToken,
            RightCurlyToken,
        ]
        ast = parse(tokens)

        expected_ast = add_ast_boilerplate(
            {
                "START": [
                    {
                        "STATEMENTS": [
                            {
                                "STATEMENT": [
                                    {
                                        "FUNCTION_DEF": [
                                            {"FUNC": []},
                                            {"IDENTIFIER": []},
                                            {"LEFT_PAREN": []},
                                            {"ARGUMENTS": []},
                                            {"RIGHT_PAREN": []},
                                            {"LEFT_CURLY": []},
                                            {"STATEMENTS": []},
                                            {"RIGHT_CURLY": []},
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        )

        self.assertTrue(compare_ast(ast, expected_ast))

    def test__LL1_parse_arguments(self):
        tokens = [
            FuncToken,
            IdentifierToken,
            LeftParenToken,
            IdentifierToken,
            CommaToken,
            IdentifierToken,
            CommaToken,
            IdentifierToken,
            RightParenToken,
            LeftCurlyToken,
            RightCurlyToken,
        ]
        ast = parse(tokens)

        expected_ast = add_ast_boilerplate(
            {
                "START": [
                    {
                        "STATEMENTS": [
                            {
                                "STATEMENT": [
                                    {
                                        "FUNCTION_DEF": [
                                            {"FUNC": []},
                                            {"IDENTIFIER": []},
                                            {"LEFT_PAREN": []},
                                            {
                                                "ARGUMENTS": [
                                                    {
                                                        "ARGUMENT": [
                                                            {
                                                                "EXPRESSION": [
                                                                    {
                                                                        "TERM": [
                                                                            {
                                                                                "FACTOR": [
                                                                                    {
                                                                                        "VAR_REF": [
                                                                                            {
                                                                                                "IDENTIFIER": [],
                                                                                            },
                                                                                            {
                                                                                                "CALL": []
                                                                                            },
                                                                                        ]
                                                                                    },
                                                                                ]
                                                                            },
                                                                            {
                                                                                "FACTOR_OPERATOR": []
                                                                            },
                                                                        ]
                                                                    },
                                                                    {
                                                                        "TERM_OPERATOR": []
                                                                    },
                                                                ]
                                                            }
                                                        ]
                                                    },
                                                    {"COMMA": [],},
                                                    {
                                                        "ARGUMENT": [
                                                            {
                                                                "EXPRESSION": [
                                                                    {
                                                                        "TERM": [
                                                                            {
                                                                                "FACTOR": [
                                                                                    {
                                                                                        "VAR_REF": [
                                                                                            {
                                                                                                "IDENTIFIER": [],
                                                                                            },
                                                                                            {
                                                                                                "CALL": []
                                                                                            },
                                                                                        ]
                                                                                    },
                                                                                ]
                                                                            },
                                                                            {
                                                                                "FACTOR_OPERATOR": []
                                                                            },
                                                                        ]
                                                                    },
                                                                    {
                                                                        "TERM_OPERATOR": []
                                                                    },
                                                                ]
                                                            }
                                                        ]
                                                    },
                                                    {"COMMA": [],},
                                                    {
                                                        "ARGUMENT": [
                                                            {
                                                                "EXPRESSION": [
                                                                    {
                                                                        "TERM": [
                                                                            {
                                                                                "FACTOR": [
                                                                                    {
                                                                                        "VAR_REF": [
                                                                                            {
                                                                                                "IDENTIFIER": [],
                                                                                            },
                                                                                            {
                                                                                                "CALL": []
                                                                                            },
                                                                                        ]
                                                                                    },
                                                                                ]
                                                                            },
                                                                            {
                                                                                "FACTOR_OPERATOR": []
                                                                            },
                                                                        ]
                                                                    },
                                                                    {
                                                                        "TERM_OPERATOR": []
                                                                    },
                                                                ]
                                                            }
                                                        ]
                                                    },
                                                ]
                                            },
                                            {"RIGHT_PAREN": []},
                                            {"LEFT_CURLY": []},
                                            {"STATEMENTS": []},
                                            {"RIGHT_CURLY": []},
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        )

        self.assertTrue(compare_ast(ast, expected_ast))


class StatementTests(unittest.TestCase):
    pass


class IOTests(unittest.TestCase):
    def test__LL1_parse__print(self):
        tokens = [
            PrintToken,
        ]
        ast = parse(tokens)
        print(ast)
