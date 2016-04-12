#!/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)


class BaseHandlers(object):
    def __init__(self, app, runtime_state):
        self.runtime_state = runtime_state
        self.application = app

    def close(self, *args):
        # TODO close and write files as necessary
        self.application.window.destroy()
