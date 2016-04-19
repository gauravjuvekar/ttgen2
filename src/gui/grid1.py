#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import gui

class Handler_Grid(gui.handlers.BaseHandlers):
    #def onDeleteWindow(self, *args):
        """
        button1 = self.runtime_state.builder.get_object("show_tt")
        Gtk.main_quit(*args)
        """
    #    print ("1")
    ##def abhishek(self, *args):
    ##    button1 = self.runtime_state.builder.get_object("show_tt")
        
    ##    print("Hello World!")
        #win = MyWindow()
        #win.connect("delete-event", Gtk.main_quit)
        #win.show_all()
        
        ##print ("2")
        def abhishek(self, notebook, *args):
        show_button = self.runtime_state.builder.get_object(
            "show_tt")
        print ("abhi")
"""
class TransparentButton(Gtk.Label):
	def __init__(self, *args):
		Gtk.Label.__init__(self)
		#self.set_property("opacity", 1.0)
		self.set_property("expand", True)
		self.set_text("hi")
		self.show()
"""
"""
class Grid_Window(Gtk.Window):
    def __init__(self, *args):
        Gtk.Window.__init__(self, title="Hello World")

        self.grid = Gtk.Grid()
        self.add(self.grid)

        #self.sample = Gtk.Button()

        for i in range(0, 10):
            for v in range(0, 10):
                self.grid.attach(TransparentButton(), i, v, 1, 1)
        self.grid.remove(self.grid.get_child_at(0, 0))
        #self.grid.attach(self.sample, 0, 0, 1, 1)

        def on_buttonPlus_clicked(self, widget):
            print("Plus")
"""
"""
class Grid_Handlers(gui.handlers.BaseHandlers):
    def show_grid(self, *args):

        builder = Gtk.Builder()
        builder.add_from_file("grid.glade")
        builder.connect_signals(Handler_Grid())
        window = builder.get_object("window1")
        window.show_all()
        Gtk.main()

        #button1 = self.runtime_state.builder.get_object("show_tt")
"""
