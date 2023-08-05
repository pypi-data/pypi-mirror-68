import click
from .scanner import Scanner
from .report import ReportPrinter


@click.command()
@click.argument("target", required=1)
def scan(target):
    """
    Get statistics about directory.\n
    e.g. gigabloat scan myphotos
    """
    target_scanner = Scanner(target)
    target_scanner.full_scan()
    ReportPrinter(target_scanner).print_full_report()
    # since flask might not be needed probably delete next line later
    # return targetScanner
