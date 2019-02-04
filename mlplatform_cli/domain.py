import git
from git import Repo
import os
import tempfile
import yaml
from shutil import copyfile
from .comp import Comp
from cookiecutter.main import cookiecutter


class Domain():
    def __init__(self, url, branch='master'):
        self.url = url
        self.branch = branch

    def install(self, install_requirements=False):

        folder = tempfile.TemporaryDirectory()
        repo = git.Repo.clone_from(self.url, folder.name, branch=self.branch)
        project_dir = cookiecutter(folder.name)
        domain_name = os.path.basename(project_dir)
        with open(os.path.join(project_dir, 'mlplatform-domain.yml'), 'r') as stream:
            domain_cfg = yaml.load(stream)
            domain_name = domain_cfg['name']
            print('[domain] ', domain_name)
            self.install_docker_compose(project_dir)
            self.install_comps(domaincfg=os.path.join(
                project_dir, 'mlplatform-domain.yml'), project_dir=project_dir,
                install_requirements=install_requirements)
        print(project_dir)

    def install_docker_compose(self, project_dir):
        dirname = os.path.dirname(__file__)
        docker_compose = os.path.join(dirname, 'res', 'docker-compose.yml')
        backenddockerfile = os.path.join(dirname, 'res', 'backend.Dockerfile')
        frontenddockerfile = os.path.join(
            dirname, 'res', 'frontend.Dockerfile')
        inituserdb = os.path.join(dirname, 'res', 'init-user-db.sh')
        if not os.path.exists(os.path.join(project_dir, 'docker-compose.yml')):
            copyfile(docker_compose,
                    os.path.join(project_dir, 'docker-compose.yml'))
        if not os.path.exists(os.path.join(project_dir, 'backend.Dockerfile')):
            copyfile(backenddockerfile,
                 os.path.join(project_dir, 'backend.Dockerfile'))
        if not os.path.exists(os.path.join(project_dir, 'frontend.Dockerfile')):
            copyfile(frontenddockerfile,
                 os.path.join(project_dir, 'frontend.Dockerfile'))
        os.makedirs(os.path.join(project_dir, 'docker', 'postgres'))
        if not os.path.exists(os.path.join(project_dir, 'docker', 'postgres', 'init-user-db.sh')):
            copyfile(inituserdb,
                 os.path.join(project_dir, 'docker', 'postgres', 'init-user-db.sh'))

    @staticmethod
    def install_comps(domaincfg='mlplatform-domain.yml', project_dir=None, install_requirements=False):
        bundles_path = os.path.join(project_dir, 'bundles')
        frontend_path = os.path.join(project_dir, 'frontend', 'app', 'comps')
        if not os.path.exists(bundles_path):
            os.makedirs(bundles_path)
            open(os.path.join(bundles_path, '__init__.py'), 'a').close()
        if not os.path.exists(frontend_path):
            os.makedirs(frontend_path)
        with open(domaincfg, 'r') as stream:
            domain_cfg = yaml.load(stream)
            for comp_url in domain_cfg['comps']:
                comp = Comp(comp_url, root_path=project_dir)
                comp.install(install_requirements=install_requirements)
