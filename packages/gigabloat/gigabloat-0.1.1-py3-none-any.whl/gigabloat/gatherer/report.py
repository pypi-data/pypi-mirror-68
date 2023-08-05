from functools import reduce

from tabulate import tabulate
import click

ROOT_HEADERS = ["Scan root", "#Files", "#Directories", "Size", "Size (bytes)"]
NOEXT_HEADERS = ["Name", "Size", "Size (bytes)"]
DIRECTORY_HEADERS = ["Directory path", "Size"]
FILETYPE_HEADERS = ["File type", "Count"]
CATEGORY_HEADERS = ["Category", "Count"]

EXIT_PAGER_HINT = "\nPress Ctrl + Z to exit"


def make_title(title):
    return f"\n>>> {title}:\n"


class ReportPrinter:
    def __init__(self, scanner):
        self.scanner = scanner

    def print_full_report(self):
        reports = [
            self.prepare_root_stats(),
            self.prepare_category_stats(),
            self.prepare_type_stats(),
            self.prepare_no_extension_files(),
            self.prepare_directories(),
            self.prepare_tree(with_files=True),
            EXIT_PAGER_HINT,
        ]
        all_reports = reduce(lambda x, y: x + y, reports)
        click.echo_via_pager(all_reports)
        # self.prepare_all_files()

    def print_short_report(self):
        click.echo_via_pager(self.prepare_root_stats())

    def prepare_directories(self):
        table = [
            [dir.path, f"{dir.size} ({dir.hr_size})"]
            for dir in self.scanner.directories
        ]
        table_print = tabulate(table, headers=DIRECTORY_HEADERS, tablefmt="fancy_grid")
        return make_title("Directories") + table_print

    def prepare_type_stats(self):
        sorted_filetypes = sorted(
            self.scanner.filetypes.items(), key=lambda item: item[1], reverse=True
        )
        sorted_stats = [
            ["no extension" if ext == "" else ext, count]
            for ext, count in sorted_filetypes
        ]
        table_print = tabulate(
            sorted_stats, headers=FILETYPE_HEADERS, tablefmt="fancy_grid"
        )
        return make_title("File types") + table_print

    def prepare_category_stats(self):
        sorted_categories = sorted(
            self.scanner.categories.items(), key=lambda item: item[1], reverse=True
        )
        sorted_stats = [[cat, count] for cat, count in sorted_categories]
        table_print = tabulate(
            sorted_stats, headers=CATEGORY_HEADERS, tablefmt="fancy_grid"
        )
        return make_title("Categories") + table_print

    def prepare_no_extension_files(self):
        noext_files = list(filter(lambda f: f.filetype == "", self.scanner.files))
        tab_noext_files = [[f.name, f.hr_size, f.size] for f in noext_files]
        table_print = tabulate(
            tab_noext_files, headers=NOEXT_HEADERS, tablefmt="fancy_grid"
        )
        return make_title("Files with no extension") + table_print

    def prepare_root_stats(self):
        # TODO: root should be absolute bath, not just dot or name of folder
        table = [
            [
                self.scanner.root,
                self.scanner.file_count,
                self.scanner.dir_count,
                self.scanner.hr_size,
                self.scanner.size,
            ]
        ]
        table_print = tabulate(table, headers=ROOT_HEADERS, tablefmt="fancy_grid")
        return make_title("Scan results") + table_print

    def prepare_all_files(self):
        all_files_headers = [
            f"File ({self.scanner.file_count})",
            "Size",
            "Size (bytes)",
        ]
        tab_files = [[f.name, f.hr_size, f.size] for f in self.scanner.files]
        table_print = tabulate(
            tab_files, headers=all_files_headers, tablefmt="fancy_grid"
        )
        return make_title("All files") + table_print

    def prepare_tree(self, with_files=False):
        # Experimental thing
        lines = []

        def print_directory(directory, level=0, with_files=False):
            if level == 0:
                indent = " " * level
            else:
                indent = "├" + "─" * level
            dir_stats = f"({directory.file_count} files, {directory.subdir_count} subdirectories, {directory.hr_size})"
            lines.append(f"{indent}{directory.name} {dir_stats}\n")
            if with_files and directory.files:
                for file in directory.files:
                    print_file(file, level)
            if directory.subdirectories:
                for dir_object in directory.subdirectories:
                    print_directory(dir_object, level=level + 2, with_files=with_files)

        def print_file(file, level):
            indent = "├" + "─" * (level + 2)
            lines.append(indent + file.name + "\n")

        print_directory(self.scanner.root_directory, with_files=with_files)
        all_lines = reduce(lambda x, y: x + y, lines)
        return make_title("Tree") + all_lines
