
# symbol table

tablestack = [{},]

def update_entry(symbol, attributes):
    global tablestack
    tablestack[-1][symbol] = attributes

def enter_scope():
    global tablestack
    tablestack.append({})

def leave_scope():
    global tablestack
    tablestack.pop()

def search_symbol(symbol):
    global tablestack
    return tablestack[-1].get(symbol, None)
