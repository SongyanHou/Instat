import traceback
import datetime
import re
import sys
import runtimeError
everys = 0

def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True
#
#if module_exists("RPi.GPIO"):
#    thermoStat = '''
#from r_pi import ThermoStat
#myThermoStat = ThermoStat.Sim_ThermoStat()
#'''
#else:
#    thermoStat = '''
#from r_pi import Fake_ThermoStat
#myThermoStat = Fake_ThermoStat.Fake_ThermoStat()   
#'''



class codeGenerator(object):
    def __init__(self, tree):
        # Keep track of scopes
        self.scopes = [[]]
        self.scopeDepth = 0
        # Symbols table "id" => {type, value}
        self.symbolTable = {}
        # Function parameter type lookup
        self.functionTable = {}
        self.returnTable = {}
        self.returnNumber = 0
        # Variable to store the code
        self.ret = "import datetime\n" 
        self.ret += "import sys\n"
        #self.ret += "every_list = []\n" + "log_file = open('instatLog.txt', 'a')\n"  + thermoStat
        self.ret += "print \"Welcome to instat \\n==================== \"\n"
        body = self.dispatch(tree)
        self.ret += runtimeError.errorBeginning(body)
        self.ret += runtimeError.errorEnd()
        # 
        # Keeps track of the number of every's

    #temporary exit function when exceptions are raised
    def exit(self, exit_msg):
        print exit_msg
        #sys.exit()

    
    def dispatch(self, tree, flag=None):
        '''Dispatches based on type of node'''
        if isinstance(tree, list):
            temp = ""
            for t in tree:
                temp += self.dispatch(t)
            return temp

        method = getattr(self, "_"+tree.type)
        code = method(tree, flag)
        return code

    def dispatchTuple(self, tree, flag=None):
        arg = self.dispatch(tree, flag)
        if type(arg) is tuple:
            arg = arg[1]
        return str(arg)

    def inBlock(self):
        self.scopeDepth += 1
        self.scopes.append([])

    def outBlock(self):
        for variable in self.scopes[self.scopeDepth]:
            del self.symbolTable[variable]
        del self.scopes[self.scopeDepth]
        self.scopeDepth -= 1
        
    def _program(self, tree, flag=None):
        return self.dispatch(tree.children)

    def _external_declaration(self, tree, flag=None):
        return self.dispatch(tree.children)

    def _statement_list(self, tree, flag=None):
        return self.dispatch(tree.children)

    def _statement(self, tree, flag=None):
        return self.dispatch(tree.children) + "\n"
                

    #whoever wrote this, please have a look at _assignnment_statement_list_index
    def _assignment_statement(self, tree, flag=None):
        print tree.children[0]
        arg = self.dispatch(tree.children[0]);
        #print arg;
        scpDepth = 0
        for scpDepth in range(0, self.scopeDepth + 1):
            if tree.leaf + "__" + str(scpDepth) + "__" in self.symbolTable:
                var_type = self.symbolTable[tree.leaf + "__" + str(scpDepth) + "__"][0]
                if self.symbolTable[tree.leaf + "__" + str(scpDepth) + "__"][0] != arg[0]:
                    exit(tree.leaf + " is of type " + var_type + ". Cannot assign "  + arg[0] + " to it.")
                break
        self.symbolTable[tree.leaf + "__" + str(scpDepth) + "__"] = [arg[0], arg[1]]
        if scpDepth == self.scopeDepth:
            self.scopes[self.scopeDepth].append(tree.leaf + "__" + str(self.scopeDepth) + "__")
        # print self.symbolTable #uncomment to check symbol table
        # print self.scopes

        if type(arg) is not str: arg = str(arg)
        string = ""
        if scpDepth != self.scopeDepth:
            string += "global " + tree.leaf + "\n"
        string += tree.leaf + " = " + arg
        return string

    def _for_statement(self, tree, flag=None):
        #for iterator in a range
        or_expression1 = self.dispatch(tree.children[0])
        or_expression2 = self.dispatch(tree.children[1])
        the_id = tree.leaf
        self.symbolTable[tree.leaf] = ["NUM", None] #this might be bad because it just holds a dummy variable but we'll deal
        
        if type(or_expression1) is tuple: or_expression1 = or_expression1[1]
        if type(or_expression2) is tuple: or_expression2 = or_expression2[1]
        if type(or_expression1) is float: or_expression1 = str(int(or_expression1))
        if type(or_expression2) is float: or_expression2 = str(int(or_expression2))
        
        s = "for " + the_id + " in range( " + or_expression1 + " , " + or_expression2 + " + 1 ) : \n"
        self.inBlock()
        lines = self.dispatch(tree.children[2]).splitlines()

        for line in lines:
            s+= "    " + line +"\n"
        self.outBlock()
        return s

    def _iteration_statement(self, tree, flag=None):
        condition = self.dispatch(tree.children[0])
        if type(condition) is tuple:
            condition = condition[1]
        
        #s = "while(" + self.dispatch(tree.children[0]) + "):\n"
        s = "while(" + condition + "):\n"
        self.inBlock()
        lines = self.dispatch(tree.children[1]).splitlines()

        for line in lines:
            s+= "    " + line +"\n"
        self.outBlock()
        return s

    def _selection_statement(self, tree, flag=None):
        condition = self.dispatch(tree.children[0])
        if type(condition) is tuple:
            condition = condition[1]
        if len(tree.children) == 2:
            s = "if(" + condition + "):\n"
            self.inBlock()
            lines = self.dispatch(tree.children[1]).splitlines()
            for line in lines:
                s+= "    " + line +"\n"
            self.outBlock()
            return s
        else:
            s = "if(" + condition + "):\n"
            self.inBlock()
            lines = self.dispatch(tree.children[1]).splitlines()
            for line in lines:
                s+= "    " + line +"\n"
            self.outBlock()
            s += "else:\n"
            self.inBlock()
            lines = self.dispatch(tree.children[2]).splitlines()
            for line in lines:
                s+= "    " + line +"\n"
            self.outBlock()
            return s

    def _primary_expression_boolean(self, tree, flag=None):
        return "BOOLEAN", str(tree.leaf).title()

    def _primary_expression_string(self, tree, flag=None):
        return "STRING", tree.leaf

    def _or_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag)


    def _and_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag)  

    def _equality_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0],flag)

    def _relational_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag) 

    def _additive_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag)

    def _multiplicative_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag) 


    def _to_expression(self, tree, flag=None):
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0])


    def _power_expression(self, tree, flag=None):

        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag) 

    #this needs to be fixed        

    def _primary_expression(self, tree, flag=None):
        
        if tree.leaf == None:
            arg = self.dispatch(tree.children[0])
            if type(arg) is tuple:
                arg1 = str(arg[1])
            else:
                arg1 = arg
            return arg[0], "(" + arg1 + ")"

    def _primary_expression_constant(self, tree, flag=None):
        return "NUM", float(tree.leaf)    
    

    def _during_or_expression(self, tree, flag=None):
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0], flag)
      

    def _during_and_expression(self, tree, flag=None):
        if len(tree.children) == 1:
            arg = self.dispatch(tree.children[0], flag)
            return arg
      

    def _primary_expression_funct(self, tree, flag= None):
        arg = self.dispatch(tree.children[0])
        funcname = arg.split("(")[0]
        return self.functionTable[funcname][1], arg

    def _print_statement(self, tree, flag=None):
        arg = self.dispatch(tree.children[0])
        if type(arg) is tuple:
            if arg[0] == "TIME":
                arg = "(" + arg[1] + ").time()"
            else:
                arg = arg[1]
        
        if type(arg) is int or type(arg) is float:
            arg = str(arg)
        s = "print " + arg
        return s

class TypeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
