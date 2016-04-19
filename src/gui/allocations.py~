#!/usr/bin/env python3

from gi.repository import Gtk
import logging
logger = logging.getLogger(__name__)

import gui
import core


def liststore_row(allocation):
    return [allocation.subject.name,
            allocation.teacher.name,
            allocation.batch.name]


class AllocationHandlers(gui.handlers.BaseHandlers):
    def allocation__add_ok(self, *args):
        subject = self.runtime_state.builder.get_object(
            "allocations_add_window_subject_combobox").props.active
        teacher = self.runtime_state.builder.get_object(
            "allocations_add_window_teacher_combobox").props.active
        batch = self.runtime_state.builder.get_object(
            "allocations_add_window_batch_combobox").props.active
        if any(_ == -1 for _ in (subject, teacher, batch)):
            return
        subject = self.runtime_state.state.subjects[subject]
        teacher = self.runtime_state.state.teachers[teacher]
        batch = self.runtime_state.state.batches[batch]
        if ((self.runtime_state.state.prefs.n_times *
                len(self.runtime_state.state.rooms)) <
                len(self.runtime_state.state.allocations) + 1):
            dialog = self.runtime_state.builder.get_object(
                "infeasibly_many_allocations_dialog")
            res = dialog.run()
            dialog.hide()
            if (res == Gtk.ResponseType.CANCEL or res ==
                    Gtk.ResponseType.DELETE_EVENT):
                return
            else:
                raise RuntimeError(
                    "Unknown response from " +
                    "infeasibly many allocations dialog")
            return
        else:
            allocation = core.allocation.Allocation(
                batch=batch,
                subject=subject,
                teacher=teacher)
            self.runtime_state.state.allocations.append(allocation)
            del self.runtime_state.state.population[:]
            store = self.runtime_state.builder.get_object(
                "allocations_list_store")
            view = self.runtime_state.builder.get_object(
                "allocations_tree_view")
            tree_iter = store.append(liststore_row(allocation))
            view.get_selection().select_iter(tree_iter)
            self.runtime_state.unsaved_changes = True
        self.allocation__add_cancel()

    def allocation__add_cancel(self, *args):
        self.runtime_state.builder.get_object("allocations_add_window").hide()
        # Return True to prevent the window being destroyed
        return True
