#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import enum

import logging
logger = logging.getLogger(__name__)

import gui


class GridViewFilterType(enum.IntEnum):
    ALL = 0
    TEACHER = 1
    ROOM = 2
    BATCH = 3

grid_view_filiter_maps = [
    "table_view_filter_all_placeholder_combobox",
    "table_view_filter_teacher",
    "table_view_filter_room",
    "table_view_filter_batch"]


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

    def grid__type_change(self, *args):
        new_type = GridViewFilterType(
            self.runtime_state.builder.get_object(
                "table_view_type_selection_combobox").props.active)
        logger.debug("Switching grid view to %s", new_type)
        box = self.runtime_state.builder.get_object(
            "table_view_selection_homogenous_box")
        children = box.get_children()
        children.remove(
            self.runtime_state.builder.get_object(
                "table_view_type_selection_combobox"))
        assert(len(children) == 1)
        box.remove(children[0])
        box.add(
            self.runtime_state.builder.get_object(
                grid_view_filiter_maps[new_type]))
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
        schedule = self.runtime_state.state.population[sched_index]

        draw_type = GridViewFilterType(
            self.runtime_state.builder.get_object(
                "table_view_type_selection_combobox").props.active)
        logger.debug(
            "Drawing schedule %s by %s", sched_index, draw_type.name)
        if draw_type == GridViewFilterType.ALL:
            self.grid__draw_all(schedule)
        else:
            index = self.runtime_state.builder.get_object(
                grid_view_filiter_maps[draw_type]).props.active
            if index != -1:
                if draw_type == GridViewFilterType.BATCH:
                    self.grid__draw_by_batch(
                        schedule,
                        self.runtime_state.state.batches[index])
                elif draw_type == GridViewFilterType.TEACHER:
                    self.grid__draw_by_teacher(
                        schedule,
                        self.runtime_state.state.teachers[index])
                elif draw_type == GridViewFilterType.ROOM:
                    self.grid__draw_by_room(
                        schedule,
                        index)

    def grid__draw_by_batch(self, schedule, batch):
        viewport = self.runtime_state.builder.get_object(
            "timetable_viewport")
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        for day in range(self.runtime_state.state.prefs._n_days):
            text = "Day {}".format(day + 1)
            grid.attach(
                TransparentButton(text),
                (day + 1), 0, 1, 1)
        for time in range(self.runtime_state.state.prefs._n_times_per_day):
            text = "Time {}".format(time + 1)
            grid.attach(
                TransparentButton(text),
                0, time + 1, 1, 1)
        for time, slot in enumerate(schedule.slots[(None, None):]):
            text = ""
            for room, alloc in enumerate(slot):
                if alloc is not None and alloc.batch is batch:
                    text = "T:{teacher}\nS:{subject}\nR:{room}".format(
                        teacher=alloc.teacher.name,
                        subject=alloc.subject.name,
                        room=self.runtime_state.state.rooms[room].name)
            grid.attach(
                TransparentButton(text),
                (time // self.runtime_state.state.prefs._n_times_per_day
                    + 1),
                time % self.runtime_state.state.prefs._n_times_per_day + 1,
                1, 1)
        viewport.add(grid)
        viewport.show_all()

    def grid__draw_by_teacher(self, schedule, teacher):
        viewport = self.runtime_state.builder.get_object(
            "timetable_viewport")
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        for day in range(self.runtime_state.state.prefs._n_days):
            text = "Day {}".format(day + 1)
            grid.attach(
                TransparentButton(text),
                (day + 1), 0, 1, 1)
        for time in range(self.runtime_state.state.prefs._n_times_per_day):
            text = "Time {}".format(time + 1)
            grid.attach(
                TransparentButton(text),
                0, time + 1, 1, 1)
        for time, slot in enumerate(schedule.slots[(None, None):]):
            text = ""
            for room, alloc in enumerate(slot):
                if alloc is not None and alloc.teacher is teacher:
                    text = "B:{batch}\nS:{subject}\nR:{room}".format(
                        batch=alloc.batch.name,
                        subject=alloc.subject.name,
                        room=self.runtime_state.state.rooms[room].name)
            grid.attach(
                TransparentButton(text),
                (time // self.runtime_state.state.prefs._n_times_per_day
                    + 1),
                time % self.runtime_state.state.prefs._n_times_per_day + 1,
                1, 1)
        viewport.add(grid)
        viewport.show_all()

    def grid__draw_by_room(self, schedule, room):
        viewport = self.runtime_state.builder.get_object(
            "timetable_viewport")
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        for day in range(self.runtime_state.state.prefs._n_days):
            text = "Day {}".format(day + 1)
            grid.attach(
                TransparentButton(text),
                (day + 1), 0, 1, 1)
        for time in range(self.runtime_state.state.prefs._n_times_per_day):
            text = "Time {}".format(time + 1)
            grid.attach(
                TransparentButton(text),
                0, time + 1, 1, 1)
        for time, slot in enumerate(schedule.slots[(None, None):]):
            text = ""
            alloc = slot[room]
            if alloc is not None:
                text = "T:{teacher}\nS:{subject}\nB:{batch}".format(
                    teacher=alloc.teacher.name,
                    subject=alloc.subject.name,
                    batch=alloc.batch.name)
            grid.attach(
                TransparentButton(text),
                (time // self.runtime_state.state.prefs._n_times_per_day
                    + 1),
                time % self.runtime_state.state.prefs._n_times_per_day + 1,
                1, 1)
        viewport.add(grid)
        viewport.show_all()

    def grid__draw_all(self, schedule):
        viewport = self.runtime_state.builder.get_object(
            "timetable_viewport")
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        for day in range(self.runtime_state.state.prefs._n_days):
            text = "Day {}".format(day + 1)
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
