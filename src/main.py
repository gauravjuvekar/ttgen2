#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gio

import logging
logger = logging.getLogger(__name__)

import sys

import state
import gui


class Handlers(
        gui.menubar.MenubarHandlers,
        gui.notebook.NotebookHandlers):
    pass


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
        try:
            self.builder = Gtk.Builder.new_from_file(glade_file)
            self.handlers = Handlers(
                runtime_state=state.RuntimeState(
                    builder=self.builder,
                    state=state.State()),
                app=self)
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
