#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handlers(object):
    def main_window__delete(self, *args):
        Gtk.main_quit(*args)


def main(builder):
    window = builder.get_object("main_window")
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    builder = Gtk.Builder()
    builder.add_from_file("gui.ui")
    builder.connect_signals(Handlers())
    main(builder)
