[![Build Test and Publish](https://github.com/Gaius-Augustus/pygustus/workflows/Build%20Test%20and%20Publish/badge.svg)](https://github.com/Gaius-Augustus/pygustus/actions?query=workflow%3A"Build+Test+and+Publish")

# Pygustus
A python wrapper for the gene prediction program AUGUSTUS.

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)

# Requirements
To use Pygustus, an installed or built AUGUSTUS with minimum program version 3.3.2 is required. Using Ubuntu, AUGUSTUS can be installed as follows.

    sudo apt install augustus augustus-data augustus-doc

More information can be found on the [AUGUSTUS GitHub page](https://github.com/Gaius-Augustus/Augustus).

To run Pygustus properly it is necessary that the AUGUSTUS environment variable `AUGUSTUS_CONFIG_PATH` is set correctly and points to the configuration directory.

If AUGUSTUS was built from source and no installation was done (so the command `augustus` is not executable), then the path to the executable can be set as described in the [configuration](#configuration) section.

For Pygustus Python version 3.6 or higher is required.

The following examples assume that Python 3 is the default on the executing system. To ensure the usage of Python 3, the use of a virtual environment is recommended. A virtual environment can be created with [venv](https://docs.python.org/3/library/venv.html).

# Installation
Pygustus is in alpha development status. **Currently it is not recommended for productive use.** Pygustus can be installed from PyPi as follows.
~~~
pip install pygustus
~~~
## Building Pygustus from source
As an alternative to installing Pygustus from PyPi, Pygustus can also be built from source as follows. After cloning the repository from GitHub,
~~~
git clone git@github.com:Gaius-Augustus/pygustus.git
~~~
required dependencies need to be installed.
~~~
pip install -r requirements.txt
pip install -r requirements-dev.txt
~~~
After that Pygustus can be built and installed as follows.
~~~
python setup.py sdist bdist_wheel
pip install dist/pygustus-<VERSION>.tar.gz
~~~
For the execution of the tests `pytest` is used. Example usage:
~~~
pytest -m ghactions tests/
~~~
The test cases marked with `ghactions` are those that are not too expensive in terms of runtime.
# Usage
Pygustuts supports the training and prediction of AUGUSTUS. The prediction can be executed either in a single thread or in parallel. In multithreaded execution, the input file is split into smaller pieces and AUGUSTUS is executed in parallel on partial inputs. Finally, the partial results are joined together.

As values of the parameters for all Pygustus programs only the Python types are permissible.

## Training
To train AUGUSTUS, the etraining program was adopted in Pygustus. More information about the program can be found [here](https://github.com/Gaius-Augustus/Augustus/blob/master/docs/RUNNING-AUGUSTUS.md#retraining-augustus). The usage in Pygustus is as follows.
~~~
from pygustus import etraining

etraining.train('path/to/trainfilename.gb',  species='SPECIES')
~~~
The species to be trained must be present in the config folder of AUGUSTUS (see also AUGUSTUS_CONFIG_PATH). To create a new species, the Perl script `new_species.pl` from the script folder of AUGUSTUS can be used.

If the path to the etraining executable is to be specified temporarily, the Pygustus parameter `path_to_binary=path/to/etraining` can be used.

## Prediction
To run a prediction AUGUSTUS can be executed on the input file as usual or the input file can be split and AUGUSTUS is run on input parts in parallel. For the second variant the Pygustus parameter `jobs=n` must be set with `n > 1`.

### Default (Single Thread)
If the prediction is executed with `jobs=1` (default, may be ommitted), AUGUSTUS is executed on the input file exactly as if one would start AUGUSTUS from the console. Usage example:
~~~
from pygustus import augustus

augustus.predict('path/to/input/file', species='human',
                    UTR=True, softmasking=False)
~~~
To redirect the output to a file the AUGUSTUS parameters `outfile` and `errfile` can be used. Application example for the output of the prediction and the possible errors that occurred 
~~~
augustus.predict('path/to/input/file', species='human',
                UTR=True, softmasking=False
                outfile='out.gff', errfile='out.err')
~~~
If the path to the AUGUSTUS executable is to be specified temporarily, the Pygustus parameter `path_to_binary=path/to/augustus` can be used.

### Multithreaded
If the Pygustus parameter `jobs=n` is set with `n > 1`, then the input file is split into several small files and Augustus is run in parallel for each file with the given parameters. After AUGUSTUS has been executed on all parts, the partial results are combined to the final result. If the parameter `outfile` is set, the result will be saved in the file given there. Otherwise, the result will be saved in the file `augustus.gff` (default). A usage example is shown below.
~~~
from pygustus import augustus

augustus.predict('path/to/input/file', [augustus_parameters],
                    [pygustus_parameters], jobs=n)
~~~
All parameters permitted for AUGUSTUS can be used as augustus_parameters. The following pygustus_parameters are additionally available.

| Parameter | Default Value | Description |
| ----------| --------------| ------------|
| jobs (int) | 1 | If `jobs=n` with `n > 1` is set, AUGUSTUS is executed in parallel on sequence segments or split input files using `n` jobs. After the execution of all jobs, the output files are merged. |
| chunksize (int) | 2500000 | If `chunksize=n` with `n > 0` is set and `jobs > 1`, each AUGUSTUS instance is executed on sequence segments of the maximum size `n`. |
| overlap (int) | 500000 | If `overlap=n` with `n > 1` is set and `jobs > 1`, each AUGUSTUS instance is executed on sequence segments of size `chunksize` and the segments overlap by `n`. |
| partitionHints (bool) | False | If this option is set to True, a hints file is given and `jobs > 1`, then the hints file is split into appropriate pieces for the respective AUGUSTUS jobs. |
| minSplitSize (int) | 0 | The input fasta file is spilt to at least `minSplitSize=n` base pairs. Set `n=0` to split the input in single sequence files. |
| partitionLargeSeqeunces (bool) | False | Parallelize large sequences by automatically setting the AUGUSTUS parameters `predictionStart` and `predictionEnd` based on the given values for `chunksize` and `overlap`. |
| maxSeqSize (int) | 3500000 | The maximum length of a sequence from which the sequence is started to be partitioned. To turn on the paritioning `partitionLargeSeqeunces=True` must be set|
debugOutputDir (string) | None | If the directory is specified, all generated files, i.e. the split of the input file and intermediate results, as well as the generated AUGUSTUS command lines are stored there. This option works only for the parallelization, i. e. `jobs > 1` is set. |
path_to_bin (string) | None | Sets the path to the desired executable version of AUGUSTUS when `augustus.predict()` is called or etraining when `etraining.train()` is called. The path is not saved for further executions.|

To redirect the output to a file the AUGUSTUS parameters `outfile` and `errfile` can be used as for the default case.

## Configuration
The paths to the `augustus` and `etraining` binaries be configured. This path is only used if the Pygustus parameter `path_to_bin` is not specified. This configuration is saved until the next change. The configuration is identical for `pygustus.etraining` and `pygustus.augustus`, so that the following example is restricted to `pygustus.augustus`.

### Read the configured path
To get the the currently configured path to the executable of AUGUSTUS you can proceed as follows.
~~~
from pygustus import augustus

augustus.config_get_bin()
~~~

### Update the path to the binary
To update the currently configured path to the executable of AUGUSTUS you can proceed as follows.
~~~
augustus.config_set_bin(path/to/augustus)
~~~

### Set the default binary
To set the default binary you can proceed as follows.
~~~
augustus.config_set_default_bin()
~~~
This method sets the configured path to the AUGUSTUS executable to `augustus`. This should exist if AUGUSTUS is properly installed on the system.

As mentioned earlier, the configured path can be overridden by specifying the Pygustus parameter `path_to_bin` for the current prediction with augustus or the current training with etraining.

## Help
To have easy access to the AUGUSTUS and Pygustus help system, the following methods are available.

| Method | Description |
| ------ | ----------- |
| help() | Shows usage information about the Pygustus wrapper and its parameters. |
| show_aug_help() | Shows the help output of AUGUSTUS, equivalent to the AUGUSTUS call with the parameter `--help`.|
| show_aug_paramlist() | Shows all possible parameter names of AUGUSTUS, equivalent to the AUGUSTUS call with the parameter `--paramlist`.|
| show_species_info() | Shows species information of AUGUSTUS, equivalent to the AUGUSTUS call with the parameter `--species=help`.|

Usage example
~~~
from pygustus import augustus

augustus.help()
~~~

# Examples
The use of Pygustus is also demonstrated with an executable Python script and a Jupyter notebook. The script assumes that Pygustus and AUGUSTUS are installed as described above.

## Executable example
The following command lines install required dependencies, download the script and execute it. The script creates a folder structure in the working directory and downloads required data. After that different AUGUSTUS prediction examples are executed with Pygtustus.
~~~
pip install wget
wget https://raw.githubusercontent.com/Gaius-Augustus/pygustus/main/examples/aug_run_examples.py
chmod +x aug_run_examples.py
./aug_run_examples.py
~~~
After execution, the debug folder contains the generated AUGUSTUS command lines as well as the split input files for parallel execution.

## Jupyter notebook
How the output of the examples should look like can also be taken from a Jupyter [notebook](https://github.com/Gaius-Augustus/pygustus/blob/main/examples/run_examples.ipynb).
