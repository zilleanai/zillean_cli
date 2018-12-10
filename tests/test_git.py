import pytest
import git
from git import Repo
import os
import tempfile

test_repo = os.environ["TEST_REPO"]


def test_clone():
    repo = None
    if not os.path.isdir('test_repo'):
        repo = git.Repo.clone_from(test_repo, os.path.join(
            '.', 'test_repo'), branch='master')
    else:
        repo = Repo('test_repo')
    print(repo.head.commit)


def test_temp_clone():
    repo = None
    folder = tempfile.TemporaryDirectory()
    print(folder.name)
    repo = git.Repo.clone_from(test_repo, folder.name, branch='master')
    print(repo.head.commit)
