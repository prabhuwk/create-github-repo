import os
import sys
import click
import yaml
from pathlib import Path
from github import Github, GithubException
from github_repo.github_repo_model import GitHubRepoModel
from pydantic import ValidationError
from functools import wraps


def _github_operation_handler(github_operation):
    @wraps(github_operation)
    def github_operation_wrapper(self):
        try:
            return github_operation(self)
        except GithubException as e:
            raise e

    return github_operation_wrapper


class GitHubRepo:
    def __init__(self, file: str):
        self._file = file
        self._cr = None
        self._github_instance = self._create_github_instance()
        self._repo_list = self._github_repo_list()

    @staticmethod
    def _create_github_instance() -> Github:
        access_token = os.environ.get("ACCESS_TOKEN")
        return Github(access_token)

    @staticmethod
    def _read_repo_spec_file(file: str) -> dict:
        if Path(file).exists():
            return yaml.safe_load(open(file).read())
        raise FileNotFoundError(file)

    @property
    def cr(self) -> GitHubRepoModel:
        if not self._cr:
            content_obj = self._read_repo_spec_file(self._file)
            try:
                self._cr = GitHubRepoModel.parse_obj(content_obj)
            except ValidationError as e:
                sys.exit(e)
        return self._cr

    @_github_operation_handler
    def _github_repo_list(self) -> list:
        repos = (repo.name for repo in self._github_instance.get_user().get_repos())
        return list(repos)

    @_github_operation_handler
    def _create_repo(self) -> str:
        user = self._github_instance.get_user()
        repo = user.create_repo(self.cr.metadata.name)
        return repo.full_name

    def create(self) -> None:
        repo_name = self.cr.metadata.name
        if repo_name in self._repo_list:
            click.secho(f"{repo_name} repo already exists.")
            return
        repo_name = self._create_repo()
        click.secho(f"{repo_name} successfully created.")

    @_github_operation_handler
    def _delete_repo(self) -> None:
        user = self._github_instance.get_user()
        repo = user.get_repo(self.cr.metadata.name)
        repo.delete()
        return

    def delete(self) -> None:
        repo_name = self.cr.metadata.name
        if repo_name in self._repo_list:
            self._delete_repo()
            click.secho(f"{repo_name} successfully deleted.")
            return
        click.secho(f"{repo_name} repo does not exists.")
