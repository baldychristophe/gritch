import os
from typing import Union

from github import Github, Repository


def get_github_access_token() -> Union[str, None]:
    return os.environ.get('GIT_ACCESS_TOKEN')


def get_github() -> Github:
    return Github(get_github_access_token())


def get_user():
    return get_github().get_user()


def get_repositories(user) -> Repository:
    return user.get_repos()
