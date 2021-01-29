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
        TYPE: TYPE_STRING,
        USAGE: '--species=SPECIES queryfilename',
        DESCRIPTION: 'The "queryfilename" is the filename (including relative path) to the file containing the query sequence(s) and SPECIES is an identifier for the species. Use --species=help to see a list in fasta format.'
    },
    {
        NAME: 'strand',
        TYPE: TYPE_STRING,
        USAGE: '--strand=both/forward/backward',
        VALUES: ['both', 'forward', 'backward'],
        DEFAULT: 'both',
        DESCRIPTION: 'Report predicted genes on both strands, just the forward or just the backward strand.'
    },
    {
        NAME: 'genemodel',
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
        TYPE: TYPE_STRING,
        USAGE: '--UTR=on/off',
        VALUES: ['on', 'off'],
        DESCRIPTION: 'Predict the untranslated regions in addition to the coding sequence. This currently works only for a subset of species.'
    },
    {
        NAME: 'singlestrand',
        TYPE: TYPE_STRING,  # TODO: bool??
        USAGE: '--singlestrand=true',
        VALUES: ['true'],
        DESCRIPTION: 'Predict genes independently on each strand, allow overlapping genes on opposite strands. This option is turned off by default.'
    },
    {
        NAME: 'hintsfile',
        TYPE: TYPE_STRING,
        USAGE: '--hintsfile=hintsfilename',
        DESCRIPTION: 'When this option is used the prediction considering hints (extrinsic information) is turned on. The hintsfile contains the hints in gff format.'
    },
    {
        NAME: 'AUGUSTUS_CONFIG_PATH',
        TYPE: TYPE_STRING,
        USAGE: '--AUGUSTUS_CONFIG_PATH=path',
        DESCRIPTION: 'Path to config directory (if not specified as environment variable).'
    },
    {
        NAME: 'alternatives-from-evidence',
        TYPE: TYPE_STRING,  # TODO: bool??
        USAGE: '--alternatives-from-evidence=true/false',
        VALUES: ['true', 'false'],
        DESCRIPTION: 'Report alternative transcripts when they are suggested by hints.'
    },
    {
        NAME: 'alternatives-from-sampling',
        TYPE: TYPE_STRING,  # TODO: bool??
        USAGE: '--alternatives-from-sampling=true/false',
        VALUES: ['true', 'false'],
        DESCRIPTION: 'Report alternative transcripts generated through probabilistic sampling.'
    },
    {
        NAME: 'sample',
        TYPE: TYPE_INT,
        USAGE: '--sample=n',
        DEFAULT: 100,
        DESCRIPTION: 'The number of sampling iterations. The higher "n" is the more accurate is the estimation but it usually is not important that the posterior probability is very accurate.'
    },
    {
        NAME: 'minexonintronprob',
        TYPE: TYPE_FLOAT,
        USAGE: '--minexonintronprob=p',
        # TODO: add some text and/or update reference? Dependencies?
        DESCRIPTION: 'For a description see section 4 of README.TXT'
    },
    {
        NAME: 'minmeanexonintronprob',
        TYPE: TYPE_FLOAT,
        USAGE: '--minmeanexonintronprob=p',
        # TODO: add some text and/or update reference? Dependencies?
        DESCRIPTION: 'For a description see section 4 of README.TXT'
    },
    {
        NAME: 'maxtracks',
        TYPE: TYPE_INT,
        USAGE: '--maxtracks=n',
        # TODO: add some text and/or update reference? Dependencies?
        DESCRIPTION: 'For a description see section 4 of README.TXT'
    },
    {
        NAME: 'proteinprofile',
        TYPE: TYPE_STRING,
        USAGE: '--proteinprofile=filename',
        DESCRIPTION: 'When this option is used the prediction will consider the protein profile provided as parameter. The protein profile extension is described in section 7 of README.TXT.'  # TODO: update reference?
    },
    {
        NAME: 'progress',
        TYPE: TYPE_STRING,  # TODO: bool??
        USAGE: '--progress=true',
        VALUES: ['true'],
        DESCRIPTION: 'Show a progressmeter.'
    },
    {
        NAME: 'gff3',
        TYPE: TYPE_STRING,
        USAGE: '--gff3=on/off',
        VALUES: ['on', 'off'],
        DESCRIPTION: 'Output in gff3 format.'
    },
    {
        NAME: 'predictionStart',
        TYPE: TYPE_STRING,
        USAGE: '--predictionStart=A --predictionEnd=B',
        DESCRIPTION: 'A and B define the range of the sequence for which predictions should be found.',
        DEPENDENCIES: 'predictionEnd'
    },
    {
        NAME: 'predictionEnd',
        TYPE: TYPE_STRING,
        USAGE: '--predictionStart=A --predictionEnd=B',
        DESCRIPTION: 'A and B define the range of the sequence for which predictions should be found.',
        DEPENDENCIES: 'predictionStart'
    },
    {
        NAME: 'noInFrameStop',
        TYPE: TYPE_STRING,  # TODO: bool??
        USAGE: '--noInFrameStop=true/false',
        VALUES: ['true', 'false'],
        DEFAULT: 'false',
        DESCRIPTION: 'Do not report transcripts with in-frame stop codons. Otherwise, intron-spanning stop codons could occur.'
    },
    {
        NAME: 'noprediction',
        TYPE: TYPE_STRING,  # TODO: bool??
        USAGE: '--noprediction=true/false',
        VALUES: ['true', 'false'],
        DESCRIPTION: 'If true and input is in genbank format, no prediction is made. Useful for getting the annotated protein sequences.'
    },
    {
        NAME: 'uniqueGeneId',
        TYPE: TYPE_STRING,  # TODO: bool??
        USAGE: '--uniqueGeneId=true/false',
        VALUES: ['true', 'false'],
        DESCRIPTION: 'If true, output gene identifyers like this: seqname.gN.'
    }
]


def export(filename='parameters.json'):
    with open(filename, 'w') as file:
        json.dump(allowed_parameters, file, indent=4, sort_keys=False)


if __name__ == '__main__':
    if args.filename is not None:
        export(args.filename)
    else:
        export()
