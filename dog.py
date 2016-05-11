# -*- coding: UTF-8 -*-
__author__ = 'lijie'
from Tkinter import *
from cptp import *
from threading import Timer
import  select
from socket import *
import struct

class point:
    def __init__(self, root, id, v, name, x, y, unit, kind):
        self.root = root
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.bytes = []
        self.kind = kind
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

    def get_bytes(self):
        if  self.kind == 'INT':
            return int(self.s.get().split(' ')[0])
        elif self.kind == 'F1' or self.kind == 'F2':
            v = struct.pack("f", float(self.s.get().split(' ')[0]))
            v = struct.unpack('i', v)[0]
            return v
        else:
            return int(self.bytes[0])

    def set_bytes(self, b):
        if  self.kind == 'INT':
            pass
        elif self.kind == 'F1':
            pass
        elif self.kind == 'F2':
            pass
        else:
            return self.bytes[0]

def cptp_server_main(root, port):
    pass

def compress(l):
    return struct.pack("B"*len(l), *l)

class UI:
    def __init__(self):
        self.root = Tk()
        #self.log = Tk()
        self.client = []
        self.server = []
        self.cptp = cptp()

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
            pt = point(self.root, line[0], line[2], line[1], x, y, line[3], line[4])
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
        b = Button(self.root, text="从站功能：刷新", command=self.refresh_client, bg="#DD0")
        b.grid(row=row, column=2)
        b = Button(self.root, text="主站功能：读取", command=self.read_client, bg="#0DD")
        b.grid(row=row, column=3)
        b = Button(self.root, text="主站功能：写入", command=self.write_client, bg="#0DD")
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
        b = Button(self.root, text="主站功能：刷新", command=self.refresh_server, bg="#0DD")
        b.grid(row=row, column=2)
        b = Button(self.root, text="从站功能：读取", command=self.read_server, bg="#DD0")
        b.grid(row=row, column=3)
        b = Button(self.root, text="从站功能：写入", command=self.write_server, bg="#DD0")
        b.grid(row=row, column=4)
        return row + 1

    def search_point(self, source, id):
        for p in source:
            if int(p.id) == id:
                return p
        return None

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
            return buf
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
            return buf
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
            return buf
        p.patch_request_header(buf, src, des, cptp_head.FUNC_REFRESH, 1, cptp_head.WITHOUT_TSP)
        for pt in checked:
            p.patch_point(buf, int(pt['id']), int(pt['v']))
        p.patch_tail(buf)
        p.dump(buf)
        return buf

    def refresh_client(self):
        buf = self.refresh(self.client, int(self.server_addr.get()), int(self.client_addr.get()))
        if len(buf):
            cbuf = compress(buf)
            self.client_socket.send(cbuf)

    def read_client(self):
       buf = self.read(self.client, int(self.client_addr.get()), int(self.server_addr.get()))
       if len(buf):
           cbuf = compress(buf)
           self.client_socket.send(cbuf)

    def write_client(self):
        buf = self.write(self.client, int(self.client_addr.get()), int(self.server_addr.get()))
        if len(buf):
            cbuf = compress(buf)
            self.client_socket.send(cbuf)

    def check_all_server(self):
        self.check_all(self.server)

    def uncheck_all_server(self):
        self.uncheck_all(self.server)

    def refresh_server(self):
        buf = self.refresh(self.server, int(self.client_addr.get()), int(self.server_addr.get()))
        if len(buf):
            cbuf = compress(buf)
            self.client_socket.send(cbuf)

    def read_server(self):
        buf = self.read(self.server, int(self.server_addr.get()), int(self.client_addr.get()))
        if len(buf):
           cbuf = compress(buf)
           self.client_socket.send(cbuf)

    def write_server(self):
        buf = self.write(self.server, int(self.server_addr.get()), int(self.client_addr.get()))
        if len(buf):
           cbuf = compress(buf)
           self.client_socket.send(cbuf)

    def start_server(self):
        print u"启动服务器"

    def about_request(self, source, peer, frame, des, src, func, count, len):
        if func == cptp_head.FUNC_RD:
            ack = []
            ids = []
            p = cptp()
            for i in range(count):
                id = frame[ cptp_head.HEAD_SIZE + i * 2 + 0] + frame[ cptp_head.HEAD_SIZE + i * 2 + 1] * 256
                ids.append(id)
            p.patch_request_header(ack, des, src, cptp_head.FUNC_REFRESH, 1, cptp_head.WITHOUT_TSP)
            for pt in ids:
                thiz = self.search_point(source, pt)
                if thiz is None:
                    continue
                p.patch_point(ack, pt, thiz.get_bytes())
            p.patch_tail(ack)
            print ack

        elif func == cptp_head.FUNC_WR:
            print "写"
        elif func == cptp_head.FUNC_REFRESH:
            print "刷新"
        else:
            print u"不支持功能码%d" % func

    def about_ack(self, source, peer, frame, des, src, func, count, len):
        if func == cptp_head.FUNC_RD:
            print "读数据应答"
        elif func == cptp_head.FUNC_WR:
            print "写数据应答"
        elif func == cptp_head.FUNC_REFRESH:
            print "刷新数据应答"
        else:
            print u"不支持功能码%d" % func

    def about_recv_frame(self, frame):
        p = cptp_head(frame)
        if p.des == int(self.server_addr.get()) and p.kind == cptp_head.TYPE_ACK:
            return self.about_ack(self.server, self.client, frame, p.des, p.src, p.func, p.count, p.len)
        if p.des == int(self.server_addr.get()) and p.kind == cptp_head.TYPE_REQUEST:
            return self.about_request(self.server, self.client, frame, p.des, p.src, p.func, p.count, p.len)
        elif p.des == int(self.client_addr.get()) and p.kind == cptp_head.TYPE_ACK:
            return self.about_ack(self.client, self.server, frame, p.des, p.src, p.func, p.count, p.len)
        elif p.des == int(self.client_addr.get()) and p.kind == cptp_head.TYPE_REQUEST:
            return self.about_request(self.client, self.server, frame, p.des, p.src, p.func, p.count, p.len)
        else:
            print "非法地址%d->%d" % (p.src, p.des)

    def timer_proc(self):
        if self.client_socket:
            r, w, e = select.select([self.client_socket], [self.client_socket], [self.client_socket], None)
            if self.client_socket in r:
                buf = self.client_socket.recv(1024)
                if buf is None or len(buf) == 0:
                    print "socket closed!"
                    self.client_socket.close()
                    self.client_socket = None
                    return
                else:
                    print buf
                    self.cptp.push_bytes(buf)
                    while len(self.cptp.rx_frame):
                        self.about_recv_frame(self.cptp.rx_frame.pop(0))
            if self.client_socket in e:
                print "error"
        self.timer = Timer(0.2, self.timer_proc)
        self.timer.start()

    def link_server(self):
        h = self.server_host.get()
        h = h.split(':')
        if self.client_socket:
            return
        self.client_socket = socket()
        self.client_socket.connect((h[0], int(h[1])))
        if self.client_socket > 0:
            self.timer_proc()

    def run_main(self):
        self.server_host = StringVar(self.root)
        self.server_addr = StringVar(self.root)
        self.client_addr = StringVar(self.root)
        self.server_port = StringVar(self.root)
        self.server_host.set("127.0.0.1:9999")
        self.server_port.set(9999)
        self.server_addr.set(1)
        self.client_addr.set(128)
        self.client_socket = None
        self.root.title("CPTP解码狗 V3.45.298")
        #self.log.title("CPTP数据流")

        l = Label(self.root, text=u"服务器地址").grid(row=0, column=0)
        l = Entry(self.root, textvariable=self.server_host, width=30)
        l.grid(row=0, column=1, columnspan=2, sticky="w")

        b = Button(self.root, text="连接服务器", command=self.link_server, bg="#FF0")
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
        b = Button(self.root, text="启动服务器", command=self.start_server, bg="#0FF")
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
