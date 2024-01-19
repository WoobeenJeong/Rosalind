### have to change code



#__validation_dataset__ = 'http://bioinformaticsalgorithms.com/data/extradatasets/alignment/alignment_affine_gap_penalties.txt'
__input_data__ = '''\
PRTEINS
PRTWPSEIN
'''
import basupport
import sys
import numpy as np

BLOSUM62 = """\
   A  C  D  E  F  G  H  I  K  L  M  N  P  Q  R  S  T  V  W  Y
A  4  0 -2 -1 -2  0 -2 -1 -1 -1 -1 -2 -1 -1 -1  1  0  0 -3 -2
C  0  9 -3 -4 -2 -3 -3 -1 -3 -1 -1 -3 -3 -3 -3 -1 -1 -1 -2 -2
D -2 -3  6  2 -3 -1 -1 -3 -1 -4 -3  1 -1  0 -2  0 -1 -3 -4 -3
E -1 -4  2  5 -3 -2  0 -3  1 -3 -2  0 -1  2  0  0 -1 -2 -3 -2
F -2 -2 -3 -3  6 -3 -1  0 -3  0  0 -3 -4 -3 -3 -2 -2 -1  1  3
G  0 -3 -1 -2 -3  6 -2 -4 -2 -4 -3  0 -2 -2 -2  0 -2 -3 -2 -3
H -2 -3 -1  0 -1 -2  8 -3 -1 -3 -2  1 -2  0  0 -1 -2 -3 -2  2
I -1 -1 -3 -3  0 -4 -3  4 -3  2  1 -3 -3 -3 -3 -2 -1  3 -3 -1
K -1 -3 -1  1 -3 -2 -1 -3  5 -2 -1  0 -1  1  2  0 -1 -2 -3 -2
L -1 -1 -4 -3  0 -4 -3  2 -2  4  2 -3 -3 -2 -2 -2 -1  1 -2 -1
M -1 -1 -3 -2  0 -3 -2  1 -1  2  5 -2 -2  0 -1 -1 -1  1 -1 -1
N -2 -3  1  0 -3  0  1 -3  0 -3 -2  6 -2  0  0  1  0 -3 -4 -2
P -1 -3 -1 -1 -4 -2 -2 -3 -1 -3 -2 -2  7 -1 -2 -1 -1 -2 -4 -3
Q -1 -3  0  2 -3 -2  0 -3  1 -2  0  0 -1  5  1  0 -1 -2 -2 -1
R -1 -3 -2  0 -3 -2  0 -3  2 -2 -1  0 -2  1  5 -1 -1 -3 -3 -2
S  1 -1  0  0 -2  0 -1 -2  0 -2 -1  1 -1  0 -1  4  1 -2 -3 -2
T  0 -1 -1 -1 -2 -2 -2 -1 -1 -1 -1  0 -1 -1 -1  1  5  0 -2 -2
V  0 -1 -3 -2 -1 -3 -3  3 -2  1  1 -3 -2 -2 -3 -2  0  4 -3 -1
W -3 -2 -4 -3  1 -2 -2 -3 -3 -2 -1 -4 -4 -2 -3 -3 -2 -3 11  2
Y -2 -2 -3 -2  3 -3  2 -1 -2 -1 -1 -2 -3 -1 -2 -2 -2 -1  2  7
"""

def load_scoring_matrix(inputtxt):
    inputrows = inputtxt.splitlines()
    header = inputrows[0].split()
    scores = {}
    for line in inputrows[1:]:
        fields = line.split()
        aafrom = fields[0]
        for aato, score in zip(header, map(int, fields[1:])):
            scores[aafrom, aato] = score
    return scores

def do_global_alignment(seq1, seq2, scoremtx, gapopen=11, gapext=1):
#def do_global_alignment(seq1, seq2, scoremtx, gapopen=15, gapext=5):
    S = np.zeros([len(seq1) + 1, len(seq2) + 1], dtype=np.int64)
    Gi = S.copy()
    Gj = S.copy()
    T = np.zeros([len(seq1) + 1, len(seq2) + 1], dtype=np.int8)
    Ti = T.copy()
    Tj = T.copy()

    # Build scoring matrix
    for i in range(1, len(seq1) + 1):
        S[i, 0] = -gapopen - gapext * (i - 1)
        Gj[i, 0] = -99999
        T[i, 0] = 1
    for j in range(1, len(seq2) + 1):
        S[0, j] = -gapopen - gapext * (j - 1)
        Gi[0, j] = -99999
        T[0, j] = 2

    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            # Gi (insertion)
            insext = Gi[i - 1, j] - gapext
            insopen = S[i - 1, j] - gapopen
            Gi[i, j] = max(insext, insopen)
            Ti[i, j] = 1 if Gi[i, j] == insext else 0

            # Gj (deletion)
            delext = Gj[i, j - 1] - gapext
            delopen = S[i, j - 1] - gapopen
            Gj[i, j] = max(delext, delopen)
            Tj[i, j] = 2 if Gj[i, j] == delext else 0

            midmatch = S[i - 1, j - 1] + scoremtx[seq1[i - 1], seq2[j - 1]]

            S[i, j] = max(midmatch, Gi[i, j], Gj[i, j])
            if S[i, j] == Gi[i, j]:
                T[i, j] = 1
            elif S[i, j] == Gj[i, j]:
                T[i, j] = 2
            else:
                T[i, j] = 0

    # Build alignment from backtrack matrix
    i = len(seq1)
    j = len(seq2)
    Q1, Q2 = [], []
    ingap = 0
    while i > 0 or j > 0:
        if ingap == 1 or T[i, j] == 1:
            Q1.append(seq1[i - 1])
            Q2.append('-')
            ingap = Ti[i, j]
            i -= 1
        elif ingap == 2 or T[i, j] == 2:
            Q1.append('-')
            Q2.append(seq2[j - 1])
            ingap = Tj[i, j]
            j -= 1
        else:
            Q1.append(seq1[i - 1])
            Q2.append(seq2[j - 1])
            i -= 1
            j -= 1

    return S[len(seq1), len(seq2)], ''.join(Q1[::-1]), ''.join(Q2[::-1])

scoring_matrix = load_scoring_matrix(BLOSUM62)
seq1 = basupport.input[0]
seq2 = basupport.input[1]

score, seq1aln, seq2aln = do_global_alignment(seq1, seq2, scoring_matrix)
print(score)
print(seq1aln)
print(seq2aln)
