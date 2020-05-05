from __future__ import annotations
from typing import List, Optional, Callable, Dict, Union

from langtools.ast.ast import ASTNode


class ScopeTreeNode:
    def __init__(self, parent: Optional[ScopeTreeNode]):
        self.parent = parent
        # $RETURN store return values and cannot conflict with other identifiers ($)
        # $RETURN flag is set to true once a return statement in encountered
        self.symbols: Dict[str, Union[Function, int, None, bool]] = {
            "$RETURN": None,
            "$RETURN_FLAG": False,
            "$BREAK_FLAG": False,
        }
        self.children: List[ScopeTreeNode] = []

    def get_symbol(self, identifier: str) -> int:
        if identifier in self.symbols:
            return self.symbols[identifier]
        elif self.parent is not None:
            return self.parent.get_symbol(identifier)
        else:
            raise Exception(f"Use of undefined symbol {identifier}")

    def set_symbol(self, identifier: str, value: int) -> None:
        if identifier in self.symbols:
            self.symbols[identifier] = value
        elif self.parent is not None:
            self.parent.set_symbol(identifier, value)
        else:
            raise Exception(f"Reference of undefined symbol {identifier}")


class Function:
    def __init__(
        self, ast: ASTNode, arg_parse_func: Callable[[List[int], ScopeTreeNode], None]
    ):
        assert ast.name == "FUNCTION_DEF"

        self.ast = ast
        self.arg_parse_func = arg_parse_func

    def __call__(self, evaluator: Evaluator, args: List[int]) -> Optional[int]:
        new_scope = ScopeTreeNode(evaluator.curr_scope)
        self.arg_parse_func(args, new_scope)
        evaluator.curr_scope = new_scope
        evaluator._evaluate_statements(self.ast.children[6])

        return new_scope.symbols["$RETURN"]


