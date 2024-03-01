### Trim a Peptide Leaderboard
### 이전의 linear_score를 이용하여 leaderboard를 trim하는 문제

### 1. linear_score를 이용하여 각 peptide의 score를 계산
### 2. score를 기준으로 leaderboard를 정렬, 상위 N개의 peptide를 제외한 나머지를 제거
### 3. 만약 상위 N개의 peptide의 score와 같은 score를 가진 peptide가 존재한다면, 그것도 포함해서 제거

integer_mass = { 'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 
                  'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114, 
                  'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 
                  'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186 }

def linear_spectrum(peptide):
    pep_spectrum = [0]
    for i in range(len(peptide)):
        for j in range(i + 1, len(peptide) + 1):
            pep_spectrum.append(sum([integer_mass[peptide[k]] for k in range(i, j)]))
    return sorted(pep_spectrum)

def linear_score(peptide, spectrum):
    pep_spectrum = linear_spectrum(peptide)
    score = 0
    for mass in spectrum:
        if mass in pep_spectrum:
            score += 1
            pep_spectrum.remove(mass)
            
    return score

######################################################

def trim(leaderboard, spectrum, top_n):
    linear_scores = [linear_score(peptide, spectrum) for peptide in leaderboard]
    leaderboard = [x for _, x in sorted(zip(linear_scores, leaderboard), reverse=True)]
    linear_scores.sort(reverse=True)
    for j in range(top_n, len(leaderboard)):
        if linear_scores[j] < linear_scores[top_n-1]:
            return leaderboard[:j]
    return leaderboard

######################################################

with open ('bioinfo2/rosalind_ba4l.txt', 'r') as file:
    leaderboard = file.readline().strip().split()
    spectrum = list(map(int, file.readline().split()))
    top_n = int(file.readline())

result =  trim(leaderboard, spectrum, top_n)
print(' '.join(result))
