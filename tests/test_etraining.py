import pytest
from pygustus import *
import os
import pygustus.util as util
import shutil


@pytest.mark.ghactions
def test_etraining():
    test_species_name = 'pygustus_test_spec'
    # create new species
    config_dir = os.environ['AUGUSTUS_CONFIG_PATH']
    path_list = config_dir.split('/')
    path_list = path_list[1: len(path_list) - 2]
    path_list.append('scripts')
    script_dir = os.path.join('/', *path_list)
    cmd = f'{script_dir}/new_species.pl'
    options = [f'--species={test_species_name}']
    util.execute_bin(cmd, options)

    etraining.train('tests/data/genes.gb.train',
                    species=test_species_name, softmasking=False)

    # remove test species
    species_dir = os.path.join(config_dir, 'species', test_species_name)
    shutil.rmtree(species_dir)


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
