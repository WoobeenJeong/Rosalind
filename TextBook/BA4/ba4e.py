### Cycle 가능한 peptide로 만들 수 있는 spectrum 찾기
### Error버전이 있으니, 비교해서 어떻게 다른지 확인 할 것 (ba4e_error.py)

### 무엇보다 어려웠던 점은, 113, 128 분자량이 중복되는 점
### cyclic peptide생성 조건에 잘림이 발생 (아래처럼 하면 5-1을 가진 것이 4개... foward 다 못찾음)

### 예를 들어, (1-2-3-4-5)가 cyclic peptide라면, 가능한 경우는

### 1-2-3-4-5           5-4-3-2-1
###   2-3-4-5-1           4-3-2-1-5
###     3-4-5-1-2           3-2-1-5-4
###       4-5-1-2-3           2-1-5-4-3 
###         5-1-2-3-4           1-5-4-3-2

mass_only = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]

############################################

def check_same(ref, spectrum):
    listed = [0]
    for ref00 in range(len(ref)):
        subpeps = listed[ref00] + ref[ref00]
        listed.append(subpeps)
        # print(listed)
        
    visited = [0]
    for ref01 in range(len(ref)):
        for ref02 in range(ref01 + 1, len(ref) + 1):
            eachsum = listed[ref02] - listed[ref01]
            visited.append(eachsum)
            if eachsum not in spectrum:
                return False
    visited.sort()
    # print(visited)

    if sum(ref) > spectrum[-1] - mass_only[0]:
        return False
    return True

############################################

def rolling(peptide):
    cyclepeps = [0, sum(peptide)]
    # print(cyclepeps)
    largerpeps = peptide + peptide
    for after in range(1, len(peptide)):
        for before in range(len(peptide)):
            subpeptide = largerpeps[before:before + after]
            cyclepeps.append(sum(subpeptide))
    cyclepeps.sort()
    # print(cyclepeps)
    return cyclepeps

############################################

def find_cyclopep(spectrum):
    result = set()
    peptides = [[]]

    while peptides:
        
        new_peptides = []
        for peps in peptides:
            for mass in mass_only:
                new_peptides.append(peps + [mass])
        peptides = new_peptides
        
        for peptide in peptides:
            if sum(peptide) == max(spectrum):
                if rolling(peptide) == spectrum:
                    result.add("-".join(map(str, peptide)))
                peptides = [pep for pep in peptides if pep != peptide]
            elif not check_same(peptide, spectrum):
                peptides = [pep for pep in peptides if pep != peptide]

    return result

############################################

with open('bioinfo2/rosalind_ba4e.txt', 'r') as f:
    spectrum = list(map(int, f.readline().split()))
    print(spectrum)
    
result = find_cyclopep(spectrum)
for each in result:
    print(each, end = ' ')
