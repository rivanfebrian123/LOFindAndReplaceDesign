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
    btn_find_and_replace = GtkTemplate.Child()
    textview_text = GtkTemplate.Child()
    textbuffer_buffer = GtkTemplate.Child()

    # Null objects. Keep them alphabeticaly sorted
    fnr_window = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        # Cursor iter should placed correctly
        self.textbuffer_buffer.place_cursor(
            self.textbuffer_buffer.get_start_iter())

    @GtkTemplate.Callback
    def on_btn_find_and_replace_clicked(self, widget):
        if not self.fnr_window:
            self.fnr_window = FindAndReplaceWindow(transient_for=self)
            self.fnr_window.connect(
                "destroy", self.on_fnr_window_destroy)
        self.fnr_window.present()

    def on_fnr_window_destroy(self, widget):
        self.fnr_window = None
