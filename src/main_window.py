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

    # Child widgets. Keep them alphabetically sorted
    btn_create = GtkTemplate.Child()
    btn_find_and_replace = GtkTemplate.Child()
    btn_go_to_writer = GtkTemplate.Child()
    flwbox_type = GtkTemplate.Child()
    hdrbar_fnr = GtkTemplate.Child()
    img_selection = GtkTemplate.Child()
    stk_content = GtkTemplate.Child()
    stk_header = GtkTemplate.Child()
    txtview_text = GtkTemplate.Child()
    txtbfr_buffer = GtkTemplate.Child()

    # Null objects. Keep them alphabetically sorted
    fnr_window = None
    selected_child_name = ""

    # Properties' storage. Keep them alphabetically sorted
    _visible_sub_app = ""

    #---------------------------------
    # The init function
    #
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        # Cursor iter should be placed correctly
        self.txtbfr_buffer.place_cursor(self.txtbfr_buffer.get_start_iter())

    #-----------------------------------
    # Properties. Keep them alphabetically sorted
    #
    # Visible Sub App property
    def get_visible_sub_app(self):
        return self._visible_sub_app

    def set_visible_sub_app(self, value):
        self._visible_sub_app = value

        header_title = ""

        if self.fnr_window:
            self.fnr_window.destroy()
        if value == "greeter":
            self.stk_header.set_visible_child_name("greeter")
            self.stk_content.set_visible_child_name("greeter")
        else:
            if value == "writer":
                header_title = "My Awesome Journal"
                self.stk_content.set_visible_child_name("writer")
            else:
                if value == "calc":
                    header_title = "My Amazing Spreadsheet"
                elif value == "impress":
                    header_title = "My Friendly Presentation"
                elif value == "draw":
                    header_title = "My Elegant Design"
                self.img_selection.set_from_icon_name(
                    "libreoffice-" + value, 192)
                self.stk_content.set_visible_child_name("nothing")
            self.hdrbar_fnr.set_title(header_title)
            self.stk_header.set_visible_child_name("fnr")

    #--------------------------------------
    # Callbacks functions / procedures. Keep them alphabetically sorted
    #
    @GtkTemplate.Callback
    def on_btn_create_clicked(self, widget):
        self.set_visible_sub_app(self.selected_child_name)

    @GtkTemplate.Callback
    def on_btn_find_and_replace_clicked(self, widget):
        if not self.fnr_window:
            self.fnr_window = FindAndReplaceWindow(transient_for=self)
            self.fnr_window.connect(
                "destroy", self.on_fnr_window_destroy)
        self.fnr_window.present()

    @GtkTemplate.Callback
    def on_btn_go_to_writer_clicked(self, widget):
        self.set_visible_sub_app("writer")

    @GtkTemplate.Callback
    def on_btn_new_document_clicked(self, widget):
        self.set_visible_sub_app("greeter")

    @GtkTemplate.Callback
    def on_flwbox_type_selected_children_changed(self, widget):
        child = self.flwbox_type.get_selected_children()[0]
        active = child.get_sensitive()

        if active:
            self.selected_child_name = child.get_name()
        self.btn_create.set_sensitive(active)

    def on_fnr_window_destroy(self, widget):
        self.fnr_window = None
