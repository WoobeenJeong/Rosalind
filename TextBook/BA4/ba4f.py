### spectrum 내의 모든 값 중 배수가 되는 값을 찾고
### score을 계산하여 가장 높은 값을 가지는 score를 반환

### score = ('NEQL', [0, 99, 113, 114, 128, 227, 257, 370, 371, 484])의 경우
### NEQL =     0    113 114 128 129 227 242 242 257     355 356 370 371 484
### spectrum = 0 99 113 114 128     227         257 299 355 356 370 371 484
### 겹치는 수   1     2   3   4       5           6       7   8   9   10  11

### 만약 242처럼 여러번 존재하는게 중복이 있다면 2번 이상은 score += 2 

###################################################

integer_mass_table = { 'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 
                      'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114, 
                      'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 
                      'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186 }

for values in integer_mass_table.values():
    mass_only = list(integer_mass_table.values())
mass_only = list(set(mass_only))

###########################################################
### 일단, input aa seq부터 cyclospectrum을 구하기

def cyclospectrum(peptide, integer_mass_table):

    subpeptides = []
    for r in range(1, len(peptide)):
        for i in range(len(peptide)):
            if i + r <= len(peptide):
                subpeptides.append(peptide[i:i+r])
            else:
                subpeptides.append(peptide[i:] + peptide[:i+r-len(peptide)])
    subpeptides.append(peptide)
    
    mass_count = [0]
    for peps in subpeptides:
        sums = sum([integer_mass_table[aa] for aa in peps])
        mass_count.append(int(sums))
        
    mass_count.sort()
    # print(mass_count)
    
    return mass_count

###########################################################

def scoring(peptide, spectrum):
    cyclospec = cyclospectrum(peptide, integer_mass_table)
    score = 0
    
    ### 간단 버전
    # all_possible = set(cyclospec + spectrum)
    # for mass in all_possible:
    #     score += min(cyclospec.count(mass), spectrum.count(mass))
    
    ### 원리 이해 버전
    visited = []
    for mass in cyclospec:
        if mass in spectrum:
            if cyclospec.count(mass) == 1 and not mass in visited:
                score += 1
                visited.append(mass)
                
            elif cyclospec.count(mass) > 1 and not mass in visited:
                if cyclospec.count(mass) <= spectrum.count(mass):
                    score += cyclospec.count(mass)
                    visited.append(mass)
                else:
                    score += spectrum.count(mass)
                    visited.append(mass)

    return score

###########################################################

with open('bioinfo2/rosalind_ba4f.txt', 'r') as f:
    peptide = f.readline().strip()
    spectrum = list(map(int, f.readline().split()))

# print(peptide, spectrum)

print(scoring(peptide, spectrum))
