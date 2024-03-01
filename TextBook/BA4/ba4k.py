### Compute the score of a linear peptide with respect to a spectrum.
### linear한 peptide의 score를 계산
### 그걸 위해서는 먼저 linear한 spectrum을 구해야 함
### 이후에 주어진 spectrum과 비교하여 score를 계산 (포함된 mass의 개수)

integer_mass = { 'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 
                  'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114, 
                  'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 
                  'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186 }

def linear_spectrum(peptide):
    pep_spectrum = [0]
    for i in range(len(peptide)):
        for j in range(i + 1, len(peptide) + 1):
            pep_spectrum.append(sum([integer_mass[peptide[k]] for k in range(i, j)]))
    # print(pep_spectrum)
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

with open('bioinfo2/rosalind_ba4k.txt', 'r') as file:
    peptide = file.readline().strip()
    spectrum = list(map(int, file.readline().split()))

print(linear_score(peptide, spectrum))
