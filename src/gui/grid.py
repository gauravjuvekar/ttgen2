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
    def __init__(self, text, grid_pos, callback_obj):
        TransparentButton.__init__(self, text)
        self.grid_pos = grid_pos
        self.callback_obj = callback_obj
        self.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [],
                             Gdk.DragAction.COPY)
        self.drag_dest_set(Gtk.DestDefaults.ALL, [],
                           Gdk.DragAction.COPY)
        self.drag_dest_set_target_list(None)
        self.drag_dest_add_text_targets()
        self.drag_source_set_target_list(None)
        self.drag_source_add_text_targets()

    def do_drag_data_get(self, context, selection, *args):
        send = repr(self.grid_pos)
        logger.debug("Drag from %s", send)
        selection.set_text(send, -1)

    def do_drag_data_received(self, context, x, y, selection, *args):
        src = eval(selection.get_text())
        dst = self.grid_pos
        logger.debug("Drag to %s from %s", dst, src)
        self.callback_obj.grid__dnd(src, dst)


class GridHandler(gui.handlers.BaseHandlers):
    def grid__clear(self, *args):
        grid = self.runtime_state.builder.get_object(
            "timetable_viewport").get_child()
        if(grid is not None):
            grid.destroy()

    def grid__dnd(self, src, dst, *args):
        store = self.runtime_state.builder.get_object("schedules_list_store")
        view = self.runtime_state.builder.get_object("schedules_tree_view")
        tree_iter = view.get_selection().get_selected()[1]
        if tree_iter is None:
            raise RuntimeError("Schedule must be selected for dnd to occur")
        sched_index = store.get_value(tree_iter, 0)
        sched = self.runtime_state.state.population[sched_index]
        sched.swap(src, dst)
        # Column 1 is the fitness column
        new_model_fitness = gui.schedules.liststore_row(sched)[0]
        logger.debug("Post user swap fitness %s", new_model_fitness)
        store.set_value(tree_iter, 1, new_model_fitness)
        self.grid__redraw()

    def grid__redraw(self, *args):
        logger.debug("Redrawing grid")
        self.grid__clear()

        store = self.runtime_state.builder.get_object("schedules_list_store")
        view = self.runtime_state.builder.get_object("schedules_tree_view")
        tree_iter = view.get_selection().get_selected()[1]
        if tree_iter is None:
            logger.debug("No selected schedule to draw")
            return

        sched_index = store.get_value(tree_iter, 0)
        logger.debug("Drawing schedule %s", sched_index)
        viewport = self.runtime_state.builder.get_object(
            "timetable_viewport")
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
                    text = ""
                else:
                    text = str(schedule.slots[(time, room)])
                grid.attach(
                    DndButton(text, (time, room), self),
                    time + 1, room + 2,
                    1, 1)
        viewport.add(grid)
        viewport.show_all()
