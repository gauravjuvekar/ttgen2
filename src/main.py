#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gio

import logging
logger = logging.getLogger(__name__)

import sys

import core

import pickle
import meta


class Handlers(object):
    def __init__(self, app, builder=None, meta=None):
        self.builder = builder
        self.meta = meta
        self.application = app

    def close(self, *args):
        # TODO close and write files as necessary
        self.application.window.destroy()

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
    def __init__(
            self,
            application_id="com.ttgen2.ttgen2",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
            glade_file="gui/gui.glade"):
        Gtk.Application.__init__(
            self,
            application_id=application_id,
            flags=flags)
        self.handlers = Handlers(meta=meta.Meta(), app=self)
        try:
            self.builder = Gtk.Builder.new_from_file(glade_file)
            self.builder.connect_signals(self.handlers)
        except GObject.GError:
            logger.critical("Error reading glade file %s", glade_file)
            raise

    def do_activate(self):
        self.window = self.builder.get_object("main_window")
        self.window.set_application(self)
        self.window.connect('destroy', self.on_quit)
        self.window.show_all()
        self.add_window(self.window)

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def on_quit(self, *args):
        self.quit()


def main():
    ttgen2 = TTgen2()
    sys.exit(ttgen2.run(sys.argv))


if __name__ == "__main__":
    log_level = logging.DEBUG
    format_str = "{levelname:8s} {asctime} {name}"
    format_str += ": {message}"

    logging.basicConfig(
        level=log_level,
        style='{',
        format=format_str)
    main()
