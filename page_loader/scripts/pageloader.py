#!/usr/bin/env python3
from page_loader.cli import parse_args
from page_loader import download
import sys


def main():
    args = parse_args()
    try:
        download(args.address, args.output)
    except Exception:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
