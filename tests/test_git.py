import pytest
import git
from git import Repo
import os

test_repo = os.environ["TEST_REPO"]


def test_clone():
    repo = None
    if not os.path.isdir('test_repo'):
        repo = git.Repo.clone_from(test_repo, os.path.join(
            '.', 'test_repo'), branch='master')
    else:
        repo = Repo('test_repo')
    print(repo.head.commit)