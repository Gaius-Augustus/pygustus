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
        NAME: 'path_to_bin',
        DEVELOPMENT: False,
        TYPE: TYPE_STRING,
        USAGE: 'path_to_binary=path/to/binary',
        DESCRIPTION: 'Sets the path to the desired executable version of AUGUSTUS when augustus.predict() is called or etraining when etraining.train() is called. The path is not saved for further executions.',
        EXCLUDE_APPS: [EXCLUDE_AUGUSTUS, EXCLUDE_ETRAINING]
    },
    {
        NAME: 'jobs',
        DEVELOPMENT: False,
        TYPE: TYPE_INT,
        USAGE: 'jobs=n',
        DEFAULT: '1',
        DESCRIPTION: 'If this option is set, AUGUSTUS is executed in parallel on sequence segments or split input files using n jobs. After the execution of all jobs, the output files are merged.',
        EXCLUDE_APPS: [EXCLUDE_AUGUSTUS, EXCLUDE_ETRAINING]
    },
    {
        NAME: 'chunksize',
        DEVELOPMENT: False,
        TYPE: TYPE_INT,
        USAGE: 'chunksize=n',
        DEFAULT: '2500000',
        DESCRIPTION: 'If this option is set and jobs > 1, each AUGUSTUS instance is executed on sequence segments of the maximum size n.',
        EXCLUDE_APPS: [EXCLUDE_AUGUSTUS, EXCLUDE_ETRAINING]
    },
    {
        NAME: 'overlap',
        DEVELOPMENT: False,
        TYPE: TYPE_INT,
        USAGE: 'overlap=n',
        DEFAULT: '500000',
        DESCRIPTION: 'If this option is set and jobs > 1, each AUGUSTUS instance is executed on sequence segments and the segments overlap by n.',
        EXCLUDE_APPS: [EXCLUDE_AUGUSTUS, EXCLUDE_ETRAINING]
    },
    {
        NAME: 'partitionHints',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: 'partitionHints=True/False',
        DEFAULT: 'False',
        DESCRIPTION: 'If this option is set to True, a hints file is given and jobs > 1, then the hints file is split into appropriate pieces for the respective AUGUSTUS jobs.',
        EXCLUDE_APPS: [EXCLUDE_AUGUSTUS, EXCLUDE_ETRAINING]
    },
    {
        NAME: 'minSplitSize',
        DEVELOPMENT: False,
        TYPE: TYPE_INT,
        USAGE: 'minSplitSize=n',
        DEFAULT: '0',
        DESCRIPTION: 'The input fasta file is spilt to at least n base pairs. Set this to 0 to split the input in single sequence files.',
        EXCLUDE_APPS: [EXCLUDE_AUGUSTUS, EXCLUDE_ETRAINING]
    },
    {
        NAME: 'maxSeqSize',
        DEVELOPMENT: False,
        TYPE: TYPE_INT,
        USAGE: 'maxSeqSize=n',
        DEFAULT: '3500000',
        DESCRIPTION: 'The maximum length of a sequence from which the sequence is started to be partitioned.',
        EXCLUDE_APPS: [EXCLUDE_AUGUSTUS, EXCLUDE_ETRAINING]
    },
    {
        NAME: 'partitionLargeSeqeunces',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: 'partitionLargeSeqeunces=True/False',
        DEFAULT: 'False',
        DESCRIPTION: 'Parallelize large sequences by automatically setting the AUGUSTUS parameters predictionStart and predictionEnd based on the given values for chunksize and overlap.',
        EXCLUDE_APPS: [EXCLUDE_AUGUSTUS, EXCLUDE_ETRAINING]
    },
    {
        NAME: 'debugOutputDir',
        DEVELOPMENT: False,
        TYPE: TYPE_STRING,
        USAGE: 'debugOutputDir=path/to/dir',
        DEFAULT: None,
        DESCRIPTION: 'If the directory is specified, all generated files, i.e. the split of the input file and intermediate results, as well as the generated AUGUSTUS command lines are stored there. This option works only for the parallelization, i. e. jobs > 1 is set.',
        EXCLUDE_APPS: [EXCLUDE_AUGUSTUS, EXCLUDE_ETRAINING]
    },
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
        DESCRIPTION: 'Predict genes on both strands, just the forward or just the backward strand. This effects the algorithm and for most cases "both" is recommended, even if genes on the unwanted strand then need to be ignored after they are predicted.',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
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
             'exactlyone': 'predict exactly one complete gene'},
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'UTR',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--UTR=true/false',
        DEFAULT: 'False',
        DESCRIPTION: 'Predict the untranslated regions in addition to the coding sequence. This works only for a subset of species for which an UTR model was trained.'
    },
    {
        NAME: 'singlestrand',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--singlestrand=true/false',
        DEFAULT: 'False',
        DESCRIPTION: 'Predict genes independently on each strand, allow overlapping genes on opposite strands. This is less accurate on average.',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'hintsfile',
        DEVELOPMENT: False,
        TYPE: TYPE_STRING,
        USAGE: '--hintsfile=hintsfilename',
        DESCRIPTION: 'When this option is used the prediction uses hints (= extrinsic information). The hintsfile contains the hints in GFF format.',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'AUGUSTUS_CONFIG_PATH',
        DEVELOPMENT: False,
        TYPE: TYPE_STRING,
        USAGE: '--AUGUSTUS_CONFIG_PATH=path',
        DESCRIPTION: 'Path to config directory (overrides environment variable $AUGUSTUS_CONFIG_PATH).',
    },
    {
        NAME: 'alternatives-from-evidence',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--alternatives-from-evidence=true/false',
        DESCRIPTION: 'Report alternative transcripts when they are suggested by hints. AUGUSTUS can then find alternative splice forms when the extrinsic evidence is not reconcilable with constitutive splicing only (1 tx per gene) and no overlaps.',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'alternatives-from-sampling',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--alternatives-from-sampling=true/false',
        DESCRIPTION: 'Report alternative transcripts generated through probabilistic sampling. This can be useful to produce suboptimal but still plausible alternative gene structures.',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'sample',
        DEVELOPMENT: False,
        TYPE: TYPE_INT,
        USAGE: '--sample=n',
        DEFAULT: '100',
        DESCRIPTION: 'The number of sampling iterations. The higher "n" is the more accurate is the estimation of probabilities (=scores output in 6th GFF column) but it usually is not important that the posterior probability is very accurate.',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'minexonintronprob',
        DEVELOPMENT: False,
        TYPE: TYPE_FLOAT,
        USAGE: '--minexonintronprob=p',
        DEFAULT: '0.0',
        DESCRIPTION: 'The posterior probability of every exon and every intron in a transcript must be at least "minexonintronprob", otherwise the transcript is not reported. Value between 0 and 1 (default 0.0).',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]        
    },
    {
        NAME: 'minmeanexonintronprob',
        DEVELOPMENT: False,
        TYPE: TYPE_FLOAT,
        USAGE: '--minmeanexonintronprob=p',
        DEFAULT: '0.0',
        DESCRIPTION: 'The geometric mean of the probabilities of all exons and introns must be at least "minmeanexonintronprob". A value of 0.4 is reasonable if a restriction of results is desired at all. Value between 0 and 1 (default 0.0).',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'maxtracks',
        DEVELOPMENT: False,
        TYPE: TYPE_INT,
        USAGE: '--maxtracks=n',
        DEFAULT: '-1',
        DESCRIPTION: 'The maximum number of tracks when displayed in a genome browser is "maxtracks" (unless maxtracks=-1, then it is unbounded). In cases where all transcripts of a gene overlap at some position this is also the maximal number of transcripts for that gene. We recommend increasing the parameter "maxtracks" for improving sensitivity and setting "maxtracks" to 1 and increasing  minmeanexonintronprob and/or minexonintronprob in order to improve specificity. (default -1)',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'proteinprofile',
        DEVELOPMENT: False,
        TYPE: TYPE_STRING,
        USAGE: '--proteinprofile=filename',
        DESCRIPTION: 'Use the provided protein profile in the Protein-Profile-eXtension (PPX). See PPX section of RUNNING-AUGUSTUS.md.',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'progress',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--progress=true',
        DEFAULT: 'False',
        DESCRIPTION: 'Show a progressmeter.',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'gff3',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--gff3=true/false',
        DEFAULT: 'False',
        DESCRIPTION: 'Output in gff3 format.',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'predictionStart',
        DEVELOPMENT: False,
        TYPE: TYPE_INT,
        USAGE: '--predictionStart=A',
        DESCRIPTION: 'Start prediction at sequence coordinate A. Default: 1. The output coordinates are nevertheless with respect to the sequence start. This is used, for example, to run augustus in parallel on overlappinging tiles of a large chromosome. ',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'predictionEnd',
        DEVELOPMENT: False,
        TYPE: TYPE_INT,
        USAGE: '--predictionEnd=B',
        DESCRIPTION: 'End prediction at sequence coodinate B. Default: sequence length. Feature for pros: If predictionEnd = predictionStart < 0  augustus uses the whole input sequence and just left-shift hints coordinates by B. This is intended for applications in which a sequence fragment is cut out of a chromosome for input to augustus but the hints have still original coordinates.',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'noInFrameStop',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--noInFrameStop=true/false',
        DEFAULT: 'False',
        DESCRIPTION: 'Do not report transcripts with in-frame stop codons. Otherwise, intron-spanning stop codons could occur. Such transcripts are then removed from the output.',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'noprediction',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--noprediction=true/false',
        DESCRIPTION: 'No gene predition is performed. Useful for getting the annotated protein sequences if the input is in Genbank format.',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'uniqueGeneId',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--uniqueGeneId=true/false',
        DEFAULT: 'False',
        DESCRIPTION: 'If true, output gene identifyers like this: seqname.gN. This can be useful to avoid gene name conflicts when parallelizing.',
        EXCLUDE_APPS: [EXCLUDE_ETRAINING]
    },
    {
        NAME: 'softmasking',
        DEVELOPMENT: False,
        TYPE: TYPE_BOOL,
        USAGE: '--softmasking=True/False',
        DEFAULT: 'True',
        DESCRIPTION: 'Softmasked regions are treated as nonexonpart hints. As a consequence, exon overlapping the masked regions are discouraged. If the bases in repeat regions are lower case (a,c,g,t instead of A,C,G,T) in the input, then softmasking should be turned on. Softmasking is on average more accurate then hard-masking with Ns.'
    },
    {
        NAME: 'allow_hinted_splicesites',
        DEVELOPMENT: False,
        TYPE: TYPE_LIST_STRING,
        USAGE: '--allow_hinted_splicesites=atac,...',
        DESCRIPTION: 'Allows other non-standard splice sites, such as at-ac. The given list is appended to the list of standard splice site dinucleotide consensus pairs: gtag,gcag'
    },
    {
        NAME: 'alnfile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/augustus/verbosity',
        DEVELOPMENT: False,
        TYPE: TYPE_INT,
        USAGE: '--/augustus/verbosity=n',
        DEFAULT: '1',
        DESCRIPTION: 'Value of 0, 1, 2 or 3 produce increasingly verbose output.'
    },
    {
        NAME: '/BaseCount/weighingType',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/BaseCount/weightMatrixFile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'bridge_genicpart_bonus',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'canCauseAltSplice',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'capthresh',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'cds',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'checkExAcc',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'codingseq',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'codonAlignmentFile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'complete_genes',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/assmotifqthresh',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/assqthresh',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/dssqthresh',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/compSigScoring',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/conservation',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/covPen',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/ec_score',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_gain',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_loss',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/ali_error',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/computeNumSubs',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/maxIterations',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/mil_factor',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/ec_factor',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/ec_addend',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/ec_thold',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/ic_thold',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/genesWithoutUTRs',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/liftover_all_ECs',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/logreg',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/maxCov',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/omega',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/num_omega',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/num_features',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/scale_codontree',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/oeExtensionWidth',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/onlySampledECs',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/only_species',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/outdir_orthoexons',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/outdir',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/printOrthoExonAli',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/printExonCandsMSA',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/printConservationWig',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/phylo_factor',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/phylo_model',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/dd_factor',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/dd_rounds',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/dd_step_rule',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/dualdecomp',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/overlapcomp',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/lambda',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/almost_identical_maxdiff',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/amberprob',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/ass_end',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/ass_maxbinsize',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/ass_start',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/ass_upwindow_size',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/decomp_num_at',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/decomp_num_gc',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/decomp_num_steps',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/dss_end',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/dss_maxbinsize',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/dss_start',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/gc_range_max',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/gc_range_min',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/init_coding_len',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/intterm_coding_len',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/max_contra_supp_ratio',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/min_coding_len',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/ochreprob',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/opalprob',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/probNinCoding',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/subopt_transcript_threshold',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/tis_maxbinsize',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/trans_init_window',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Constant/tss_upwindow_size',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'contentmodels',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'CRF',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'CRF_N',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'CRF_TRAIN',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'CRFtrainCDS',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'CRFtrainIntron',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'CRFtrainIgenic',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'CRFtrainSS',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'CRFtrainUTR',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'CRFtrainTIS',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'dbaccess',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'dbhints',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/EHMMTraining/state00',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/EHMMTraining/state01',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/EHMMTraining/state02',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/EHMMTraining/state03',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/EHMMTraining/statecount',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/EHMMTraining/trainfile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'emiprobs',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'errfile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'evalset',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'exoncands',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/etorder',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/etpseudocount',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/exonlengthD',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/infile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/k',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/lenboostE',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/lenboostL',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/maxexonlength',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/minexonlength',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/minPatSum',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/minwindowcount',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/outfile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/patpseudocount',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/slope_of_bandwidth',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/tisalpha',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/tis_motif_memory',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/tis_motif_radius',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ExonModel/verbosity',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'exonnames',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'extrinsicCfgFile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'GCwinsize',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'GD_stepsize',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/genbank/verbosity',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/HMMTraining/savefile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IGenicModel/infile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IGenicModel/k',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IGenicModel/outfile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IGenicModel/patpseudocount',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IGenicModel/verbosity',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/allow_dss_consensus_gc',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/ass_motif_memory',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/ass_motif_radius',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/asspseudocount',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/d',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/dssneighborfactor',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/dsspseudocount',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/infile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/k',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/minwindowcount',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/non_ag_ass_prob',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/non_gt_dss_prob',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/outfile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/patpseudocount',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/sf_with_motif',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/slope_of_bandwidth',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/splicefile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/ssalpha',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/IntronModel/verbosity',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'introns',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'keep_viterbi',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'label_flip_prob',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'learning_rate',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'lossweight',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'locustree',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'maxDNAPieceSize',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'maxOvlp',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'max_sgd_inter',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'mea',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'mea_evaluation',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/no_compatible_edges',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/alpha_E',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/alpha_I',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/x0_E',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/x0_I',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/x1_E',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/x1_I',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/y0_E',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/y0_I',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/i1_E',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/i1_I',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/i2_E',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/i2_I',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/j1_E',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/j1_I',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/j2_E',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/j2_I',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/weight_base',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/r_be',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/r_bi',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/weight_exon',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/weight_gene',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/MeaPrediction/weight_utr',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'min_intron_len',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'optCfgFile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'printEvidence',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'printHints',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'printMEA',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'printOEs',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'printSampled',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'printGeneRangesBED',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'printGeneRangesGFF',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'outfile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'param_outfile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'print_blocks',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'print_utr',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'protein',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ProteinModel/allow_truncated',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ProteinModel/exhaustive_substates',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ProteinModel/block_threshold_spec',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ProteinModel/block_threshold_sens',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ProteinModel/blockpart_threshold_spec',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ProteinModel/blockpart_threshold_sens',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ProteinModel/global_factor_threshold',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ProteinModel/absolute_malus_threshold',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ProteinModel/invalid_score',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/ProteinModel/weight',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'referenceFile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'refSpecies',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'rescaleBoni',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'rLogReg',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'scorediffweight',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'speciesfilenames',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'start',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'stop',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'stopCodonExcludedFromCDS',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'temperature',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'tieIgenicIntron',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'trainFeatureFile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'translation_table',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'treefile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'truncateMaskedUTRs',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'tss',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'tts',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'uniqueCDS',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'useAminoAcidRates',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'useNonCodingModel',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'use_sgd',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'useTFprob',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/d_polya_cleavage_max',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/d_polya_cleavage_min',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/d_polyasig_cleavage',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/d_tss_tata_max',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/d_tss_tata_min',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/exonlengthD',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/infile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/k',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/max3singlelength',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/max3termlength',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/maxexonlength',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/minwindowcount',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/outfile',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/patpseudocount',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/prob_polya',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/slope_of_bandwidth',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/tata_end',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/tata_pseudocount',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/tata_start',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/tss_end',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/tss_start',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/tssup_k',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/tssup_patpseudocount',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/tts_motif_memory',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/utr3patternweight',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/utr5patternweight',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/utr3prepatternweight',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/utr5prepatternweight',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/UtrModel/verbosity',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Testing/testMode',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/Testing/workingDir',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score0',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score1',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score2',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score3',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score4',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score5',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score6',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score7',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score8',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score9',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score10',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score11',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score12',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score13',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score14',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score15',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score16',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score17',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score18',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score19',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score20',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score21',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score22',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score23',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score24',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score25',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score26',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score27',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score28',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score29',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score30',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score31',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score32',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score33',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score34',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score35',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/exon_score36',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/intron_score0',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/intron_score1',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/intron_score2',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/CompPred/intron_score3',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'lg_exon_score0',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'lg_exon_score1',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'lg_exon_score2',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: 'lg_exon_score3',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/NAMGene/statecount',
        DEVELOPMENT: True,
        DESCRIPTION: ''
    },
    {
        NAME: '/NAMGene/SynchState',
        DEVELOPMENT: True,
        DESCRIPTION: ''
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
