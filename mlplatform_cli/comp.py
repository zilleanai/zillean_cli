import git
from git import Repo
import os
import tempfile
import yaml
from shutil import copyfile, copytree
import subprocess

class Comp():
    def __init__(self, url, branch='master', root_path='comps'):
        self.url = url
        self.branch = branch
        self.root_path = root_path

    def install(self, install_requirements=False):
        folder = tempfile.TemporaryDirectory()
        repo = git.Repo.clone_from(self.url, folder.name, branch=self.branch)
        compname = 'unnamed'
        with open(os.path.join(folder.name, 'mlplatform-comp.yml'), 'r') as stream:
            comp_cfg = yaml.load(stream)
            compname = comp_cfg['name']
            print('[comp] ', compname)
        if install_requirements:
            try:
                subprocess.run(["pip", "install", "-r", os.path.join(folder.name, 'requirements.txt')])
            except SystemExit as e:
                pass

        copytree(os.path.join(folder.name, compname),
            os.path.join(self.root_path, compname))
        copyfile(os.path.join(folder.name, 'mlplatform-comp.yml'),
                 os.path.join(self.root_path, compname, 'mlplatform-comp.yml'))

        self.install_deps(os.path.join(self.root_path, compname, 'mlplatform-comp.yml'))

    def install_deps(self, compcfg='mlplatform-comp.yml', install_requirements=False):
        with open(compcfg, 'r') as stream:
            comp_cfg = yaml.load(stream)
            if 'depends' in comp_cfg:
                for comp_url in comp_cfg['depends']:
                    comp = Comp(comp_url, root_path=self.root_path)
                    comp.install(install_requirements=install_requirements)
