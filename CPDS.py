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

    def __setitem__(self,key,that):
        self.slot[key] = that ; return self
    def __lshift__(self,that):
        self[that.val] = that ; return self
    def __floordiv__(self,that):
        self.nest.append(that) ; return self

# print( Frame('Hello') // Frame('World') << Frame('shifted') )

## Primitives

class Prim(Frame): pass
class Sym(Prim): pass
class Str(Prim): pass

## Active

class Active(Frame): pass
class Cmd(Active): pass
class VM(Active): pass

## FORTH machine

vm = VM('metaL')

## no-syntax lexer

import ply.lex as lex

tokens = ['sym','str']

t_ignore = '[ \t\r\n]+'

def t_sym(t):
    r'[^ \t\r\n]+'
    return Sym(t.value)

def t_error(t):
    raise SyntaxError(t)

## interpreter

def INTERP(ctx):
    ctx.lexer = lex.lex() ; ctx.lexer.input(ctx.pop().val)
    while True:
        print(vm)
        if not WORD(ctx): break

if __name__ == '__main__':
    vm // Str(open(sys.argv[0][:-3]+'.ini').read())
    INTERP(vm)
