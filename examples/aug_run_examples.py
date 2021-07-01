#!/usr/bin/env python3

"""Executable examples for Pygustus."""

from pygustus import augustus
import shutil
import wget
import os


data_dir = 'data'
out_dir = 'out'
debug_dir = 'debug'


def get_data():
    download_data(
        'https://raw.githubusercontent.com/Gaius-Augustus/pygustus/main/tests/data/example.fa',
        os.path.join(data_dir, 'example.fa'))

    download_data(
        'https://raw.githubusercontent.com/Gaius-Augustus/pygustus/main/tests/data/genome.fa',
        os.path.join(data_dir, 'genome.fa'))


def download_data(data_url, data_file):
    if not os.path.exists(data_file):
        wget.download(data_url, out=data_file)


def init_dir():
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    if os.path.exists(debug_dir):
        shutil.rmtree(debug_dir)
    os.makedirs(debug_dir)


def run_augustus_simple():
    # Executes a simple example and outputs the
    # results on the command line.

    augustus.predict(
        os.path.join(data_dir, 'example.fa'),
        species='human',
        UTR=True, softmasking=False)


def run_augustus_simple_outfile():
    # Executes a simple example and outputs the
    # results in debug/aug_simple.gff.

    out_file = os.path.join(out_dir, 'aug_simple.gff')
    augustus.predict(
        os.path.join(data_dir, 'example.fa'),
        species='human',
        UTR=True, softmasking=False,
        outfile=out_file)


def run_augustus_parallel():
    # Example for parallel execution (input file is split).
    # Joined results stored in out/aug_parallel.gff.
    # Debug output stored in folder debug/run_augustus_parallel.

    out_file = os.path.join(out_dir, 'aug_parallel.gff')
    cur_debug_dir = os.path.join(
        debug_dir, run_augustus_parallel.__name__)
    augustus.predict(
        os.path.join(data_dir, 'example.fa'),
        species='human',
        UTR=True, softmasking=True, jobs=2,
        outfile=out_file,
        debugOutputDir=cur_debug_dir)


def run_augustus_parallel_on_seq():
    # Example for parallel execution (automatically setting the AUGUSTUS
    # parameters predictionStart and predictionEnd based on the given values
    # for chunksize and overlap).
    # Joined results stored in out/aug_parallel_on_seq.gff.
    # Debug output stored in folder debug/run_augustus_parallel_on_seq.

    out_file = os.path.join(out_dir, 'aug_parallel_on_seq.gff')
    cur_debug_dir = os.path.join(
        debug_dir, run_augustus_parallel_on_seq.__name__)
    augustus.predict(
        os.path.join(data_dir, 'genome.fa'),
        species='human',
        UTR=True, softmasking=True, jobs=5,
        outfile=out_file,
        partitionLargeSeqeunces=True,
        chunksize=250000,
        overlap=50000,
        maxSeqSize=750000,
        debugOutputDir=cur_debug_dir)


def show_fileinfo():
    # Shows fasta file information.
    augustus.show_fasta_info('data/example.fa')


if __name__ == '__main__':
    print('##### Init structure #####')
    init_dir()
    get_data()
    print('\n##### Run run_augustus_simple #####')
    run_augustus_simple()
    print('\n##### Run run_augustus_simple_outfile #####')
    run_augustus_simple_outfile()
    print('\n##### Run run_augustus_parallel #####')
    run_augustus_parallel()
    print('\n##### Run run_augustus_parallel_on_seq #####')
    run_augustus_parallel_on_seq()
    print('\n##### Run show_fileinfo #####')
    show_fileinfo()
