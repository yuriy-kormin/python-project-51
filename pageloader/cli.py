import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        prog='page-loader',
        description='hello'
    )
    args = parser.parse_args()
    return args
