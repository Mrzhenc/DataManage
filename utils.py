#!/usr/bin/python
# encoding=utf-8
from common import *


ini_content = """[user_info]
user_name = 
password = 
phone_num = 
"""


class CConfig:
    def __init__(self, _path):
        self.path = _path
        try:
            if not os.path.exists(_path):
                fp = open(_path, 'w')
                fp.write(ini_content)
                fp.close()
            self.cf = ConfigParser.ConfigParser()
            self.cf.read(self.path)
        except:
            print "error"

    def get(self, field, key):
        try:
            result = self.cf.get(field, key)
        except:
            result = ""
        return result

    def set(self, _filed, key, value):
        try:
            self.cf.set(_filed, key, value)
            self.cf.write(open(self.path, 'w'))
        except:
            return False


def new_image_from_name(file_name):
    path = os.getcwd() + '/UI/' + file_name
    image = gtk.image_new_from_file(path)
    return image


def modify_font(_label, _size):
    font = "Arail %d" % _size
    desc = pango.FontDescription(font)
    _label.modify_font(desc)


class CNotifyDlg(gtk.Window):
    def __init__(self, _info_str, _time_out=5, _show_close_btn=True):

        super(CNotifyDlg, self).__init__(gtk.WINDOW_POPUP)
        self.set_keep_above(True)
        # self.set_modal(True)
        self.__startY = 0
        self.__startX = 0
        self.__endY = 0
        self.__time_out = _time_out * 1000
        self.set_decorated(False)
        self.__fixed = gtk.Fixed()
        self.__info_label = None
        self.__info_str = _info_str
        self.__bg_w = 0
        self.__bg_h = 0
        self.__close_timer = None
        self.__opacity_timer = None
        self.__b_closed = False
        self.__b_show_close_btn = _show_close_btn
        self.ui_init()

    def ui_init(self):

        _bg_image = image_from_file(res_file_get("tishi_bg.png"))
        self.__bg_w = _bg_image.get_pixbuf().get_width()
        self.__bg_h = _bg_image.get_pixbuf().get_height()
        self.__startY = -self.__bg_h
        self.__startX = (WINDOW_X_SIZE - self.__bg_w)/2
        self.__endY = 10
        self.move((WINDOW_X_SIZE - self.__bg_w)/2, -self.__bg_h)
        self.__fixed.set_size_request(self.__bg_w, self.__bg_h)
        self.__fixed.put(_bg_image, 0, 0)
        self.set_size_request(self.__bg_w, self.__bg_h)

        _icon_image = image_from_file(res_file_get("jinggao_icon.png"))
        _icon_w = _icon_image.get_pixbuf().get_width()
        _icon_h = _icon_image.get_pixbuf().get_height()
        self.__fixed.put(_icon_image, 5, (self.__bg_h - _icon_h)/2)

        self.__info_label = gtk.Label(self.__info_str)
        self.__info_label.set_alignment(gtk.JUSTIFY_LEFT, gtk.JUSTIFY_FILL)
        self.__info_label.set_size_request(self.__bg_w - _icon_w * 3, self.__bg_h)
        self.__fixed.put(self.__info_label, _icon_w + 20, -8)
        self.add(self.__fixed)
        # self.show_all()
        self.run()

    def btn_cb(self, widget):
        self.__b_closed = True
        self.destroy()

    def run(self):
        y = self.__startY
        timer_interval = 50

        while y < self.__endY:
            y += 1
            gobject.timeout_add(timer_interval, self.move_dlg, self.__startX, y)
            timer_interval += 15

    def move_dlg(self, x, y):
        self.move(x, y)
        self.show_all()

        if y == self.__endY:
            self.__close_timer = gobject.timeout_add(self.__time_out, self.close_dlg)

    def close_dlg(self):
        self.__b_closed = True
        self.destroy()
        # _op = 1.0
        # timer_interval = 500
        # while _op >= 0.1:
        #     _op -= 0.008
        #     self.__opacity_timer = gobject.timeout_add(timer_interval, self.change_opacity, _op)
        #     timer_interval += 5

    def change_opacity(self, _op):
        self.set_opacity(_op)
        self.show_all()

        if _op <= 0.1:
            self.__b_closed = True
            self.destroy()

    def get_is_closed(self):
        return self.__b_closed

    def get_label_str(self):
        return self.__info_label.get_text()

    def set_label_str(self, _label_str):
        self.__info_label.set_text(_label_str)


def image_from_file(image_file):
    pixbuf = gdk.pixbuf_new_from_file(image_file)
    image = gtk.image_new_from_pixbuf(pixbuf)

    del pixbuf
    return image


def res_file_get(_filename):
    return os.path.join(os.getcwd(), _filename)


def new_btn_fixed(image_name):
    _fixed = gtk.Fixed()
    _image = image_from_file(res_file_get(image_name))
    _w = _image.get_pixbuf().get_width()
    _h = _image.get_pixbuf().get_height()
    # print _w, _h
    _fixed.set_size_request(_w, _h)

    if _w > 250:
        _fixed.put(_image, -8, -8)
    elif _w > 160:
        _fixed.put(_image, -8, -8)
    elif _w > 150:
        _fixed.put(_image, -6, -6)
    elif image_name.find("arrow") >= 0:
        _fixed.put(_image, -7, -7)
    else:
        _fixed.put(_image, -8, -8)

    return _fixed, _w, _h