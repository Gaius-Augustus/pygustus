#!/usr/bin/env python3

import json
import argparse
import constant as const

parser = argparse.ArgumentParser(
    description='Creates JSON file with all allowed AUGUSTUS parameters.')
parser.add_argument('-n', '--filename',
                    help='Desired file name for the JSON export. Default: parameters.json.')
args = parser.parse_args()

allowed_parameters = [
    {
        const.NAME: 'species',
        const.TYPE: const.TYPE_STRING,
        const.USAGE: '--species=SPECIES queryfilename',
        const.DESCRIPTION: 'The "queryfilename" is the filename (including relative path) to the file containing the query sequence(s) and SPECIES is an identifier for the species. Use --species=help to see a list in fasta format.'
    },
    {
        const.NAME: 'strand',
        const.TYPE: const.TYPE_STRING,
        const.USAGE: '--strand=both/forward/backward',
        const.VALUES: ['both', 'forward', 'backward'],
        const.DEFAULT: 'both',
        const.DESCRIPTION: 'Report predicted genes on both strands, just the forward or just the backward strand.'
    },
    {
        const.NAME: 'genemodel',
        const.TYPE: const.TYPE_STRING,
        const.USAGE: '--genemodel=partial/intronless/complete/atleastone/exactlyone',
        const.VALUES: ['partial', 'intronless', 'complete', 'atleastone', 'exactlyone'],
        const.DEFAULT: 'partial',
        const.DESCRIPTION:
            {'partial': 'allow prediction of incomplete genes at the sequence boundaries (default)',
             'intronless': 'only predict single-exon genes like in prokaryotes and some eukaryotes',
             'complete': 'only predict complete genes',
             'atleastone': 'predict at least one complete gene',
             'exactlyone': 'predict exactly one complete gene'}
    },
    {
        const.NAME: 'UTR',
        const.TYPE: const.TYPE_STRING,
        const.USAGE: '--UTR=on/off',
        const.VALUES: ['on', 'off'],
        const.DESCRIPTION: 'Predict the untranslated regions in addition to the coding sequence. This currently works only for a subset of species.'
    },
    {
        const.NAME: 'singlestrand',
        const.TYPE: const.TYPE_STRING,  # TODO: bool??
        const.USAGE: '--singlestrand=true',
        const.VALUES: ['true'],
        const.DESCRIPTION: 'Predict genes independently on each strand, allow overlapping genes on opposite strands. This option is turned off by default.'
    },
    {
        const.NAME: 'hintsfile',
        const.TYPE: const.TYPE_STRING,
        const.USAGE: '--hintsfile=hintsfilename',
        const.DESCRIPTION: 'When this option is used the prediction considering hints (extrinsic information) is turned on. The hintsfile contains the hints in gff format.'
    },
    {
        const.NAME: 'AUGUSTUS_CONFIG_PATH',
        const.TYPE: const.TYPE_STRING,
        const.USAGE: '--AUGUSTUS_CONFIG_PATH=path',
        const.DESCRIPTION: 'Path to config directory (if not specified as environment variable).'
    },
    {
        const.NAME: 'alternatives-from-evidence',
        const.TYPE: const.TYPE_STRING,  # TODO: bool??
        const.USAGE: '--alternatives-from-evidence=true/false',
        const.VALUES: ['true', 'false'],
        const.DESCRIPTION: 'Report alternative transcripts when they are suggested by hints.'
    },
    {
        const.NAME: 'alternatives-from-sampling',
        const.TYPE: const.TYPE_STRING,  # TODO: bool??
        const.USAGE: '--alternatives-from-sampling=true/false',
        const.VALUES: ['true', 'false'],
        const.DESCRIPTION: 'Report alternative transcripts generated through probabilistic sampling.'
    },
    {
        const.NAME: 'sample',
        const.TYPE: const.TYPE_INT,
        const.USAGE: '--sample=n',
        const.DEFAULT: 100,
        const.DESCRIPTION: 'The number of sampling iterations. The higher "n" is the more accurate is the estimation but it usually is not important that the posterior probability is very accurate.'
    },
    {
        const.NAME: 'minexonintronprob',
        const.TYPE: const.TYPE_FLOAT,
        const.USAGE: '--minexonintronprob=p',
        # TODO: add some text and/or update reference? Dependencies?
        const.DESCRIPTION: 'For a description see section 4 of README.TXT'
    },
    {
        const.NAME: 'minmeanexonintronprob',
        const.TYPE: const.TYPE_FLOAT,
        const.USAGE: '--minmeanexonintronprob=p',
        # TODO: add some text and/or update reference? Dependencies?
        const.DESCRIPTION: 'For a description see section 4 of README.TXT'
    },
    {
        const.NAME: 'maxtracks',
        const.TYPE: const.TYPE_INT,
        const.USAGE: '--maxtracks=n',
        # TODO: add some text and/or update reference? Dependencies?
        const.DESCRIPTION: 'For a description see section 4 of README.TXT'
    },
    {
        const.NAME: 'proteinprofile',
        const.TYPE: const.TYPE_STRING,
        const.USAGE: '--proteinprofile=filename',
        const.DESCRIPTION: 'When this option is used the prediction will consider the protein profile provided as parameter. The protein profile extension is described in section 7 of README.TXT.'  # TODO: update reference?
    },
    {
        const.NAME: 'progress',
        const.TYPE: const.TYPE_STRING,  # TODO: bool??
        const.USAGE: '--progress=true',
        const.VALUES: ['true'],
        const.DESCRIPTION: 'Show a progressmeter.'
    },
    {
        const.NAME: 'gff3',
        const.TYPE: const.TYPE_STRING,
        const.USAGE: '--gff3=on/off',
        const.VALUES: ['on', 'off'],
        const.DESCRIPTION: 'Output in gff3 format.'
    },
    {
        const.NAME: 'predictionStart',
        const.TYPE: const.TYPE_STRING,
        const.USAGE: '--predictionStart=A --predictionEnd=B',
        const.DESCRIPTION: 'A and B define the range of the sequence for which predictions should be found.',
        const.DEPENDENCIES: 'predictionEnd'
    },
    {
        const.NAME: 'predictionEnd',
        const.TYPE: const.TYPE_STRING,
        const.USAGE: '--predictionStart=A --predictionEnd=B',
        const.DESCRIPTION: 'A and B define the range of the sequence for which predictions should be found.',
        const.DEPENDENCIES: 'predictionStart'
    },
    {
        const.NAME: 'noInFrameStop',
        const.TYPE: const.TYPE_STRING,  # TODO: bool??
        const.USAGE: '--noInFrameStop=true/false',
        const.VALUES: ['true', 'false'],
        const.DEFAULT: 'false',
        const.DESCRIPTION: 'Do not report transcripts with in-frame stop codons. Otherwise, intron-spanning stop codons could occur.'
    },
    {
        const.NAME: 'noprediction',
        const.TYPE: const.TYPE_STRING,  # TODO: bool??
        const.USAGE: '--noprediction=true/false',
        const.VALUES: ['true', 'false'],
        const.DESCRIPTION: 'If true and input is in genbank format, no prediction is made. Useful for getting the annotated protein sequences.'
    },
    {
        const.NAME: 'uniqueGeneId',
        const.TYPE: const.TYPE_STRING,  # TODO: bool??
        const.USAGE: '--uniqueGeneId=true/false',
        const.VALUES: ['true', 'false'],
        const.DESCRIPTION: 'If true, output gene identifyers like this: seqname.gN.'
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
