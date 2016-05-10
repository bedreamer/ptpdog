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
        return y + 1

    def load_client_point(self, f, row):
        row = self._load_point(self.client, f, row)
        self.client_refresh_ttl = StringVar(self.root)
        row = row + 1
        b = Button(self.root, text="取消选择")
        b.grid(row=row, column=0)
        b = Button(self.root, text="全选")
        b.grid(row=row, column=1)
        b = Button(self.root, text="添加刷新")
        b.grid(row=row, column=2)
        return row

    def load_server_point(self, f, row):
        row = self._load_point(self.server, f, row)
        self.server_refresh_ttl = StringVar(self.root)
        row = row + 1
        b = Button(self.root, text="取消选择")
        b.grid(row=row, column=0)
        b = Button(self.root, text="全选")
        b.grid(row=row, column=1)
        b = Button(self.root, text="添加刷新")
        b.grid(row=row, column=2)
        return row

    def run_main(self):
        self.server_host = StringVar(self.root)
        self.server_addr = StringVar(self.root)
        self.client_addr = StringVar(self.root)
        self.server_host.set("127.0.0.1:9999")

        l = Label(self.root, text=u"服务器地址").grid(row=0, column=0)
        l = Entry(self.root, textvariable=self.server_host, width=30)
        l.grid(row=0, column=1, columnspan=2, sticky="w")

        b = Button(self.root, text="连接服务器")
        b.grid(row=0, column=3, sticky='e')

        l = Label(self.root, text=u"+++++++++++++"*10).grid(row=1, column=0, columnspan=10, sticky="w")
        Label(self.root, text=u"从站数据点:").grid(row=2, column=0, sticky="w")
        l = Label(self.root, text=u"从站地址:").grid(row=2, column=1)
        l = Entry(self.root, textvariable=self.client_addr, width=5)
        l.grid(row=2, column=2, sticky="w")
        row = self.load_client_point("client.csv", 3)

        row = row + 1
        l = Label(self.root, text=u"+++++++++++++"*10).grid(row=row, column=0, columnspan=10, sticky="w")

        row = row + 1
        Label(self.root, text=u"主站数据点:").grid(row=row, column=0, sticky="w")
        l = Label(self.root, text=u"主站地址:").grid(row=row, column=1)
        l = Entry(self.root, textvariable=self.client_addr, width=5)
        l.grid(row=row, column=2, sticky="w")

        row = self.load_server_point("client.csv", row)

        self.root.mainloop()

ui = UI()
ui.run_main()
