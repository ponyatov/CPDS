## metaL core

import os,sys

## Marvin Minsky extended frame model

class Frame:
    def __init__(self, V):
        self.type = self.__class__.__name__.lower()
        self.val = V
        self.slot = {}
        self.nest = []

    ## dump

    def __repr__(self):
        return self.dump()
    def dump(self, depth=0, prefix=''):
        tree = self._pad(depth) + self.head(prefix)
        for i in self.slot:
            tree += self.slot[i].dump(depth+1,prefix=i+' = ')
        for j in self.nest:
            tree += j.dump(depth+1)
        return tree
    def head(self,prefix=''):
        return '%s<%s:%s> @%x' % (prefix,self.type,self._val(),id(self))
    def _pad(self,depth):
        return '\n' + '\t' * depth
    def _val(self):
        return '%s' % self.val

    ## operators

    def __getitem__(self,key):
        return self.slot[key]
    def __setitem__(self,key,that):
        self.slot[key] = that ; return self
    def __lshift__(self,that):
        self[that.val] = that ; return self
    def __floordiv__(self,that):
        self.nest.append(that) ; return self

    ## stack

    def pop(self):
        return self.nest.pop(-1)
    def top(self):
        return self.nest[-1]
    def dropall(self):
        self.nest = [] ; return self

    ## evan & convert

    def eval(self,ctx):
        ctx // self

    def plot(self,depth=0,parent=None,link=None):
        tree = ''
        if parent: par = ', parent:0x%x ' % id(parent)
        else: par = ''
        if link: par += ', link:"%s" ' % link
        tree += '{ key:0x%x, node:"%s:%s" %s },\n' % (id(self), self.type,self._val(), par)
        for i in self.slot:
            tree += self.slot[i].plot(depth+1,parent=self,link=i)
        return tree

# print( Frame('Hello') // Frame('World') << Frame('shifted') )

## Primitives

class Prim(Frame): pass
class Sym(Prim): pass
class Str(Prim): pass

## Active

class Active(Frame): pass

class Cmd(Active):
    def __init__(self,F):
        Active.__init__(self, F.__name__)
        self.fn = F
    def eval(self,ctx):
        self.fn(ctx)

class VM(Active):
    def __setitem__(self,key,F):
        if callable(F): self[key] = Cmd(F) ; return self
        else: Active.__setitem__(self,key,F)
    def __lshift__(self,F):
        if callable(F): return self << Cmd(F)
        else: return Active.__lshift__(self,F)

## FORTH machine

vm = VM('metaL')

## debug

def Q(ctx): print(ctx)
vm['?'] = Q

## stack

def DOT(ctx): ctx.dropall()
vm['.'] = DOT

## manipulations

def EQ(ctx): addr = ctx.pop().val ; ctx[addr] = ctx.pop()
vm['='] = EQ

## no-syntax lexer

import ply.lex as lex

tokens = ['sym','str']

t_ignore = '[ \t\r\n]+'

states = (('str','exclusive'),)

t_str_ignore = ''
def t_str(t):
    r"'"
    t.lexer.push_state('str') ; t.lexer.string = ''
def t_str_str(t):
    r"'"
    t.lexer.pop_state() ; return Str(t.lexer.string)
def t_str_any(t):
    r"."
    t.lexer.string += t.value

def t_sym(t):
    r'[`]|[^ \t\r\n]+'
    return Sym(t.value)

def t_ANY_error(t):
    raise SyntaxError(t)

## interpreter

def QUOTE(ctx): WORD(ctx)
vm['`'] = QUOTE

def WORD(ctx):
    token = ctx.lexer.token()
    if token: ctx // token
    return token

def FIND(ctx):
    token = ctx.pop()
    try: ctx // ctx[token.val] ; return True
    except KeyError: ctx // token ; return False

def EVAL(ctx):
    ctx.pop().eval(ctx)

def INTERP(ctx):
    ctx.lexer = lex.lex() ; ctx.lexer.input(ctx.pop().val)
    while True:
        if not WORD(ctx): break
        if isinstance(ctx.top(),Sym):
            if not FIND(ctx): raise SyntaxError(ctx)
        EVAL(ctx)

## Web

class IO(Frame): pass
class Net(IO): pass
class IP(Net): pass
class Port(Net): pass
class Web(Net):
    flask = __import__('flask')
    def __init__(self,V):
        Net.__init__(self,V)
        self['ip'] = IP('127.0.0.1')
        self['port'] = Port(8888)
    def eval(self,ctx):
        from flask import Flask,render_template
        app = Flask(self.val)
        app.config['SECRET_KEY'] = os.urandom(32)

        @app.route('/')
        def index(): return render_template('index.html',ctx=ctx)

        @app.route('/<path>.js')
        def jslib(path): return app.send_static_file(path + '.js')

        app.run(host=self['ip'].val,port=self['port'].val,debug=True)

def WEB(ctx): ctx['WEB'] = Web(ctx.val) ; ctx['WEB'].eval(ctx)
vm << WEB

if __name__ == '__main__':
    vm // Str(open(sys.argv[0][:-3]+'.ini').read())
    INTERP(vm)
