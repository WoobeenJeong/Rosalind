### 문제 정의에서 gap에 대한 Affine penalty(k=서열길이) = σ + ε · (k − 1)
### 여기서 σ는 gap opening penalty, ε는 gap extension penalty
### 문제에서 주어진 패널티는 각각 σ = 11, ε = 1 이므로, Affine penalty = 11 + 1 · (k − 1) = 10 + k
### 기반은 needleman-wunsch 알고리즘 (global이라 처음부터 끝까지 일치)

### sigma = σ = open패널티 , epsilon = ε = extend패널티
### 이전에 만든 BLOSUM 파일 활용

import numpy as np

sigma = 11                                                   # sigma = σ = open패널티
epsilon = 1                                                  # epsilon = ε = extend패널티

with open('bioinfo2/BLOSUM62.txt', 'r') as file:
    lines = file.readlines()
    blosum62 = []
    aa = lines[0].strip().split()[0:]
    for line in lines[1:]:
        row = [int(x) for x in line.strip().split()[1:]]
        blosum62.append(row)

# penalty = blosum62[aa.index('A')][aa.index('A')]           # 확인차 penalty를 A-A로 설정 4가 나와야 함
# print(penalty)

def affine(ref, alt, blosum62, sigma, epsilon):
    
    diag = np.zeros((len(ref) + 1, len(alt) + 1))
    insertion = np.zeros((len(ref) + 1, len(alt) + 1))
    deletion = np.zeros((len(ref) + 1, len(alt) + 1))
    trace = np.zeros((len(ref) + 1, len(alt) + 1))
    trace_ins = np.zeros((len(ref) + 1, len(alt) + 1))
    trace_del = np.zeros((len(ref) + 1, len(alt) + 1))
    
    for i in range(1, len(ref) + 1):
        diag[i][0] = -sigma - epsilon * (i - 1)
        deletion[i][0] = -np.inf
        trace[i][0] = 1

    for j in range(1, len(alt) + 1):
        diag[0][j] = -sigma - epsilon * (j - 1)
        insertion[0][j] = -np.inf
        trace[0][j] = 2

    for i in range(1, len(ref) + 1):
        for j in range(1, len(alt) + 1):

            insertion[i][j] = max(insertion[i - 1][j] - epsilon, diag[i - 1][j] - sigma)
            trace_ins[i][j] = 1 if insertion[i][j] == insertion[i - 1][j] - epsilon else 0          # 1이면 insertion, 0이면 diag

            deletion[i][j] = max(deletion[i][j - 1] - epsilon, diag[i][j - 1] - sigma)
            trace_del[i][j] = 2 if deletion[i][j] == deletion[i][j - 1] - epsilon else 0            # 2이면 deletion, 0이면 diag   

            midmatch = diag[i - 1][j - 1] + blosum62[aa.index(ref[i - 1])][aa.index(alt[j - 1])]
            diag[i][j] = max(midmatch, insertion[i][j], deletion[i][j])
            if diag[i][j] == insertion[i][j]:
                trace[i][j] = 1
            elif diag[i][j] == deletion[i][j]:
                trace[i][j] = 2
            else:
                trace[i][j] = 0

    print(f"{diag}\n{trace}")

    return diag, trace, trace_ins, trace_del

def traceback(ref, alt):
    
    diag, trace, trace_ins, trace_del = affine(ref, alt, blosum62, sigma, epsilon)
    i,j = len(ref),len(alt)
    
    refseq, altseq = [], []
    gap_ext = 0                             # gap_ext는 gap이 연속되는 것을 확인하기 위한 변수

    while i > 0 and j > 0:
        if trace[i][j] == 1 or gap_ext == 1:
            refseq.append(ref[i - 1])
            altseq.append('-')
            gap_ext = trace_ins[i][j]       # 여기서 gap_ext는 1이면 gap이 연속되는 것이므로, 1로 계속 유지
            i -= 1
            
        elif trace[i][j] == 2 or gap_ext == 2:
            refseq.append('-')
            altseq.append(alt[j - 1])
            gap_ext = trace_del[i][j]       # 마찬가지로 gap_ext는 2이면 gap이 연속되는 것이므로, 2로 계속 유지
            j -= 1
            
        else:
            refseq.append(ref[i - 1])
            altseq.append(alt[j - 1])
            i -= 1
            j -= 1

        # print(f"{diag}")

    max_score = diag[len(ref)][len(alt)]
    
    reference = ''.join(refseq[::-1])        # refseq[::-1] = refseq.reverse() 
    alternative = ''.join(altseq[::-1])        # altseq[::-1] = altseq.reverse() 

    return f"{int(max_score)}\n{reference}\n{alternative}"

##########################################################

with open('bioinfo2/rosalind_ba5j.txt', 'r') as file:
    lines = file.readlines()
    ref = lines[0].strip().split()[0]
    alt = lines[1].strip().split()[0]         

# print(f"{ref}\n{alt}")

print(f"{traceback(ref, alt)}")
