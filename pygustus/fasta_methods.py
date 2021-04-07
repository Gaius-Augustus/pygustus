import os
from Bio import SeqIO


def summarize_acgt_content(inputfile):
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
    for l in letters:
        if l != 'n':
            summary_acgt += f'   {file_sum[l]} {l}'
            complete_bp += file_sum[l]

    if file_sum['n'] > 0:
        summary_acgt += f'   {file_sum[l]} {l}'
        complete_bp += file_sum['n']

    if file_sum['rest'] > 0:
        summary_acgt += f'   {file_sum[l]} {l}'
        complete_bp += file_sum['rest']

    gc = 100 * float(file_sum['g'] + file_sum['c']) / complete_bp

    print(f'summary: BASE COUNT  {summary_acgt}')
    print(f'total {complete_bp}bp in {seq_count} sequences.')
    print(f'gc: {gc}%')


def update_values(file_sum, key, value):
    cur_value = file_sum[key]
    file_sum.update({key: cur_value + value})


def split(inputfile, outputpath, minsize=0):
    fileidx = 0
    cursize = 0
    records_to_write = list()
    records = list(SeqIO.parse(inputfile, 'fasta'))

    for seq_record in records:
        cursize += len(seq_record)
        records_to_write.append(seq_record)
        if minsize == 0 or cursize >= minsize or seq_record.id == records[-1].id:
            fileidx += 1
            filename = os.path.basename(inputfile)
            f_name, f_ext = os.path.splitext(filename)
            s_filename = f'{f_name}.split.{fileidx:05d}{f_ext}'
            splitpath = os.path.join(outputpath, s_filename)
            SeqIO.write(records_to_write, splitpath, 'fasta')
            cursize = 0
            records_to_write.clear()
