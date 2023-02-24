from Bio import SeqIO
import pygustus.util as util


def summarize_acgt_content(inputfile):
    util.check_file(inputfile)

    letters = ['a', 'c', 'g', 't', 'n']
    file_sum = dict.fromkeys(letters, 0)
    file_sum.update({'rest': 0})
    seq_count = 0

    for seq_record in SeqIO.parse(inputfile, 'fasta'):
        seq_count += 1
        seq_sum = 0
        print_seq_acgt = ''

        for l in letters:
            value = seq_record.seq.lower().count(l)
            seq_sum += value
            if l != 'n':
                print_seq_acgt += f'   {value} {l}'
            else:
                if value > 0:
                    print_seq_acgt += f'   {value} {l}'

            update_values(file_sum, l, value)

        rest = len(seq_record) - seq_sum
        if rest > 0:
            print_seq_acgt += f'   {rest} ?'
            update_values(file_sum, 'rest', rest)

        print_seq_line = f'{len(seq_record)} bases.\t{seq_record.id} BASE COUNT  {print_seq_acgt}'
        print(print_seq_line)

    summary_acgt = ''
    complete_bp = 0
    sum_acgt = 0

    for l in letters:
        if l != 'n':
            summary_acgt += f'   {file_sum[l]} {l}'
            complete_bp += file_sum[l]

    sum_acgt += complete_bp

    if file_sum['n'] > 0:
        summary_acgt += f'   {file_sum[l]} {l}'
        complete_bp += file_sum['n']

    if file_sum['rest'] > 0:
        summary_acgt += f'   {file_sum[l]} {l}'
        complete_bp += file_sum['rest']

    gc = 100 * float(file_sum['g'] + file_sum['c']) / sum_acgt

    print(f'summary: BASE COUNT  {summary_acgt}')
    print(f'total {complete_bp}bp in {seq_count} sequence(s).')
    print(f'gc: {gc}%')


def update_values(file_sum, key, value):
    cur_value = file_sum[key]
    file_sum.update({key: cur_value + value})


def split(inputfile, outputdir, chunksize, overlap, partition_sequences, minsize, max_seq_size):
    util.check_file(inputfile)
    util.rmtree_if_exists(outputdir, even_none_empty=True)
    util.mkdir_if_not_exists(outputdir)

    fileidx = 0
    run = 0
    filesize = 0
    records_to_write = list()
    records = list(SeqIO.parse(inputfile, 'fasta'))
    run_information = list()

    for seq_record in records:
        seqsize = len(seq_record)

        if seqsize > max_seq_size:
            if len(records_to_write) > 0:
                fileidx += 1
                run += 1
                run_information.append(
                    {
                        'run': run,
                        'fileidx': fileidx,
                        'seqinfo': {x.id: [0, 0] for x in records_to_write}
                    })
                write_file(records_to_write, inputfile, outputdir, fileidx)
                filesize = 0

            fileidx += 1
            write_file([seq_record], inputfile, outputdir, fileidx)
            if partition_sequences:
                if chunksize == 0:
                    chunksize = 2500000
                if chunksize > 3500000:
                    chunksize = 3500000
                if overlap == 0:
                    overlap = int(chunksize / 6)
                chunks = list()
                go_on = True
                while go_on:
                    if len(chunks) == 0:
                        chunks.append([1, chunksize])
                    else:
                        last_start, last_end = chunks[-1]
                        start = last_end + 1 - overlap
                        end = start + chunksize - 1
                        if end >= seqsize:
                            end = seqsize
                            go_on = False
                        chunks.append([start, end])
                for c in chunks:
                    run += 1
                    run_information.append(
                        {
                            'run': run,
                            'fileidx': fileidx,
                            'seqinfo': {seq_record.id: [c[0], c[1]]}
                        })
            else:
                run += 1
                run_information.append(
                    {
                        'run': run,
                        'fileidx': fileidx,
                        'seqinfo': {seq_record.id: [0, 0]}
                    })
        elif minsize == 0 or filesize + seqsize >= minsize or seq_record.id == records[-1].id:
            records_to_write.append(seq_record)
            fileidx += 1
            run += 1
            run_information.append(
                {
                    'run': run,
                    'fileidx': fileidx,
                    'seqinfo': {x.id: [0, 0] for x in records_to_write}
                })
            write_file(records_to_write, inputfile, outputdir, fileidx)
            filesize = 0
        else:
            records_to_write.append(seq_record)
            filesize += seqsize

    return run_information


def write_file(records_to_write, inputfile, outputdir, fileidx):
    splitpath = util.create_split_filenanme(
        inputfile, outputdir, fileidx)
    SeqIO.write(records_to_write, splitpath, 'fasta')
    records_to_write.clear()


def get_sequence_count(inputfile):
    util.check_file(inputfile)
    sequences = list(SeqIO.parse(inputfile, 'fasta'))
    return len(sequences)


def get_sequence_size(inputfile, idx=0):
    util.check_file(inputfile)
    sequences = list(SeqIO.parse(inputfile, 'fasta'))
    return len(sequences[idx])


def get_sequence_id(inputfile, idx=0):
    util.check_file(inputfile)
    sequences = list(SeqIO.parse(inputfile, 'fasta'))
    return sequences[idx].id
