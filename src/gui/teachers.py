#!/usr/bin/env python3

from gi.repository import Gtk
import logging
logger = logging.getLogger(__name__)

import gui
import core


def liststore_row(teacher):
    return [teacher.name]


class TeacherHandlers(gui.handlers.BaseHandlers):
    def teacher__add_ok(self, *args):
        name = self.runtime_state.builder.get_object(
            "teachers_add_window_name_entry").props.text
        if not len(name):
            return
        teacher = core.teacher.Teacher(name)
        self.runtime_state.state.teachers.append(teacher)
        store = self.runtime_state.builder.get_object("teachers_list_store")
        view = self.runtime_state.builder.get_object("teachers_tree_view")
        tree_iter = store.append(liststore_row(teacher))
        view.get_selection().select_iter(tree_iter)
        self.runtime_state.unsaved_changes = True
        self.teacher__add_cancel()

    def teacher__add_cancel(self, *args):
        self.runtime_state.builder.get_object(
            "teachers_add_window_name_entry").props.text = ''
        self.runtime_state.builder.get_object("teachers_add_window").hide()
        # Return True to prevent the window being destroyed
        return True
