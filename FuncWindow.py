#!/usr/bin/python
# encoding=utf-8
from common import *
from utils import *


class CFuncWindow(gtk.Window):
    def __init__(self, _parent):
        super(CFuncWindow, self).__init__(gtk.WINDOW_TOPLEVEL)
        self.set_modal(True)
        self.set_size_request(WINDOW_X_SIZE, WINDOW_Y_SIZE)
        self.set_title("医药管理系统")
        self.set_transient_for(_parent)
        self.set_keep_above(True)
        self.set_position(gtk.WIN_POS_CENTER)

        self.fixed = gtk.Fixed()
        self.ui_init()
        self.add(self.fixed)
        self.show_all()

    def ui_init(self):
        image = new_image_from_name('bg.jpg')
        self.fixed.put(image, 0, 0)

        start_x = WINDOW_X_SIZE/3
        start_y = WINDOW_Y_SIZE/3

        image = new_image_from_name('find.jpg')
        _fixed = gtk.Fixed()
        _fixed.set_size_request(FUN_BTN_SIZE_X, FUN_BTN_SIZE_Y)
        _fixed.put(image, 0, 0)
        _find_btn = gtk.Button()
        _find_btn.connect('clicked', self.btn_cb, 'find')
        _find_btn.add(_fixed)
        self.fixed.put(_find_btn, start_x-FUN_BTN_SIZE_X, start_y)

        image = new_image_from_name('delete.jpg')
        _fixed = gtk.Fixed()
        _fixed.set_size_request(FUN_BTN_SIZE_X, FUN_BTN_SIZE_Y)
        _fixed.put(image, 0, 0)
        _delete_btn = gtk.Button()
        _delete_btn.connect('clicked', self.btn_cb, 'modify')
        _delete_btn.add(_fixed)
        self.fixed.put(_delete_btn, start_x+FUN_BTN_SIZE_X, start_y)

        image = new_image_from_name('add.jpg')
        _fixed = gtk.Fixed()
        _fixed.set_size_request(FUN_BTN_SIZE_X, FUN_BTN_SIZE_Y)
        _fixed.put(image, 0, 0)
        _add_btn = gtk.Button()
        _add_btn.connect('clicked', self.btn_cb, 'add')
        _add_btn.add(_fixed)
        self.fixed.put(_add_btn, start_x*2, start_y)

    def btn_cb(self, widget, opt):
        if 'add' == opt:
            CAddData(self)
        elif 'modify' == opt:
            CModifyData(self)
        elif 'find' == opt:
            CFindData(self)


