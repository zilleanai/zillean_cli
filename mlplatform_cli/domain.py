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
        domain_name = None
        with open(os.path.join(folder.name, 'mlplatform-domain.yml'), 'r') as stream:
            domain_cfg = yaml.load(stream)
            domain_name = domain_cfg['name']
            if not os.path.exists(domain_name):
                os.makedirs(domain_name)
            copyfile(os.path.join(folder.name, 'mlplatform-domain.yml'),
                     os.path.join(domain_name, 'mlplatform-domain.yml'))
            self.install_docker_compose(domain_name)
            self.install_comps(domaincfg=os.path.join(
                domain_name, 'mlplatform-domain.yml'), domain_name=domain_name)

    def install_docker_compose(self, domain_name):
        dirname = os.path.dirname(__file__)
        docker_compose = os.path.join(dirname, 'res', 'docker-compose.yml')
        copyfile(docker_compose,
                 os.path.join(domain_name, 'docker-compose.yml'))

    def install_comps(self, domaincfg='mlplatform-domain.yml', domain_name=None):
        root_path = os.path.join(domain_name, 'comps')
        if not os.path.exists(root_path):
            os.makedirs(root_path)
        with open(domaincfg, 'r') as stream:
            domain_cfg = yaml.load(stream)
            for comp_url in domain_cfg['comps']:
                comp = Comp(comp_url, root_path=root_path)
                comp.install()
