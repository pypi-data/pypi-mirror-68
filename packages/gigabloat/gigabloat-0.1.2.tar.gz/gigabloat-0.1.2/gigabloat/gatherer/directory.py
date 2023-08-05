import os
import collections
from functools import reduce

import humanize


class Directory:
    def __init__(self, path, parent_dir):
        self.path = path
        self.name = os.path.basename(path)
        self.parent_dir = parent_dir
        self.files = None
        self.file_count = 0
        self.subdirectories = None
        self.subdir_count = 0
        self.size = None
        self.hr_size = None
        self.filetypes = {}
        self.categories = {}

    def __repr__(self):
        return f"{self.path}, {self.hr_size} ({self.size})"

    def update_content(self, files, subdirectories):
        self.files = files or None
        self.file_count = len(files)
        self.subdirectories = subdirectories or None
        self.subdir_count = len(subdirectories)
        self.get_size()
        self.get_extra_stats()

    def get_size(self):
        if self.files:
            files_total = reduce((lambda x, y: x + y.size), self.files, 0)
        else:
            files_total = 0
        if self.subdirectories:
            subdirs_size = reduce((lambda x, y: x + y.size), self.subdirectories, 0)
        else:
            subdirs_size = 0
        self.size = files_total + subdirs_size
        self.hr_size = humanize.naturalsize(self.size)

    def get_extra_stats(self):
        if self.files:
            filetypes_counter = collections.Counter()
            categories_counter = collections.Counter()
            for current_file in self.files:
                filetypes_counter.update([current_file.filetype])
                categories_counter.update([current_file.category])
            self.filetypes = dict(filetypes_counter)
            self.categories = dict(categories_counter)
