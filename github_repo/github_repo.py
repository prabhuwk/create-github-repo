import sys
from pathlib import Path
import yaml
from github_repo.github_repo_model import Model
from pydantic import ValidationError


class GitHubRepo:
    def __init__(self, file: str):
        self._file = file
        self._content = None

    @property
    def file(self):
        return self._file

    @staticmethod
    def _read_repo_file(file: str) -> dict:
        if Path(file).exists():
            return yaml.safe_load(open(file).read())
        raise FileNotFoundError(file)

    @property
    def content(self):
        if not self._content:
            content_obj = self._read_repo_file(self._file)
            try:
                self._content = Model.parse_obj(content_obj)
            except ValidationError as e:
                sys.exit(e)
        return self._content

    def create(self):
        pass

    def delete(self):
        pass
