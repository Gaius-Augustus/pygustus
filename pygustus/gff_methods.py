import os
import re


"""
Support to join results from different AUGUSTUS runs. Based on
the AUGUSTUS script join_aug_pred.pl
"""
# TODO: gff3 support


class Gene:
    def __init__(self, name, start, end, txt):
        self.name = name
        self.start = start
        self.end = end
        self.txt = txt

    def __eq__(self, o: object) -> bool:
        # TODO: use sequence or end also for comparison?
        return isinstance(o, Gene) and self.start == o.start

    def __ne__(self, o: object) -> bool:
        return not self == o

    def __str__(self) -> str:
        return f'Gene {self.name} starts at {self.start} and ends at {self.end}.'

    def rename(self, name):
        old_name = self.name
        self.name = name
        self.txt = self.txt.replace(old_name, name)


class GFFFile:
    def __init__(self) -> None:
        self.header = None
        self.genes = list()

    def add_content(self, filepath):
        """
        Joins the given AUGUSTUS results. The files should be passed in the order of the AUGUSTUS runs.
        """
        if not os.path.isfile(filepath):
            raise ValueError(f'Could not open {filepath}')

        gene_txt = ''
        gene_collection = False
        with open(filepath) as file:
            line = file.readline()
            file_header = ''
            while line:
                # read file header
                if not self.header:
                    go_on1 = not 'prediction on sequence number' in line.strip()
                    go_on2 = not re.search(
                        "Looks like.*is in.*format", line.strip())
                    if go_on1 and go_on2:
                        file_header += line
                    else:
                        self.header = file_header

                # read genes
                # if back compatibility is required add condition like re.search("^### gene g", line.strip())
                if re.search("^# start gene g", line.strip()):
                    gene_collection = True

                if gene_collection:
                    gene_txt += line

                l_split = line.strip().split('\t')
                if len(l_split) > 5:
                    if l_split[2] == 'gene':
                        gname = l_split[-1]
                        gstart = l_split[3]
                        gend = l_split[4]

                # if back compatibility is required add condition like re.search("^### end gene g", line.strip())
                if re.search("^# end gene g", line.strip()):
                    gene = Gene(gname, gstart, gend, gene_txt)

                    # use unique gene name (ids)
                    gid = int(gname.replace('g', ''))
                    if gid <= len(self.genes):
                        new_gid = len(self.genes) + 1
                        gene.rename(f'g{new_gid}')

                    # do not add redundant genes of two possibly overlapping neighboring runs
                    if len(self.genes) > 0:
                        if not gene in self.genes:
                            last_gene = self.genes[-1]
                            if gene.start > last_gene.end:
                                self.genes.append(gene)
                    else:
                        self.genes.append(gene)

                    gene_collection = False
                    gene_txt = ''

                line = file.readline()

    def write(self, filename):
        with open(filename, "w") as file:
            file.write(self.header)
            for g in self.genes:
                file.write(g.txt)
