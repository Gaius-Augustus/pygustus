#!/usr/bin/env python3

from pygustus import augustus


def run_augustus_help():
    augustus.predict('--help')


def change_bin():
    augustus.config_set_bin('/home/daniel/git/Augustus/bin/augustus')


def change_bin_to_default():
    augustus.config_set_default_bin()


def run_augustus_simple():
    augustus.predict('../tests/data/example.fa', species='human',
                     UTR=True, softmasking=False)


def run_augustus_parallel():
    augustus.predict('../tests/data/example.fa', species='human',
                     UTR=True, softmasking=False, jobs=2)


def show_fileinfo():
    augustus.show_fasta_info('../tests/data/example.fa')


if __name__ == '__main__':
    # run_augustus_help()
    # change_bin()
    # run_augustus_simple()
    # change_bin_to_default()
    # run_augustus_simple()
    show_fileinfo()
    run_augustus_parallel()
