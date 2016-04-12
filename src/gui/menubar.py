#!/usr/bin/env python3

from gi.repository import Gtk
import pickle
import logging
logger = logging.getLogger(__name__)

import gui


class MenubarHandlers(gui.handlers.BaseHandlers):
    def menubar__file__new(self, *args):
        # TODO ask to save current file if dirty
        pass

    def menubar__file__open(self, *args):
        dialog = Gtk.FileChooserDialog(
            "Open file",
            parent=self.builder.get_object("main_window"),
            action=Gtk.FileChooserAction.OPEN,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                     Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))
        res = dialog.run()
        if res == Gtk.ResponseType.ACCEPT:
            file_name = dialog.get_filename()
        elif res in (Gtk.ResponseType.CANCEL, Gtk.ResponseType.DELETE_EVENT):
            return
        else:
            raise RuntimeError()
        logger.debug("Opening file %s", file_name)
        dialog.destroy()
        with open(file_name, 'rb') as f:
            try:
                self.meta = pickle.load(f)
            except pickle.UnpicklingError:
                dialog = Gtk.MessageDialog(
                    "Cannot open that file",
                    parent=self.builder.get_object("main_window"),
                    flags=(Gtk.DialogFlags.MODAL |
                           Gtk.DialogFlags.DESTROY_WITH_PARENT),
                    message_type=Gtk.MessageType.ERROR,
                    buttons=(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE),
                    text="Error reading file {}".format(file_name),
                    title="Cannot open file")
                dialog.run()
                dialog.destroy()
        # TODO refresh everything
