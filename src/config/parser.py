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


# NON TERMINAL

START = NonTerminal(name="START")
STATEMENTS = NonTerminal(name="STATEMENTS",)
STATEMENT = NonTerminal(name="STATEMENT",)
ANOTHER_STATEMENT = NonTerminal(name="STATEMENTS",)
IDENTIFIER_REF = NonTerminal(name="FUNCTION_REF",)
FUNCTION_DEF = NonTerminal(name="FUNCTION_DEF",)
FUNCTION_CALL = NonTerminal(name="FUNCTION_DEF",)
IF_BLOCK = NonTerminal(name="IF_BLOCK")
IF_BLOCK_CONTINUE = NonTerminal(name="IF_BLOCK_CONTINUE")
IF = NonTerminal(name="IF")
ELSE_IF = NonTerminal(name="ELSE_IF")
ELSE_IF_CONTINUE = NonTerminal(name="ELSE_IF_CONTINUE")
ELSE = NonTerminal(name="ELSE")
CONDITION = NonTerminal(name="CONDITION")
FOR_BLOCK = NonTerminal(name="FOR_BLOCK")
WHILE_BLOCK = NonTerminal(name="WHILE_BLOCK")
VAR_DEF = NonTerminal(name="VAR_DEF")
VAR_REF = NonTerminal(name="VAR_DEF")
EXPRESSION = NonTerminal(name="EXPRESSION")
ARGUMENTS = NonTerminal(name="ARGUMENTS")
OPERATOR = NonTerminal(name="OPERATOR")
CALL = NonTerminal(name="OPERATOR")

PRODUCTION_RULES = [
    ProductionRule(START, [STATEMENTS]),
    ProductionRule(STATEMENTS, [STATEMENT, ANOTHER_STATEMENT]),
    ProductionRule(ANOTHER_STATEMENT, [STATEMENTS, Epsilon()]),
    ProductionRule(STATEMENT, [VAR_DEF]),
    ProductionRule(STATEMENT, [FUNCTION_DEF]),
    ProductionRule(STATEMENT, [IF_BLOCK]),
    ProductionRule(IF_BLOCK, [IF_BLOCK, IF_BLOCK_CONTINUE]),
    ProductionRule(IF_BLOCK_CONTINUE, [Epsilon()]),
    ProductionRule(IF_BLOCK_CONTINUE, [ELSE]),
    ProductionRule(IF_BLOCK_CONTINUE, [ELSE_IF, IF_BLOCK_CONTINUE]),
    ProductionRule(STATEMENT, [FOR_BLOCK]),
    ProductionRule(
        FOR_BLOCK,
        [
            for_kw,
            left_paren,
            VAR_DEF,
            semi_colon,
            CONDITION,
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
            CONDITION,
            right_paren,
            left_curly,
            STATEMENTS,
            right_curly,
        ],
    ),
    ProductionRule(STATEMENT, [FUNCTION_DEF]),
    ProductionRule(
        FUNCTION_DEF,
        [
            func_kw,
            left_paren,
            ARGUMENTS,
            right_paren,
            left_curly,
            STATEMENTS,
            right_curly,
        ],
    ),
    ProductionRule(STATEMENT, [EXPRESSION]),
    ProductionRule(EXPRESSION, [VAR_REF]),
    ProductionRule(VAR_REF, [identifier, OPERATOR]),
    ProductionRule(OPERATOR, [plus]),
    ProductionRule(OPERATOR, [minus]),
    ProductionRule(OPERATOR, [multiply]),
    ProductionRule(OPERATOR, [power]),
    ProductionRule(OPERATOR, [divide]),
    ProductionRule(OPERATOR, [CALL]),
    ProductionRule(OPERATOR, [Epsilon()]),
    ProductionRule(CALL, [left_paren, ARGUMENTS, right_paren]),
    ProductionRule(STATEMENT, [VAR_DEF]),
    ProductionRule(VAR_DEF, [let, identifier, assign, integer]),
]
