#!/usr/bin/env python3

import augustus


def run_augustus_simple():
    augustus.run('../tests/data/example.fa', species='human', UTR='on',
                 softmasking=False, augustus_parameter_file='../augustus/options/parameters.json')


if __name__ == '__main__':
    run_augustus_simple()
