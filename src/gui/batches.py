#!/usr/bin/env python3

from gi.repository import Gtk
import logging
logger = logging.getLogger(__name__)

import gui
import core


def liststore_row(batch):
    return [batch.name, batch.n_students]


class BatchHandlers(gui.handlers.BaseHandlers):
    def batch__add_ok(self, *args):
        name = self.runtime_state.builder.get_object(
            "batches_add_window_name_entry").props.text
        if not len(name):
            return
        n_students = int(self.runtime_state.builder.get_object(
            "batches_add_window_capacity_adjustment").props.value)
        batch = core.batch.Batch(name, n_students)
        self.runtime_state.state.batches.append(batch)
        store = self.runtime_state.builder.get_object("batches_list_store")
        view = self.runtime_state.builder.get_object("batches_tree_view")
        tree_iter = store.append(liststore_row(batch))
        view.get_selection().select_iter(tree_iter)
        self.runtime_state.unsaved_changes = True
        self.batch__add_cancel()

    def batch__add_cancel(self, *args):
        self.runtime_state.builder.get_object(
            "batches_add_window_name_entry").props.text = ''
        self.runtime_state.builder.get_object("batches_add_window").hide()
        # Return True to prevent the window being destroyed
        return True