class BaseWindow(gtk.Window):
    def __init__(self, _parent):
        super(BaseWindow, self).__init__(gtk.WINDOW_TOPLEVEL)
        self.set_size_request(SUB_WINDOW_X, SUB_WINDOW_Y)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_modal(True)
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_transient_for(_parent)
        self.is_save = False

        self.fixed = gtk.Fixed()
        self.add(self.fixed)
        self.title_label = None
        _textBuf = gtk.TextBuffer()
        self.__textView = gtk.TextView(_textBuf)
        self.ok_btn = gtk.Button('确定')
        self.__type_entry = gtk.Entry()
        self.__type_combobox = gtk.combo_box_new_text()
        self.ui_init()

    def get_is_save(self): return self.is_save

    def set_is_save(self, flag): self.is_save = flag

    def set_btn_label(self, _label):
        self.ok_btn.set_label(_label)

    def set_window_size(self, x, y):
        self.set_size_request(x, y)

    def get_type_from_file(self):
        path = os.getcwd() + "/type/"
        if not os.path.exists(path):
            return []
        return commands.getoutput("ls %s" % path).strip().split('\n')

    def ui_init(self):
        self.title_label = gtk.Label()
        self.title_label.set_size_request(300, 50)
        modify_font(self.title_label, 30)
        self.fixed.put(self.title_label, (SUB_WINDOW_X-300)/2, 50)

        start_x = (SUB_WINDOW_X - 400) / 2
        start_y = 120
        _label = gtk.Label("病史类型")
        modify_font(_label, 15)
        self.fixed.put(_label, start_x, start_y)

        self.__type_combobox.connect('changed', self.combo_changed)
        self.__type_combobox.set_wrap_width(1)
        self.__type_combobox.set_size_request(150, 35)
        type_list = self.get_type_from_file()
        for type in type_list:
            try:
                t = type.strip().split('_')[1]
                if t == "":
                    continue
                self.__type_combobox.append_text(t)
            except IndexError:
                continue

        self.fixed.put(self.__type_combobox, start_x+100, start_y+5)

        start_y += 40
        self.__type_entry.set_size_request(200, 30)
        self.fixed.put(self.__type_entry, start_x, start_y)

        start_y += 35
        self.add_scroll(start_x, start_y)

        self.ok_btn.set_size_request(80, 30)
        self.fixed.put(self.ok_btn, SUB_WINDOW_X - 90, SUB_WINDOW_Y - 40)

        cancel_btn = gtk.Button('关闭')
        cancel_btn.connect("clicked", self.btn_cancel)
        cancel_btn.set_size_request(80, 30)
        self.fixed.put(cancel_btn, SUB_WINDOW_X - 80*2 - 20, SUB_WINDOW_Y - 40)

    def hide_type_entry(self):
        self.__type_entry.hide()

    def combo_changed(self, widget):
        _type = widget.get_active_text()
        if _type == '添加':
            self.__type_entry.show()
        else:
            self.__type_entry.hide()

    def get_type_text(self):
        return self.__type_entry.get_text()

    def append_add_combobox(self):
        self.__type_combobox.append_text('添加')

    def get_combobox_active(self):
        return self.__type_combobox.get_active_text()

    def btn_cancel(self, widget):
        if self.get_type_text() == "" and self.get_text_view() == "":
            self.destroy()
            return
        if not self.is_save:
            CNotifyDlg('请先保存数据')
            return
        else:
            self.destroy()

    def get_text_view(self):
        start = self.__textView.get_buffer().get_start_iter()
        end = self.__textView.get_buffer().get_end_iter()
        return self.__textView.get_buffer().get_text(start, end)

    def btn_cb(self, widget, data):
        _text = self.get_text_view()
        _type = self.get_combobox_active()
        path = os.getcwd() + "/type/type_%s" % _type

        if "find" == data:
            self.set_is_save(True)
            if not os.path.exists(path):
                CNotifyDlg('未查找到%s病史' % _type)
                return
            fp = open(path, 'r')
            _text = ""
            i = 1
            for line in fp.readlines():
                if line.strip() == "":
                    continue
                _text += "%d:%s" % (i, line.strip().replace('|', '\n'))
                _text += '\n'
                i += 1
            self.set_text_view(_text)
            fp.close()
        elif "add" == data:
            if _text == "":
                return
            _type = self.get_type_text()
            path = os.getcwd() + "/type/type_%s" % _type
            self.set_is_save(True)
            if not os.path.exists(path):
                os.system("touch %s" % path)
            fp = open(path, 'a+')
            fp.write('\n\n')
            fp.write(_text.replace('\n', '|'))
            fp.close()
            CNotifyDlg('添加成功')
        elif "modify" == data:
            self.set_is_save(True)
            fp = open(path, 'w+')
            fp.write('\n\n')
            fp.write(_text.replace('\n', '|'))
            fp.close()
            CNotifyDlg('修改成功')

    def set_text_view(self, _text):
        self.__textView.get_buffer().set_text(_text)

    def set_editable(self, flag):
        self.__textView.set_editable(flag)

    def set_label(self, _title):
        self.title_label.set_text(_title)

    def set_window_title(self, _title):
        self.set_title(_title)

    def add_scroll(self, x, y):
        self.__textView.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        self.__textView.set_size_request(SUB_WINDOW_X - 50, 200)

        _scroll = gtk.ScrolledWindow()
        _scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        _scroll.set_size_request(SUB_WINDOW_X/2, 200)
        _scroll.add(self.__textView)
        self.fixed.put(_scroll, x, y)


class CFindData(BaseWindow):
    def __init__(self, _parent):
        super(CFindData, self).__init__(_parent)
        self.set_label("病史查询")
        self.init()
        self.show_all()
        self.hide_type_entry()

    def init(self):
        self.set_editable(False)
        self.set_is_save(True)
        self.ok_btn.connect("clicked", self.btn_cb, 'find')
        self.show_all()


class CModifyData(BaseWindow):
    def __init__(self, _parent):
        super(CModifyData, self).__init__(_parent)
        self.set_label("病史修改")
        self.show_all()
        self.set_is_save(False)
        self.init()
        self.show_all()
        self.hide_type_entry()

    def init(self):
        self.ok_btn.connect("clicked", self.btn_cb, "modify")
        self.set_btn_label('修改')
        _ok_btn = gtk.Button('查询')
        _ok_btn.set_size_request(80, 30)
        _ok_btn.connect("clicked", self.btn_cb, 'find')
        self.fixed.put(_ok_btn, SUB_WINDOW_X - 3*80 - 30, SUB_WINDOW_Y - 40)


class CAddData(BaseWindow):
    def __init__(self, _parent):
        super(CAddData, self).__init__(_parent)
        self.set_label("病史增加")
        self.init()
        self.set_is_save(False)
        self.show_all()
        self.hide_type_entry()
        self.append_add_combobox()

    def init(self):
        self.ok_btn.connect("clicked", self.btn_cb, 'add')


