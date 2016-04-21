#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import logging
logger = logging.getLogger(__name__)

import gui


class TransparentButton(Gtk.Button):
    def __init__(self, text):
        Gtk.Label.__init__(self, text)

        self.set_property("opacity", 1.0)
        self.set_property("expand", True)
        #self.set_selectable("True")
        #self.set_text("hi")
        self.show()

class GridHandler(
        gui.subjects.SubjectHandlers,
        gui.rooms.RoomHandlers,
        gui.teachers.TeacherHandlers,
        gui.batches.BatchHandlers,
        gui.allocations.AllocationHandlers,
        gui.handlers.BaseHandlers):
    def set_adjus1(self, *args):
        builder = self.runtime_state.builder
        adjustment1 = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        builder.get_object("swap1").set_adjustment(adjustment1)
        builder.get_object("swap1").set_value_as_int(builder.get_object("swap1").get_value_as_int())

    def set_adjus2(self, *args):
        builder = self.runtime_state.builder
        adjustment2 = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        builder.get_object("swap2").set_adjustment(adjustment2)
        builder.get_object("swap2").set_value_as_int(builder.get_object("swap2").get_value_as_int())

    def show_tt_win(self, sched_index, *args):
        builder = self.runtime_state.builder
        #builder.get_object("Grid_TT").show_all()
        #builder.connect_signals(Handler_Grid())
        #builder.get_object("timetable_scrolled_window")
        #print (builder.get_objects)
        tt_viewport = builder.get_object("timetable_viewport")
        grid = builder.get_object("timetable_viewport").get_child()
        if(grid is not None):
            grid.destroy()
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        schedule = self.runtime_state.state.population[sched_index]
        """text = ""
        for i in range(0, schedule._n_rooms):
            for v in range(0, schedule._n_times):
                builder.get_object("lecture_grid").attach(TransparentButton(text), i + 1, v + 2, 1, 1)
        builder.get_object("lecture_grid").show_all()
        """
        for day in range(self.runtime_state.state.prefs._n_days):
                text = "Day" + str(day + 1)
                grid.attach(TransparentButton(text), day * self.runtime_state.state.prefs._n_times_per_day + 1, 0, self.runtime_state.state.prefs._n_times_per_day, 1)
                for time in range(self.runtime_state.state.prefs._n_times_per_day):
                        text = "Time " + str(time + 1)
                        grid.attach(TransparentButton(text), (day * self.runtime_state.state.prefs._n_times_per_day + 1) + time, 1, 1, 1)
        #for day in range(self.runtime_state.state.prefs._n_days):
        #        for time in range(self.runtime_state.state.prefs._n_times_per_day):
        #                text = "Time " + str(time + 1)
        #                grid.attach(TransparentButton(text), day * time + 1, 1, 1, 1)

        for i, room in enumerate(self.runtime_state.state.rooms):
                text = room.name
                grid.attach(TransparentButton(text), 0, i + 2, 1, 1)
        for i in range(0, schedule._n_times):
            for v in range(0, schedule._n_rooms):
                #builder.timetable_scrolled_window.timetable_viewport.lecture_grid.attach(TransparentButton(), i, v, 1, 1)
                #text = str(i * 10 + v)
                if (schedule.slots[(i, v)] is None):
                    text = "-"
                else :
                    text = str(schedule.slots[(i,v)])
                grid.attach(TransparentButton(text), i + 1, v + 2, 1, 1)
                #lecture_grid.remove(self.grid.get_child_at(0, 0))
        tt_viewport.add(grid)
        tt_viewport.show_all()

    """
    def swap_lectures(self, *args):
        builder = self.runtime_state.builder
        #adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        #builder.get_object("swap1").set_adjustment(adjustment)
        #builder.get_object("swap2").set_adjustment(adjustment)
        swap1 = int(builder.get_object("swap1").get_value_as_int())
        swap2 = int(builder.get_object("swap2").get_value_as_int())
        swap1_column = swap1 % 10
        swap1_row = swap1 / 10
        swap2_column = swap2 % 10
        swap2_row = swap2 / 10

        item1 = str(builder.get_object("lecture_grid").get_child_at(swap1_row, swap1_column))
        item2 = str(builder.get_object("lecture_grid").get_child_at(swap2_row, swap2_column))

        builder.get_object("lecture_grid").attach(TransparentButton(item1), swap2_row, swap2_column, 1, 1)
        builder.get_object("lecture_grid").attach(TransparentButton(item2), swap1_row, swap1_column, 1, 1)
        #print (swap1)
        #print (swap2)
        builder.get_object("lecture_grid").show_all()
    """
