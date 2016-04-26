#!/usr/bin/env python3

from gi.repository import Gtk
import logging
logger = logging.getLogger(__name__)

import gui
import enum


class Tabs(enum.IntEnum):
    ALLOCATIONS = 0
    SCHEDULES = 1
    TEACHERS = 2
    ROOMS = 3
    BATCHES = 4
    SUBJECTS = 5


class NotebookHandlers(
        gui.subjects.SubjectHandlers,
        gui.rooms.RoomHandlers,
        gui.teachers.TeacherHandlers,
        gui.batches.BatchHandlers,
        gui.allocations.AllocationHandlers,
        gui.schedules.ScheduleHandlers,
        gui.handlers.BaseHandlers):
    def notebook__switch_page(self, notebook, page, page_num, *args):
        add_button = self.runtime_state.builder.get_object(
            "notebook_add_button")
        remove_button = self.runtime_state.builder.get_object(
            "notebook_remove_button")
        if page_num == Tabs.SCHEDULES:
            add_button.set_sensitive(False)
            remove_button.set_sensitive(False)
        else:
            add_button.set_sensitive(True)
            remove_button.set_sensitive(True)

    def notebook__refresh(self, *args):
        logger.debug("Refreshing all notebooks")
        self.subject__refresh()
        self.room__refresh()
        self.teacher__refresh()
        self.batch__refresh()
        self.allocation__refresh()
        self.schedule__refresh()

    def notebook__remove(self, *args):
        current_tab = Tabs(
            self.runtime_state.builder.get_object(
                "notebook").get_current_page())
        self.notebook__remove_cb[current_tab](self)
        del self.runtime_state.state.population[:]
        self.notebook__refresh()
        self.runtime_state.unsaved_changes = True

    def notebook__add(self, *args):
        current_tab = Tabs(
            self.runtime_state.builder.get_object(
                "notebook").get_current_page())
        self.notebook__add_cb[current_tab](self)

    def notebook__remove_allocation(self, *args):
        store = self.runtime_state.builder.get_object("allocations_list_store")
        view = self.runtime_state.builder.get_object("allocations_tree_view")
        tree_iter = view.get_selection().get_selected()[1]
        if tree_iter is None:
            return
        else:
            index = store.get_value(tree_iter, 0)
            del self.runtime_state.state.allocations[index]

    def notebook__remove_schedule(self, *args):
        raise RuntimeError("Schedule should not be removable from GUI")

    def notebook__remove_teacher(self, *args):
        store = self.runtime_state.builder.get_object("teachers_list_store")
        view = self.runtime_state.builder.get_object("teachers_tree_view")
        tree_iter = view.get_selection().get_selected()[1]
        if tree_iter is None:
            return
        else:
            index = store.get_value(tree_iter, 0)
            teach = self.runtime_state.state.teachers[index]
            del self.runtime_state.state.teachers[index]
            self.runtime_state.state.allocations = [
                x for x in self.runtime_state.state.allocations if
                x.teacher != teach]

    def notebook__remove_batch(self, *args):
        store = self.runtime_state.builder.get_object("batches_list_store")
        view = self.runtime_state.builder.get_object("batches_tree_view")
        tree_iter = view.get_selection().get_selected()[1]
        if tree_iter is None:
            return
        else:
            index = store.get_value(tree_iter, 0)
            batch = self.runtime_state.state.batches[index]
            del self.runtime_state.state.batches[index]
            self.runtime_state.state.allocations = [
                x for x in self.runtime_state.state.allocations if
                x.batch != batch]

    def notebook__remove_subject(self, *args):
        store = self.runtime_state.builder.get_object("subjects_list_store")
        view = self.runtime_state.builder.get_object("subjects_tree_view")
        tree_iter = view.get_selection().get_selected()[1]
        if tree_iter is None:
            return
        else:
            index = store.get_value(tree_iter, 0)
            sub = self.runtime_state.state.subjects[index]
            del self.runtime_state.state.subjects[index]
            self.runtime_state.state.allocations = [
                x for x in self.runtime_state.state.allocations if
                x.subject != sub]

    def notebook__remove_room(self, *args):
        store = self.runtime_state.builder.get_object("rooms_list_store")
        view = self.runtime_state.builder.get_object("rooms_tree_view")
        tree_iter = view.get_selection().get_selected()[1]
        if tree_iter is None:
            return
        else:
            index = store.get_value(tree_iter, 0)
            del self.runtime_state.state.rooms[index]
            for i, room in enumerate(self.runtime_state.state.rooms):
                room.pk = i

    def notebook__add_allocation(self, *args):
        self.runtime_state.builder.get_object(
            "allocations_add_window").show_all()

    def notebook__add_schedule(self, *args):
        raise RuntimeError(
            "Cannot add schedule directly. " +
            "Option should not have been sensitive")

    def notebook__add_teacher(self, *args):
        self.runtime_state.builder.get_object(
            "teachers_add_window").show_all()

    def notebook__add_room(self, *args):
        self.runtime_state.builder.get_object(
            "rooms_add_window").show_all()

    def notebook__add_batch(self, *args):
        self.runtime_state.builder.get_object(
            "batches_add_window").show_all()

    def notebook__add_subject(self, *args):
        self.runtime_state.builder.get_object(
            "subjects_add_window").show_all()

    notebook__remove_cb = {
        Tabs.ALLOCATIONS: notebook__remove_allocation,
        Tabs.SCHEDULES: notebook__remove_schedule,
        Tabs.TEACHERS: notebook__remove_teacher,
        Tabs.ROOMS: notebook__remove_room,
        Tabs.BATCHES: notebook__remove_batch,
        Tabs.SUBJECTS: notebook__remove_subject}

    notebook__add_cb = {
        Tabs.ALLOCATIONS: notebook__add_allocation,
        Tabs.SCHEDULES: notebook__add_schedule,
        Tabs.TEACHERS: notebook__add_teacher,
        Tabs.ROOMS: notebook__add_room,
        Tabs.BATCHES: notebook__add_batch,
        Tabs.SUBJECTS: notebook__add_subject}
