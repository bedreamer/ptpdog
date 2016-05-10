# -*- coding: UTF-8 -*-
__author__ = 'lijie'
from Tkinter import *

class point:
    def __init__(self, root, id, v, name, x, y, unit):
        self.root = root
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.unit = unit
        self.s = StringVar(root)
        self.s.set(v + ' ' + unit)
        self.c = Checkbutton(root, text=name)
        self.e = Entry(root, width="8", textvariable=self.s)
        self.c.grid(row=x, column=y, sticky="w")
        self.e.grid(row=x, column=y+1)
    def set_v(self, v):
        self.s.set(v)

    def get_v(self):
        return self.s.get()

class UI:
    def __init__(self):
        self.root = Tk()
        self.client = []
        self.server = []

    def _load_point(self, p, f, row):
        fd = open(f, "r")
        lines = fd.readlines()
        x = row
        y = 0
        lines.pop(0)
        while len(lines):
            line = lines.pop(0)
            line = line.split(',')
            if len(line[0]) <= 0:
                break
            pt = point(self.root, line[0], line[2], line[1], x, y, line[3])
            y = y + 2
            if y >= 5 * 2:
                x = x + 1
                y = 0
            p.append(pt)

    def load_client_point(self, f, row):
        self._load_point(self.client, f, row)

    def load_server_point(self, f, row):
        self._load_point(self.server, f, row)

    def run_main(self):
        l = Label(self.root, text=u"服务器地址").grid(row=0, column=0)
        self.server_addr = StringVar(self.root)
        self.server_addr.set("127.0.0.1:9999")
        l = Entry(self.root, textvariable=self.server_addr, width=30)
        l.grid(row=0, column=1, columnspan=2, sticky="w")
        b = Button(self.root, text="连接服务器")
        b.grid(row=0, column=3, sticky='e')
        self.load_client_point("client.csv", 1)
        #self.load_server_point('server.csv', 1)
        self.root.mainloop()

ui = UI()
ui.run_main()
