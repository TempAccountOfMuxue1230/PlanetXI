"""
File: helper/utils.py
File Version: 1.1
"""


class Version:
    def __init__(self, version: str):
        self.name = version.split(" ")[0]
        self.type = version.split(" ")[2]
        self.version = tuple(version.split(" ")[1].replace("V", "").split("."))

    def get_version_type(self):
        return self.type

    def get_product_name(self):
        return self.name

    def get_product_version(self):
        return self.version

    def __eq__(self, other):
        return self.version == other.version

    def __lt__(self, other):
        for v in self.version:
            if v < other.version[self.version.index(v)]:
                return True
        return False

    def __gt__(self, other):
        for v in self.version:
            if v > other.version[self.version.index(v)]:
                return True
        return False

    def __str__(self):
        return f"<Version {self.name} - {'.'.join(self.version)} - {self.type}>"
