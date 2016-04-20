#!/usr/bin/env python3

from gi.repository import Gtk
import logging
logger = logging.getLogger(__name__)

import gui
import core


def liststore_row(schedule):
    return [schedule._fitness]


class ScheduleHandlers(gui.handlers.BaseHandlers):
    def schedule__refresh(self, *args):
        logger.debug("Refreshing schedules")
        store = self.runtime_state.builder.get_object("schedules_list_store")
        view = self.runtime_state.builder.get_object("schedules_tree_view")
        store.clear()
        for i, schedule in enumerate(self.runtime_state.state.population):
            store.append([i] + liststore_row(schedule))
        view.get_selection().unselect_all()

    def schedule__redraw(self, *args):
        store = self.runtime_state.builder.get_object("schedules_list_store")
        view = self.runtime_state.builder.get_object("schedules_tree_view")
        tree_iter = view.get_selection().get_selected()[1]
        sched_index = int((store.get_value(tree_iter, 0)))
        self.show_tt_win(sched_index)

    def evolve(self, *args):
        logger.debug("Evolving")
        target_fitness = float(self.runtime_state.builder.get_object(
            "target_fitness_adjustment").props.value)
        max_generations = int(self.runtime_state.builder.get_object(
            "target_generations_adjustment").props.value)
        core.evolve.population_evolve(
            self.runtime_state.state,
            generations=max_generations,
            fitness=target_fitness)
        self.schedule__refresh()
        self.runtime_state.unsaved_changes = True
