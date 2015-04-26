import ply.yacc as yacc
from compiler import ast, misc

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

# Get the token map from the lexer.  This is required.
from instatLex import *
from codeGenerator import *

class Node(object):
    """ Node class. Used to build the AST. Each node has a type,
    children and a leaf.
    """
    # Function to initialize the node, needs type, the rest is
    # optional.
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf
    
    # Function to print out the tree.
    def __str__(self):
        return "\n" + self.traverse(1)
    # Function to traverse the tree and print it out.
    def traverse(self, i):
        temp = ""
        if self.leaf:
            temp = ": " + `self.leaf`
        s = self.type + temp + "\n"
        for children in self.children:
            if isinstance(children, Node):
                s += "-"*(i-1) + ">" + children.traverse(i+1)
            else:
                s += "-"*(i-1) + ">" + children
        return s

def p_program(p):
    """ program : external_declaration
                | program external_declaration
    """
    if len(p) == 2:
        p[0] = Node("program", [p[1]])
    else:
        p[0] = Node("program", [p[1], p[2]])

def p_external_declaration(p):
    """ external_declaration : statement"""
    p[0] = Node("external_declaration", [p[1]])


def p_statement_list(p):
    """ statement_list : statement
                       | statement_list statement
    """
    if len(p) == 2:
        p[0] = Node("statement_list", [p[1]])
    else:
        p[0] = Node("statement_list", [p[1], p[2]])

# Add types of statements here, e.g. selection, iteration, etc!
def p_statement(p):
    """ statement : assignment_statement SEMICOLON
                  | print_statement SEMICOLON
                  | for_statement 
                  | iteration_statement 
                  | selection_statement 
                  | statement
    """
    #maybe add | list_change NEWLINE
    p[0] = Node("statement", [p[1]])
    #print p[0]

def p_for_statement(p):
    """ for_statement : FOR ID IN or_expression TO or_expression COLON  LBRACK statement RBRACK
    """
    p[0] = Node("for_statement", [p[4], p[6], p[10]], p[2])
    #print p[0]

def p_iteration_statement(p):
    """ iteration_statement : WHILE or_expression LBRACK statement_list RBRACK
    """
    p[0] = Node("iteration_statement", [p[2], p[4]])
    #print p[0]

def p_selection_statement(p):
    """ selection_statement : IF or_expression LBRACK statement_list RBRACK
                            | IF or_expression LBRACK statement_list RBRACK ELSE LBRACK statement_list RBRACK
    """
    if len(p) == 5:
        p[0] = Node("selection_statement", [p[2], p[4]])
    else:
        p[0] = Node("selection_statement", [p[2], p[4], p[8]]) #i dont know if this is even right


def p_print_statement(p):
    """ print_statement : PRINT LPAREN or_expression RPAREN
    """
    p[0] = Node("print_statement", [p[3]])

# is this correct?? need to fix according to grammar... Remember to fix the one below it too!
def p_assignment_statement(p):
    """ assignment_statement : ID EQUALS or_expression"""
    
    p[0] = Node("assignment_statement", [p[3]], p[1])

def p_or_expression(p):
    """ or_expression : and_expression"""
    if len(p) == 2:
        p[0] = Node("or_expression", [p[1]])
    else:
        p[0] = Node("or_expression", [p[1], p[3], p[2]])


def p_and_expression(p):
    """ and_expression : equality_expression"""
    if len(p) == 2:
        p[0] = Node("and_expression", [p[1]])
    else:
        p[0] = Node("and_expression", [p[1], p[3], p[2]])

def p_equality_expression(p):
    """ equality_expression : relational_expression"""
    if len(p) == 2:
        p[0] = Node("equality_expression", [p[1]])
    else:
        p[0] = Node("equality_expression", [p[1], p[3], p[2]])

def p_relational_expression(p):
    """ relational_expression : during_or_expression"""
    if len(p) == 2:
        p[0] = Node("relational_expression", [p[1]])
    else:
        p[0] = Node("relational_expression", [p[1], p[3], p[2]])

