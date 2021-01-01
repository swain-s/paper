class ins(object):
    def __init__(self, value, op):
        self.value = value
        self.op = op

class Mystack(object):
    def __init__(self):
        self.count = 0

    def init_stack(self):
        self.mystack = []
        return 0

    def push_value(self, s, myvalue):
        value_ins = ins(myvalue, None)
        s.append(value_ins)
        return 0

    def push_op(self, s, myop):
        op_ins = ins(None ,myop)
        s.append(op_ins)
        return 0

    def spop(self, s):
        temp = s[-1]
        del(s[-1])
        return temp

    def run(self, s):
        counter = []
        while len(s) > 1:
            print(s[-1].value)
            node = self.spop(s)
            if node.value:
                counter.append(node.value)
            elif node.op:
                if node.op == "+":
                    result = counter[0] + counter[1]
                    counter.clear()
                    s.append(result)
                elif node.op == "+":
                    result = counter[0] - counter[1]
                    counter.clear()
                    s.append(result)
                elif node.op == "+":
                    result = counter[0] * counter[1]
                    counter.clear()
                    s.append(result)
                elif node.op == "+":
                    result = counter[0]/counter[1]
                    counter.clear()
                    node.append(result)
                else:
                    print("op error")
        print(s[0])

ms = Mystack()

ms.init_stack()
ms.push_value(ms.mystack, 3)
ms.push_value(ms.mystack, 5)
ms.push_op(ms.mystack, "+")

ms.run(ms.mystack)