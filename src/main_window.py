# main_window.py
#
# Copyright 2020 Muhammad Rivan Febrian <rivanfebrian123@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk
from .gi_composites import GtkTemplate
from .fnr_window import FindAndReplaceWindow


@GtkTemplate(ui='/org/gnome/Lofindandreplacedesign/main_window.ui')
class MainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "MainWindow"

    # Child widgets. Keep them alphabeticaly sorted
    btn_create = GtkTemplate.Child()
    btn_find_and_replace = GtkTemplate.Child()
    flowbox_type = GtkTemplate.Child()
    headerbar_fnr = GtkTemplate.Child()
    stk_content = GtkTemplate.Child()
    stk_headerbar = GtkTemplate.Child()
    textview_text = GtkTemplate.Child()
    textbuffer_buffer = GtkTemplate.Child()

    # Null objects. Keep them alphabeticaly sorted
    fnr_window = None

    #---------------------------------
    # The init function
    #
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        # Cursor iter should be placed correctly
        self.textbuffer_buffer.place_cursor(
            self.textbuffer_buffer.get_start_iter())

    #--------------------------------------
    # Callbacks functions / procedures. Keep them alphabeticaly sorted
    #
    @GtkTemplate.Callback
    def on_btn_create_clicked(self, widget):
        child_name = self.flowbox_type.get_selected_children()[0].get_name()
        header_title = ""

        if child_name == "writer":
            header_title = "My Awesome Journal"
        elif child_name == "calc":
            header_title = "My Amazing Spreadsheet"
        elif child_name == "impress":
            header_title = "My Friendly Presentation"
        elif child_name == "draw":
            header_title = "My Elegant Design"
        elif child_name == "math":
            header_title = "My Number One Math Formula"
        elif child_name == "base":
            header_title = "My Website Database"

        self.headerbar_fnr.set_title(header_title)
        self.stk_headerbar.set_visible_child_name("fnr")
        self.stk_content.set_visible_child_name(child_name)

    @GtkTemplate.Callback
    def on_btn_find_and_replace_clicked(self, widget):
        if not self.fnr_window:
            self.fnr_window = FindAndReplaceWindow(transient_for=self)
            self.fnr_window.connect(
                "destroy", self.on_fnr_window_destroy)
        self.fnr_window.present()

    @GtkTemplate.Callback
    def on_btn_new_document_clicked(self, widget):
        self.stk_headerbar.set_visible_child_name("greeter")
        self.stk_content.set_visible_child_name("greeter")

    def on_fnr_window_destroy(self, widget):
        self.fnr_window = None
