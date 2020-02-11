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
    btnbox_existing_text = GtkTemplate.Child()
    btnbox_replace_with = GtkTemplate.Child()
    chkbtn_use_regex = GtkTemplate.Child()
    chkbtn_use_similarity_srch = GtkTemplate.Child()
    chkbtn_whole_word = GtkTemplate.Child()
    img_search_notif = GtkTemplate.Child()
    lbl_search_notif = GtkTemplate.Child()
    menubtn_existing_text = GtkTemplate.Child()
    menubtn_replace_with = GtkTemplate.Child()
    menubtn_sound_like = GtkTemplate.Child()
    menubtn_use_similarity_srch = GtkTemplate.Child()
    rvlr_advanced_options = GtkTemplate.Child()
    rvlr_replace_with = GtkTemplate.Child()
    rvlr_search_notif = GtkTemplate.Child()
    stk_find_or_replace = GtkTemplate.Child()
    srchent_existing_text = GtkTemplate.Child()
    srchent_replace_with = GtkTemplate.Child()
    tglbtn_replace = GtkTemplate.Child()

    # Null objects. Keep them alphabeticaly sorted
    parent = Gtk.ApplicationWindow()

    # Other variables. Keep them alphabeticaly sorted
    search_flag = Gtk.TextSearchFlags.CASE_INSENSITIVE

    # Properties' storage. Keep them alphabeticaly sorted
    _replace_mode = True
    _advanced_mode = False

    #---------------------------------
    # The init function
    #
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        # Set null variables
        self.parent = self.get_transient_for()
        self.parent_handler = self.parent.textbuffer_buffer.connect(
            "mark-set", self.on_parent_textbuffer_mark_set)

        # We've to set these properties manually because GtkTemplate
        # doesn't do it well. Keep them alphabeticaly sorted
        self.btnbox_existing_text.set_homogeneous(False)
        self.btnbox_replace_with.set_homogeneous(False)
        self.menubtn_sound_like.set_sensitive(False)
        self.menubtn_use_similarity_srch.set_sensitive(False)

        # Init widgets
        parent_selected_text = \
            self.match_parent_selected_text(self.search_flag)[2]

        if parent_selected_text:
            self.srchent_existing_text.set_text(parent_selected_text)

    #-----------------------------------
    # Properties. Keep them alphabeticaly sorted
    #
    # Advanced Mode property
    def get_advanced_mode(self):
        return self._advanced_mode

    def set_advanced_mode(self, value):
        # Save the value first
        self._advanced_mode = value

        # Refresh the integrations
        self.rvlr_advanced_options.set_reveal_child(value)
        self.menubtn_existing_text.set_visible(value)
        self.menubtn_replace_with.set_visible(value)

    # Replace Mode property
    def get_replace_mode(self):
        return self._replace_mode

    def set_replace_mode(self, value):
        widget = self.btn_find_or_replace_all
        stylectx = widget.get_style_context()

        # Save the value first
        self._replace_mode = value

        # Refresh the integrations
        self.rvlr_replace_with.set_reveal_child(value)
        if value:
            stylectx.add_class("destructive-action")
            widget.set_label("Replace All")
        else:
            stylectx.remove_class("destructive-action")
            widget.set_label("Find All")
        self.refresh_match_integration()

    #---------------------------------------------
    # Integration refreshment functions / procedures. Keep them
    # alphabeticaly sorted
    #
    def refresh_match_integration(self):
        matching, keyword = \
            self.match_parent_selected_text(self.search_flag)[0:2]
        widget = self.stk_find_or_replace

        widget.set_sensitive(keyword != "")
        if matching:
            if self.get_replace_mode():
                widget.set_visible_child_name("replace_act")
            else:
                widget.set_visible_child_name("main_act")
        else:
            widget.set_visible_child_name("main_act")

    #-----------------------------------
    # Other functions / procedures. Keep them alphabeticaly sorted
    #
    def find_and_select(self, direction):
        selected_text_matching, keyword, y, _buffer, selection_bounds = \
            self.match_parent_selected_text(self.search_flag)
        search_options = keyword, self.search_flag, None
        cursor_iter = Gtk.TextIter()
        found = False
        match = None
        icon = ""
        label = ""

        if selected_text_matching:
            if direction == Direction.FORWARD:
                cursor_iter = selection_bounds[1]
            elif direction == Direction.BACKWARD:
                cursor_iter = selection_bounds[0]
        else:
            cursor_iter = _buffer.get_iter_at_mark(_buffer.get_insert())

        for x in range(2):
            # Search once more from the start or the end of the documents
            # if nothing matching at first trial
            if direction == Direction.FORWARD:
                if x == 1:
                    cursor_iter = _buffer.get_start_iter()
                match = cursor_iter.forward_search(*search_options)
            elif direction == Direction.BACKWARD:
                if x == 1:
                    cursor_iter = _buffer.get_end_iter()
                match = cursor_iter.backward_search(*search_options)

            if match:
                found = True
                if x == 1:
                    icon = "dialog-information-symbolic"
                    if direction == Direction.FORWARD:
                        label = "Reached the end of the document"
                    elif direction == Direction.BACKWARD:
                        label = "Reached the beginning of the document"
                break

        if found:
            _buffer.select_range(*match)
        else:
            icon = "dialog-error-symbolic"
            label = "Search key not found"

        if label:
            self.lbl_search_notif.set_label(label)
            self.img_search_notif.set_from_icon_name(
                icon, Gtk.IconSize.LARGE_TOOLBAR)
            self.rvlr_search_notif.set_reveal_child(True)

    def match_parent_selected_text(self, flag):
        _buffer = self.parent.textbuffer_buffer
        selection_bounds = _buffer.get_selection_bounds()
        selected_text = ""
        keyword = self.srchent_existing_text.get_text()
        matching = False

        if selection_bounds:
            selected_text = _buffer.get_text(*selection_bounds, True)
            if keyword:
                if flag == Gtk.TextSearchFlags.CASE_INSENSITIVE:
                    keyword = keyword.lower()
                    selected_text = selected_text.lower()
                if selected_text == keyword:
                    matching = True

        return matching, keyword, selected_text, _buffer, selection_bounds

    #--------------------------------------
    # Callbacks functions / procedures. Keep them alphabeticaly sorted
    #
    @GtkTemplate.Callback
    def on_btn_close_search_notif_clicked(self, widget):
        self.rvlr_search_notif.set_reveal_child(False)

    @GtkTemplate.Callback
    def on_btn_find_next_clicked(self, widget):
        self.find_and_select(Direction.FORWARD)

    @GtkTemplate.Callback
    def on_btn_find_previous_clicked(self, widget):
        self.find_and_select(Direction.BACKWARD)

    @GtkTemplate.Callback
    def on_btn_replace_clicked(self, widget):
        matching, x, y, _buffer, z = \
            self.match_parent_selected_text(self.search_flag)

        if matching:
            _buffer.delete_selection(False, False)
            _buffer.insert_at_cursor(self.srchent_replace_with.get_text(), -1)
        self.stk_find_or_replace.set_visible_child_name("main_act")

    @GtkTemplate.Callback
    def on_btn_skip_clicked(self, widget):
        self.stk_find_or_replace.set_visible_child_name("main_act")

    @GtkTemplate.Callback
    def on_chkbtn_sound_like_toggled(self, widget):
        self.menubtn_sound_like.set_sensitive(widget.get_active())

    @GtkTemplate.Callback
    def on_chkbtn_use_regex_toggled(self, widget):
        active = widget.get_active()

        self.chkbtn_use_similarity_srch.set_sensitive(not active)
        self.chkbtn_whole_word.set_sensitive(not active)
        self.chkbtn_whole_word.set_inconsistent(active)

    @GtkTemplate.Callback
    def on_chkbtn_use_similarity_srch_toggled(self, widget):
        active = widget.get_active()

        self.menubtn_use_similarity_srch.set_sensitive(active)
        self.chkbtn_use_regex.set_sensitive(not active)

    @GtkTemplate.Callback
    def on_FindAndReplaceWindow_destroy(self, widget):
        self.parent.textbuffer_buffer.disconnect(self.parent_handler)

    @GtkTemplate.Callback
    def on_tglbtn_replace_toggled(self, widget):
        self.set_replace_mode(widget.get_active())

    def on_parent_textbuffer_mark_set(self, location, mark, widget):
        self.refresh_match_integration()

    @GtkTemplate.Callback
    def on_rdbtn_options_mode_toggled(self, widget):
        self.set_advanced_mode(widget.get_name() == "advanced_mode")

    @GtkTemplate.Callback
    def on_srchent_existing_text_changed(self, widget):
        self.refresh_match_integration()
