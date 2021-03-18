import pytest
from pygustus import *


def test_augustus_help():
    augustus.predict('--help')


def test_augustus_simple():
    augustus.predict('data/example.fa', species='human',
                     UTR=True, softmasking=False)


def test_augustus_wrong_parameter():
    with pytest.raises(ValueError):
        augustus.predict('data/example.fa', species='human',
                         UTR=True, smasking=False)


def test_augustus_wrong_bin_path():
    with pytest.raises(RuntimeError):
        augustus.predict('data/example.fa', species='human',
                         UTR=True, softmasking=False, path_to_bin='/usr/local/bin')
