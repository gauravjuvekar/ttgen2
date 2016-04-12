#!/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)


class BaseHandlers(object):
    def __init__(self, app, builder, meta):
        self.builder = builder
        self.meta = meta
        self.application = app

    def close(self, *args):
        # TODO close and write files as necessary
        self.application.window.destroy()
