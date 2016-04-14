#!/usr/bin/env python3

from gi.repository import Gtk
import logging
logger = logging.getLogger(__name__)

import gui


class AllocationHandlers(gui.handlers.BaseHandlers):
    def allocation__add_ok(self, *args):
        pass

    def allocation__add_cancel(self, *args):
        self.runtime_state.builder.get_object("allocations_add_window").hide()
        # Return True to prevent the window being destroyed
        return True
