import os
import pytest
from github import Github
from github_repo.github_repo_model import GitHubRepoModel
from github_repo.github_repo import GitHubRepo


class TestGitHubRepo:
    def test_create_github_instance(self):
        github_instance = GitHubRepo._create_github_instance()
        assert type(github_instance) == Github

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
