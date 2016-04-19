#!/usr/bin/env python3

from gi.repository import Gtk

class TransparentButton(Gtk.Label):
    def __init__(self):
        Gtk.Label.__init__(self)
        #self.set_property("opacity", 1.0)
        self.set_property("expand", True)
	self.set_text("hi")        
	self.show()


class Grid_Handlers(gui.handlers.BaseHandlers):
    def show_grid(self, *args):
	print ("Hello")        
	"""Gtk.Window.__init__(self, title="Hello World")

        self.grid = Gtk.Grid()
        self.add(self.grid)

        #self.sample = Gtk.Button()

        for i in range(0, 10):
            for v in range(0, 10):
                self.grid.attach(TransparentButton(), i, v, 1, 1)
        self.grid.remove(self.grid.get_child_at(0, 0))
        #self.grid.attach(self.sample, 0, 0, 1, 1)
	"""	
	def on_buttonPlus_clicked(self, widget):
            print("Plus")
    
