import git
from git import Repo
import os
import tempfile
import yaml
from shutil import copyfile
from .comp import Comp

class Domain():
    def __init__(self, url, branch='master'):
        self.url = url
        self.branch = branch

    def install(self):
        folder = tempfile.TemporaryDirectory()
        repo = git.Repo.clone_from(self.url, folder.name, branch=self.branch)
        copyfile(os.path.join(folder.name, 'mlplatform-domain.yml'),
                 os.path.join('.', 'mlplatform-domain.yml'))
        self.install_comps(domaincfg=os.path.join(
            '.', 'mlplatform-domain.yml'))

    def install_comps(self, domaincfg='mlplatform-domain.yml'):
        with open("mlplatform-domain.yml", 'r') as stream:
            domain_cfg = yaml.load(stream)
            for comp_url in domain_cfg['comps']:
                comp = Comp(comp_url)
                comp.install()