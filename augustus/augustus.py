import subprocess
import sys

__all__ = ['run']

# can be overriden by user to specify path to AUGUSTUS
AUGUSTUS_COMMAND = "augustus"


class AugustusOptions:
    # can easily be read from file, validation info could also be stored there - could also be ignored.
    _allowed_options = [
        "allow_hinted_splicesites",
        "alnfile",
        "alternatives-from-evidence",
        "alternatives-from-sampling",
        "/augustus/verbosity",
        "/BaseCount/weighingType",
        "/BaseCount/weightMatrixFile",
        "bridge_genicpart_bonus",
        "canCauseAltSplice",
        "capthresh",
        "cds",
        "checkExAcc",
        "codingseq",
        "codonAlignmentFile",
        "complete_genes",
        "/CompPred/assmotifqthresh",
        "/CompPred/assqthresh",
        "/CompPred/dssqthresh",
        "/CompPred/compSigScoring",
        "/CompPred/conservation",
        "/CompPred/covPen",
        "/CompPred/ec_score",
        "/CompPred/exon_gain",
        "/CompPred/exon_loss",
        "/CompPred/ali_error",
        "/CompPred/computeNumSubs",
        "/CompPred/maxIterations",
        "/CompPred/mil_factor",
        "/CompPred/ec_factor",
        "/CompPred/ec_addend",
        "/CompPred/ec_thold",
        "/CompPred/ic_thold",
        "/CompPred/genesWithoutUTRs",
        "/CompPred/liftover_all_ECs",
        "/CompPred/logreg",
        "/CompPred/maxCov",
        "/CompPred/omega",
        "/CompPred/num_omega",
        "/CompPred/num_features",
        "/CompPred/scale_codontree",
        "/CompPred/oeExtensionWidth",
        "/CompPred/onlySampledECs",
        "/CompPred/only_species",
        "/CompPred/outdir_orthoexons",
        "/CompPred/outdir",
        "/CompPred/printOrthoExonAli",
        "/CompPred/printConservationWig",
        "/CompPred/phylo_factor",
        "/CompPred/phylo_model",
        "/CompPred/dd_factor",
        "/CompPred/dd_rounds",
        "/CompPred/dd_step_rule",
        "/CompPred/dualdecomp",
        "/CompPred/overlapcomp",
        "/CompPred/lambda",
        "/Constant/almost_identical_maxdiff",
        "/Constant/amberprob",
        "/Constant/ass_end",
        "/Constant/ass_maxbinsize",
        "/Constant/ass_start",
        "/Constant/ass_upwindow_size",
        "/Constant/decomp_num_at",
        "/Constant/decomp_num_gc",
        "/Constant/decomp_num_steps",
        "/Constant/dss_end",
        "/Constant/dss_maxbinsize",
        "/Constant/dss_start",
        "/Constant/gc_range_max",
        "/Constant/gc_range_min",
        "/Constant/init_coding_len",
        "/Constant/intterm_coding_len",
        "/Constant/max_contra_supp_ratio",
        "/Constant/min_coding_len",
        "/Constant/ochreprob",
        "/Constant/opalprob",
        "/Constant/probNinCoding",
        "/Constant/subopt_transcript_threshold",
        "/Constant/tis_maxbinsize",
        "/Constant/trans_init_window",
        "/Constant/tss_upwindow_size",
        "contentmodels",
        "CRF",
        "CRF_N",
        "CRF_TRAIN",
        "CRFtrainCDS",
        "CRFtrainIntron",
        "CRFtrainIgenic",
        "CRFtrainSS",
        "CRFtrainUTR",
        "CRFtrainTIS",
        "dbaccess",
        "dbhints",
        "/EHMMTraining/state00",
        "/EHMMTraining/state01",
        "/EHMMTraining/state02",
        "/EHMMTraining/state03",
        "/EHMMTraining/statecount",
        "/EHMMTraining/trainfile",
        "emiprobs",
        "errfile",
        "evalset",
        "exoncands",
        "/ExonModel/etorder",
        "/ExonModel/etpseudocount",
        "/ExonModel/exonlengthD",
        "/ExonModel/infile",
        "/ExonModel/k",
        "/ExonModel/lenboostE",
        "/ExonModel/lenboostL",
        "/ExonModel/maxexonlength",
        "/ExonModel/minexonlength",
        "/ExonModel/minPatSum",
        "/ExonModel/minwindowcount",
        "/ExonModel/outfile",
        "/ExonModel/patpseudocount",
        "/ExonModel/slope_of_bandwidth",
        "/ExonModel/tisalpha",
        "/ExonModel/tis_motif_memory",
        "/ExonModel/tis_motif_radius",
        "/ExonModel/verbosity",
        "exonnames",
        "GCwinsize",
        "GD_stepsize",
        "/genbank/verbosity",
        "gff3",
        "/HMMTraining/savefile",
        "/IGenicModel/infile",
        "/IGenicModel/k",
        "/IGenicModel/outfile",
        "/IGenicModel/patpseudocount",
        "/IGenicModel/verbosity",
        "/IntronModel/allow_dss_consensus_gc",
        "/IntronModel/ass_motif_memory",
        "/IntronModel/ass_motif_radius",
        "/IntronModel/asspseudocount",
        "/IntronModel/d",
        "/IntronModel/dssneighborfactor",
        "/IntronModel/dsspseudocount",
        "/IntronModel/infile",
        "/IntronModel/k",
        "/IntronModel/minwindowcount",
        "/IntronModel/non_ag_ass_prob",
        "/IntronModel/non_gt_dss_prob",
        "/IntronModel/outfile",
        "/IntronModel/patpseudocount",
        "/IntronModel/sf_with_motif",
        "/IntronModel/slope_of_bandwidth",
        "/IntronModel/splicefile",
        "/IntronModel/ssalpha",
        "/IntronModel/verbosity",
        "introns",
        "keep_viterbi",
        "label_flip_prob",
        "learning_rate",
        "lossweight",
        "locustree",
        "maxDNAPieceSize",
        "maxOvlp",
        "maxtracks",
        "max_sgd_inter",
        "mea",
        "mea_evaluation",
        "/MeaPrediction/no_compatible_edges",
        "/MeaPrediction/alpha_E",
        "/MeaPrediction/alpha_I",
        "/MeaPrediction/x0_E",
        "/MeaPrediction/x0_I",
        "/MeaPrediction/x1_E",
        "/MeaPrediction/x1_I",
        "/MeaPrediction/y0_E",
        "/MeaPrediction/y0_I",
        "/MeaPrediction/i1_E",
        "/MeaPrediction/i1_I",
        "/MeaPrediction/i2_E",
        "/MeaPrediction/i2_I",
        "/MeaPrediction/j1_E",
        "/MeaPrediction/j1_I",
        "/MeaPrediction/j2_E",
        "/MeaPrediction/j2_I",
        "/MeaPrediction/weight_base",
        "/MeaPrediction/r_be",
        "/MeaPrediction/r_bi",
        "/MeaPrediction/weight_exon",
        "/MeaPrediction/weight_gene",
        "/MeaPrediction/weight_utr",
        "minexonintronprob",
        "min_intron_len",
        "minmeanexonintronprob",
        "noInFrameStop",
        "noprediction",
        "printHints",
        "printMEA",
        "printOEs",
        "printSampled",
        "printGeneRangesBED",
        "printGeneRangesGFF",
        "outfile",
        "param_outfile",
        "predictionEnd",
        "predictionStart",
        "print_blocks",
        "print_utr",
        "progress",
        "protein",
        "/ProteinModel/allow_truncated",
        "/ProteinModel/exhaustive_substates",
        "/ProteinModel/block_threshold_spec",
        "/ProteinModel/block_threshold_sens",
        "/ProteinModel/blockpart_threshold_spec",
        "/ProteinModel/blockpart_threshold_sens",
        "/ProteinModel/global_factor_threshold",
        "/ProteinModel/absolute_malus_threshold",
        "/ProteinModel/invalid_score",
        "/ProteinModel/weight",
        "proteinprofile",
        "referenceFile",
        "refSpecies",
        "rescaleBoni",
        "rLogReg",
        "sample",
        "scorediffweight",
        "softmasking",
        "speciesfilenames",
        "start",
        "stop",
        "stopCodonExcludedFromCDS",
        "strand",
        "temperature",
        "tieIgenicIntron",
        "trainFeatureFile",
        "translation_table",
        "treefile",
        "truncateMaskedUTRs",
        "tss",
        "tts",
        "uniqueCDS",
        "uniqueGeneId",
        "useAminoAcidRates",
        "useNonCodingModel",
        "use_sgd",
        "useTFprob",
        "/UtrModel/d_polya_cleavage_max",
        "/UtrModel/d_polya_cleavage_min",
        "/UtrModel/d_polyasig_cleavage",
        "/UtrModel/d_tss_tata_max",
        "/UtrModel/d_tss_tata_min",
        "/UtrModel/exonlengthD",
        "/UtrModel/infile",
        "/UtrModel/k",
        "/UtrModel/max3singlelength",
        "/UtrModel/max3termlength",
        "/UtrModel/maxexonlength",
        "/UtrModel/minwindowcount",
        "/UtrModel/outfile",
        "/UtrModel/patpseudocount",
        "/UtrModel/prob_polya",
        "/UtrModel/slope_of_bandwidth",
        "/UtrModel/tata_end",
        "/UtrModel/tata_pseudocount",
        "/UtrModel/tata_start",
        "/UtrModel/tss_end",
        "/UtrModel/tss_start",
        "/UtrModel/tssup_k",
        "/UtrModel/tssup_patpseudocount",
        "/UtrModel/tts_motif_memory",
        "/UtrModel/utr3patternweight",
        "/UtrModel/utr5patternweight",
        "/UtrModel/utr3prepatternweight",
        "/UtrModel/utr5prepatternweight",
        "/UtrModel/verbosity"]

    def __init__(self, *args, **kwargs):
        # TODO possibly load allowed_parameters, including additional information, from text file
        self._options = {}
        self._args = []
        if len(args) > 0:
            self._args += args
        for option, value in kwargs.items():
            self.set_value(option, value)

    def add_arguments(self, *args):
        self._args += args

    def add_argument(self, arg):
        print(arg)
        self._args.append(arg)

    def get_arguments(self):
        return self._args

    def set_value(self, option, value):
        if option not in self._allowed_options:
            # raise ValueError('Invalid Parameter for Augustus: %s' % option)
            # TODO disable check for now
            pass
        # TODO possibly also validate type of option and value here
        self._options[option] = value

    def get_value(self, option):
        if option not in self._options:
            raise ValueError('Unknown option: %s' % option)
        return self._options[option]

    def get_options(self):
        opts = []
        for option, value in self._options.items():
            opts.append("--%s=%s" % (option, value))
        opts += self._args
        return opts

    def __str__(self):
        optstr = ""
        for option, value in self._options.items():
            optstr += "--%s=%s " % (option, value)
        if len(self._args):
            optstr += " ".join(self._args)
        return optstr


def run(*args, options=None, **kwargs):
    if options is None:
        options = AugustusOptions(*args, **kwargs)
    else:
        for arg in args:
            options.add_argument(arg)
        for option, value in kwargs.items():
            options.set_value(option, value)

    cmd = "%s %s" % (AUGUSTUS_COMMAND, options)
    process = subprocess.Popen(
        [AUGUSTUS_COMMAND] + options.get_options(), stdout=subprocess.PIPE)
    # TODO better output handling including stderr
    for line in process.stdout:
        sys.stdout.write(line)
