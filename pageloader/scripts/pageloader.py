#!/usr/bin/env python3
from pageloader.cli import parse_args
from pageloader import download
import errno
import logging


def main():
    args = parse_args()
    try:
        download(args.address, args.output)
    except Exception as e:
        if e.errno == errno.ENOENT:
            logging.error('specified path does not exists')
        elif e.errno == errno.EACCES:
            logging.error('specified path write permission denied')


if __name__ == '__main__':
    main()
