#!/usr/bin/env python3

from gi.repository import Gtk
import pickle
import logging
logger = logging.getLogger(__name__)


def save_if_unsaved_changes(runtime_state):
    """
    Returns True if the caller can continue, False otherwise
    """
    if runtime_state.unsaved_changes:
        dialog = runtime_state.builder.get_object("unsaved_changes_dialog")
        res = dialog.run()
        dialog.hide()
        if res == Gtk.ResponseType.ACCEPT:
            # Save and continue with action
            save(runtime_state)
            return True
        elif (res == Gtk.ResponseType.CANCEL or
                res == Gtk.ResponseType.DELETE_EVENT):
            # Cancel or close dialog
            return False
        elif res == Gtk.ResponseType.REJECT:
            # Discard changes and continue
            return True
    else:
        return True


def save(runtime_state):
    if runtime_state.filename is None:
        dialog = Gtk.FileChooserDialog(
            "Open file",
            parent=runtime_state.builder.get_object("main_window"),
            action=Gtk.FileChooserAction.SAVE,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                     Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
        res = dialog.run()
        if res == Gtk.ResponseType.ACCEPT:
            file_name = dialog.get_filename()
        elif res in (Gtk.ResponseType.CANCEL, Gtk.ResponseType.DELETE_EVENT):
            return
        else:
            raise RuntimeError()
        logger.debug("Saving to file %s", file_name)
        dialog.destroy()
        runtime_state.filename = file_name
    with open(runtime_state.filename, 'wb') as f:
        pickle.dump(runtime_state.state, f)
    runtime_state.unsaved_changes = False
