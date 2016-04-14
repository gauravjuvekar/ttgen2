#!/usr/bin/env python3

from gi.repository import Gtk
import logging
logger = logging.getLogger(__name__)

import gui


class BatchHandlers(gui.handlers.BaseHandlers):
    def batch__add_ok(self, *args):
        pass

    def batch__add_cancel(self, *args):
        self.runtime_state.builder.get_object(
            "batches_add_window_name_entry").props.text = ''
        self.runtime_state.builder.get_object("batches_add_window").hide()
        # Return True to prevent the window being destroyed
        return True
