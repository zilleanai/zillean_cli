import git
from git import Repo
import os
import tempfile
import yaml
from shutil import copyfile


class Comp():
    def __init__(self, url, branch='master'):
        self.url = url
        self.branch = branch

    def install(self):
        folder = tempfile.TemporaryDirectory()
        repo = git.Repo.clone_from(self.url, folder.name, branch=self.branch)
        compname = 'unnamed'
        with open(os.path.join(folder.name, 'mlplatform-comp.yml'), 'r') as stream:
            comp_cfg = yaml.load(stream)
            compname = comp_cfg['name']
        os.makedirs(compname, exist_ok=True)
        copyfile(os.path.join(folder.name, 'mlplatform-comp.yml'),
                 os.path.join(compname, 'mlplatform-comp.yml'))
