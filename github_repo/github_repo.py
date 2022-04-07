import os
import sys
import click
import yaml
from pathlib import Path
from github import Github, GithubException
from github_repo.github_repo_model import Model
from pydantic import ValidationError
from functools import wraps


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
    def _read_repo_spec_file(file: str):
        if Path(file).exists():
            return yaml.safe_load(open(file).read())
        raise FileNotFoundError(file)

    @property
    def cr(self):
        if not self._cr:
            content_obj = self._read_repo_spec_file(self._file)
            try:
                self._cr = Model.parse_obj(content_obj)
            except ValidationError as e:
                sys.exit(e)
        return self._cr

    def _github_exception_handler(github_interaction):
        @wraps(github_interaction)
        def github_status_wrapper(self):
            try:
                return github_interaction(self)
            except GithubException as e:
                raise e

        return github_status_wrapper

    @_github_exception_handler
    def _get_list_of_repos(self):
        repos_list = [
            repo.name for repo in self._github_instance.get_user().get_repos()
        ]
        return repos_list

    @_github_exception_handler
    def _create_repo(self):
        user = self._github_instance.get_user()
        repo = user.create_repo(self.cr.metadata.name)
        return repo.full_name

    def _find_repo_in_list(self):
        repo_name = self.cr.metadata.name
        repos_list = self._get_list_of_repos()
        if len(repos_list) > 0 and repo_name in repos_list:
            return repo_name
        return

    def create(self):
        repo_name = self._find_repo_in_list()
        if repo_name:
            click.secho(f"{repo_name} repo already exists.")
            return
        repo_name = self._create_repo()
        click.secho(f"{repo_name} successfully created.")

    @_github_exception_handler
    def _delete_repo(self):
        user = self._github_instance.get_user()
        repo = user.get_repo(self.cr.metadata.name)
        repo.delete()
        return

    def delete(self):
        repo_name = self._find_repo_in_list()
        if repo_name:
            self._delete_repo()
            click.secho(f"{repo_name} successfully deleted.")
            return
        click.secho(f"{self.cr.metadata.name} repo does not exists.")
