### false masses와 missing masses를 고려한 형태의
##T theoretical spectrum matching and ideal spectrum of cyclic peptide 
### 이전의 ba4c, ba4e, ba4f를 활용
### 일치하는 정도의 score를 계산해서, leaderboard 작성 및 top N highest scoring peptides 출력

integer_mass_table = { 'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 
                      'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114, 
                      'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 
                      'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186 }

mass_only = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]

#####################################################
### ba4e : peptide -> cyclospectrum

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

#####################################################
### ba4f : calculate score

def scoring(peptide, spectrum):
    pep_spec = rolling(peptide)
    result = 0
    unique_masses = set(pep_spec + spectrum)
    for mass in unique_masses:
        result += min(pep_spec.count(mass), spectrum.count(mass))
    return result

#####################################################

def leaderboard_pep(spectrum, top_nth, integer_mass_table):
    
    leaderboard = [[]]
    leader_peptide = []
    
    while leaderboard:
        updates = []
        for pep in leaderboard:
            for mass in integer_mass_table.values():
                updates.append(pep + [mass])
        leaderboard = updates
        # print(leader_peptide, leaderboard)
        
        for peptide in leaderboard[:]:
            if sum(peptide) == spectrum[-1]:
                if scoring(peptide, spectrum) > scoring(leader_peptide, spectrum):
                    leader_peptide = peptide
            elif sum(peptide) > spectrum[-1]:
                leaderboard = [pep for pep in leaderboard if pep != peptide]

        if len(leaderboard) > top_nth:
            score = {}
            for ith, peps in enumerate(leaderboard):
                score[ith] = scoring(peps, spectrum)
            
            threshold = sorted(score.values(), reverse=True)[top_nth-1]
            leaderboard = [pep for pep in leaderboard if scoring(pep, spectrum) >= threshold]
    
    return leader_peptide

#####################################################

with open('bioinfo2/rosalind_ba4g.txt') as f:
    top_nth = int(f.readline().strip())
    spectrum = list(map(int, f.readline().strip().split()))

# print(top_nth, spectrum)

result = leaderboard_pep(spectrum, top_nth, integer_mass_table)
print('-'.join(map(str, result)))
