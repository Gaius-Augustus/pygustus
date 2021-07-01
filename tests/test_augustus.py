import pytest
import os
import shutil
from pygustus import *
import pygustus.aug_out_filter as afilter
import pygustus.aug_comparator as comp
import wget
import tarfile

# TODO: [GH-Actions] upload generated html diff??


@pytest.mark.ghactions
def test_augustus_help():
    augustus.predict('--help')


@pytest.mark.ghactions
def test_augustus_simple():
    augustus.predict('tests/data/example.fa', species='human',
                     UTR=True, softmasking=False)


@pytest.mark.ghactions
def test_augustus_wrong_parameter():
    with pytest.raises(ValueError):
        augustus.predict('tests/data/example.fa', species='human',
                         UTR=True, smasking=False)


@pytest.mark.ghactions
def test_augustus_wrong_parameter():
    with pytest.raises(ValueError):
        augustus.predict('tests/data/example.fa', species='human',
                         UTR=True, softmasking=0.42)


@pytest.mark.ghactions
def test_augustus_wrong_bin_path():
    with pytest.raises(RuntimeError):
        augustus.predict('tests/data/example.fa', species='human',
                         UTR=True, softmasking=False, path_to_bin='/usr/local/bin')


@pytest.mark.ghactions
def test_augustus_wrong_bin_path_format():
    with pytest.raises(ValueError):
        augustus.predict('tests/data/example.fa', species='human',
                         UTR=True, softmasking=False, path_to_bin=False)


@pytest.mark.ghactions
def test_augustus_parallel_two_jobs_and_sequences():
    name = test_augustus_parallel_two_jobs_and_sequences.__name__
    options = {'species': 'human', 'UTR': True, 'softmasking': False}

    run_parallel_tests('tests/data/example.fa', jobs=2, testname=name,
                       options=options)


@pytest.mark.ghactions
def test_augustus_parallel_with_hints():
    name = test_augustus_parallel_with_hints.__name__
    options = {'species': 'human', 'UTR': True, 'softmasking': False,
               'hintsfile': 'tests/data/hints.gff',
               'extrinsicCfgFile': 'tests/data/config/extrinsic/extrinsic.MPE.cfg'}

    run_parallel_tests('tests/data/example.fa', jobs=2, testname=name,
                       options=options)


@pytest.mark.ghactions
def test_augustus_parallel_two_jobs_unique_geneid():
    name = test_augustus_parallel_two_jobs_unique_geneid.__name__
    options = {'species': 'human', 'UTR': True, 'softmasking': False,
               'uniqueGeneId': True}

    run_parallel_tests('tests/data/example.fa', jobs=2, testname=name,
                       options=options)


@pytest.mark.ghactions
def test_augustus_parallel_two_jobs_and_sequences_gff3():
    name = test_augustus_parallel_two_jobs_and_sequences_gff3.__name__
    options = {'species': 'human', 'UTR': True, 'softmasking': False,
               'gff3': True}

    run_parallel_tests('tests/data/example.fa', jobs=2, testname=name,
                       options=options)


@pytest.mark.ghactions
def test_augustus_parallel_two_jobs_gff3_and_geneid():
    name = test_augustus_parallel_two_jobs_gff3_and_geneid.__name__
    options = {'species': 'human', 'UTR': True, 'softmasking': False,
               'gff3': True, 'uniqueGeneId': True}

    run_parallel_tests('tests/data/example.fa', jobs=2, testname=name,
                       options=options)


@pytest.mark.ghactions
def test_augustus_parallel_one_large_sequence():
    name = test_augustus_parallel_one_large_sequence.__name__
    options = {
        'species': 'human',
        'UTR': True,
        'softmasking': True,
        'partitionLargeSeqeunces': True,
        'chunksize': 250000,
        'overlap': 50000,
        'maxSeqSize': 750000
        }

    run_parallel_tests('tests/data/genome.fa', jobs=5, testname=name,
                       options=options)


def run_parallel_tests(inputfile, jobs, testname, options):
    outdir = os.path.join('tests/out', testname)
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
    augustus.predict(inputfile, **options, outfile=out_augustus_tmp)
    assert os.path.exists(out_augustus_tmp)

    # run multiple augustus jobs on the same input file
    augustus.predict(inputfile, **options,
                     outfile=out_augustus_joined_tmp, jobs=jobs)
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


