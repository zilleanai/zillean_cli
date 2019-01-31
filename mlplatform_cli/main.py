import argparse
from .domain import Domain
from .comp import Comp

def main():
    parser = argparse.ArgumentParser(prog='mlplatform-cli',
                                     description='mlplatform command line interface')
    subparsers = parser.add_subparsers(
        dest='subparser_name', help='sub-command help')
    parser_domain = subparsers.add_parser('domain', help='domain help')
    parser_domain.add_argument('COMMAND', type=str, help='COMMAND help')
    parser_domain.add_argument('url', type=str,
                               help='git url for domain or domaincfg')

    parser_comp = subparsers.add_parser('comp', help='comp help')
    parser_comp.add_argument('COMMAND', type=str, help='COMMAND help')
    parser_comp.add_argument('url', type=str,
                               help='git url for comp')
    

    args = parser.parse_args()
    if args.subparser_name == 'domain':
        if args.COMMAND == 'install':
            domain = Domain(url=args.url)
            domain.install(install_requirements=False)
        if args.COMMAND == 'install_requirements':
            Domain.install_comps(domaincfg=args.url, project_dir='.', install_requirements=True)
    if args.subparser_name == 'comp':
        if args.COMMAND == 'install':
            comp = Comp(url=args.url)
            comp.install()


if __name__ == "__main__":
    main()
