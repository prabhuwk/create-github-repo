import os
import yaml
import pytest
from github import Github
from github_repo.github_repo_model import GitHubRepoModel
from github_repo.github_repo import GitHubRepo


class TestGitHubRepo:
    def test_create_github_instance(self):
        github_instance = GitHubRepo._create_github_instance()
        assert type(github_instance) == Github

    def test_access_token(self):
        assert "ACCESS_TOKEN" in os.environ

    def test_init_success(self, sample_repo_file):
        github_instance = GitHubRepo(sample_repo_file)
        assert type(github_instance.cr) == GitHubRepoModel
        assert type(github_instance) == GitHubRepo

    def test_init_failure_file_not_found(self, sample_repo_file_not_exist):
        with pytest.raises(FileNotFoundError) as e:
            GitHubRepo(sample_repo_file_not_exist).cr()
        assert sample_repo_file_not_exist in str(e.value)

    def test_init_failure_model(self, sample_repo_invalid_file):
        with pytest.raises(SystemExit) as e:
            GitHubRepo(sample_repo_invalid_file).cr()
        assert (
            f"1 validation error for GitHubRepoModel\nspec\n  field required (type=value_error.missing)"
            in str(e.value)
        )

    def test_read_repo_spec_file(self, sample_repo_manifest, sample_repo_file):
        assert sample_repo_manifest == GitHubRepo._read_repo_spec_file(sample_repo_file)

    def test_read_repo_spec_file_not_found(self, sample_repo_file_not_exist):
        with pytest.raises(FileNotFoundError) as e:
            GitHubRepo._read_repo_spec_file(sample_repo_file_not_exist)
        assert sample_repo_file_not_exist in str(e.value)

    def test_github_repo_list(self, sample_repo_file):
        repo_list = GitHubRepo(sample_repo_file)._github_repo_list()
        assert "manage-github-repo" in repo_list

    def test_create(self, sample_repo_file, capsys):
        GitHubRepo(sample_repo_file).create()
        captured = capsys.readouterr()
        assert captured.out == ("prabhuwk/sample-repo successfully created.") or (
            "sample-repo repo already exists."
        )

    def test_delete(self, sample_repo_file, capsys):
        GitHubRepo(sample_repo_file).delete()
        captured = capsys.readouterr()
        assert captured.out == ("sample-repo successfully deleted.") or (
            "sample-repo repo does not exists."
        )
