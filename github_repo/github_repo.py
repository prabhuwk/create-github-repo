import os
import sys
import click
import yaml
from pathlib import Path
from github import Github
from github_repo.github_repo_model import Model
from pydantic import ValidationError


class AccessTokenNotFound(Exception):
    """Exception for github access token not found"""


class GitHubRepo:
    def __init__(self, file: str):
        self._file = file
        self._cr = None
        self._github_instance = self._create_github_instance()

    @staticmethod
    def _create_github_instance():
        _access_token = os.environ.get("ACCESS_TOKEN")
        if _access_token:
            return Github(_access_token)
        raise AccessTokenNotFound("Github access token not found.")

    @property
    def file(self):
        return self._file

    @staticmethod
    def _read_repo_file(file: str):
        if Path(file).exists():
            return yaml.safe_load(open(file).read())
        raise FileNotFoundError(file)

    @property
    def cr(self):
        if not self._cr:
            content_obj = self._read_repo_file(self._file)
            try:
                self._cr = Model.parse_obj(content_obj)
            except ValidationError as e:
                sys.exit(e)
        return self._cr

    def create(self):
        repos_list = [
            repo.name for repo in self._github_instance.get_user().get_repos()
        ]
        if self.cr.metadata.name not in repos_list:
            user = self._github_instance.get_user()
            repo = user.create_repo(self.cr.metadata.name)
            click.secho(f"{repo.full_name} successfully created.")

    def delete(self):
        pass
