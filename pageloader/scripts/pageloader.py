#!/usr/bin/env python3
from pageloader.cli import parse_args
from pageloader.download import download


def main():
    args = parse_args()
    path = download(args.address, args.output)
    print(path)


if __name__ == '__main__':
    main()
