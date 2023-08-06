import os

from mgsc.blueprints import Repository


class Namespace:
    def __init__(self, name: str, repositories: [Repository] = None, parent=None):
        self.name = name
        self.parent = parent
        self.repositories = repositories

    @property
    def path(self):
        pathlist = []
        pointer = self
        while isinstance(pointer.parent, (Namespace)):
            pathlist.append(pointer)
            pointer = pointer.parent
        pathlist.append(pointer.parent)
        return pathlist

    @property
    def fspath(self):
        os.path.sep.join(self.path[::-1])

    def __repr__(self):
        return f"{self.name}"
