import ntpath
import humanize
from .categories import get_category


class File:
    def __init__(self, path, size, filetype, directory):
        self.path = path
        self.directory = directory
        self.name = ntpath.basename(path)
        self.size = size
        self.hr_size = humanize.naturalsize(size)
        self.filetype = filetype
        self.category = get_category(filetype)

    def __repr__(self):
        return f"File ({self.filetype}): {self.name}, {self.hr_size} ({self.size})"
