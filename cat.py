# -*- coding: utf8 -*-
__author__ = 'Administrator'
import time
from Tkinter import *

class node:
    def __init__(self, root, id, p, nr, show):
        self.NI = p
        self.now_NI = p
        self.nr = nr
        self.show = show
        self.id = id
        self.root = root
        self.s = StringVar(root)
        self.s.set(self.now_NI)
        self.e = Entry(root, width="8", textvariable=self.s)
        self.l = Label(root, text=str(self.id)+":"+show)
        self.l.grid(row=id-1, column=0)
        self.e.grid(row=id-1, column=1)

    def update(self):
        self.now_NI = int(self.s.get())

    def show_yourself(self):
        print "[%d.%d] %s" % (self.NI, self.nr, self.show)

def gen_seq(nr):
    P3 = []
    P2 = []
    P1 = []
    P0 = []
    Pn1 = []
    Pn2 = []
    seq = []
    for nd in nodes:
        if nd.now_NI == -2 and nr % 4 == 0:
            Pn2.append(nd)
        elif nd.now_NI == -1 and nr % 2 == 0:
            Pn1.append(nd)
        elif nd.now_NI == 0:
            P0.append(nd)
        elif nd.now_NI == 1:
            P1.append(nd)
        elif nd.now_NI == 2:
            P2.append(nd)
        elif nd.now_NI == 3:
            P3.append(nd)
        else:
            pass

    '''
    P3优先级最高，直接返回P3优先级的所有节点
    '''
    if len(P3):
        return P3

    '''
    周期执行P2
    序列中首先执行P1
    '''
    p1notset = True
    for nP0 in P0:
        if len(P2):
            for nP2 in P2:
                seq.append(nP2)
        if len(P1) and p1notset:
            p1notset = False
            for nP1 in P1:
                seq.append(nP1)
        seq.append(nP0)

    '''
    执行低优先级
    '''
    if len(Pn1):
        for nPn1 in Pn1:
            seq.append(nPn1)
    if len(Pn2):
        for nPn2 in Pn2:
            seq.append(nPn2)

    return seq

def ids(s):
    id = []
    for i in s:
        id.append(i.id)
    return id

count = 0
def repack():
    global count
    for n in nodes:
        n.update()
    seq = gen_seq( count )
    print count, ids(seq)
    count = count + 1

root = Tk()
nodes = []
SHOW = ["tom", "cat", "jerry", "hanks", "jack", "cup", "bedreamer", "cuplision", "helloworld"]
for i in range(len(SHOW)):
    p = node(root, i + 1, 0, 0, SHOW[i])
    nodes.append(p)
b = Button(root, text="更新序列", command=repack)
b.grid(row= len(SHOW), column=1, columnspan=2)

nodes[4].now_NI = 1
nodes[7].now_NI = 2
root.mainloop()
'''
while True:
    time.sleep(5)

'''