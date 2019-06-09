import sys

tblptr = []
offset = []
tokenset = {}
class Token(object):
    def __init__(self, name, tpye_, wo):
        self.name = name
        self.tpye_ = tpye_
        self.wo = wo # width or offset

    def set_offset(self, a):
        self.offset = a

class Proc(object):
    def __init__(self, name, new_table):
        self.name = name
        self.tpye_ = "%-10s"%"proc"
        self.new_table = new_table
        new_table.name = name
        

class Table(object):
    def __init__(self, previous):
        self.name = "main"
        self.previous = previous
        self.width = 0
        self.items = []

def enter(table, token):
    table.items.append(token)

def addwidth(table, width):
    table.width = width

def enterproc(table, proc):
    table.items.append(proc)

def tbprint(table):
    print("")
    print(30*"-")
    print("table name: " + table.name)
    print("table width: " + str(table.width))
    print(30*"-")
    print("Id_Name\t%-10s\tOffset"%"Type")
    # print(tblptr)
    for item in table.items:
        if item.tpye_ != "%-10s"%"proc":
            print("%-7s"%item.name + "\t" + item.tpye_ + "\t" + str(item.wo))
        else:
            print("%-7s"%item.name + "\t" + item.tpye_ + "\t" + "--")
    print(30*"-")
    print("")


def step(prod):
    # print(tokenset)
    tokens = prod.split(" ")
    for i in range(10):
        prod = prod.replace(str(i),'')
    prod = prod.strip().strip()
    # print(prod)
    if prod == "P -> M D":
        t = tblptr.pop()
        w = offset.pop()
        addwidth(t, w)
        tbprint(t)
    elif prod == "M -> e":
        t = Table(None)
        tblptr.append(t)
        offset.append(0)
    elif prod == "D -> D ; D":
        pass
    elif prod == "D -> proc id ; N D ; s":
        t = tblptr.pop()
        w = offset.pop()
        addwidth(t, w)
        proc = Proc(tokens[3] ,t)
        tbprint(t)
        enterproc(tblptr[-1], proc)
    elif prod == "D -> id : T":
        T = tokenset[tokens[4]]
        idt = Token(tokens[2], "%-10s"%T.tpye_, offset[-1])
        enter(tblptr[-1], idt)
        offset[-1] += T.wo
    elif prod == "N -> e":
        # print(prod)
        t = Table(tblptr[-1])
        tblptr.append(t)
        offset.append(0)
    elif prod == "T -> integer":
        name = tokens[0]
        t = Token(name, "integer", 4)
        tokenset[name] = t
    elif prod == "T -> real":
        name = tokens[0]
        t = Token(name, "real", 8)
        tokenset[name] = t
    elif prod == "T -> ^ T":
        name1 = tokens[0]
        name2 = tokens[3]
        t1 = tokenset[name2]
        t = Token(name1, "^"+t1.tpye_, 4)
        tokenset[name1] = t
    else:
        print("something wrong!")
        print(prod)


if __name__ == '__main__':
    file_name = sys.argv[1]
    with open(file_name, "r") as f:
        for line in f.readlines():
            line = line.replace('\n','')
            step(line)