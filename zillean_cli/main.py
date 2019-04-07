import argparse
from .domain import Domain
from .comp import Comp

def main():
    parser = argparse.ArgumentParser(prog='zillean-cli',
                                     description='zillean command line interface')
    subparsers = parser.add_subparsers(
        dest='subparser_name', help='sub-command help')
    parser_domain = subparsers.add_parser('domain', help='domain help')
    parser_domain.add_argument('COMMAND', type=str, help='COMMAND help')
    parser_domain.add_argument('url', type=str,
                               help='git url for domain or domaincfg')
    parser_domain.add_argument('--no_py', action='store_true',
                               help='do not install python requirements')
    parser_domain.add_argument('--no_js', action='store_true',
                               help='do not install javascript dependencies')

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
            Domain.install_comps(domaincfg=args.url, project_dir='.', install_requirements=True, no_py=args.no_py, no_js=args.no_js)
    if args.subparser_name == 'comp':
        if args.COMMAND == 'install':
            comp = Comp(url=args.url)
            comp.install()


if __name__ == "__main__":
    main()
