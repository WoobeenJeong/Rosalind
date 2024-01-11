### Greedy search with pseudocounts
### 이전 ba2d.py에서 pseudocounts를 추가한 함수
### pseudocounts가 어디에 추가되는지 확인! -> 더 효과적 방법 존재?

def make_profile(motifs, pseudo):
    k = len(motifs[0])
    profile = { 'A': [pseudo]*k, 'C': [pseudo]*k, 'G': [pseudo]*k, 'T': [pseudo]*k }
    motif_count = len(motifs)
    
    for i in range(k):
        for j in range(motif_count):
            nt = motifs[j][i]
            profile[nt][i] += 1

    for nt in profile:
        for i in range(k):
            profile[nt][i] /= (motif_count+4*pseudo)

    # print(profile)
    return profile

def most(string, k, profile):
    max_prob = 0
    most = string[:k]

    for i in range(len(string) - k + 1):
        kmer = string[i:i + k]
        prob = 1.0
        for j in range(k):
            nt = kmer[j]
            prob *= profile[nt][j]

        if prob > max_prob:
            max_prob = prob
            most = kmer

    return most
    
def scoring(motifs):
        common = ''
        score = 0


        for j in range(len(motifs[0])):
            count = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
            for motif in motifs:
                count[motif[j]] += 1
            common += max(count, key=count.get)
        
        for motif in motifs:
            for j in range(len(motifs[0])):
                if motif[j] != common[j]:
                    score += 1
        
        return score
    
def greedy_pseudo(strings, k, t, pseudo):

    bestmotifs = [each[:k] for each in strings]
    
    for i in range(len(strings[0]) - k + 1):
        motifs = [strings[0][i:i + k]]
        
        for j in range(1, t):
            profile = make_profile(motifs, pseudo)
            motifs.append(most(strings[j], k, profile))
        
        if scoring(motifs) < scoring(bestmotifs):
            bestmotifs = motifs

    return bestmotifs

##############################################

with open("bioinfo2/rosalind_ba2e.txt", "r") as file:
    lines = file.readlines()

k, d = map(int, lines[0].split())
strings = [line.strip() for line in lines[1:]]

for line in lines:
    print(line.strip())
    
result = greedy_pseudo(strings, k, d, 1)    ### pseudocounts = 1
for motif in result:
    print(motif)
