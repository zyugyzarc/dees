#!/bin/python3
import re
import os
import sys

class Token:
    def __init__(self, type, value):
        self.t = type
        self.v = value
    def __repr__(self):
        return f'token<{repr(self.t)}, {repr(self.v)}>'

class Parser:
    def __init__(self):
        self.tokens={
            "__CTX,(,)" : "CONTEXT_()",
            "__CTX,[,]" : "CONTEXT_[]",
            "__CTX,{,}" : "CONTEXT_{}",
            "__CTX,/*,*/" : "CONTEXT_//",
            "([\"'])(.*?)\\1" : "LITERAL_S",
            "\\n" : "LINE_END",
            ";"   : "LINE_END",
            "[,]" : "SEPARATOR",
            "[.]" : "SEPARATOR",  # TEMPORARY CHANGE, get __getattr__ and __setattr__ working, with __dict__
            "[-][>]" : "FUNC_DEF",
            "[=][=]":"OPERATOR",
            '[=]' : "ASSIGN",
            "[+]" : "OPERATOR",
            "[-]" : "OPERATOR",
            "[/]" : "OPERATOR",
            "[**]" : "OPERATOR",
            "[*]" : "OPERATOR",
            "[<]" : "OPERATOR",
            "[%]" : "OPERATOR",
            "and" : "OPERATOR",
            "or" : "OPERATOR",
            "not" : "OPERATOR",
            "if" : "KEYWORD",
            "while" : "KEYWORD",
            "for" : "KEYWORD_FOR",
            "else if" : "KEYWORD",
            "else" : "KEYWORD",
            "return" : "KEYWORD",
            "[0-9.]+" : "LITERAL_N",
            "null" : "LITERAL_NULL",
            "[a-zA-Z0-9_]+" : "IDENTIFIER"
        }

        self.BUILTINS = [
            "input", "print"
        ]

    def _tokenize(self, code):
        self.code = code
        token_tree = []
        i = 0
        while i < len(self.code):
            l, value, type = self.search_token(i)
            if type:
                if type.startswith("CONTEXT"):
                    token_tree.append( Token( type, self._tokenize(value[1:]) ))
                    self.code = code
                elif type == 'LITERAL_S':
                    token_tree.append( Token(type, value[1:-1]))
                else:
                    token_tree.append( Token(type, value))
            i += l
        return token_tree

    def tokenize(self, code):
        self.token_tree = self._tokenize(code + '\n')

    def search_token(self, pos):
        for t in self.tokens:
            v = self.check_token(t, pos)
            if v:
                return len(v), v, self.tokens[t]
        return 1, 0, 0

    def check_token(self, token, pos):
        
        if token.startswith('__CTX'):

            s, e = token.split(',')[1], token.split(',')[2]
            if s != e:
                c,i = 0, 0
                while i < len(self.code[pos:]):
                    if self.code[pos+i] == s: c += 1
                    if self.code[pos+i] == e: c -= 1
                    if c <= 0: break
                    i += 1
                return self.code[ pos:pos+i ]
        else:
            s = re.search( token, self.code[pos:], re.S )
            if s:
                if 0 == s.span()[0]:
                    return s.group()

    def _transcompile(self, tree, var_stack = [], ctx = ''):

        rules = {}
        i = 0
        x = ''
        var_stack = var_stack

        def rule(*args):
            def _(func):
                rules[args]= func
            return _

        def comp(s, _ctx=0):
            # ctx
            # 0 None
            # 1 No ";"
            return self._transcompile(s, var_stack, _ctx or ctx)

        @rule("IDENTIFIER", "CONTEXT_()", "FUNC_DEF", "CONTEXT_{}")
        def func_def(name, args, _, block):
            x = f'var {name} = var(0);\n'\
            f'{name}.__exec__ = (std::function<var(var)>)[=, &{name}](var __args){{' 
            for i, e in enumerate(args):
                if e.t == 'IDENTIFIER':
                    x += f'var {e.v} = __args.__getitem__(var({i}));\n'
                    var_stack.append(e.v)
            return x + comp(block) + ';return var(0,0);}'

        @rule("KEYWORD_FOR", "CONTEXT_()", "CONTEXT_()", "CONTEXT_()", "CONTEXT_{}")
        def for_def(_, i, c, u, block):
            return f"for({comp(i, _ctx=1)}; {comp(c, _ctx=1)}; {comp(u, _ctx=1)}){{\n{comp(block)}\n}}"

        @rule("IDENTIFIER", "ASSIGN")
        def var_assign(v, _):
            if v in var_stack:
                return v+'='
            var_stack.append(v)
            return f'var {v}='

        @rule("IDENTIFIER", "CONTEXT_()")
        def func_call(f, a):
            if f in self.BUILTINS:
                return f'{f}(var({{{comp(a, _ctx=1)}}}))'
            return f'{f}.__exec__(var({{{comp(a, _ctx=1)}}}))'

        @rule("LITERAL_S")
        def string(x):
            return f'var("{x}")'

        @rule("OPERATOR")
        def operator(x):    
            try:
                return {
                    "and" : "&&",
                    "or" : "||",
                    "not" : "!"
                }[x]
            except KeyError:
                return x

        rule('CONTEXT_()')(lambda x:f'({comp(x)})')
        rule('CONTEXT_[]')(lambda x:f'[{comp(x)}]')
        rule('CONTEXT_{}')(lambda x:f'{{{comp(x)}}}')

        rule('LITERAL_S')(lambda x:f'var((std::string)"{x}")')
        rule('LITERAL_N')(lambda x:f'var({x})')
        rule('LINE_END')(lambda x:';\n' if ctx != 1 else '')


        pattern = [j.t for j in tree]
        values = [j.v for j in tree]

        while i < len(pattern):
            l = 1
            #print( pattern[i], repr(values[i]), sep=' | ' )
            for k, v in rules.items():
                if list(k) == pattern[i:i+len(k)]:
                    x += v(*values[i:i+len(k)])
                    l = len(k)
                    break
            else:
                x += str(values[i])
            i += l
        return x

def _compile(filename):
    p = Parser()
    with open(filename) as f:
        p.tokenize( f.read() )
        compiled = p._transcompile(
            p.token_tree
        )
        with open('header.cpp') as f:
            compiled = f.read().replace('%%main', compiled)
            with open('.temp.cpp', 'w') as f:
                f.write(compiled)

    if not '-r' in sys.argv:
         os.system('g++ -o main .temp.cpp && rm .temp.cpp && ./main')

def compile(filename):
    p = Parser()
    with open(filename) as f:
        p.tokenize( f.read() )
        compiled = p._transcompile(
            p.token_tree
        )
        
        with open( os.path.join(os.path.dirname(__file__) ,'header.cpp'), 'r') as h:
            with open('.temp.cpp', 'w') as f:
                f.write(
                        h.read().replace('%%main', compiled)
                    )

    if not '-r' in sys.argv:
         os.system('g++ -o main .temp.cpp && rm .temp.cpp && ./main')

compile( sys.argv[1] )