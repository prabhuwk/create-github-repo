import click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points
from github_repo.github_repo import GitHubRepo


@with_plugins(iter_entry_points("github.plugins"))
@click.group("github")
def github():
    """Entry point for github commands."""


@github.group("repo")
def repo():
    """Manage GitHub Repository"""


@repo.command("create")
@click.option("--file", "-f", help="Path to Repo Specification", required=True)
def create_repo(file: str):
    """Create GitHub Repository"""
    GitHubRepo(file).create()


@repo.command("delete")
@click.option("--file", "-f", help="Path to Repo Specification", required=True)
def delete_repo(file: str):
    """Delete GitHub Repository"""
    GitHubRepo(file).delete()
