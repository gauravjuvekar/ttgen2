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
        gui.handlers.BaseHandlers):
    def notebook__switch_page(self, notebook, page, page_num, *args):
        add_button = self.runtime_state.builder.get_object(
            "notebook_add_button")
        if page_num == Tabs.SCHEDULES:
            add_button.set_sensitive(False)
        else:
            add_button.set_sensitive(True)

    def notebook__remove(self, *args):
        current_tab = Tabs(
            self.runtime_state.builder.get_object(
                "notebook").get_current_page())
        self.notebook__remove_cb[current_tab](self)

    def notebook__add(self, *args):
        current_tab = Tabs(
            self.runtime_state.builder.get_object(
                "notebook").get_current_page())
        self.notebook__add_cb[current_tab](self)

    def notebook__remove_allocation(self, *args):
        print("removing allocation")

    def notebook__remove_schedule(self, *args):
        print("removing schedule")

    def notebook__remove_teacher(self, *args):
        print("removing teacher")

    def notebook__remove_room(self, *args):
        print("removing room")

    def notebook__remove_batch(self, *args):
        print("removing batch")

    def notebook__remove_subject(self, *args):
        print("removing subject")

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