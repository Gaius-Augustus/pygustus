import pytest
from pygustus import *
import os
import pygustus.util as util
import shutil


@pytest.mark.ghactions
def test_etraining_new_species():
    test_species_name = 'pygustus_test_spec'
    test_config_dir = 'tests/data/config'
    os.environ['AUGUSTUS_CONFIG_PATH'] = test_config_dir

    # remove test species if exists
    species_dir = os.path.join(test_config_dir, 'species', test_species_name)
    if os.path.exists(species_dir):
        shutil.rmtree(species_dir)

    # create species
    cmd = 'tests/data/scripts/new_species.pl'
    options = [f'--species={test_species_name}']
    util.execute_bin(cmd, options)

    # execute training for new species
    etraining.train('tests/data/genes.gb.train',
                    species=test_species_name, softmasking=False)


@pytest.mark.ghactions
def test_etraining_wrong_parameter():
    with pytest.raises(ValueError):
        etraining.train('tests/data/genes.gb.train',
                        species='pygustus_test_spec', smasking=False)


@pytest.mark.ghactions
def test_etraining_wrong_parameter_format():
    with pytest.raises(ValueError):
        etraining.train('tests/data/genes.gb.train',
                        species=True, softmasking=False)


@pytest.mark.ghactions
def test_etraining_wrong_bin_path():
    with pytest.raises(RuntimeError):
        etraining.train('tests/data/genes.gb.train', species='pygustus_test_spec',
                        softmasking=False, path_to_bin='/usr/local/bin')


@pytest.mark.ghactions
def test_etraining_wrong_bin_path_format():
    with pytest.raises(ValueError):
        etraining.train('tests/data/genes.gb.train', species='pygustus_test_spec',
                        softmasking=False, path_to_bin=42)
