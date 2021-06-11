[![Build Test and Publish](https://github.com/Gaius-Augustus/pygustus/workflows/Build%20Test%20and%20Publish/badge.svg)](https://github.com/Gaius-Augustus/pygustus/actions?query=workflow%3A"Build+Test+and+Publish")

# Pygustus
A python wrapper for the gene prediction program AUGUSTUS.

## Requirements
To use Pygustus, an installed or built version of AUGUSTUS is required. Using Ubuntu, AUGUSTUS can be installed as follows.

    sudo apt install augustus augustus-data augustus-doc

More information can be found on the [AUGUSTUS GitHub page](https://github.com/Gaius-Augustus/Augustus).

## Installation
TODO

## Usage
Pygustuts supports the training and prediction of AUGUSTUS. The prediction can be executed either in a single thread or in parallel. In multithreaded execution, the input file is split into smaller pieces and AUGUSTUS is executed in parallel on partial inputs. Finally, the partial results are joined together.

As values of the parameters for all Pygustus programs only the Python types are permissible.

### Training
To train AUGUSTUS, the etraining program was adopted in Pygustus. More information about the program can be found [here](https://github.com/Gaius-Augustus/Augustus/blob/master/docs/RUNNING-AUGUSTUS.md#retraining-augustus). The usage in Pygustus is as follows.
~~~
from pygustus import etraining

etraining.train('path/to/trainfilename',  species='SPECIES')
~~~
The species to be trained must be present in the config folder of AUGUSTUS (see also AUGUSTUS_CONFIG_PATH). To create a new species, the Pearl script `new_species.pl` from the script folder of AUGUSTUS can be used.

If the path to the etraining executable is to be specified temporarily, the Pygustus parameter `path_to_binary=path/to/etraining` can be used.

### Prediction
To run a prediction AUGUSTUS can be executed on the input file as usual or the input file can be split and AUGUSTUS is run on input parts in parallel. For the second variant the Pygustus parameter `jobs=n` must be set with `n > 1`.

#### Default (Single Thread)
If the prediction is started without the Pygustus parameter `jobs=n` or with `n == 1`, AUGUSTUS is executed on the input file exactly as if one would start AUGUSTUS from the console. Usage example:
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

#### Multithreaded
If the Pygustus parameter `jobs=n` is set with `n > 1`, then the input file is split into several small files and Augustus is run in parallel for each file with the given parameters. After AUGUSTUS has been executed on all parts, the partial results are combined to the final result. A usage example is shown below.
~~~
from pygustus import augustus

augustus.predict('path/to/input/file', [augustus_parameters],
                    [pygustus_parameters], jobs=n)
~~~
All parameters permitted for AUGUSTUS can be used as augustus_parameters. The following parameters for Pygustus are available.

| Parameter | Default Value | Description |
| ----------| --------------| ------------|
| jobs (int) | 1             | If this option is set, AUGUSTUS is executed in parallel on sequence segments or split input files using n jobs. After the execution of all jobs, the output files are merged. |
| chunksize (int) | 0 | If this option is set and `jobs > 1`, each AUGUSTUS instance is executed on sequence segments of the maximum size `n`. |
| overlap (int) | 0 | If this option is set and `jobs > 1`, each AUGUSTUS instance is executed on sequence segments of size `chunksize` and the segments overlap by `n`. |
| partitionHints (bool) | False | If this option is set to True, a hints file is given and `jobs > 1`, then the hints file is split into appropriate pieces for the respective AUGUSTUS jobs. |
| minSplitSize (int) | 0 | The input fasta file is spilt to at least `minSplitSize=n` base pairs. Set this to 0 to split the input in single sequence files. |
| partitionLargeSeqeunces (bool) | False | Parallelize large sequences by automatically setting the AUGUSTUS parameters `predictionStart` and `predictionEnd` based on the given values for `chunksize` and `overlap`.





To redirect the output to a file the AUGUSTUS parameters `outfile` and `errfile` can be used as for the default case.

### Configuration

### Help
