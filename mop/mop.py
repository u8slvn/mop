from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Collector:
    """Collect a list of files base on extensions in the given path directory."""
    extensions: List[str]
    recursive: bool
    exclude: bool

    def __call__(self, path: Path):
        base_pattern = '**/*' if self.recursive else '*'
        files = []
        for file in path.glob(base_pattern):
            if self._in_ext(file.suffix, self.exclude) and file.is_file():
                files.append(file)
        return files

    def _in_ext(self, extension: str, exclude: bool = False):
        if exclude:
            return extension not in self.extensions
        return extension in self.extensions


class Mop:
    """Handle files deletion in the given path for the given collector."""

    def __init__(self, dir_path: str, extensions: List[str], recursive: bool = False, exclude: bool = False):
        self.dir_path = Path(dir_path)
        self._collector = Collector(extensions=extensions, recursive=recursive, exclude=exclude)
        self._files_to_delete = []

    @property
    def files_to_delete_count(self):
        return len(self._files_to_delete)

    def collect(self):
        if not self._files_to_delete:
            self._files_to_delete = self._collector(path=self.dir_path)

    def clean(self):
        for file in self._files_to_delete:
            file.unlink()
        self._files_to_delete = []
