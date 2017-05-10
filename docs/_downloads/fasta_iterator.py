from itertools import groupby
from collections import namedtuple


Fasta = namedtuple("Fasta", ('id', 'comment', 'seq'))


def fasta_iter(fasta_path):
    """
    :param fasta_path: the path to the file containing all input sequences in fasta format.
    :type fasta_file: string
    :author: http://biostar.stackexchange.com/users/36/brentp
    :return: for a given fasta file, it returns an iterator which yields a named tuple
             Fasta (string id, string comment, string sequence)
    :rtype: iterator
    """
    # ditch the boolean (x[0]) and just keep the header or sequence since
    # we know they alternate.
    with open(fasta_path, 'r') as fasta_file:
        faiter = (x[1] for x in groupby(fasta_file, lambda line: line[0] == ">"))
        for header in faiter:
            # drop the ">"
            header = next(header)[1:].strip()
            header = header.split()
            _id = header[0]
            comment = ' '.join(header[1:])
            seq = ''.join(s.strip() for s in next(faiter))
            yield Fasta(_id, comment, seq)
