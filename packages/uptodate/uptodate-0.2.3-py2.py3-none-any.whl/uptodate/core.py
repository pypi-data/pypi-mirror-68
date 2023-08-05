import click
import requests

from rich.console import Console
from rich.table import Table
from rich.progress import track

from collections import namedtuple

from typing import List, Dict

Row = namedtuple('Row', ['name', 'current_version', 'latest_version'])


class UpToDate:
    def __init__(self) -> None:
        self.console = Console()
        self.scanner = RequirementsScanner()
        self.pypi = PyPI()
        self.printer = TablePrinter()

    def check(self, file_path) -> None:
        dependences = self.scanner.get_dependences(file_path)
        versions = self.pypi.get_versions(list(dependences.keys()))
        rows = self._prepare_rows(dependences, versions)
        if len(rows) == 0:
            self.console.print('Everything is up to date', style='green')
        else:
            table = self.printer.draw(rows)
            self.console.print(table)

    def _prepare_rows(
        self, dependences: Dict[str, str], latest_versions: Dict[str, str]
    ) -> List[Row]:
        return [
            Row(
                name=name,
                current_version=current_version,
                latest_version=latest_versions[name],
            )
            for name, current_version in dependences.items()
            if current_version != latest_versions[name]
        ]


class RequirementsScanner:
    def get_dependences(self, file_path: str) -> Dict[str, str]:
        dependences = {}

        with open(file_path, 'r') as f:
            for line in f.readlines():
                if self._is_supported(line):
                    name, version = line.strip().split('==')
                    dependences[name] = version

        return dependences

    def _is_supported(self, line: str) -> bool:
        is_supported = True

        if '==' not in line:
            is_supported = False
        if '[' in line and ']' in line:
            is_supported = False

        if not is_supported:
            click.secho('SKIPPED: {}'.format(line), fg='yellow')

        return is_supported


class PyPI:
    URL_PATTERN = 'https://pypi.org/pypi/{}/json'

    def get_versions(self, dependences: List[str]) -> Dict[str, str]:
        versions = {}

        for dependence in track(dependences, description='Checking...'):
            url = self.URL_PATTERN.format(dependence)
            response = requests.get(url)
            data = response.json()
            latest_version = data['info']['version']
            versions[dependence] = latest_version

        return versions


class TablePrinter:
    def __init__(self) -> None:
        self.table = Table(show_header=True, header_style='bold cyan')
        self.table.add_column('Name', style='dim', justify='left')
        self.table.add_column('Current', justify='center')
        self.table.add_column('Latest', justify='center')

    def draw(self, rows: List[Row]) -> Table:
        for row in rows:
            self.table.add_row(row.name, row.current_version, row.latest_version)

        return self.table
