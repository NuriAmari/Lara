from langtools.parser.cfg import CFG, Terminal, NonTerminal, ProductionRule
from langtools.parser.cfg import Epsilon

# TERMINAL

integer = Terminal(name="INTEGER")
comma = Terminal(name="COMMA")
left_curly = Terminal(name="LEFT_CURLY")
left_paren = Terminal(name="LEFT_PAREN")
right_curly = Terminal(name="RIGHT_CURLY")
right_paren = Terminal(name="RIGHT_PAREN")
semi_colon = Terminal(name="SEMI_COLON")
func_kw = Terminal(name="FUNC")
if_kw = Terminal(name="IF")
elif_kw = Terminal(name="ELIF")
else_kw = Terminal(name="ELSE")
while_kw = Terminal(name="WHILE")
for_kw = Terminal(name="FOR")
print_kw = Terminal(name="PRINT")
plus = Terminal(name="PLUS")
minus = Terminal(name="MINUS")
divide = Terminal(name="DIVIDE")
multiply = Terminal(name="MULTIPLY")
power = Terminal(name="POWER")
identifier = Terminal(name="IDENTIFIER")
let = Terminal(name="LET")
assign = Terminal(name="ASSIGN")
return_kw = Terminal(name="RETURN")


# NON TERMINAL

START = NonTerminal(name="START")
STATEMENTS = NonTerminal(name="STATEMENTS",)
STATEMENT = NonTerminal(name="STATEMENT",)
ANOTHER_STATEMENT = NonTerminal(name="ANOTHER_STATEMENT",)
IDENTIFIER_REF = NonTerminal(name="FUNCTION_REF",)
FUNCTION_DEF = NonTerminal(name="FUNCTION_DEF",)
FUNCTION_CALL = NonTerminal(name="FUNCTION_CALL",)
IF_BLOCK = NonTerminal(name="IF_BLOCK")
IF_BLOCK_CONTINUE = NonTerminal(name="IF_BLOCK_CONTINUE")
IF = NonTerminal(name="IF")
ELIF = NonTerminal(name="ELIF")
ELIF_CONTINUE = NonTerminal(name="ELIF_CONTINUE")
ELSE = NonTerminal(name="ELSE")
EXPRESSION = NonTerminal(name="EXPRESSION")
FOR_BLOCK = NonTerminal(name="FOR_BLOCK")
WHILE_BLOCK = NonTerminal(name="WHILE_BLOCK")
VAR_DEF = NonTerminal(name="VAR_DEF")
VAR_REF = NonTerminal(name="VAR_REF")
EXPRESSION = NonTerminal(name="EXPRESSION")
ARGUMENTS = NonTerminal(name="ARGUMENTS")
ARGUMENT = NonTerminal(name="ARGUMENT")
ANOTHER_ARGUMENT = NonTerminal(name="ANOTHER_ARGUMENT")
OPERATOR = NonTerminal(name="OPERATOR")
CALL = NonTerminal(name="CALL")
TERM = NonTerminal(name="TERM")
FACTOR = NonTerminal(name="FACTOR")
TERM_OPERATOR = NonTerminal(name="TERM_OPERATOR")
FACTOR_OPERATOR = NonTerminal(name="FACTOR_OPERATOR")
OUTPUT = NonTerminal(name="OUTPUT")
ARGUMENTS_DEF = NonTerminal(name="ARGUMENTS_DEF")
ARGUMENT_DEF = NonTerminal(name="ARGUMENT_DEF")
ANOTHER_ARGUMENT_DEF = NonTerminal(name="ANOTHER_ARGUMENT_DEF")
RETURN_STATEMENT = NonTerminal(name="RETURN_STATEMENT")
RETURN_VALUE = NonTerminal(name="RETURN_VALUE")
VAR_ASSIGN = NonTerminal(name="VAR_ASSIGN")