@pytest.mark.expensive
def test_augustus_parallel_large_sequence_hints():
    outdir = os.path.join(
        'tests/out', test_augustus_parallel_large_sequence_hints.__name__)
    out_html = os.path.join(outdir, 'output_html')
    out_augustus_tmp = os.path.join(
        'tests/data/chr2L/reference', 'aug.nasonia.hints.joined_tmp.gff')
    out_augustus_joined_tmp = os.path.join(outdir, 'augustus_joined_tmp.gff')
    out_augustus = os.path.join(outdir, 'aug.nasonia.hints.joined.gff')
    out_augustus_joined = os.path.join(outdir, 'augustus_joined.gff')
    options = {'species': 'nasonia', 'softmasking': True, 'chunksize': 3500000, 'overlap': 700000,
               'hintsfile': 'tests/data/chr2L/hints.gff', 'partitionLargeSeqeunces': True,
               'extrinsicCfgFile': 'tests/data/config/extrinsic/extrinsic.M.RM.E.W.cfg'}
    if (os.path.exists(outdir)):
        shutil.rmtree(outdir)
    os.makedirs(outdir)

    assert os.path.exists(outdir)

    # run multiple augustus jobs on the same input file
    augustus.predict('tests/data/chr2L/chr2L.sm.fa.gz', **options,
                     outfile=out_augustus_joined_tmp, jobs=9)
    assert os.path.exists(out_augustus_joined_tmp)

    # filter both results
    afilter.pred(out_augustus_tmp, out_augustus)
    afilter.pred(out_augustus_joined_tmp, out_augustus_joined)
    os.remove(out_augustus_joined_tmp)

    # compare results
    diff = comp.compare_files(
        out_augustus, out_augustus_joined, html=True, outputfolder=out_html)
    assert diff == ''


@pytest.mark.expensive
def test_augustus_parallel_large_sequence_partition_hints():
    outdir = os.path.join(
        'tests/out', test_augustus_parallel_large_sequence_partition_hints.__name__)
    out_html = os.path.join(outdir, 'output_html')
    out_augustus_tmp = os.path.join(
        'tests/data/chr2L/reference', 'aug.nasonia.hints.part.joined_tmp.gff')
    out_augustus_joined_tmp = os.path.join(outdir, 'augustus_joined_tmp.gff')
    out_augustus = os.path.join(outdir, 'aug.nasonia.hints.joined.gff')
    out_augustus_joined = os.path.join(outdir, 'augustus_joined.gff')
    options = {'species': 'nasonia', 'softmasking': True, 'chunksize': 3500000, 'overlap': 700000,
               'hintsfile': 'tests/data/chr2L/hints.gff', 'partitionHints': True,
               'partitionLargeSeqeunces': True,
               'extrinsicCfgFile': 'tests/data/config/extrinsic/extrinsic.M.RM.E.W.cfg'}
    if (os.path.exists(outdir)):
        shutil.rmtree(outdir)
    os.makedirs(outdir)

    assert os.path.exists(outdir)

    # run multiple augustus jobs on the same input file
    augustus.predict('tests/data/chr2L/chr2L.sm.fa.gz', **options,
                     outfile=out_augustus_joined_tmp, jobs=9)
    assert os.path.exists(out_augustus_joined_tmp)

    # filter both results
    afilter.pred(out_augustus_tmp, out_augustus)
    afilter.pred(out_augustus_joined_tmp, out_augustus_joined)
    os.remove(out_augustus_joined_tmp)

    # compare results
    diff = comp.compare_files(
        out_augustus, out_augustus_joined, html=True, outputfolder=out_html)
    assert diff == ''


@pytest.mark.expensive
def test_chlamy_parallel():
    datadir = 'tests/data'
    testdir = os.path.join(datadir, 'chlamy')

    if not os.path.exists(testdir):
        data_url = 'http://augustus.uni-greifswald.de/bioinf/downloads/data/chlamy/chlamy.tgz'
        data_file = os.path.join(datadir, 'chlamy.tgz')
        wget.download(data_url, out=data_file)

        data_tar = tarfile.open(data_file)
        data_tar.extractall(datadir)
        data_tar.close()
        os.remove(data_file)

    outdir = os.path.join(
        'tests/out', test_chlamy_parallel.__name__)
    out_augustus_joined_tmp = os.path.join(outdir, 'augustus_joined_tmp.gff')
    if (os.path.exists(outdir)):
        shutil.rmtree(outdir)
    os.makedirs(outdir)

    options = {'species': 'chlamy2011', 'softmasking': True, 'partitionLargeSeqeunces': False,
               'minSplitSize': 1000000, 'hintsfile': 'tests/data/chlamy/hints.gff', 'UTR': True,
               'extrinsicCfgFile': 'tests/data/config/extrinsic/extrinsic.M.RM.E.W.cfg'}

    augustus.predict('tests/data/chlamy/genome.fa', **options,
                     outfile=out_augustus_joined_tmp, jobs=8)
