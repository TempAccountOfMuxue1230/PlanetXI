"""
File: sense/sense_manager.py
File Version: 1.3
"""


class SenseManager:
    """
    A class to manage the screens
    """

    def __init__(self, translator):
        self.sences = {}
        self.seleted = None
        self.translator = translator

    def add(self, sence, *args, **argv):
        self.sences[sence.get_name()] = sence(self, *args, **argv)

    def select(self, sence_id):
        self.seleted = sence_id

    def get(self, sence_id=None):
        return self.sences[sence_id if sence_id else self.seleted]
