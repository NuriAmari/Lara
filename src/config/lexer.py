from langtools.lexer.nfa import Atom, Concat, Epsilon, KleeneStar, Union
from langtools.lexer.dfa import DFA
from langtools.lexer.basic_symbols import (
    DIGITS,
    NON_ZERO_DIGITS,
    ALPHABET,
    UPPERCASE_ALPHABET,
)

from src.config.tokens import (
    AssignToken,
    CommaToken,
    CompareToken,
    DivideToken,
    ElseToken,
    ElifToken,
    ForToken,
    FuncToken,
    GreaterEqualToken,
    GreaterToken,
    IdentifierToken,
    IfToken,
    IntegerToken,
    LeftCurlyToken,
    LeftParenToken,
    LessEqualToken,
    LessToken,
    LetToken,
    MinusToken,
    MultiplyToken,
    PlusToken,
    PowerToken,
    PrintToken,
    RightCurlyToken,
    RightParenToken,
    SemiColonToken,
    WhileToken,
)

# LITERALS

INTEGER = Concat(
    Union(Atom("-"), Epsilon()),
    Concat(Union(*NON_ZERO_DIGITS), KleeneStar(Union(*DIGITS))),
)
INTEGER.add_token(IntegerToken)

# OPERATORS

PLUS = Atom("+")
MINUS = Atom("-")
MULTIPLY = Atom("*")
POWER = Concat(Atom("*"), Atom("*"))
DIVIDE = Atom("/")

PLUS.add_token(PlusToken)
MINUS.add_token(MinusToken)
MULTIPLY.add_token(PowerToken)
POWER.add_token(PowerToken)
DIVIDE.add_token(DivideToken)

ASSIGN = Atom("=")
COMPARE = Concat(Atom("="), Atom("="))
LESS = Atom("<")
LESS_EQUAL = Concat(Atom("<"), Atom("="))
GREATER = Atom(">")
GREATER_EQUAL = Concat(Atom(">"), Atom("="))

ASSIGN.add_token(AssignToken)
COMPARE.add_token(CompareToken)
LESS.add_token(LessToken)
LESS_EQUAL.add_token(LessEqualToken)
GREATER.add_token(GreaterToken)
GREATER_EQUAL.add_token(GreaterEqualToken)

# IDENTIFIERS

IDENTIFIER = Concat(
    Union(*ALPHABET, *UPPERCASE_ALPHABET, Atom("_")),
    KleeneStar(Union(*ALPHABET, *UPPERCASE_ALPHABET, *DIGITS, Atom("_"))),
)

IDENTIFIER.add_token(IdentifierToken)

# CONTROL FLOW

IF = Concat(Atom("i"), Atom("f"))
WHILE = Concat(Atom("w"), Atom("h"), Atom("i"), Atom("l"), Atom("e"))
ELSE = Concat(Atom("e"), Atom("l"), Atom("s"), Atom("e"))
ELIF = Concat(Atom("e"), Atom("l"), Atom("i"), Atom("f"))
FUNC = Concat(Atom("f"), Atom("u"), Atom("n"), Atom("c"))
FOR = Concat(Atom("f"), Atom("o"), Atom("r"))

IF.add_token(IfToken)
WHILE.add_token(WhileToken)
ELSE.add_token(ElseToken)
ELIF.add_token(ElifToken)
FUNC.add_token(FuncToken)
FOR.add_token(ForToken)

# PUNCTUATION

SEMI_COLON = Atom(";")
LEFT_CURLY = Atom("{")
RIGHT_CURLY = Atom("}")
LEFT_PAREN = Atom("(")
RIGHT_PAREN = Atom(")")
COMMA = Atom(",")

SEMI_COLON.add_token(SemiColonToken)
LEFT_CURLY.add_token(LeftCurlyToken)
RIGHT_CURLY.add_token(RightCurlyToken)
LEFT_PAREN.add_token(LeftParenToken)
RIGHT_PAREN.add_token(RightParenToken)
COMMA.add_token(CommaToken)

# MISCELANEOUS KEYWORDS

PRINT = Concat(Atom("p"), Atom("r"), Atom("i"), Atom("n"), Atom("t"))
PRINT.add_token(PrintToken)

LET = Concat(Atom("l"), Atom("e"), Atom("t"))
LET.add_token(LetToken)


TOKENIZER = DFA(
    Union(
        INTEGER,
        PLUS,
        MINUS,
        MULTIPLY,
        POWER,
        DIVIDE,
        IDENTIFIER,
        IF,
        WHILE,
        ELSE,
        ELIF,
        FUNC,
        FOR,
        SEMI_COLON,
        LEFT_CURLY,
        RIGHT_CURLY,
        LEFT_PAREN,
        RIGHT_PAREN,
        COMMA,
        PRINT,
        close=False,
    )
)
