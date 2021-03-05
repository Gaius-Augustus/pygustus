#!/usr/bin/env python3

import augustus


def run_augustus_help():
    augustus.predict('--help')


def run_augustus_simple():
    augustus.predict('../tests/data/example.fa', species='human',
                 UTR=True, softmasking=False)


if __name__ == '__main__':
    #run_augustus_help()
    run_augustus_simple()
