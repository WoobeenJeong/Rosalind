### Greedy Motif Search 
### 주어진 pseudo code를 만족하기 위해서는 다음과 같은 refactoring된 함수들이 필요
### 1. profile을 kmer단위로 생성 2. 해당 profile로 가능한 kmer motif생성 3. motif점수내서 비교가능하게 하기

def make_profile(motifs):
    k = len(motifs[0])
    profile = { 'A': [0.0]*k, 'C': [0.0]*k, 'G': [0.0]*k, 'T': [0.0]*k }
    motif_count = len(motifs)
    
    for i in range(k):
        for j in range(motif_count):
            nt = motifs[j][i]
            profile[nt][i] += 1

    for nt in profile:
        for i in range(k):
            profile[nt][i] /= motif_count

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
    
def greedy(strings, k, t):

    bestmotifs = [each[:k] for each in strings]
    
    for i in range(len(strings[0]) - k + 1):
        motifs = [strings[0][i:i + k]]
        
        for j in range(1, t):
            profile = make_profile(motifs)
            motifs.append(most(strings[j], k, profile))
        
        if scoring(motifs) < scoring(bestmotifs):
            bestmotifs = motifs

    return bestmotifs

##################################################

with open("bioinfo2/rosalind_ba2d.txt", "r") as file:
    lines = file.readlines()

k, d = map(int, lines[0].split())
strings = [line.strip() for line in lines[1:]]

for line in lines:
    print(line.strip())
    
result = greedy(strings, k, d)
for motif in result:
    print(motif)
