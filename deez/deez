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

HEADER = """
#include <iostream>
#include <functional>
#include <vector>
#include <cassert> 

using namespace std;

class var{
    public:
        int type;
        float f;
        std::vector<var> __iter__;
        std::string s;
        std::function<var(var)> __exec__;

        var* _keys;
        var* _values;
        /*
        TYPEID | TYPE
        0 NULL
        1 INT   //removed, everything is a float
        2 FLOAT
        3 STRING
        4 BOOL
        5 LIST
        6 FUNCTION
        */

        explicit var(int x, int t){
            this->type = t;
            this->f = (float)x;
        }

        explicit var(int x){
            this->type = 2;
            this->f = (float)x;
        }

        explicit var(float x){
            this->type = 2;
            this->f = (float)x;
        }

        explicit var(std::string s){
            this->type = 3;
            this->s = s;
        }

        explicit var(std::function<var(var)> f){
            this->type = 6;
            this->__exec__ = f;

        }
        
        explicit var(bool x){
            this->type = 4;
            this->f = (int)x;
        }
        

        explicit var(std::initializer_list<var> arr){

            for(var i: arr){
                this->__iter__.push_back(i);
            }
            this->type = 5;

        }

        std::string __repr__(){
            if     (this->type == 0){return "null";}                       // null
            //else if(this->type == 1){return std::to_string((int)this->f);} // int
            else if(this->type == 2){                                      // int / float
                if( this->f == ((int)(float)this->f)){
                    return std::to_string((int)this->f);    
                }
                return std::to_string(this->f);
            }
            else if(this->type == 3){return this->s;}                      // string
            else if(this->type == 4){return std::to_string((bool)this->f);}// bool
            else if(this->type == 6){return "<function>";}                 // func
            else if(this->type == 5){
                string o = "[";
                for( var i:__iter__ ){
                    o = o + i.__repr__() + ", ";
                }o.pop_back();o.pop_back();
                return o+"]";
            }                                                              // list[]
            else{return "unknown type "+std::to_string(this->type);}       // *unknown
        }

        var __getitem__(var x, var y = var(0,0)){
            if(this->type == 5 && x.type == 2){
                if(x.f < this->__iter__.size()){
                    return this->__iter__.at((int)x.f);
                }return y;
            }return var(0, 0);
        }

        var __setitem__(var x, var v){
            if(this->type == 5 && x.type == 1){
                if((int)x.f < this->__iter__.size()){
                    this->__iter__[(int)x.f] = v;
                }
            }return var(0, 0);
        }

        /*
        var __getattr__(var attr){
            assert(attr.type == 3);
            int c =0;
            for (auto i = this->_keys->__iter__.begin(); i != this->_keys->__iter__.end(); ++i){
                if( i->s == attr.s){
                    break;
                }
                c++;
            }
            assert(c < this->_keys->__iter__.size());
            return this->_values->__iter__[c];
        }
        var __setattr__(var attr, var val){
            assert(attr.type == 3);
            int c =0;
            for (auto i = this->_keys->__iter__.begin(); i != this->_keys->__iter__.end(); ++i){
                if( i->s == attr.s){
                    break;
                }
                c++;
            }
            if(c < this->_values->__iter__.size()){
                this->_values->__iter__[c] = val;
            }
            else{
                this->_keys->__iter__.push_back(attr);
                this->_values->__iter__.push_back(val);
            }
            return var(0);
        }*/

        var operator + (var x){return this->__add__(x);}
        var operator - (var x){return this->__sub__(x);}
        var operator * (var x){return this->__mul__(x);}
        var operator < (var x){return this->__lt__(x);}
        var operator > (var x){return this->__gt__(x);}
        var operator % (var x){return this->__mod__(x);}
        var operator == (var x){return this->__eq__(x);}

        var __add__(var x){
            if((this->type==2 || this->type==1) && (x.type==2 || x.type==1)){
                if(this->type==1 || x.type==1){
                    return var((int)(x.f + this->f));
                }
                else{
                    return var(x.f + this->f);  
                }
            }
            else{
                return var(0, 0);
            }
        }

        var __sub__(var x){
            if((this->type==2 || this->type==1) && (x.type==2 || x.type==1)){
                if(this->type==1 || x.type==1){
                    return var((int)(this->f - x.f));
                }
                else{
                    return var(this->f - x.f);  
                }
            }
            else{
                return var(0, 0);
            }
        }

        var __mul__(var x){
            if((this->type==2 || this->type==1) && (x.type==2 || x.type==1)){
                if(this->type==1 || x.type==1){
                    return var((int)(this->f * x.f));
                }
                else{
                    return var(this->f * x.f);  
                }
            }
            else{
                return var(0, 0);
            }
        }

        var __eq__(var x){
            if(this->type == x.type){
                //cout<<this->f<<"=="<<x.f<<" ->"<< (this->f==x.f) <<endl;
                return var( this->f == x.f );
            }
            return var(0, 0);
        }

        var __lt__(var x){
            if(this->type == x.type){
                return var(this->f < x.f);
            }return var(0, 0);
        }

        var __gt__(var x){
            if(this->type == x.type){
                return var(this->f > x.f);
            }return var(0, 0);  
        }

        var __mod__(var x){
            if(this->type == x.type){
                float a = (float)this->f;
                float b = (float)x.f;
                float mod = a < 0 ? -a : a;

                while(mod >= b){
                    mod = mod - b;
                }
                return a < 0 ? var(-mod) : var(mod);
            }return var(0, 0);
        }

        operator bool(){
            return (bool)(this->f)||(bool)(this->s.size())||this->__iter__.size();
        }

};


void print(var x){
    for(var i: x.__iter__){
        cout<<i.__repr__()<<" ";
    }
    cout<<endl;
}

var input(var a){
    var x = a.__iter__[0];
    std::string v;
    cout<< x.__repr__();
    cin >> v;
    return var(v);
}
var repr(var x){
    return var(x.__repr__());
}

int main(){
    %%main
}
"""

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
        
        compiled = HEADER.replace('%%main', compiled)
        with open('.temp.cpp', 'w') as f:
            f.write(compiled)

    if not '-r' in sys.argv:
         os.system('g++ -o main .temp.cpp && rm .temp.cpp && ./main')

compile( sys.argv[1] )