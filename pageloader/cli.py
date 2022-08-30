import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        prog='page-loader',
        description='page downloader'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='set destination EXISTING folder',
        default=None
    )
    parser.add_argument(
        'address',
        type=str,
        help='resource address to download'
    )
    args = parser.parse_args()
    return args