class CForgotPassword(BaseWindow):
    def __init__(self, _parent, _conf):
        super(CForgotPassword, self).__init__(_parent)
        self.set_window_title('忘记密码')
        self.set_label('忘记密码')

        self.phone_entry = gtk.Entry()
        self.new_password1 = gtk.Entry()
        self.new_password2 = gtk.Entry()
        self.__conf = _conf
        self.init()
        self.show_all()

    def init(self):
        _label_x = 100
        _label_y = 30
        _entry_x = 300
        _entry_y = 30

        start_x = (SUB_WINDOW_X - _label_x - _entry_x) / 2
        start_y = 150

        _label_phone = gtk.Label('电话:')
        modify_font(_label_phone, 15)
        _label_phone.set_size_request(_label_x, _label_y)
        self.fixed.put(_label_phone, start_x, start_y)

        self.phone_entry.set_size_request(_entry_x, _entry_y)
        self.fixed.put(self.phone_entry, start_x + _label_x, start_y)

        start_y += 50
        _label_password = gtk.Label('新密码:')
        modify_font(_label_password, 15)
        _label_password.set_size_request(_label_x, _label_y)
        self.fixed.put(_label_password, start_x, start_y)

        self.new_password1.set_size_request(_entry_x, _entry_y)
        self.new_password1.set_visibility(False)
        self.fixed.put(self.new_password1, start_x + _label_x, start_y)

        start_y += 50
        _label_password = gtk.Label('确认密码:')
        modify_font(_label_password, 15)
        _label_password.set_size_request(_label_x, _label_y)
        self.fixed.put(_label_password, start_x, start_y)

        self.new_password2.set_size_request(_entry_x, _entry_y)
        self.new_password2.set_visibility(False)
        self.fixed.put(self.new_password2, start_x + _label_x, start_y)

        self.ok_btn.connect("clicked", self.btn_cb, 'ok')

    def btn_cb(self, widet, opt):
        if 'ok' == opt:
            _phone = self.phone_entry.get_text()
            _phone_conf = self.__conf.get('user_info', 'phone_num')
            if _phone != _phone_conf:
                CNotifyDlg('电话信息不正确')
                return
            if self.new_password2.get_text() != self.new_password1.get_text():
                CNotifyDlg('两次密码输入不一致')
                return
            if len(self.new_password1.get_text()) < 6:
                CNotifyDlg('密码必须大于6位')
                return
            self.__conf.set('user_info', 'password', self.new_password1.get_text())
            CNotifyDlg('密码修改成功')
            self.destroy()


class CRegisterDlg(BaseWindow):
    def __init__(self, _parent, _conf):
        super(CRegisterDlg, self).__init__(_parent)
        self.set_window_title("用户注册")
        self.set_label("用户注册")
        self.user_entry = gtk.Entry()
        self.password_entry = gtk.Entry()
        self.password_entry1 = gtk.Entry()
        self.phone_entry = gtk.Entry()
        self.init()
        self.__conf = _conf
        self.show_all()

    def init(self):
        _label_x = 100
        _label_y = 30
        _entry_x = 300
        _entry_y = 30

        start_x = (SUB_WINDOW_X - _label_x - _entry_x)/2
        start_y = 150

        _label_user_name = gtk.Label('用户名:')
        modify_font(_label_user_name, 15)
        _label_user_name.set_size_request(_label_x, _label_y)
        self.fixed.put(_label_user_name, start_x, start_y)

        self.user_entry.set_size_request(_entry_x, _entry_y)
        self.fixed.put(self.user_entry, start_x + _label_x, start_y)

        start_y += 50
        _label_password = gtk.Label('密码:')
        modify_font(_label_password, 15)
        _label_password.set_size_request(_label_x, _label_y)
        self.fixed.put(_label_password, start_x, start_y)

        self.password_entry.set_size_request(_entry_x, _entry_y)
        self.password_entry.set_visibility(False)
        self.fixed.put(self.password_entry, start_x + _label_x, start_y)

        start_y += 50
        _label_password = gtk.Label('确认密码:')
        modify_font(_label_password, 15)
        _label_password.set_size_request(_label_x, _label_y)
        self.fixed.put(_label_password, start_x, start_y)

        self.password_entry1.set_size_request(_entry_x, _entry_y)
        self.password_entry1.set_visibility(False)
        self.fixed.put(self.password_entry1, start_x + _label_x, start_y)

        start_y += 50
        _label_phone = gtk.Label('电话:')
        modify_font(_label_phone, 15)
        _label_phone.set_size_request(_label_x, _label_y)
        self.fixed.put(_label_phone, start_x, start_y)

        self.phone_entry.set_size_request(_entry_x, _entry_y)
        self.fixed.put(self.phone_entry, start_x + _label_x, start_y)

        self.ok_btn.connect("clicked", self.btn_cb, 'ok')

    def btn_cb(self, widget, opt):
        if 'ok' == opt:
            _password1 = self.password_entry1.get_text()
            _password = self.password_entry.get_text()
            if _password != _password1:
                CNotifyDlg('密码输入不一致')
                return
            if len(_password) < 6:
                CNotifyDlg('密码必须大于6位')
                return
            _username = self.user_entry.get_text()
            _phone = self.phone_entry.get_text()
            if not _phone.isdigit():
                CNotifyDlg('电话必须是数字')
                return
            self.__conf.set('user_info', 'user_name', _username)
            self.__conf.set('user_info', 'password', _password)
            self.__conf.set('user_info', 'phone_num', _phone)

            self.destroy()
