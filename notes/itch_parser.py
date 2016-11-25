import re
import inspect
from ply import lex
from ply import yacc
from area51.namd.base import NamdObject

class name(str):
    pass

class StringThing(NamdObject):
    def __init__(self, arg : name):
        super().__init__(arg)

class IntThing(NamdObject):
    def __init__(self, arg : int):
        super().__init__(arg)

classes = [ StringThing, IntThing ]

tokens = ('name', 'int') + tuple(c.__name__ for c in classes)
t_ignore = r' '
t_name = r'[a-zA-Z_][a-zA-Z0-9_]*'
def t_int(t):
    r'\d+'
    t.value = int(t.value)
    return t

# tagged clas
re_notag = re.compile('[^A-Z0-9]')

def make_rules(c):
    # build lexer token for class name
    def t_make(t):
        t.value = c
        return t
    t_make.__doc__ = re_notag.sub('', c.__name__)

    sig = inspect.signature(c.__init__)
    def p_make(p):
        cls = p[1]
        args = [ x for x in p[2:]]
        p[0] = cls(*args)

    params = list(sig.parameters.values())[1:]
    p_make.__doc__ = 'object : ' + c.__name__ + ' ' + ' '.join(p.annotation.__name__ for p in params)
    print(p_make.__doc__)
    return {
        't_' + c.__name__ : t_make,
        'p_' + c.__name__ : p_make
    }


for c in classes:
    globals().update(make_rules(c))

lexer = lex.lex(debug=True)
parser = yacc.yacc(debug=True)

def from_string(value):
    # Give the lexer some input
    lexer.input(value)

    # # Tokenize
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break  # No more input
    #     print(tok)

    return parser.parse(value)

def test_from_string():
    # build some parser
    thing = from_string('ST abc')
    assert isinstance(thing, StringThing)
    assert thing.__args__ == ('abc',)


    thing = from_string('IT 123')
    assert isinstance(thing, IntThing)
    assert thing.__args__ == (123, )

    thing = from_string('IT abc')