PRODUCTION_RULES = [
    ProductionRule(START, [STATEMENTS]),
    ProductionRule(STATEMENTS, [STATEMENT, STATEMENTS]),
    ProductionRule(STATEMENTS, [Epsilon()]),
    ProductionRule(ANOTHER_STATEMENT, [STATEMENTS]),
    ProductionRule(STATEMENT, [VAR_DEF, semi_colon]),
    ProductionRule(STATEMENT, [VAR_ASSIGN, semi_colon]),
    ProductionRule(STATEMENT, [IF_BLOCK]),
    ProductionRule(IF_BLOCK, [IF, IF_BLOCK_CONTINUE]),
    ProductionRule(IF_BLOCK_CONTINUE, [Epsilon()]),
    ProductionRule(IF_BLOCK_CONTINUE, [ELSE]),
    ProductionRule(IF_BLOCK_CONTINUE, [ELIF, IF_BLOCK_CONTINUE]),
    # loops
    ProductionRule(STATEMENT, [FOR_BLOCK]),
    ProductionRule(
        FOR_BLOCK,
        [
            for_kw,
            left_paren,
            VAR_DEF,
            semi_colon,
            EXPRESSION,
            semi_colon,
            STATEMENT,
            right_paren,
            left_curly,
            STATEMENTS,
            right_curly,
        ],
    ),
    ProductionRule(STATEMENT, [WHILE_BLOCK]),
    ProductionRule(
        WHILE_BLOCK,
        [
            while_kw,
            left_paren,
            EXPRESSION,
            right_paren,
            left_curly,
            STATEMENTS,
            right_curly,
        ],
    ),
    # function definitions
    ProductionRule(STATEMENT, [FUNCTION_DEF]),
    ProductionRule(
        FUNCTION_DEF,
        [
            func_kw,
            identifier,
            left_paren,
            ARGUMENTS_DEF,
            right_paren,
            left_curly,
            STATEMENTS,
            right_curly,
        ],
    ),
    # expressions
    # ProductionRule(STATEMENT, [EXPRESSION, semi_colon]),
    ProductionRule(EXPRESSION, [TERM, TERM_OPERATOR]),
    ProductionRule(TERM_OPERATOR, [plus, EXPRESSION]),
    ProductionRule(TERM_OPERATOR, [minus, EXPRESSION]),
    ProductionRule(TERM_OPERATOR, [Epsilon()]),
    ProductionRule(TERM, [FACTOR, FACTOR_OPERATOR]),
    ProductionRule(FACTOR_OPERATOR, [multiply, TERM]),
    ProductionRule(FACTOR_OPERATOR, [divide, TERM]),
    ProductionRule(FACTOR_OPERATOR, [Epsilon()]),
    ProductionRule(FACTOR, [left_paren, EXPRESSION, right_paren]),
    ProductionRule(FACTOR, [integer]),
    ProductionRule(FACTOR, [VAR_REF]),
    ProductionRule(VAR_REF, [identifier, CALL]),
    ProductionRule(CALL, [left_paren, ARGUMENTS, right_paren]),
    ProductionRule(CALL, [Epsilon()]),
    ProductionRule(VAR_DEF, [let, identifier, assign, EXPRESSION]),
    ProductionRule(VAR_ASSIGN, [identifier, assign, EXPRESSION]),
    # passing function arguments
    ProductionRule(ARGUMENTS, [ARGUMENT, ANOTHER_ARGUMENT]),
    ProductionRule(ARGUMENT, [EXPRESSION]),
    ProductionRule(ARGUMENTS, [Epsilon()]),
    ProductionRule(ANOTHER_ARGUMENT, [comma, ARGUMENTS]),
    ProductionRule(ANOTHER_ARGUMENT, [Epsilon()]),
    # declaring function arguments
    ProductionRule(ARGUMENTS_DEF, [ARGUMENT_DEF, ANOTHER_ARGUMENT_DEF]),
    ProductionRule(ARGUMENT_DEF, [identifier]),
    ProductionRule(ARGUMENTS_DEF, [Epsilon()]),
    ProductionRule(ANOTHER_ARGUMENT_DEF, [comma, ARGUMENTS_DEF]),
    ProductionRule(ANOTHER_ARGUMENT_DEF, [Epsilon()]),
    # conditionals
    ProductionRule(
        IF,
        [
            if_kw,
            left_paren,
            EXPRESSION,
            right_paren,
            left_curly,
            STATEMENTS,
            right_curly,
        ],
    ),
    ProductionRule(
        ELIF,
        [
            elif_kw,
            left_paren,
            EXPRESSION,
            right_paren,
            left_curly,
            STATEMENTS,
            right_curly,
        ],
    ),
    ProductionRule(ELSE, [else_kw, left_curly, STATEMENTS, right_curly]),
    # IO
    ProductionRule(STATEMENT, [OUTPUT]),
    ProductionRule(OUTPUT, [print_kw, left_paren, EXPRESSION, right_paren, semi_colon]),
    # return
    ProductionRule(STATEMENT, [RETURN_STATEMENT, semi_colon]),
    ProductionRule(RETURN_STATEMENT, [return_kw, RETURN_VALUE]),
    ProductionRule(RETURN_VALUE, [EXPRESSION]),
    ProductionRule(RETURN_VALUE, [Epsilon()]),
]
