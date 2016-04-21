#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import logging
logger = logging.getLogger(__name__)

import gui


class TransparentButton(Gtk.Button):
    def __init__(self, text):
        Gtk.Button.__init__(self, text)
        self.set_property("opacity", 1.0)
        self.set_property("expand", True)


class DndButton(TransparentButton):
    def __init__(self, text, grid_pos):
        TransparentButton.__init__(self, text)
        self.grid_pos = grid_pos
        self.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [],
                             Gdk.DragAction.COPY)
        self.drag_dest_set(Gtk.DestDefaults.ALL, [],
                           Gdk.DragAction.COPY)
        self.drag_dest_set_target_list(None)
        self.drag_dest_add_text_targets()
        self.drag_source_set_target_list(None)
        self.drag_source_add_text_targets()

    def do_drag_data_get(self, context, selection, *args):
        print("Drag from", repr(self.grid_pos))
        selection.set_text(repr(self.grid_pos), -1)

    def do_drag_data_received(self, context, x, y, selection, *args):
        print("Drag to", self.grid_pos, "from", selection.get_text())


class GridHandler(
        gui.subjects.SubjectHandlers,
        gui.rooms.RoomHandlers,
        gui.teachers.TeacherHandlers,
        gui.batches.BatchHandlers,
        gui.allocations.AllocationHandlers,
        gui.handlers.BaseHandlers):
    def show_tt_win(self, sched_index, *args):
        builder = self.runtime_state.builder
        tt_viewport = builder.get_object("timetable_viewport")
        grid = builder.get_object("timetable_viewport").get_child()
        if(grid is not None):
            grid.destroy()
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        schedule = self.runtime_state.state.population[sched_index]
        for day in range(self.runtime_state.state.prefs._n_days):
            text = "Day" + str(day + 1)
            grid.attach(
                TransparentButton(text),
                (day * self.runtime_state.state.prefs._n_times_per_day + 1), 0,
                self.runtime_state.state.prefs._n_times_per_day, 1)
            for time in range(self.runtime_state.state.prefs._n_times_per_day):
                text = "Time " + str(time + 1)
                grid.attach(
                    TransparentButton(text),
                    (day * self.runtime_state.state.prefs._n_times_per_day +
                        1 + time), 1,
                    1, 1)
                for i, room in enumerate(self.runtime_state.state.rooms):
                    text = room.name
                    grid.attach(TransparentButton(text), 0, i + 2, 1, 1)
        for time in range(0, schedule._n_times):
            for room in range(0, schedule._n_rooms):
                if (schedule.slots[(time, room)] is None):
                    text = "-"
                else:
                    text = str(schedule.slots[(time, room)])
                grid.attach(
                    DndButton(text, (time, room)),
                    time + 1, room + 2,
                    1, 1)
        tt_viewport.add(grid)
        tt_viewport.show_all()
