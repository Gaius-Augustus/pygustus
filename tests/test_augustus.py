import pytest
from augustus import *


def test_augustus_help():
    augustus.run('--help')


def test_augustus_simple():
    augustus.run('data/example.fa', species='human',
                 UTR=True, softmasking=False)


def test_augustus_wrong_parameter():
    with pytest.raises(ValueError):
        augustus.run('data/example.fa', species='human',
                     UTR=True, smasking=False)
