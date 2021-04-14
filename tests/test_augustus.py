import pytest
import os
import shutil
from pygustus import *
import pygustus.aug_out_filter as afilter
import pygustus.aug_comparator as comp

# TODO: [GH-Actions] upload generated html diff??


def test_augustus_help():
    augustus.predict('--help')


def test_augustus_simple():
    augustus.predict('tests/data/example.fa', species='human',
                     UTR=True, softmasking=False)


def test_augustus_wrong_parameter():
    with pytest.raises(ValueError):
        augustus.predict('tests/data/example.fa', species='human',
                         UTR=True, smasking=False)


def test_augustus_wrong_parameter():
    with pytest.raises(ValueError):
        augustus.predict('tests/data/example.fa', species='human',
                         UTR=True, softmasking=0.42)


def test_augustus_wrong_bin_path():
    with pytest.raises(RuntimeError):
        augustus.predict('tests/data/example.fa', species='human',
                         UTR=True, softmasking=False, path_to_bin='/usr/local/bin')


def test_augustus_wrong_bin_path_format():
    with pytest.raises(ValueError):
        augustus.predict('tests/data/example.fa', species='human',
                         UTR=True, softmasking=False, path_to_bin=False)


def test_augustus_parallel_two_jobs_and_sequences():
    outdir = os.path.join(
        'tests/out', test_augustus_parallel_two_jobs_and_sequences.__name__)
    out_html = os.path.join(outdir, 'output_html')
    out_augustus_tmp = os.path.join(outdir, 'augustus_tmp.gff')
    out_augustus_joined_tmp = os.path.join(outdir, 'augustus_joined_tmp.gff')
    out_augustus = os.path.join(outdir, 'augustus.gff')
    out_augustus_joined = os.path.join(outdir, 'augustus_joined.gff')

    if (os.path.exists(outdir)):
        shutil.rmtree(outdir)
    os.makedirs(outdir)

    assert os.path.exists(outdir)

    # run augustus
    augustus.predict('tests/data/example.fa', species='human',
                     UTR=True, softmasking=False, outfile=out_augustus_tmp)
    assert os.path.exists(out_augustus_tmp)

    # run augustus with two jobs on the same input file
    augustus.predict('tests/data/example.fa', species='human', jobs=2,
                     UTR=True, softmasking=False, outfile=out_augustus_joined_tmp)
    assert os.path.exists(out_augustus_joined_tmp)

    # filter both results
    afilter.pred(out_augustus_tmp, out_augustus)
    afilter.pred(out_augustus_joined_tmp, out_augustus_joined)
    os.remove(out_augustus_tmp)
    os.remove(out_augustus_joined_tmp)

    # compare results
    diff = comp.compare_files(
        out_augustus, out_augustus_joined, html=True, outputfolder=out_html)
    assert diff == ''


def test_augustus_parallel_one_large_sequence():
    outdir = os.path.join(
        'tests/out', test_augustus_parallel_one_large_sequence.__name__)
    out_html = os.path.join(outdir, 'output_html')
    out_augustus_tmp = os.path.join(outdir, 'augustus_tmp.gff')
    out_augustus_joined_tmp = os.path.join(outdir, 'augustus_joined_tmp.gff')
    out_augustus = os.path.join(outdir, 'augustus.gff')
    out_augustus_joined = os.path.join(outdir, 'augustus_joined.gff')

    if (os.path.exists(outdir)):
        shutil.rmtree(outdir)
    os.makedirs(outdir)

    assert os.path.exists(outdir)

    # run augustus
    augustus.predict('tests/data/genome.fa', species='human',
                     UTR=True, softmasking=True, outfile=out_augustus_tmp)
    assert os.path.exists(out_augustus_tmp)

    # run augustus with two jobs on the same input file
    augustus.predict('tests/data/genome.fa', species='human', jobs=5,
                     UTR=True, softmasking=True, outfile=out_augustus_joined_tmp)
    assert os.path.exists(out_augustus_joined_tmp)

    # filter both results
    afilter.pred(out_augustus_tmp, out_augustus)
    afilter.pred(out_augustus_joined_tmp, out_augustus_joined)
    os.remove(out_augustus_tmp)
    os.remove(out_augustus_joined_tmp)

    # compare results
    diff = comp.compare_files(
        out_augustus, out_augustus_joined, html=True, outputfolder=out_html)
    assert diff == ''
