import pytest
from pygustus import *


def test_etraining_simple():
    etraining.train('data/genes.gb.train', species='bug', softmasking=False)


def test_etraining_wrong_parameter():
    with pytest.raises(ValueError):
        etraining.train('data/genes.gb.train', species='bug', smasking=False)


def test_etraining_wront_parameter_format():
    with pytest.raises(ValueError):
        etraining.train('data/genes.gb.train', species=True, softmasking=False)


def test_etraining_wrong_bin_path():
    with pytest.raises(RuntimeError):
        etraining.train('data/genes.gb.train', species='bug',
                        softmasking=False, path_to_bin='/usr/local/bin')


def test_etraining_wrong_bin_path_format():
    with pytest.raises(ValueError):
        etraining.train('data/genes.gb.train', species='bug',
                        softmasking=False, path_to_bin=42)
