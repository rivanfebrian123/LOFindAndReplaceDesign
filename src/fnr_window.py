# fnr_window.py
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

class Direction():
    FORWARD = 0
    BACKWARD = 1
    WHOLE_DOCUMENT = 2

@GtkTemplate(ui='/org/gnome/Lofindandreplacedesign/fnr_window.ui')
class FindAndReplaceWindow(Gtk.Window):
    __gtype_name__ = "FindAndReplaceWindow"

    # Child widgets. Keep them alphabeticaly sorted
    btn_find_previous = GtkTemplate.Child()
    btn_find_or_replace_all = GtkTemplate.Child()
    btn_replace = GtkTemplate.Child()
    btn_skip = GtkTemplate.Child()
    btnbox_find_or_replace_styles = GtkTemplate.Child()
    chkbtn_use_regex = GtkTemplate.Child()
    chkbtn_use_similarity_srch = GtkTemplate.Child()
    chkbtn_whole_word = GtkTemplate.Child()
    img_search_notif = GtkTemplate.Child()
    lbl_search_notif = GtkTemplate.Child()
    menubtn_find_or_replace_styles = GtkTemplate.Child()
    menubtn_sound_like = GtkTemplate.Child()
    menubtn_use_similarity_srch = GtkTemplate.Child()
    rvlr_options = GtkTemplate.Child()
    rvlr_find_or_replace_styles = GtkTemplate.Child()
    rvlr_replace_with = GtkTemplate.Child()
    rvlr_search_notif = GtkTemplate.Child()
    stk_find_or_replace = GtkTemplate.Child()
    srchent_existing_text = GtkTemplate.Child()
    srchent_replace_with = GtkTemplate.Child()
    tglbtn_replace = GtkTemplate.Child()

    # Null objects. Keep them alphabeticaly sorted
    parent = Gtk.ApplicationWindow()
    whole_word_last_active = false

    # Properties' storage. Keep them alphabeticaly sorted
    _replace_mode = True
    _advanced_mode = False


    #
    # The init function
    #
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        self.parent = self.get_transient_for()
        self.parent.textbuffer_buffer.connect(
            "mark-set", self.on_parent_textbuffer_mark_set) #FIXME

        # We've to set these properties manually because GtkTemplate
        # doesn't do it well. Keep them alphabeticaly sorted
        self.btnbox_find_or_replace_styles.set_homogeneous(False)
        self.menubtn_find_or_replace_styles.set_sensitive(False)
        self.menubtn_sound_like.set_sensitive(False)
        self.menubtn_use_similarity_srch.set_sensitive(False)

    #
    # Properties
    #
    #### Advanced Mode property
    def get_advanced_mode(self):
        return self._advanced_mode

    def set_advanced_mode(self, value):
        self.rvlr_options.set_reveal_child(value)
        self.refresh_replace_mode_integration() #FIXME
        # save the value
        self._advanced_mode = value

    #### Replace Mode property
    def get_replace_mode(self):
        return self._replace_mode

    def set_replace_mode(self, value):
        widget = self.btn_find_or_replace_all
        stylectx = widget.get_style_context()

        self.rvlr_replace_with.set_reveal_child(value)
        if value:
            stylectx.add_class("destructive-action")
            widget.set_label("Replace All")
        else:
            stylectx.remove_class("destructive-action")
            widget.set_label("Find All")
        # save the value
        self._replace_mode = value

    #
    # Integration refreshment functions / procedures
    #
    def refresh_match_integration(self):
        matching = self.match_parent_selected_text()[0]
        widget = self.stk_find_or_replace

        if matching:
            if self.get_replace_mode():
                widget.set_visible_child_name("replace-act")
            else:
                widget.set_visible_child_name("main-act")
        else:
            widget.set_visible_child_name("main-act")

    def refresh_replace_mode_integration(self):
        active = self.get_replace_mode()
        widget = self.rvlr_find_or_replace_styles

        if self.get_advanced_mode():
            widget.set_reveal_child(active)
        else:
            widget.set_reveal_child(False)

    #
    # Other functions / procedures
    #
    def match_parent_selected_text(self):
        _buffer = self.parent.textbuffer_buffer
        selection_bounds = _buffer.get_selection_bounds()
        selected_text = _buffer.get_text(*selection_bounds, True)
        keyword = self.srchent_existing_text.get_text()
        matching = False

        # Make sure that keyword is not a null object, and compare it
        # with the selected text
        if selection_bounds and keyword and selected_text == keyword:
            matching = True

        return matching, keyword, _buffer, selection_bounds

    #FIXME

    def find_and_select(self, direction):
        matching, keyword, _buffer, selection_bounds = \
            match_parent_selected_text()
        search_options = keyword, Gtk.TextSearchFlags.CASE_INSENSITIVE, None
        cursor_iter = Gtk.TextIter()
        found = False
        match = None
        icon = ""
        label = ""

        if matching:
            