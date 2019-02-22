#!/usr/bin/python

import os
import gtk
import sqlite3
import gobject
import ConfigParser
import pango
from gtk import gdk

WINDOW_X_SIZE = int(gdk.screen_width())
WINDOW_Y_SIZE = int(gdk.screen_height())

SUB_WINDOW_X = 800
SUB_WINDOW_Y = 600