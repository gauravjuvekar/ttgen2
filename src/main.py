#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gio

import logging
logger = logging.getLogger(__name__)


import pickle
import meta


class Handlers(object):
    def __init__(self, builder=None, meta=None):
        self.builder = builder
        self.meta = meta

    def close(self, main_window, *args):
        print("handlers.close")
        print("main_win")
        main_window.destroy()

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


class TTgen2(Gtk.Application):
    handlers = Handlers(meta=meta.Meta())

    def __init__(self, application_id, flags):
        Gtk.Application.__init__(
            self,
            application_id=application_id,
            flags=flags)
        self.connect("activate", self.new_window)

    def new_window(self, *args):
        ApplicationWindow(self)


class ApplicationWindow(object):
    def __init__(self, application, glade="gui/gui.glade"):
        self.application = application
        try:
            builder = Gtk.Builder.new_from_file(glade)
            application.handlers.builder = builder
            application.handlers.builder.connect_signals(application.handlers)
        except GObject.GError:
            logger.critical("Error reading glade file %s", glade)
            raise
        self.main_window = builder.get_object("main_window")
        self.main_window.set_application(self.application)
        self.main_window.show()


def main():
    ttgen2 = TTgen2("com.ttgen2.ttgen2", Gio.ApplicationFlags.FLAGS_NONE)
    ttgen2.run()


if __name__ == "__main__":
    main()