#maybe put during things here.... need to not allow above cases for during in the grammar!!
def p_during_or_expression(p):
    """during_or_expression : during_and_expression"""
#                            | LPAREN during_or_expression RPAREN DURING during_and_expression"""
    if len(p) == 2:
        p[0] = Node("during_or_expression", [p[1]])
    else:
        p[0] = Node("during_or_expression", [p[1],p[3]])
#    else:
#        p[0] = Node("during_and_expression", [p[2],p[5]]) #need to write the code gen for this case

#can do something like(TUESDAY, JANUARY DURING WEDNESDAY) DURING 4:30 PM TO 5:30 PM
#could it do this too (TUESDAY, (WEDS, FRIDAY) DURING 4:30 PM TO 5:30 PM) DURING 4:30 PM TO 5:30 PM??
def p_during_and_expression(p):
    """ during_and_expression : additive_expression
                        | during_and_expression DURING additive_expression """

    if len(p) == 2:
        p[0] = Node("during_and_expression", [p[1]])
    elif len(p) == 4:
        p[0] = Node("during_and_expression", [p[1],p[3]])

        
def p_additive_expression(p):
    """ additive_expression : multiplicative_expression
    """
    if len(p) == 2:
        p[0] = Node("additive_expression", [p[1]])
    else:
        p[0] = Node("additive_expression", [p[1], p[3], p[2]])

# Change to continue sequence in grammar i.e. function_expression, etc
def p_multiplicative_expression(p):
    """ multiplicative_expression : power_expression
    """
    if len(p) == 2:
        p[0] = Node("multiplicative_expression", [p[1]])
    else:
        p[0] = Node("multiplicative_expression", [p[1], p[3], p[2]])

def p_power_expression(p):
    """ power_expression : to_expression
    """
    if len(p) == 2:
        p[0] = Node("power_expression", [p[1]])
    else:
        p[0] = Node("power_expression", [p[1], p[3], p[2]])

def p_to_expression(p):
    """ to_expression : primary_expression
    """
    if len(p) == 2:
        p[0] = Node("to_expression", [p[1]])
    else:
        p[0] = Node("to_expression", [p[1], p[3]])
 
def p_primary_expression(p):
    """ primary_expression : ID
    """
    if len(p) == 2:
        p[0] = Node('primary_expression', [], p[1])
    else:
        p[0] = Node('primary_expression', [p[2]])    


def p_primary_expression_boolean(p):
    """ primary_expression : TRUE
                            | FALSE"""
    p[0] = Node('primary_expression_boolean', [], p[1])

def p_primary_expression_string(p):
    """ primary_expression : STRING
    """
    p[0] = Node('primary_expression_string', [], p[1])

def p_primary_expression_constant(p):
    """ primary_expression : CONSTANT
    """
    p[0] = Node('primary_expression_constant', [], p[1])

# Error rule for syntax errors
def p_error(p):    
    if hasattr(p, 'lineno'):
        sys.exit("Syntax error in input! at line: "+ str(p.lineno))
    else:
        sys.exit("Syntax error in input!")
    
# wrap default parser into instat parser
class instatParser(object):
    def __init__(self, lexer = None):
        if lexer is None:
            lexer = instatLexer()
        self.lexer = lexer
        self.parser = yacc.yacc()

    def parse(self, code):
        code = code + '\n'
        self.lexer.input(code)
        result = self.parser.parse(lexer = self.lexer)
        # print result
        return result
        # return ast.Module(None, result)

if __name__ == '__main__':

    # Build the parser
    parser = instatParser()


    s = '''
'''


    result = parser.parse(s)

    # ## Prints the AST
    print result
    code = codeGenerator(result)
    # Prints the actual program
    print code.ret

    ## Makes the output file
    f = open("out.py", 'w')
    f.write(code.ret)
    print 'Done!\nCheck "out.py"'
