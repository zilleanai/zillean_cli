import argparse
from .domain import Domain


def main():
    parser = argparse.ArgumentParser(
        description='mlplatform command line interface')
    parser.add_argument('url', type=str,
                        help='git url for domain')

    args = parser.parse_args()
    print(args.url)

    domain = Domain(url=args.url)
    domain.install()


if __name__ == "__main__":
    main()
