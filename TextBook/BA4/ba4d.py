### Compute the number of peptides of given total mass
### 주어진 integer mass로 가능한 peptide의 수를 계산

###################################################
### integer table 가져오기

integer_mass_table = { 'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 
                      'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114, 
                      'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 
                      'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186 }

for values in integer_mass_table.values():
    mass_only = list(integer_mass_table.values())
mass_only = list(set(mass_only))

###################################################
### DP - memoization (cashing) 활용

def findall_possible(mass):
    cycles = [0]*(mass + 1)
    count = mass
    cycles[mass] = 1
    while count > 0:
        for each in mass_only:
            cycles[count - each] += cycles[count]
        # print(cycles)
            
        count -= 1
        while cycles[count] == 0:
            count -= 1
    # print(cycles)

    return cycles[0]

###################################################

with open('bioinfo2/rosalind_ba4d.txt', 'r') as f:
    mass = int(f.readline().strip())

# print(mass, mass_only)

print(findall_possible(mass))    
