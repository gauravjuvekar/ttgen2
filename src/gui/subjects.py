#!/usr/bin/env python3

from gi.repository import Gtk
import logging
logger = logging.getLogger(__name__)

import gui
import core


def liststore_row(subject):
    return [subject.name]


class SubjectHandlers(gui.handlers.BaseHandlers):
    def subject__add_ok(self, *args):
        name = self.runtime_state.builder.get_object(
            "subjects_add_window_name_entry").props.text
        if not len(name):
            return
        subject = core.subject.Subject(name)
        self.runtime_state.state.subjects.append(subject)
        store = self.runtime_state.builder.get_object("subjects_list_store")
        view = self.runtime_state.builder.get_object("subjects_tree_view")
        tree_iter = store.append(liststore_row(subject))
        view.get_selection().select_iter(tree_iter)
        self.runtime_state.unsaved_changes = True
        self.subject__add_cancel()

    def subject__add_cancel(self, *args):
        self.runtime_state.builder.get_object(
            "subjects_add_window_name_entry").props.text = ''
        self.runtime_state.builder.get_object("subjects_add_window").hide()
        # Return True to prevent the window being destroyed
        return True

    def subject__refresh(self, *args):
        store = self.runtime_state.builder.get_object("subjects_list_store")
        view = self.runtime_state.builder.get_object("subjects_tree_view")
        store.clear()
        for subject in self.runtime_state.state.subjects:
            store.append(liststore_row(subject))
        view.get_selection().unselect_all()
