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


class GithubInstance:
    def __new__(cls):
        return cls._create_github_instance()

    @staticmethod
    def _create_github_instance() -> Github:
        _access_token = os.environ.get("ACCESS_TOKEN")
        return Github(_access_token)


class GitHubRepo:
    def __init__(self, file: str):
        self._file = file
        self._cr = None
        self._github_instance = GithubInstance()
        self._repo_list = GitHubRepoList(self._github_instance)

    @property
    def repo_list(self) -> list:
        return self._repo_list

    @property
    def file(self) -> str:
        return self._file

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


class GitHubRepoList:
    def __init__(self, github_instance: Github):
        self._github_instance = github_instance
        self.repo_list = self._github_repo_list()

    @_github_operation_handler
    def _github_repo_list(self) -> list:
        repos_list = (
            repo.name for repo in self._github_instance.get_user().get_repos()
        )
        return list(repos_list)

    def __repr__(self):
        return repr(self.repo_list)

    def __contains__(self, repo: str):
        if len(self.repo_list) > 0 and repo in self.repo_list:
            return True
        return False


class GitHubRepoCreate(GitHubRepo):
    def __init__(self, file: str):
        super().__init__(file)
        self._create()

    @_github_operation_handler
    def _create_repo(self) -> str:
        user = self._github_instance.get_user()
        repo = user.create_repo(self.cr.metadata.name)
        return repo.full_name

    def _create(self) -> None:
        repo_name = self.cr.metadata.name
        if repo_name in self.repo_list:
            click.secho(f"{repo_name} repo already exists.")
            return
        repo_name = self._create_repo()
        click.secho(f"{repo_name} successfully created.")


class GitHubRepoDelete(GitHubRepo):
    def __init__(self, file: str):
        super().__init__(file)
        self._delete()

    @_github_operation_handler
    def _delete_repo(self) -> None:
        user = self._github_instance.get_user()
        repo = user.get_repo(self.cr.metadata.name)
        repo.delete()
        return

    def _delete(self) -> None:
        repo_name = self.cr.metadata.name
        if repo_name in self.repo_list:
            self._delete_repo()
            click.secho(f"{repo_name} successfully deleted.")
            return
        click.secho(f"{repo_name} repo does not exists.")
