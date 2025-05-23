"""
File: sense/sense_manager.py
File Version: 1.4
"""


class SenseManager:
    """
    A class to manage the screens
    """

    def __init__(self, translator):
        self.senses = {}
        self.selected = None
        self.translator = translator
        self.over_sense_gui = None
        self.osg_opened = False

    def add(self, sense, *args, **argv):
        self.senses[sense.get_name()] = sense(self, *args, **argv)

    def select(self, sense_id):
        self.selected = sense_id

    def set_osg(self, osg):
        self.over_sense_gui = self.senses[osg]

    def open_osg(self):
        self.osg_opened = True

    def close_osg(self):
        self.osg_opened = False

    def osg_is_opened(self):
        return self.osg_opened

    def get_osg(self):
        return self.over_sense_gui

    def get(self, sense_id=None):
        return self.senses[sense_id if sense_id else self.selected]
