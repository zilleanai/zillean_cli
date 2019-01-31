import git
from git import Repo
import os
import tempfile
import yaml
from shutil import copyfile, copytree
import subprocess


class Comp():
    def __init__(self, url, branch='master', root_path='.'):
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
                subprocess.run(
                    ["pip", "install", "-r", os.path.join(folder.name, 'requirements.txt')])
            except Exception as e:
                pass
            try:
                if os.path.exists(os.path.join(folder.name, 'package.json')):
                    subprocess.run(
                        ["npm", "install", "--prefix", os.path.join(folder.name)])
            except Exception as e:
                pass
        if not os.path.exists(os.path.join(self.root_path, 'comps', compname)):
            copytree(os.path.join(folder.name, compname),
                     os.path.join(self.root_path, 'comps', compname))
        # install frontend
        if os.path.exists(os.path.join(folder.name, "frontend", compname)):
            if not os.path.exists(os.path.join(self.root_path, "frontend", compname)):
                copytree(os.path.join(folder.name, "frontend", compname),
                         os.path.join(self.root_path, "frontend", compname))
        copyfile(os.path.join(folder.name, 'mlplatform-comp.yml'),
                 os.path.join(self.root_path, 'comps', compname, 'mlplatform-comp.yml'))

        self.install_deps(os.path.join(
            self.root_path, 'comps', compname, 'mlplatform-comp.yml'), install_requirements=install_requirements)

    def install_deps(self, compcfg='mlplatform-comp.yml', install_requirements=False):
        with open(compcfg, 'r') as stream:
            comp_cfg = yaml.load(stream)
            if 'depends' in comp_cfg:
                for comp_url in comp_cfg['depends']:
                    comp = Comp(comp_url, root_path=self.root_path)
                    comp.install(install_requirements=install_requirements)
