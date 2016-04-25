#!/usr/bin/env python3

from gi.repository import Gtk
import logging
logger = logging.getLogger(__name__)

import gui
import core


def liststore_row(schedule):
    return [schedule.fitness]


class ScheduleHandlers(gui.handlers.BaseHandlers):
    def schedule__refresh(self, *args):
        logger.debug("Refreshing schedules")
        store = self.runtime_state.builder.get_object("schedules_list_store")
        view = self.runtime_state.builder.get_object("schedules_tree_view")
        logger.debug("Unselecting schedules")
        store.clear()
        view.get_selection().unselect_all()
        for i, schedule in enumerate(self.runtime_state.state.population):
            store.append([i] + liststore_row(schedule))
        logger.debug("Refreshed schedules")

    def evolve(self, *args):
        if ((self.runtime_state.state.prefs.n_times *
                len(self.runtime_state.state.rooms)) <
                len(self.runtime_state.state.allocations)):
            logger.debug("Infeasibly many allocations")
            dialog = self.runtime_state.builder.get_object(
                "infeasibly_many_allocations_dialog")
            dialog.run()
            dialog.hide()
            return
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
