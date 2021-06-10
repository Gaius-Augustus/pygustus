#!/usr/bin/env python3

from pygustus import augustus
from pygustus import etraining

import subprocess


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


def run_augustus_parallel_one_sequence():
    augustus.predict('../tests/data/genome.fa', species='human',
                     UTR=True, softmasking=True, jobs=5)


def run_augustus_unique_geneid():
    augustus.predict('../tests/data/example.fa', species='human',
                     UTR=True, softmasking=False, uniqueGeneId=True)


def show_fileinfo():
    augustus.show_fasta_info('../tests/data/example.fa')


def run_training():
    etraining.train('../tests/data/genes.gb.train',
                    species='pygustus_test', softmasking=False)


if __name__ == '__main__':
    # run_augustus_help()
    # change_bin()
    # run_augustus_simple()
    # change_bin_to_default()
    run_augustus_simple()
    # show_fileinfo()
    # run_augustus_parallel()
    # run_augustus_unique_geneid()
    # run_training()
