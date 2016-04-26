#!/usr/bin/env python3

from gi.repository import Gtk
import pickle
import logging
logger = logging.getLogger(__name__)

import gui
import state


class MenubarHandlers(
        gui.notebook.NotebookHandlers,
        gui.handlers.BaseHandlers):
    def menubar__file__new(self, *args):
        if not gui.file_save.save_if_unsaved_changes(self.runtime_state):
            return
        else:
            self.runtime_state.filename = None
            self.runtime_state.state = state.State()
            self.runtime_state.unsaved_changes = False
            self.notebook__refresh()

    def menubar__file__open(self, *args):
        if not gui.file_save.save_if_unsaved_changes(self.runtime_state):
            return
        else:
            dialog = Gtk.FileChooserDialog(
                "Open file",
                parent=self.runtime_state.builder.get_object("main_window"),
                action=Gtk.FileChooserAction.OPEN,
                buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))
            res = dialog.run()
            if res == Gtk.ResponseType.ACCEPT:
                file_name = dialog.get_filename()
            elif res in (Gtk.ResponseType.CANCEL,
                         Gtk.ResponseType.DELETE_EVENT):
                return
            else:
                raise RuntimeError()
            logger.debug("Opening file %s", file_name)
            dialog.destroy()
            with open(file_name, 'rb') as f:
                try:
                    self.runtime_state.state = pickle.load(f)
                except pickle.UnpicklingError:
                    dialog = Gtk.MessageDialog(
                        "Cannot open that file",
                        parent=(self.runtime_state.
                                builder.get_object("main_window")),
                        flags=(Gtk.DialogFlags.MODAL |
                               Gtk.DialogFlags.DESTROY_WITH_PARENT),
                        message_type=Gtk.MessageType.ERROR,
                        buttons=(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE),
                        text="Error reading file {}".format(file_name),
                        title="Cannot open file")
                    dialog.run()
                    dialog.destroy()
                else:
                    self.runtime_state.filename = file_name
                    self.notebook__refresh()

    def menubar__file__save(self, *args):
        gui.file_save.save(self.runtime_state)

    def menubar__file__saveas(self, *args):
        old_name = self.runtime_state.filename
        self.runtime_state.filename = None
        gui.file_save.save(self.runtime_state)
        self.runtime_state.filename = old_name

    def menubar__edit__preferences(self, *args):
        builder = self.runtime_state.builder
        prefs = self.runtime_state.state.prefs
        builder.get_object(
            "preferences_window_" +
            "working_days_spinbutton").props.value = prefs._n_days
        builder.get_object(
            "preferences_window_" +
            "time_slots_per_day_spinbutton").props.value = (
            prefs._n_times_per_day)
        builder.get_object(
            "preferences_window_fitness_penalty_" +
            "time_clash_teacher_spinbutton").props.value = (
            prefs.penalties['clash_time_teacher'])
        builder.get_object(
            "preferences_window_fitness_penalty_" +
            "time_clash_batch_spinbutton").props.value = (
            prefs.penalties['clash_time_batch'])
        builder.get_object(
            "preferences_window_fitness_penalty_" +
            "room_capacity_spinbutton").props.value = (
            prefs.penalties['room_capacity'])
        builder.get_object(
            "preferences_window_population_spinbutton").props.value = (
            prefs.population_size)
        builder.get_object(
            "preferences_window_mutation_swaps_spinbutton").props.value = (
            prefs.mutate_counts)
        builder.get_object("preferences_window").show_all()

    def menubar__edit__preferences_ok(self, *args):
        logger.debug("Saving preferences")
        builder = self.runtime_state.builder
        prefs = self.runtime_state.state.prefs
        n_days = int(builder.get_object(
            "preferences_window_" +
            "working_days_spinbutton").props.value)
        n_times_per_day = int(builder.get_object(
            "preferences_window_" +
            "time_slots_per_day_spinbutton").props.value)
        if ((n_days != prefs._n_days) or
                (n_times_per_day != prefs._n_times_per_day)):
            del self.runtime_state.state.population[:]
            prefs._n_days = n_days
            prefs._n_times_per_day = n_times_per_day
            prefs.n_times = n_days * n_times_per_day
        prefs.penalties['clash_time_teacher'] = builder.get_object(
            "preferences_window_fitness_penalty_" +
            "time_clash_teacher_spinbutton").props.value
        prefs.penalties['clash_time_batch'] = builder.get_object(
            "preferences_window_fitness_penalty_" +
            "time_clash_batch_spinbutton").props.value
        prefs.penalties['room_capacity'] = builder.get_object(
            "preferences_window_fitness_penalty_" +
            "room_capacity_spinbutton").props.value
        population_size = int(builder.get_object(
            "preferences_window_population_spinbutton").props.value)
        del self.runtime_state.state.population[population_size:]
        prefs.population_size = population_size
        prefs.mutate_counts = int(builder.get_object(
            "preferences_window_mutation_swaps_spinbutton").props.value)
        self.runtime_state.unsaved_changes = True
        logger.debug("Saved preferences")
        builder.get_object("preferences_window").hide()
        self.schedule__refresh()

    def menubar__edit__preferences_cancel(self, *args):
        self.runtime_state.builder.get_object("preferences_window").hide()

    def menubar__help_about(self, *args):
        dialog = self.runtime_state.builder.get_object("about_dialog")
        dialog.run()
        dialog.hide()
