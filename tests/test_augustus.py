import pytest
from augustus import *


def test_augustus_help():
    augustus.run('--help')


def test_augustus_simple():
    augustus.run('data/example.fa', species='human',
                 UTR='on', softmaskingg=False)


def test_augustus_wrong_parameter():
    with pytest.raises(ValueError):
        augustus.run('data/example.fa', species='human',
                     UTR='on', smasking=False)
