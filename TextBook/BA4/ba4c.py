### integer mass 를 바탕으로
### theoretical spectrum of a cyclic peptide
### = 모든 가능한 cyclic subpeptide들의 mass를 나열 
### = cyclospetrum of a peptide
### 순서는 Daltons기준 오름차순으로 나열

# integer_mass_table = { 'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 
#                       'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114, 
#                       'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 
#                       'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186 }

from itertools import combinations
import numpy as np

molecule_mass = {'C': 12.01, 'H': 1.008, 'O': 16.00, 'N': 14.01, 'S': 32.07}
fomula_table = np.zeros((20, 5))
aminoacid = 'GASPVTCILNDKQEMHFRYW'
aa_molecule = {'G': 'C2H3N1O1', 'A': 'C3H5N1O1', 'S': 'C3H5N1O2', 'P': 'C5H7N1O1', 'V': 'C5H9N1O1',
                'T': 'C4H7N1O2', 'C': 'C3H5N1O1S1', 'I': 'C6H11N1O1', 'L': 'C6H11N1O1', 'N': 'C4H6N2O2',
                'D': 'C4H5N1O3', 'K': 'C6H12N2O1', 'Q': 'C5H8N2O2', 'E': 'C5H7N1O3', 'M': 'C5H9N1O1S1',
                'H': 'C6H7N3O1', 'F': 'C9H9N1O1', 'R': 'C6H12N4O1', 'Y': 'C9H9N1O2', 'W': 'C11H10N2O1'}

for i, (aa, formula) in enumerate(aa_molecule.items()):
    atoms = {'C': 0, 'H': 0, 'O': 0, 'N': 0, 'S': 0}
    atom = ''
    for char in formula:
        if char.isalpha():
            atom = char
        else:
            atoms[atom] = int(atoms[atom]) * 10 + int(char)
    for j, atom_symbol in enumerate(['C', 'H', 'O', 'N', 'S']):
        fomula_table[i, j] = atoms.get(atom_symbol, 0)

integer_mass_table = {}
for value in molecule_mass.values():
    molecule_array = np.array(list(molecule_mass.values()))
for i in range(20):
    integer_mass_table[aminoacid[i]] = round(sum(fomula_table[i] * molecule_array),0)
    
# print(integer_mass_table)

###################################################

def cyclospectrum(peptide, integer_mass_table):

    subpeptides = []
    for r in range(1, len(peptide)):
        for i in range(len(peptide)):
            if i + r <= len(peptide):
                # print(i,r)
                subpeptides.append(peptide[i:i+r])
            else:
                subpeptides.append(peptide[i:] + peptide[:i+r-len(peptide)])
    subpeptides.append(peptide)
    
    mass_count = [0]
    for peps in subpeptides:
        sums = sum([integer_mass_table[aa] for aa in peps])
        mass_count.append(int(sums))
        
    mass_count.sort()
                    
    return mass_count

###################################################

with open ('bioinfo2/rosalind_ba4c.txt', 'r') as file:
    peptide = file.readline().strip()

result = cyclospectrum(peptide, integer_mass_table)
print(' '.join(map(str, result)))
