#!/usr/bin/env python3
from pageloader.cli import parse_args
from pageloader import download


def main():
    args = parse_args()
    download(args.address, args.output)


if __name__ == '__main__':
    main()
