class InstatASTNode(object):
    def __init__(self, name, children_list=None):
        self.name = name
        self.children = children_list

    def add_child(self, child_node):
        if not self.children:
            self.children = []
        self.children.append(child_node)

    def add_children(self, children_list):
        if not self.children:
            self.children = []
        for child in children_list:
            self.children.append(child)

    def find_child(self, name):
        for child in self.children:
            if child.name == name:
                return child

    def traverse(self, i):
        temp = str(self.name)
        if not self.children:
            temp = ': ' + str(self.name)
        s = temp + '\n'
        if self.children:
            for child in self.children:
                s += '-'*(i-1) + '>' + child.traverse(i+1)
        return s

    def __str__(self):
        return '%s\n' % self.traverse(1)

# x = f(y+1) + 2
equals = InstatASTNode('=')
x = InstatASTNode('x')
plus = InstatASTNode('+')
plus1 = InstatASTNode('+')
two = InstatASTNode(2)
one = InstatASTNode(1)
func = InstatASTNode('function')
f = InstatASTNode('f')
y = InstatASTNode('y')
equals.add_children([x, plus])
plus.add_children([func, two])
func.add_children([f, plus1])
plus1.add_children([y, one])
print equals