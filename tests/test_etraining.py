import pytest
from pygustus import *


@pytest.mark.ghactions
def test_etraining_simple():
    etraining.train('tests/data/genes.gb.train',
                    species='bug', softmasking=False)


@pytest.mark.ghactions
def test_etraining_wrong_parameter():
    with pytest.raises(ValueError):
        etraining.train('tests/data/genes.gb.train',
                        species='bug', smasking=False)


@pytest.mark.ghactions
def test_etraining_wront_parameter_format():
    with pytest.raises(ValueError):
        etraining.train('tests/data/genes.gb.train',
                        species=True, softmasking=False)


@pytest.mark.ghactions
def test_etraining_wrong_bin_path():
    with pytest.raises(RuntimeError):
        etraining.train('tests/data/genes.gb.train', species='bug',
                        softmasking=False, path_to_bin='/usr/local/bin')


@pytest.mark.ghactions
def test_etraining_wrong_bin_path_format():
    with pytest.raises(ValueError):
        etraining.train('tests/data/genes.gb.train', species='bug',
                        softmasking=False, path_to_bin=42)
