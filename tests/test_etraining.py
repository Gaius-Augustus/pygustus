from pygustus import *


def test_etraining_simple():
    etraining.train('data/genes.gb.train', species='bug', softmasking=False)
