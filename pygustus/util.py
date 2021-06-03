import subprocess
import os
import json
import shutil
import tempfile
from shutil import which
from pygustus.options.aug_options import *
from pkg_resources import resource_filename
import pygustus.fasta_methods as fm
import pygustus.gff_methods as gff
from concurrent.futures import ThreadPoolExecutor


def execute_bin_parallel(cmd, aug_options, jobs, chunksize, overlap, partition_sequences, part_hints, minsize):
    print(f'Execute AUGUSTUS with {jobs} jobs in parallel.')

    input_file = aug_options.get_input_filename()[1]
    joined_outfile = aug_options.get_value_or_none('outfile')
    if not joined_outfile:
        joined_outfile = 'augustus.gff'
    if not chunksize:
        chunksize = 0
    if not overlap:
        overlap = 0
    if not partition_sequences:
        partition_sequences = False
    if not part_hints:
        part_hints = False
    if not minsize:
        minsize = 0

    options = list()
    outfiles = list()
    with tempfile.TemporaryDirectory(prefix='.tmp_') as tmpdir:
        hintsfile = aug_options.get_value_or_none('hintsfile')

        run_information = fm.split(
            input_file, tmpdir, chunksize, overlap, partition_sequences, minsize)

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

        # TODO: create debug output
        # for o in options:
        #     print(o)

        gff.join_aug_pred(joined_outfile, outfiles)

        # for testing purposes
        # shutil.copytree(src=tmpdir, dst='tests/tmp')


def execute_bin(cmd, options, print_err=True, std_out_file=None, error_out_file=None, mode='w'):
    # execute given binary with given options

    if std_out_file and error_out_file and mode:
        with open(std_out_file, mode) as file:
            with open(error_out_file, mode) as errfile:
                process = subprocess.Popen(
                    [cmd] + options,
                    stdout=file,
                    stderr=errfile,
                    universal_newlines=True)
    elif std_out_file and mode:
        with open(std_out_file, mode) as file:
            process = subprocess.Popen(
                [cmd] + options,
                stdout=file,
                stderr=subprocess.PIPE,
                universal_newlines=True)
    else:
        process = subprocess.Popen(
            [cmd] + options,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)

    rc = process.wait()

    if not std_out_file:
        output = process.stdout.read()
        if len(output.strip()):
            print(output)

    if print_err and process.stderr:
        error = process.stderr.read()
        if len(error.strip()):
            print(error)

    if rc != 0:
        print(f'Unexpected returncode {rc}!')


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
