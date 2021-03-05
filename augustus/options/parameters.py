#!/usr/bin/env python3

import json
import argparse
from constant import *

parser = argparse.ArgumentParser(
    description='Creates JSON file with all allowed AUGUSTUS parameters.')
parser.add_argument('-n', '--filename',
                    help='Desired file name for the JSON export. Default: parameters.json.')
args = parser.parse_args()

allowed_parameters = [
    {
        NAME: 'species',
        DEVELOPMENT: False,
        TYPE: TYPE_STRING,
        USAGE: '--species=SPECIES queryfilename',
        DESCRIPTION: 'The "queryfilename" is the filename (including relative path) to the file containing the query sequence(s) and SPECIES is an identifier for the species. Use --species=help to see a list in fasta format.'
    },
    {
        NAME: 'strand',
        DEVELOPMENT: False,
        TYPE: TYPE_STRING,
        USAGE: '--strand=both/forward/backward',
        VALUES: ['both', 'forward', 'backward'],
        DEFAULT: 'both',
        DESCRIPTION: 'Report predicted genes on both strands, just the forward or just the backward strand.'
    },
    {
        NAME: 'genemodel',
        DEVELOPMENT: False,
        TYPE: TYPE_STRING,
        USAGE: '--genemodel=partial/intronless/complete/atleastone/exactlyone',
        VALUES: ['partial', 'intronless', 'complete', 'atleastone', 'exactlyone'],
        DEFAULT: 'partial',
        DESCRIPTION:
            {'partial': 'allow prediction of incomplete genes at the sequence boundaries (default)',
             'intronless': 'only predict single-exon genes like in prokaryotes and some eukaryotes',
             'complete': 'only predict complete genes',
             'atleastone': 'predict at least one complete gene',
             'exactlyone': 'predict exactly one complete gene'}
    },
    {
        NAME: 'UTR',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--UTR=true/false',
        VALUES: [True, False],
        DEFAULT: False,
        DESCRIPTION: 'Predict the untranslated regions in addition to the coding sequence. This currently works only for a subset of species.'
    },
    {
        NAME: 'singlestrand',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--singlestrand=true/false',
        VALUES:  [True, False],
        DEFAULT: False,
        DESCRIPTION: 'Predict genes independently on each strand, allow overlapping genes on opposite strands.'
    },
    {
        NAME: 'hintsfile',
        DEVELOPMENT: False,
        TYPE: TYPE_STRING,
        USAGE: '--hintsfile=hintsfilename',
        DESCRIPTION: 'When this option is used the prediction considering hints (extrinsic information) is turned on. The hintsfile contains the hints in gff format.'
    },
    {
        NAME: 'AUGUSTUS_CONFIG_PATH',
        DEVELOPMENT: False,
        TYPE: TYPE_STRING,
        USAGE: '--AUGUSTUS_CONFIG_PATH=path',
        DESCRIPTION: 'Path to config directory (if not specified as environment variable).'
    },
    {
        NAME: 'alternatives-from-evidence',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--alternatives-from-evidence=true/false',
        VALUES: [True, False],
        DESCRIPTION: 'Report alternative transcripts when they are suggested by hints.'
    },
    {
        NAME: 'alternatives-from-sampling',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--alternatives-from-sampling=true/false',
        VALUES: [True, False],
        DESCRIPTION: 'Report alternative transcripts generated through probabilistic sampling.'
    },
    {
        NAME: 'sample',
        DEVELOPMENT: False,
        TYPE: TYPE_INT,
        USAGE: '--sample=n',
        DEFAULT: 100,
        DESCRIPTION: 'The number of sampling iterations. The higher "n" is the more accurate is the estimation but it usually is not important that the posterior probability is very accurate.'
    },
    {
        NAME: 'minexonintronprob',
        DEVELOPMENT: False,
        TYPE: TYPE_FLOAT,
        USAGE: '--minexonintronprob=p',
        # TODO: add some text and/or update reference? Dependencies?
        DESCRIPTION: 'For a description see section 4 of README.TXT'
    },
    {
        NAME: 'minmeanexonintronprob',
        DEVELOPMENT: False,
        TYPE: TYPE_FLOAT,
        USAGE: '--minmeanexonintronprob=p',
        # TODO: add some text and/or update reference? Dependencies?
        DESCRIPTION: 'For a description see section 4 of README.TXT'
    },
    {
        NAME: 'maxtracks',
        DEVELOPMENT: False,
        TYPE: TYPE_INT,
        USAGE: '--maxtracks=n',
        # TODO: add some text and/or update reference? Dependencies?
        DESCRIPTION: 'For a description see section 4 of README.TXT'
    },
    {
        NAME: 'proteinprofile',
        DEVELOPMENT: False,
        TYPE: TYPE_STRING,
        USAGE: '--proteinprofile=filename',
        DESCRIPTION: 'When this option is used the prediction will consider the protein profile provided as parameter. The protein profile extension is described in section 7 of README.TXT.'  # TODO: update reference?
    },
    {
        NAME: 'progress',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--progress=true',
        VALUES: [True, False],
        DEFAULT: False,
        DESCRIPTION: 'Show a progressmeter.'
    },
    {
        NAME: 'gff3',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--gff3=true/false',
        VALUES: [True, False],
        DESCRIPTION: 'Output in gff3 format.'
    },
    {
        NAME: 'predictionStart',
        DEVELOPMENT: False,
        TYPE: TYPE_INT,
        USAGE: '--predictionStart=A --predictionEnd=B', # TODO: update usage and description
        DESCRIPTION: 'A and B define the range of the sequence for which predictions should be found.',
    },
    {
        NAME: 'predictionEnd',
        DEVELOPMENT: False,
        TYPE: TYPE_INT,
        USAGE: '--predictionStart=A --predictionEnd=B', # TODO: update usage and description
        DESCRIPTION: 'A and B define the range of the sequence for which predictions should be found.',
    },
    {
        NAME: 'noInFrameStop',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--noInFrameStop=true/false',
        VALUES: [True, False],
        DEFAULT: False,
        DESCRIPTION: 'Do not report transcripts with in-frame stop codons. Otherwise, intron-spanning stop codons could occur.'
    },
    {
        NAME: 'noprediction',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--noprediction=true/false',
        VALUES: [True, False],
        DESCRIPTION: 'If true and input is in genbank format, no prediction is made. Useful for getting the annotated protein sequences.'
    },
    {
        NAME: 'uniqueGeneId',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--uniqueGeneId=true/false',
        VALUES: [True, False],
        DESCRIPTION: 'If true, output gene identifyers like this: seqname.gN.'
    },
    {
        NAME: 'softmasking',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--softmasking=True/False',
        VALUES: [True, False],
        DEFAULT: True,
        DESCRIPTION: 'If the bases in repeat regions are lower case (a,c,g,t instead of A,C,G,T) in the input, then softmasking should be turned on.'
    },
    {
        NAME: 'allow_hinted_splicesites',
        DEVELOPMENT: False,
        TYPE: TYPE_LIST_STRING,
        USAGE: '--allow_hinted_splicesites=gcag,atac',
        DESCRIPTION: 'Allows other non-standard splice sites, such as ac-at.'
    }
]


def export(filename='parameters.json'):
    with open(filename, 'w') as file:
        json.dump(allowed_parameters, file, indent=4, sort_keys=False)


def sort_key(item):
    return item[NAME].lower()

if __name__ == '__main__':
    allowed_parameters.sort(key=sort_key)
    if args.filename is not None:
        export(args.filename)
    else:
        export()
