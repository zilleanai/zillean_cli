import git
from git import Repo
import os
import tempfile
import yaml
import json
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
            self.install_py_requirements(
                os.path.join(folder.name, 'requirements.txt'))
            self.install_js_requirements(os.path.join(folder.name))
        if not os.path.exists(os.path.join(self.root_path, 'bundles', compname)):
            copytree(os.path.join(folder.name, compname),
                     os.path.join(self.root_path, 'bundles', compname))
        # install frontend
        if os.path.exists(os.path.join(folder.name, "frontend", compname)):
            if not os.path.exists(os.path.join(self.root_path, "frontend", "app", "comps", compname)):
                copytree(os.path.join(folder.name, "frontend", compname),
                         os.path.join(self.root_path, "frontend", "app", "comps", compname))
        copyfile(os.path.join(folder.name, 'mlplatform-comp.yml'),
                 os.path.join(self.root_path, 'bundles', compname, 'mlplatform-comp.yml'))

        self.install_deps(os.path.join(
            self.root_path, 'bundles', compname, 'mlplatform-comp.yml'), install_requirements=install_requirements)

    def install_deps(self, compcfg='mlplatform-comp.yml', install_requirements=False):
        with open(compcfg, 'r') as stream:
            comp_cfg = yaml.load(stream)
            if 'depends' in comp_cfg:
                for comp_url in comp_cfg['depends']:
                    comp = Comp(comp_url, root_path=self.root_path)
                    comp.install(install_requirements=install_requirements)

    def install_py_requirements(self, requirements_file):
        try:
            subprocess.run(
                ["pip", "install", "-r", requirements_file])
        except Exception as e:
            pass

    def install_js_requirements(self, package_folder):
        if os.path.exists(os.path.join(package_folder, 'package.json')):
            with open(os.path.join(package_folder, 'package.json')) as f:
                data = json.load(f)
                for key in data['dependencies']:
                    try:
                        subprocess.run(
                            ["npm", "install", key])
                    except Exception as e:
                        pass
