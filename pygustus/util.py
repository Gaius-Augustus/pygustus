import subprocess
import os
import re
import json
import shutil
import tempfile
from shutil import which
from pygustus.options.aug_options import *
from pkg_resources import resource_filename
import pygustus.fasta_methods as fm
import pygustus.gff_methods as gff
from concurrent.futures import ThreadPoolExecutor


def execute_bin_parallel(cmd, aug_options, jobs, chunksize, overlap, partition_sequences, part_hints, minsize, max_seq_size, debug_dir):
    print(f'Execute AUGUSTUS with {jobs} jobs in parallel.')

    input_file = aug_options.get_input_filename()[1]
    joined_outfile = aug_options.get_value_or_none('outfile')
    if not joined_outfile:
        joined_outfile = 'augustus.gff'

    options = list()
    outfiles = list()
    with tempfile.TemporaryDirectory(prefix='.tmp_') as tmpdir:
        hintsfile = aug_options.get_value_or_none('hintsfile')

        run_information = fm.split(
            input_file, tmpdir, chunksize, overlap, partition_sequences, minsize, max_seq_size)

        for ri in run_information:
            runno = str(ri['run'])
            fileidx = str(ri['fileidx'])
            seqinfo = ri['seqinfo']
            outfile = os.path.join(tmpdir, f'augustus_{runno}.gff')
            outfiles.append(outfile)
            curfile = create_split_filenanme(input_file, tmpdir, fileidx)
            aug_options.set_input_filename(curfile)
            aug_options.set_value('outfile', outfile)
            aug_options.remove('predictionStart')
            aug_options.remove('predictionEnd')
            if len(seqinfo) == 1 and list(seqinfo.values())[0][0] > 0 and list(seqinfo.values())[0][1] > 0:
                aug_options.set_value(
                    'predictionStart', list(seqinfo.values())[0][0])
                aug_options.set_value(
                    'predictionEnd', list(seqinfo.values())[0][1])
            if hintsfile and part_hints:
                tmp_hintsfile = os.path.join(
                    tmpdir, f'augustus_hints_{str(runno)}.gff')
                gff.create_hint_parts(
                    hintsfile, tmp_hintsfile, seqinfo)
                aug_options.set_value('hintsfile', tmp_hintsfile)
            options.append(aug_options.get_options())

        with ThreadPoolExecutor(max_workers=int(jobs)) as executor:
            for opt in options:
                executor.submit(execute_bin, cmd, opt)

        gff.join_aug_pred(joined_outfile, outfiles)
        print(f'Joined output written to: {joined_outfile}')

        if debug_dir:
            rmtree_if_exists(debug_dir, even_none_empty=True)
            shutil.copytree(src=tmpdir, dst=debug_dir)
            cmd_filename = os.path.join(debug_dir, 'aug_cmd_lines.txt')
            with open(cmd_filename, "w") as file:
                for o in options:
                    file.write(str(o) + '\n' + '\n')


def execute_bin(cmd, options):
    # execute given binary with given options
    result = ''

    try:
        result = subprocess.check_output(
            [cmd] + options,
            stderr=subprocess.STDOUT,
            universal_newlines=True)
    except subprocess.CalledProcessError as cpe:
        print("Returncode", cpe.returncode, cpe.output)

    if len(result.strip()):
        print(result.strip())


def check_bin(bin):
    if which(bin) is None:
        raise RuntimeError(
            f'{bin} cannot be found or is not executable!')


def check_file(inputfile):
    if not os.path.exists(inputfile):
        raise ValueError(f'Could not open {inputfile}')


def mkdir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)


def rmtree_if_exists(dir, even_none_empty=False):
    if os.path.exists(dir):
        if even_none_empty or len(os.listdir(dir)) == 0:
            shutil.rmtree(dir)


def get_options(*args, options, path_to_params, program, **kwargs):
    if options is None:
        options = AugustusOptions(
            *args, parameter_file=path_to_params, app=program, **kwargs)
    else:
        for arg in args:
            options.add_argument(arg)
        for option, value in kwargs.items():
            options.set_value(option, value)
    return options


def get_path_to_binary(options, program):
    bin = options.get_value_or_none('path_to_bin')
    if bin and not os.path.exists(bin):
        raise ValueError(
            f'{program} binaries cannot be found under specified path: {bin}.')
    return bin


def get_config_item(name):
    config_file = resource_filename('pygustus', 'config.json')
    with open(config_file, 'r') as file:
        config = json.load(file)

    return config.get(name)


def set_config_item(name, value):
    config_file = resource_filename('pygustus', 'config.json')
    with open(config_file, 'r+') as file:
        config = json.load(file)
        config.update({name: value})
        file.seek(0)
        file.truncate()
        json.dump(config, file, indent=4, sort_keys=False)


def create_split_filenanme(inputfile, outputdir, idx):
    filename = os.path.basename(inputfile)
    f_name, f_ext = os.path.splitext(filename)
    s_filename = f'{f_name}.split.{str(idx)}{f_ext}'
    return os.path.join(outputdir, s_filename)


def check_aug_version(aug_bin, min_aug_version):
    result = subprocess.run(
        [aug_bin, '--version'],
        capture_output=True, encoding='UTF-8')

    version_str = re.findall(r'\d+.\d+.\d+', result.stderr)[0]
    min_version_no = version_str_to_int(min_aug_version)
    version_no = version_str_to_int(version_str)

    if version_no < min_version_no:
        raise RuntimeError(
            f'AUGUSTUS version {min_aug_version} or higher is required!')


def version_str_to_int(version_str):
    vnumbers = [int(x) for x in version_str.split('.')]
    vnumbers.reverse()
    version_no = sum(x * (100 ** i) for i, x in enumerate(vnumbers))
    return version_no


def get_path_to_parameters_file():
    param_path = os.environ.get('AUGUSTUS_CONFIG_PATH')

    if not param_path:
        raise RuntimeError(
            f'Environment varibale "AUGUSTUS_CONFIG_PATH" is required but not set!')

    param_path = os.path.join(param_path, 'parameters',
                              'aug_cmdln_parameters.json')

    if not os.path.exists(param_path):
        # raise RuntimeError(
        #     f'Parameters file {param_path} cannot be found. Pelase check AUGUSTUS_CONFIG_PATH!')

        # TODO: throw error above and delete the following line when
        # Debian package contains the parameter configutration file
        param_path = resource_filename('pygustus.options', 'parameters.json')

    return param_path


def set_tmp_config_path(options=None, **kwargs):
    '''Set a temporary AUGUSTUS_CONFIG_PATH if it has been passed to the current AUGUSTUS call.'''
    tmp_config_path = kwargs.get('AUGUSTUS_CONFIG_PATH')
    if not tmp_config_path and options:
        tmp_config_path = options.get_value_or_none('AUGUSTUS_CONFIG_PATH')
    if tmp_config_path:
        os.environ['AUGUSTUS_CONFIG_PATH'] = tmp_config_path
