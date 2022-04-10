from pathlib import Path

import pytest
import yaml


@pytest.fixture
def fixture_path():
    return f"{Path(__file__).parent}/fixtures"


@pytest.fixture
def sample_repo_file(fixture_path):
    return f"{fixture_path}/example/sample-repo.yaml"


@pytest.fixture
def sample_repo_manifest(sample_repo_file):
    with open(sample_repo_file) as f:
        return yaml.safe_load(f)


@pytest.fixture
def sample_repo_invalid_file(fixture_path):
    return f"{fixture_path}/example/sample-repo-invalid.yaml"


@pytest.fixture()
def sample_repo_file_not_exist(fixture_path):
    return f"{fixture_path}/example/sample-repo-not-exist.yaml"


@pytest.fixture
def sample_repo_manifest_invalid(sample_repo_invalid_file):
    with open(sample_repo_invalid_file) as f:
        return yaml.safe_load(f)
