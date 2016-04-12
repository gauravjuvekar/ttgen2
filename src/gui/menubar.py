#!/usr/bin/env python3

from gi.repository import Gtk
import pickle
import logging
logger = logging.getLogger(__name__)

import gui
import state


class MenubarHandlers(gui.handlers.BaseHandlers):
    def menubar__file__new(self, *args):
        if not gui.file_save.save_if_unsaved_changes(self.runtime_state):
            return
        else:
            self.runtime_state.filename = None
            self.runtime_state.state = state.State()
            self.runtime_state.unsaved_changes = False
            # TODO refresh

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
                    # TODO refresh everything

    def menubar__file__save(self, *args):
        gui.file_save.save(self.runtime_state)

    def menubar__file__saveas(self, *args):
        old_name = self.runtime_state.filename
        self.runtime_state.filename = None
        gui.file_save.save(self.runtime_state)
        self.runtime_state.filename = old_name
