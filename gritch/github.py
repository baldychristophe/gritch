import os
from typing import Union

from github import Github, Repository


def get_github_access_token() -> Union[str, None]:
    return os.environ.get('GIT_ACCESS_TOKEN')


def get_github() -> Github:
    return Github(get_github_access_token())


def get_repositories() -> Repository:
    return get_github().get_user().get_repos()