class Evaluator:
    def __init__(self, ast: ASTNode):
        self.ast = ast
        self.scope_tree = ScopeTreeNode(None)
        self.curr_scope = self.scope_tree

    def _evaluate_arguments(self, ast: ASTNode) -> List[int]:
        assert ast.name == "ARGUMENTS"
        result: List[int] = []
        for child in ast.children:
            if child.name == "ARGUMENT":
                result.append(self._evaluate_expression(child.children[0]))
        return result

    def _evaluate_arguments_def(self, ast: ASTNode) -> List[str]:
        assert ast.name == "ARGUMENTS_DEF"

        result: List[str] = []
        for child in ast.children:
            if child.name == "ARGUMENT_DEF":
                identifier_lexme = child.children[0].lexme
                if identifier_lexme is None:
                    raise Exception("Identifier missing lexme")
                result.append(identifier_lexme)
        return result

    def _evaluate_var_definition(self, ast: ASTNode) -> None:
        assert ast.name == "VAR_DEF"

        identifier_lexme = ast.children[1].lexme
        if identifier_lexme is None:
            raise Exception("Identifier lexme missing")

        value = self._evaluate_expression(ast.children[-1])

        if identifier_lexme in self.curr_scope.symbols:
            raise Exception(f"Duplicate definition of symbol: {identifier_lexme}")

        self.curr_scope.symbols[identifier_lexme] = value

    def _evaluate_var_reference(self, ast: ASTNode) -> int:
        assert ast.name == "VAR_REF"

        identifier, call = ast.children

        if identifier.lexme is None:
            raise Exception("Missing lexme on identifier")

        symbol = self.curr_scope.get_symbol(identifier.lexme)

        if call.children:
            return symbol(self, self._evaluate_arguments(call.children[1]))

        return symbol

    def _evaluate_factor(self, ast: ASTNode) -> int:
        assert ast.name == "FACTOR"

        # FACTOR -> left_paren, EXPRESSION, left_paren
        if len(ast.children) == 3:
            return self._evaluate_expression(ast.children[1])
        elif ast.children[0].name == "INTEGER":
            if ast.children[0].lexme is None:
                raise Exception("Integer node missing lexme")
            return int(ast.children[0].lexme)
        elif ast.children[0].name == "VAR_REF":
            return self._evaluate_var_reference(ast.children[0])
        else:
            raise Exception("Invalid factor children")

    def _evaluate_term(self, ast: ASTNode) -> int:
        assert ast.name == "TERM"

        factor, factor_operator = ast.children
        result = self._evaluate_factor(factor)

        if factor_operator.children:
            if factor_operator.children[0].name == "MULTIPLY":
                result *= self._evaluate_term(factor_operator.children[1])
            elif factor_operator.children[0].name == "DIVIDE":
                # TODO handle floats at some point
                result //= self._evaluate_term(factor_operator.children[1])
            else:
                raise Exception(
                    f"Invalid factor operator: {factor_operator.children[0].name}"
                )

        return result

    def _evaluate_operand(self, ast: ASTNode) -> int:
        assert ast.name == "OPERAND"

        term, term_operator = ast.children
        result = self._evaluate_term(term)

        # if operator found
        if term_operator.children:
            if term_operator.children[0].name == "PLUS":
                result += self._evaluate_operand(term_operator.children[1])
            elif term_operator.children[0].name == "MINUS":
                result -= self._evaluate_operand(term_operator.children[1])
            else:
                raise Exception(f"Invalid Term Operator: {term.children[0].name}")

        return result

    def _evaluate_expression(self, ast: ASTNode) -> int:
        assert ast.name == "EXPRESSION"

        operand, operand_operator = ast.children
        result = self._evaluate_operand(operand)

        # if operator found
        if operand_operator.children:
            if operand_operator.children[0].name == "LESS":
                result = (
                    1
                    if result < self._evaluate_expression(operand_operator.children[1])
                    else 0
                )
            elif operand_operator.children[0].name == "GREATER":
                result = (
                    1
                    if result > self._evaluate_expression(operand_operator.children[1])
                    else 0
                )
            elif operand_operator.children[0].name == "LESS_EQUAL":
                result = (
                    1
                    if result <= self._evaluate_expression(operand_operator.children[1])
                    else 0
                )
            elif operand_operator.children[0].name == "GREATER_EQUAL":
                result = (
                    1
                    if result >= self._evaluate_expression(operand_operator.children[1])
                    else 0
                )
            else:
                raise Exception(
                    f"Invalid Operand Operator: {operand_operator.children[0].name}"
                )

        return result

    def _bool_cast_expression(self, ast: ASTNode) -> bool:
        assert ast.name == "EXPRESSION"
        return bool(self._evaluate_expression(ast))

    def _evaluate_return(self, ast: ASTNode) -> None:
        assert ast.name == "RETURN_STATEMENT"

        retval = None

        # If there is a return value provided
        if ast.children[1].children:
            # Evaluate it
            retval = self._evaluate_expression(ast.children[1].children[0])

        self.curr_scope.symbols["$RETURN"] = retval
        self.curr_scope.symbols["$RETURN_FLAG"] = True

    def _evaluate_break(self, ast: ASTNode) -> None:
        assert ast.name == "BREAK_STATEMENT"

        self.curr_scope.symbols["$BREAK_FLAG"] = True

    def _evaluate_var_mutation(self, ast: ASTNode) -> None:
        assert ast.name == "VAR_ASSIGN"

        identifier_lexme = ast.children[0].lexme

        if identifier_lexme is None:
            raise Exception("Missing identifier lexme")

        value = self._evaluate_expression(ast.children[2])
        self.curr_scope.set_symbol(identifier_lexme, value)

    def _evaluate_io(self, ast: ASTNode) -> None:
        assert ast.name == "OUTPUT"

        print(self._evaluate_expression(ast.children[2]))

    def _evaluate_if_block(self, ast: ASTNode) -> None:
        assert ast.name == "IF_BLOCK"

        path_taken = False
        for child in ast.children:
            if child.name == "IF":
                if self._bool_cast_expression(child.children[1]):
                    self._evaluate_statements(child.children[4])
                    path_taken = True
            elif child.name == "ELIF":
                if not path_taken and self._bool_cast_expression(child.children[1]):
                    self._evaluate_statements(child.children[4])
                    path_taken = True
            elif child.name == "ELSE":
                if not path_taken:
                    self._evaluate_statements(child.children[1])
            else:
                raise Exception(f"Invalid conditional branch name: {child.name}")

    def _evaluate_for_block(self, ast: ASTNode) -> None:
        assert ast.name == "FOR_BLOCK"

        var_def = ast.children[2]
        condition = ast.children[4]
        var_mutation = ast.children[6]

        self._evaluate_var_definition(var_def)

        scope_when_loop_started = self.curr_scope

        while self._bool_cast_expression(condition):
            self._evaluate_statements(ast.children[9])

            if self.curr_scope != scope_when_loop_started:
                # Return statement was executed
                return
            if self.curr_scope.symbols["$BREAK_FLAG"]:
                self.curr_scope.symbols["$BREAK_FLAG"] = False
                return

            self._evaluate_var_mutation(var_mutation)

    # A less than ideal hack to maintain an LL1 parseable grammar
    def _evaluate_root_var_ref(self, ast: ASTNode) -> None:
        assert ast.name == "ROOT_VAR_REF"

        identifier_lexme = ast.children[0].lexme

        if identifier_lexme is None:
            raise Exception("Identifier lexme is missing")

        root_var_ref_operator = ast.children[1]

        if root_var_ref_operator.children[0].name == "LEFT_PAREN":
            self.curr_scope.get_symbol(identifier_lexme)(
                self, self._evaluate_arguments(root_var_ref_operator.children[1])
            )
        elif root_var_ref_operator.children[0].name == "ASSIGN":
            self.curr_scope.set_symbol(
                identifier_lexme,
                self._evaluate_expression(root_var_ref_operator.children[1]),
            )

    def _evaluate_statement(self, ast: ASTNode) -> None:
        assert ast.name == "STATEMENT"

        if ast.children[0].name == "OUTPUT":
            self._evaluate_io(ast.children[0])
        elif ast.children[0].name == "VAR_DEF":
            self._evaluate_var_definition(ast.children[0])
        elif ast.children[0].name == "FUNCTION_DEF":
            self._evaluate_function_definition(ast.children[0])
        elif ast.children[0].name == "RETURN_STATEMENT":
            self._evaluate_return(ast.children[0])
        elif ast.children[0].name == "VAR_ASSIGN":
            self._evaluate_var_mutation(ast.children[0])
        elif ast.children[0].name == "IF_BLOCK":
            self._evaluate_if_block(ast.children[0])
        elif ast.children[0].name == "FOR_BLOCK":
            self._evaluate_for_block(ast.children[0])
        elif ast.children[0].name == "ROOT_VAR_REF":
            self._evaluate_root_var_ref(ast.children[0])
        elif ast.children[0].name == "BREAK_STATEMENT":
            self._evaluate_break(ast.children[0])
        else:
            raise Exception(f"Invalid Statement: {ast.children[0].name}")

    def _evaluate_statements(self, ast: ASTNode) -> None:
        assert ast.name == "STATEMENTS"

        for statement in ast.children:
            self._evaluate_statement(statement)
            if self.curr_scope.symbols["$RETURN_FLAG"]:
                if self.curr_scope.parent is not None:
                    self.curr_scope = self.curr_scope.parent
                else:
                    raise Exception("Use of return outside of function")
                break

            if self.curr_scope.symbols["$BREAK_FLAG"]:
                break

    def _evaluate_function_definition(self, ast: ASTNode) -> None:
        assert ast.name == "FUNCTION_DEF"

        identifier_lexme = ast.children[1].lexme

        if identifier_lexme is None:
            raise Exception("Identifier lexme is missing")

        if identifier_lexme in self.curr_scope.symbols:
            raise Exception(f"Duplicate function definition: {identifier_lexme}")

        identifier_list = self._evaluate_arguments_def(ast.children[3])

        def augment_scope(args: List[int], scope: ScopeTreeNode):
            for identifier, arg in zip(identifier_list, args):
                scope.symbols[identifier] = arg

        new_function = Function(ast, augment_scope)
        self.curr_scope.symbols[identifier_lexme] = new_function

    def evaluate(self) -> None:
        self._evaluate_statements(self.ast.children[1].children[0])
