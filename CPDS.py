class Frame:
    def __init__(self, V):
        self.type = self.__class__.__name__.lower()
        self.val = V
        self.slot = {}
        self.nest = []

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
