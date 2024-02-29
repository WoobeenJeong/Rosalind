### convolution cyclopeptide sequencing
### 중복이 허용되어 주어진 mass spectrum 내에서
### 57~200 사이의 Convolution spectrum의 상위 m개
### leaderboard의 상위 n개 내에서 Cyclopeptide sequencing
### input: spectrum, m, n

### 이전 코드와 비교해서, 어떤 부분이 다른지 꼭 확인

############################################################

def convolution(spectrum):
    convoluted = {}
    
    for i in range(len(spectrum)):
        for j in range(i + 1, len(spectrum)):
            diff = abs(spectrum[i] - spectrum[j])
            if diff > 0:
                convoluted[diff] = convoluted.get(diff, 0) + 1
            # print(convoluted)
                
    init_list = sorted(convoluted.items(), key=lambda x: x[1], reverse=True)
    # print(init_list)
    return init_list

############################################################

def scoring(peptide, spectrum, cyclo=True):
    cycle_spectrum, score = [0, sum(peptide)] if cyclo else [], 0
    
    if cyclo:                                                       # cyclic peptide
        for i in range(1, len(peptide) + 1):
            for j in range(len(peptide)):
                cycle_spectrum += [sum((peptide[j:] + peptide[:j])[0:i])]
    else:                                                           # linear peptide (do not use rolling for all substrings)
        for i in range(len(peptide)):
            for j in range(i + 1, len(peptide) + 1):
                cycle_spectrum.append(sum(map(int, peptide[i:j])))

    for mass in spectrum:
        if mass in cycle_spectrum:
            score += 1
            cycle_spectrum.remove(mass)
    return score

def leaderboard_pep(spectrum, top_nth, integer_mass):
    leaderboard  = [[]]
    leader_peps = []
    while len(leaderboard):
        leaderboard = [pep + [mass] for mass in integer_mass for pep in list(leaderboard)]
        for pep in leaderboard.copy():
            if sum(pep) == spectrum[-1]:
                if scoring(pep, spectrum, cyclo=True) > scoring(leader_peps, spectrum, cyclo=True):
                    leader_peps = pep
            elif sum(pep) > spectrum[-1]:
                leaderboard.remove(pep)
        if len(leaderboard) >= top_nth:
            linepep = [scoring(pep, spectrum, cyclo=False) for pep in leaderboard]
            threshold = sorted(linepep, reverse=True)[top_nth - 1]
            leaderboard = [pep for pep, linepep in zip(leaderboard, linepep) if linepep >= threshold]
    return leader_peps

############################################################

def conv_cyclopep_seq(topm, top_nth, spectrum):
    conv_peps = convolution(spectrum)
    conv_peps = [(diff, counts) for diff, counts in conv_peps if 57 <= diff <= 200]
    integer_mass = [diff for diff, counts in conv_peps if counts >= conv_peps[topm - 1][1]]
    return leaderboard_pep(spectrum, top_nth, integer_mass)

############################################################
    
with open('bioinfo2/rosalind_ba4i.txt', 'r') as f:
    topm = int(f.readline().strip())
    top_nth = int(f.readline().strip())
    spectrum = list(map(int, f.readline().split()))

result = conv_cyclopep_seq(topm, top_nth, spectrum)
print(*result, sep="-")
