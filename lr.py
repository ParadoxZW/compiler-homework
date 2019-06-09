from semantic import *
ACTION = [{"proc":"s3", "id":"s4"},
          {"#":"acc"},
          {";":"s5", "proc":"r1", "id":"r1", "s":"r1",
           ":":"r1", "integer":"r1", "real":"r1", "^":"r1" , "#":"r1"},
          {"id":"s6"},
          {":":"s7"},
          {"proc":"s3", "id":"s4"},
          {";":"s9"},
          {"integer":"s11", "real":"s12", "^":"s13"},
          {";":"s5", "proc":"r2", "id":"r2", "s":"r2",
           ":":"r2", "integer":"r2", "real":"r2", "^":"r2" , "#":"r2"},
          {"proc":"s3", "id":"s4"},
          {";":"r4", "proc":"r4", "id":"r4", "s":"r4",
           ":":"r4", "integer":"r4", "real":"r4", "^":"r4" , "#":"r4"},
          {";":"r5", "proc":"r5", "id":"r5", "s":"r5",
           ":":"r5", "integer":"r5", "real":"r5", "^":"r5" , "#":"r5"},
          {";":"r6", "proc":"r6", "id":"r6", "s":"r6",
           ":":"r6", "integer":"r6", "real":"r6", "^":"r6" , "#":"r6"},
          {"integer":"s11", "real":"s12", "^":"s13"},
          {";":"s16"},
          {";":"r7", "proc":"r7", "id":"r7", "s":"r7",
           ":":"r7", "integer":"r7", "real":"r7", "^":"r7" , "#":"r7"},
          {"proc":"s3", "id":"s4", "s":"s17"},
          {";":"r3", "proc":"r3", "id":"r3", "s":"r3",
           ":":"r3", "integer":"r3", "real":"r3", "^":"r3" , "#":"r3"},]
GOTO = [{} for _ in range(18)]
GOTO[0] = {"P": 1, "D":2}
GOTO[5] = {"D":8}
GOTO[7] = {"T":10}
GOTO[9] = {"D":14}
GOTO[13] = {"T":15}
GOTO[16] = {"D":8}
grams = ["P -> D", "D -> D ; D", "D -> proc id ; D ; s",
         "D -> id : T", "T -> integer", "T -> real", "T -> ^ T"] 


location = 0  # 输入位置
status_stack = []  # 状态栈
symbol_stack = []  # 符号栈
N_stack = [] # 记录N的下标的栈
now_state = ''  # 栈顶状态
input_ch = ''  # 栈顶字符
input_str = ''  # 输入串
now_step = 0  # 当前步骤




def reduce():
    global location
    status_stack.append(0)
    prod = "M -> e"
    print(prod)
    step(prod)
    find = None
    while True:
        try:
            now_state = status_stack[-1]
            input_ch = input_str[location]
            # print(status_stack)
            # print(symbol_stack, input_ch)
            # print(input_str[location:])
            find = ACTION[now_state][input_ch]
            # print(find)
            # print("")
        except:
            print("something wrong when reduce!")


        if find[0] == 's':
            name = sym_name[location]
            if name == "proc":
                N = N_gen()
                N_stack.append(N)
                prod = N + " -> e"
                print(prod)
                step(prod)
            symbol_stack.append(name)
            status_stack.append(int(find[1:]))
            location += 1

        elif find[0] == 'r':
            num = int(find[1])
            g = grams[num - 1]
            gs = g.split(" ")
            right_num = len(gs) - 2
            rs = ""
            for i in range(right_num):
                status_stack.pop()
                rs = symbol_stack.pop() + " " + rs
            X = give_idx(g[0])
            symbol_stack.append(X)
            now_state = status_stack[-1]
            symbol_ch = g[0]
            try:
                find = GOTO[now_state][symbol_ch]
            except:
                print("GOTO wrong!")
                return -1
            status_stack.append(find)
            if X == "P":
                prod = X + " -> M " + rs
                print(prod)
                step(prod)
            elif gs[2] == "proc":
                N = N_stack.pop()
                prod = X + " -> " + rs.replace("D", N +" D")
                print(prod)
                step(prod)
            else:
                prod = X + " -> " + rs
                print(prod)
                step(prod)
        elif find == "acc":
            print("Analyzing is successfully finished!")
            return 0
        else:
            return -1
    return 0

di = 0
def D_gen():
    global di
    di += 1
    return "D" + str(di)

ti = 0
def T_gen():
    global ti
    ti += 1
    return "T" + str(ti)

ni = 0
def N_gen():
    global ni
    ni += 1
    return "N" + str(ni)

def give_idx(g):
    if g == "D":         
        return D_gen()
    elif g == "T":
        return T_gen()
    else:
        return g



if __name__ == '__main__':
    # input_strd = "id1 : real ; proc id2 ; id3 : real ; s #"
    # input_strd = "id1 : real ; id2 : ^ integer ; id3 : integer #"
    # input_strd = "id1 : ^ real ; proc id2 ; id3 : integer ; s #"
    input_strd = "id1 : real ; id2 : ^ real ; proc id3 ; id4 : real ; s ; proc id5 ; id6 : real ; s ; id7 : real #"

    sym_name = input_strd.split(" ")
    for i in range(10):
        input_strd = input_strd.replace(str(i),'')
    input_str = input_strd.split(" ")
    stat = reduce()
    if(stat == 0):
        print("%s is regular" % input_strd)
    else:
        print("%s is irregular" % input_strd)