#!/usr/bin/python
# encoding=utf-8

from utils import *
from FuncWindow import CFuncWindow, CRegisterDlg, CForgotPassword


class CMainWindow(gtk.Window):
    def __init__(self):
        super(CMainWindow, self).__init__(gtk.WINDOW_TOPLEVEL)

        self.fixed = gtk.Fixed()
        self.func_fixed = gtk.Fixed()
        self.init_window()
        self.login_btn = gtk.Button('登录')
        self.exit_btn = gtk.Button('关机')
        self.username_entry = gtk.Entry()
        self.password_entry = gtk.Entry()
        self.login = False
        self.__conf = CConfig(os.getcwd()+ "/conf.ini")
        self.user_name = self.__conf.get('user_info', 'user_name')
        self.password = self.__conf.get('user_info', 'password')

        self.init_login_window()
        self.init_func_window()

    def init_window(self):
        self.set_modal(True)
        self.set_decorated(False)
        self.connect("destroy", gtk.main_quit)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_size_request(WINDOW_X_SIZE, WINDOW_Y_SIZE)
        self.set_keep_above(True)
        self.set_title("医药管理系统")
        image = new_image_from_name("bg.jpg")
        self.fixed.put(image, 0, 0)
        self.add(self.fixed)

    def switch_ui(self):
        if not self.login:
            self.fixed.set_no_show_all(0)
            self.func_fixed.set_no_show_all(1)
            self.fixed.show_all()
            self.func_fixed.hide()
        else:
            self.fixed.set_no_show_all(1)
            self.func_fixed.set_no_show_all(0)
            self.fixed.hide()
            self.func_fixed.show_all()

    def init_func_window(self):
        image = new_image_from_name('bg.jpg')
        self.func_fixed.put(image, 0, 0)

    def init_login_window(self):

        label_size_x = 100
        label_size_y = 30

        entry_size_x = 300
        entry_size_y = 30

        start_x = (WINDOW_X_SIZE-label_size_x-entry_size_x)/2
        start_y = (WINDOW_Y_SIZE)/2
        user_label = gtk.Label('用户名:')
        user_label.set_size_request(label_size_x, label_size_y)
        self.fixed.put(user_label, start_x, start_y)

        self.username_entry.set_size_request(entry_size_x, entry_size_y)
        self.fixed.put(self.username_entry, start_x+100, start_y)

        start_y += 40
        password_label = gtk.Label('密码:')
        password_label.set_size_request(label_size_x, label_size_y)
        self.fixed.put(password_label, start_x, start_y)

        self.password_entry.set_size_request(entry_size_x, entry_size_y)
        self.password_entry.set_visibility(False)
        self.fixed.put(self.password_entry, start_x+100, start_y)

        start_y += 40
        start_x += 320
        self.login_btn.set_size_request(80, 30)
        self.login_btn.connect("clicked", self.btn_cb, "login")
        self.fixed.put(self.login_btn, start_x, start_y)

        start_x -= 90
        self.exit_btn.set_size_request(80, 30)
        self.exit_btn.connect("clicked", self.btn_cb, "shutdown")
        self.fixed.put(self.exit_btn, start_x, start_y)

        start_x -= 90
        _btn = gtk.Button('忘记密码')
        _btn.set_size_request(80, 30)
        _btn.connect("clicked", self.btn_cb, "forgot_password")
        self.fixed.put(_btn, start_x, start_y)

        start_x -= 90
        _btn = gtk.Button('注册')
        _btn.set_size_request(80, 30)
        _btn.connect("clicked", self.btn_cb, "register")
        self.fixed.put(_btn, start_x, start_y)

    def btn_cb(self, widget, opt):
        if "shutdown" == opt:
            os.system("shutdown -h now")
        elif "login" == opt:
            self.login_system()
        elif "forgot_password" == opt:
            CForgotPassword(self, self.__conf)
        elif "register" == opt:
            CRegisterDlg(self, self.__conf)

    def login_system(self):
        _password = self.password_entry.get_text()
        if _password == "" or self.username_entry.get_text() == "":
            CNotifyDlg('请输入用户名和密码')
            return
        self.password = self.__conf.get('user_info', 'password')
        self.user_name = self.__conf.get('user_info', 'user_name')
        if self.user_name != self.username_entry.get_text():
            CNotifyDlg('用户名或密码不正确')
            return
        if self.password != _password:
            CNotifyDlg('密码不正确')
            return
        CFuncWindow(self)

    def run(self):
        self.show_all()
        gtk.main()
