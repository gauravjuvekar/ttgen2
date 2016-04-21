#!/usr/bin/env python3

from gi.repository import Gtk
import logging
logger = logging.getLogger(__name__)

import gui
import core


def liststore_row(room):
    return [room.pk, room.name, room.capacity]


class RoomHandlers(gui.handlers.BaseHandlers):
    def room__add_ok(self, *args):
        name = self.runtime_state.builder.get_object(
            "rooms_add_window_name_entry").props.text
        if not len(name):
            return
        capacity = int(self.runtime_state.builder.get_object(
            "rooms_add_window_capacity_adjustment").props.value)
        pk = len(self.runtime_state.state.rooms)
        room = core.room.Room(name, capacity, pk=pk)
        self.runtime_state.state.rooms.append(room)
        del self.runtime_state.state.population[:]
        store = self.runtime_state.builder.get_object("rooms_list_store")
        view = self.runtime_state.builder.get_object("rooms_tree_view")
        tree_iter = store.append(liststore_row(room))
        view.get_selection().select_iter(tree_iter)
        self.runtime_state.unsaved_changes = True
        self.room__add_cancel()

    def room__add_cancel(self, *args):
        self.runtime_state.builder.get_object(
            "rooms_add_window_name_entry").props.text = ''
        self.runtime_state.builder.get_object("rooms_add_window").hide()
        # Return True to prevent the window being destroyed
        return True

    def room__refresh(self, *args):
        store = self.runtime_state.builder.get_object("rooms_list_store")
        view = self.runtime_state.builder.get_object("rooms_tree_view")
        store.clear()
        for i, room in enumerate(self.runtime_state.state.rooms):
            store.append(liststore_row(room))
        view.get_selection().unselect_all()
