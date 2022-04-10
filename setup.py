from setuptools import setup, find_packages

setup(
    name="github",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "Click-plugins",
        "pydantic",
        "pyyaml",
        "PyGithub",
    ],
    entry_points={
        "console_scripts": [
            "github = github_repo.cli:github",
        ],
    },
    extras_require={"development": ["mypy", "black[d]", "flake8", "devtools"]},
)
