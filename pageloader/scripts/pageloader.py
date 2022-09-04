#!/usr/bin/env python3
import requests
from pageloader.cli import parse_args
from pageloader import download
import logging


def main():
    args = parse_args()
    try:
        download(args.address, args.output)
    except FileNotFoundError:
        logging.error('Specified path does not exists')
    except PermissionError:
        logging.error('Specified path write permission denied')
    except requests.URLRequired:
        logging.error('Invalid URL address')
    except requests.ConnectionError:
        logging.error(
            'Cannot connect to specified URL. Probably, some network problem')
    except requests.TooManyRedirects:
        logging.error('Too many redirects on address')
    except requests.Timeout:
        logging.error(
            'Request timed out while trying to connect to the remote server.')


if __name__ == '__main__':
    main()
