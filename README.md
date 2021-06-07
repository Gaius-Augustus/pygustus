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

### Training

### Prediction

#### Default (Single Thread)

#### Multithreaded

### Configuration

### Help
