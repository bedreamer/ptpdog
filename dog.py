# -*- coding: UTF-8 -*-
__author__ = 'lijie'
from Tkinter import *
from cptp import *

class point:
    def __init__(self, root, id, v, name, x, y, unit):
        self.root = root
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.checked = False
        self.unit = unit
        self.s = StringVar(root)
        self.cv = StringVar(root)
        self.s.set(v + ' ' + unit)
        self.c = Checkbutton(root, text=name, variable =self.cv, onvalue=1, offvalue=0, command=self.check_call_back)
        self.e = Entry(root, width="8", textvariable=self.s)
        self.c.grid(row=x, column=y, sticky="w")
        self.e.grid(row=x, column=y+1)
        self.uncheck()

    def check(self):
        self.cv.set(1)
        self.checked = True

    def uncheck(self):
        self.cv.set(0)
        self.checked = False

    def check_call_back(self):
        if self.checked:
            print "uncheck", self.id, self.s.get()
            self.checked = False
        else:
            print "check", self.id, self.s.get()
            self.checked = True

    def set_v(self, v):
        self.s.set(v)

    def get_v(self):
        return self.s.get().split(' ')[0]

class UI:
    def __init__(self):
        self.root = Tk()
        #self.log = Tk()
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
        return x + 1

    def load_client_point(self, f, row):
        row = self._load_point(self.client, f, row)
        self.client_refresh_ttl = StringVar(self.root)
        print row
        row = row + 1
        b = Button(self.root, text="取消选择", command=self.uncheck_all_client)
        b.grid(row=row, column=0)
        b = Button(self.root, text="全选", command=self.check_all_client)
        b.grid(row=row, column=1)
        b = Button(self.root, text="刷新", command=self.refresh_client)
        b.grid(row=row, column=2)
        b = Button(self.root, text="读取", command=self.read_client)
        b.grid(row=row, column=3)
        b = Button(self.root, text="写入", command=self.write_client)
        b.grid(row=row, column=4)
        return row + 1

    def load_server_point(self, f, row):
        row = self._load_point(self.server, f, row)
        self.server_refresh_ttl = StringVar(self.root)
        print row
        row = row + 1
        b = Button(self.root, text="取消选择", command=self.uncheck_all_server)
        b.grid(row=row, column=0)
        b = Button(self.root, text="全选", command=self.check_all_server)
        b.grid(row=row, column=1)
        b = Button(self.root, text="刷新", command=self.refresh_server)
        b.grid(row=row, column=2)
        b = Button(self.root, text="读取", command=self.read_server)
        b.grid(row=row, column=3)
        b = Button(self.root, text="写入", command=self.write_server)
        b.grid(row=row, column=4)
        return row + 1

    def get_checked(self, pts):
        s = []
        for p in pts:
            if p.checked:
                s.append({'id':p.id, 'v':p.get_v()})
        return s

    def check_all(self, pts):
        for p in pts:
            p.check()

    def uncheck_all(self, pts):
        for p in pts:
            p.uncheck()

    def check_all_client(self):
        self.check_all(self.client)

    def uncheck_all_client(self):
        self.uncheck_all(self.client)

    def read(self, pts, src, des):
        p = cptp()
        buf = []
        checked = self.get_checked(pts)
        if len(checked) == 0:
            return
        p.patch_request_header(buf, src, des, cptp_head.FUNC_RD, 1, cptp_head.WITHOUT_TSP)
        for pt in checked:
            p.patch_id(buf, int(pt['id']))
        p.patch_tail(buf)
        p.dump(buf)
        return buf

    def write(self, pts, src, des):
        p = cptp()
        buf = []
        checked = self.get_checked(pts)
        if len(checked) == 0:
            return
        p.patch_request_header(buf, src, des, cptp_head.FUNC_WR, 1, cptp_head.WITHOUT_TSP)
        for pt in checked:
            p.patch_point(buf, int(pt['id']), int(pt['v']))
        p.patch_tail(buf)
        p.dump(buf)
        return buf

    def refresh(self, pts, src, des):
        p = cptp()
        buf = []
        checked = self.get_checked(pts)
        if len(checked) == 0:
            return
        p.patch_request_header(buf, src, des, cptp_head.FUNC_REFRESH, 1, cptp_head.WITHOUT_TSP)
        for pt in checked:
            p.patch_point(buf, int(pt['id']), int(pt['v']))
        p.patch_tail(buf)
        p.dump(buf)
        return buf

    def refresh_client(self):
        self.refresh(self.client, int(self.server_addr.get()), int(self.client_addr.get()))

    def read_client(self):
       self.read(self.client, int(self.client_addr.get()), int(self.server_addr.get()))

    def write_client(self):
        self.write(self.client, int(self.client_addr.get()), int(self.server_addr.get()))

    def check_all_server(self):
        self.check_all(self.server)

    def uncheck_all_server(self):
        self.uncheck_all(self.server)

    def refresh_server(self):
        self.refresh(self.server, int(self.client_addr.get()), int(self.server_addr.get()))

    def read_server(self):
        self.read(self.server, int(self.server_addr.get()), int(self.client_addr.get()))

    def write_server(self):
        self.write(self.server, int(self.server_addr.get()), int(self.client_addr.get()))

    def start_server(self):
        print u"启动服务器"

    def link_server(self):
        print u"连接服务器"

    def run_main(self):
        self.server_host = StringVar(self.root)
        self.server_addr = StringVar(self.root)
        self.client_addr = StringVar(self.root)
        self.server_port = StringVar(self.root)
        self.server_host.set("127.0.0.1:9999")
        self.server_port.set(9999)
        self.server_addr.set(1)
        self.client_addr.set(128)
        self.root.title("CPTP解码狗 V3.45.298")
        #self.log.title("CPTP数据流")

        l = Label(self.root, text=u"服务器地址").grid(row=0, column=0)
        l = Entry(self.root, textvariable=self.server_host, width=30)
        l.grid(row=0, column=1, columnspan=2, sticky="w")

        b = Button(self.root, text="连接服务器", command=self.link_server)
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
        l = Label(self.root, text=u"服务端口").grid(row=row, column=0)
        l = Entry(self.root, textvariable=self.server_port, width=8)
        l.grid(row=row, column=1, sticky="w")
        b = Button(self.root, text="启动服务器", command=self.start_server)
        b.grid(row=row, column=2, sticky='e')

        row = row + 1
        Label(self.root, text=u"主站数据点:").grid(row=row, column=0, sticky="w")
        l = Label(self.root, text=u"主站地址:").grid(row=row, column=1)
        l = Entry(self.root, textvariable=self.server_addr, width=5)
        l.grid(row=row, column=2, sticky="w")

        row = self.load_server_point("server.csv", row + 1)

        self.root.mainloop()

ui = UI()
ui.run_main()
