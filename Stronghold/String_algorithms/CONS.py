### dna strings 여러 줄에서 
### 하나의 profile matrix를 생성하고
### 이를 바탕으로 consensus string을 만들기

### 이문제 함정있음 : fasta file은 > 뒤에 여러줄 \n으로 구분되어서 나옴 ''.join 이나 .replace('\n','')해줘야 함

import numpy as np

#####################################

def make_profile(strings):
    profile = np.zeros((4, len(strings[0])), dtype=int)
    
    for string in strings: 
        for i in range(len(string)):
            if string[i] == "A":
                profile[0][i] += 1
            elif string[i] == "C":
                profile[1][i] += 1
            elif string[i] == "G":
                profile[2][i] += 1
            elif string[i] == "T":
                profile[3][i] += 1

    return profile

def make_consensus(strings):
    profile = make_profile(strings)
    consensus = ""
    for i in range(profile.shape[1]):
        consensus += "ACGT"[np.argmax(profile[:,i])]
    return consensus, profile

#####################################

dnaset = []
with open('bioinfo2/rosalind_cons.txt', 'r') as file:
    strings = file.read().split('>')[1:]
    trimmed = lambda x: x.split('\n', 1)[1].replace('\n', '')
    dnaset = list(map(trimmed, strings))
    
print(dnaset)

#####################################
### Output format

consensus, profile = make_consensus(dnaset)
print(consensus)
for i in range(4):
    print(f"{'ACGT'[i]}: {' '.join(map(str, profile[i]))}")

#####################################
### output.txt로 결과 저장

with open('cons_output.txt', 'w') as file:
    file.write(consensus + "\n")
    for i in range(4):
        file.write(f"{'ACGT'[i]}: {' '.join(map(str, profile[i]))}\n")
