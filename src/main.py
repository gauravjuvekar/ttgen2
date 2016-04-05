#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, Gio

import logging
logger = logging.getLogger(__name__)


class Handlers(object):
    pass


class TTgen2(Gtk.Application):
    handlers = Handlers()

    def __init__(self, application_id, flags):
        Gtk.Application.__init__(
            self,
            application_id=application_id,
            flags=flags)
        self.connect("activate", self.new_window)

    def new_window(self, *args):
        ApplicationWindow(self, self.handlers)


class ApplicationWindow(object):
    def __init__(self, application, handlers, glade="gui.glade"):
        self.application = application
        try:
            builder = Gtk.Builder.new_from_file(glade)
            builder.connect_signals(handlers)
        except GObject.GError:
            logger.critical("Error reading glade file %s", glade)
            raise
        self.main_window = builder.get_object("main_window")
        self.main_window.set_application(self.application)
        self.main_window.show()

    def close(self, *args):
        self.main_window.destroy()


class Handlers(object):
    def main_window__delete(self, *args):
        Gtk.main_quit(*args)


def main():
    ttgen2 = TTgen2("com.ttgen2.ttgen2", Gio.ApplicationFlags.FLAGS_NONE)
    ttgen2.run()


if __name__ == "__main__":
    main()
