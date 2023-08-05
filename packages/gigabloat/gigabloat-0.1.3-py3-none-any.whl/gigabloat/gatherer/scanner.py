import os
import pathlib
import collections
from .file import File
from .directory import Directory


class Scanner:
    def __init__(self, root):
        self.root = root
        self.size = None
        self.hr_size = None
        self.files = []
        self.file_count = 0
        self.dir_count = 0
        self.directories = []
        self.root_directory = None
        self.filetypes = {}
        self.categories = {}

    def full_scan(self):
        self.scan_directory(self.root)
        self.get_size()
        self.get_extra_stats()

    def scan_directory(self, dir_to_scan, parent=None):
        self.dir_count = self.dir_count + 1
        treeobjects = os.listdir(dir_to_scan)
        new_directory = Directory(dir_to_scan, parent)

        # 1. Get files
        filepaths = [
            os.path.join(dir_to_scan, f)
            for f in treeobjects
            if os.path.isfile(os.path.join(dir_to_scan, f))
        ]
        dir_files = [
            File(path, os.stat(path).st_size, pathlib.Path(path).suffix, new_directory)
            for path in filepaths
        ]
        self.file_count = self.file_count + len(dir_files)

        # 2. Get subdirectories
        dirnames = [
            os.path.join(dir_to_scan, d)
            for d in treeobjects
            if os.path.isdir(os.path.join(dir_to_scan, d))
        ]
        subdirs = [self.scan_directory(d, parent) for d in dirnames]

        new_directory.update_content(dir_files, subdirs)

        self.directories.append(new_directory)
        if dir_to_scan == self.root:
            self.root_directory = new_directory
        # TODO: we don't really need to return root directory, right?
        return new_directory

    def get_extra_stats(self):
        filetypes_counter = collections.Counter()
        categories_counter = collections.Counter()
        for current_dir in self.directories:
            filetypes_counter.update(current_dir.filetypes)
            categories_counter.update(current_dir.categories)
        self.filetypes = dict(filetypes_counter)
        self.categories = dict(categories_counter)

    def get_size(self):
        self.size = self.root_directory.size
        self.hr_size = self.root_directory.hr_size
