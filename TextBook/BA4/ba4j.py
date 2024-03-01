### 전체 아미노산의 prefix amss를 구하고,
### MASS(prefix2자리) = prefix_mass(첫문자) + prefix_mass(두번째문자)

integer_mass = { 'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 
                  'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114, 
                  'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 
                  'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186 }

def linearspectrum(peptide, integer_mass):
    prefix_mass = [0]
    for i in range(len(peptide)):
        prefix_mass.append(prefix_mass[i] + integer_mass[peptide[i]])
    linear_spectrum = [0]
    for i in range(len(peptide)):
        for j in range(i+1, len(peptide)+1):
            linear_spectrum.append(prefix_mass[j] - prefix_mass[i])
    linear_spectrum.sort()
    return linear_spectrum

##############################################

with open('bioinfo2/rosalind_ba4j.txt', 'r') as file:
    peptide = file.readline().strip()

result = linearspectrum(peptide, integer_mass)
print(' '.join(map(str, result)))
