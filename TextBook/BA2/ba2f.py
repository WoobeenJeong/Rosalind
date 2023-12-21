import random
random.seed(12)

with open("bioinfo2/rosalind_ba2f.txt", "r") as file:
    lines = file.readlines()

k, t = map(int, lines[0].split())
Dna = [line.strip() for line in lines[1:]]

for line in lines:
    print(line.strip())

### 가장 probability 높은 motif 찾기 : profile input 필요 ###
    
def most(profile, Dna, k):

    motifs = []                                 # 이전 코드와 달라진 점은, most를 바로 출력한 것과 달리 list의 형태로 가능한 motif 모두 출력
    
    for sequence in Dna:                        # 여기서 부터는 모든 과정이 Num10, 11 과제에서 작성한 내용과 동일
        most = ''
        max = 0
        
        for i in range(len(sequence) - k + 1):
            kmer = sequence[i:i + k]
            prob = 1
            for j in range(k):
                prob *= profile[kmer[j]][j]
                
            if prob > max:
                max = prob
                most = kmer
                
        motifs.append(most)                     # 가장 probability가 높은 profile에서 계산된 kmer(most한)들의 집합을 motifs로 저장, 출력
                                                # 이때, 각 Dna string별로 결과를 낼 것이기 때문에, sort해서 혼란을 주지 않도록 할 것임
    return motifs

### most함수에 들어가는 profile matrix 작성하는 코드 : kmer motif 만들어 input 필요 ### 

def Profile(motifs):
    k = len(motifs[0])
    
    profile = {'A': [1] * k, 'C': [1] * k, 'G': [1] * k, 'T': [1] * k}      # probability 저장 할 dictionary 만들기
    t = len(motifs) + 4                                                     # 이때 [0]이 아닌 [1]을 넣어서, 그리고 +4로 시작해서 pseudo count

    for i in range(k):
        for j in range(len(motifs)):
            profile[motifs[j][i]][i] += 1

    for nt in 'ACGT':
        for i in range(k):
            profile[nt][i] /= t

    return profile

### common에 가장 공통서열로 score비교(다를수록높은값) : most함수로 나온 "motifs" (motif아님)를 [] list 형태로 input ###

def Score(motifs):
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
    
### Score함수를 통해 motif중 score가장 낮은 것으로 "string"별로 도출 ###

def randomized(Dna, k, t, iter):
    best_motifs = []  
    best_score = float('inf')                              # 초기값을 inf로 해야 작은 값 가져가기 편함

    for repeat in range(iter):                                  # iteration은 높여도 됨
        motifs = []
        for i in range(t):
            kmer = random.randint(0, len(Dna[i]) - k)      # random seed값의 경우 1로 설정
            motifs.append(Dna[i][kmer:kmer + k])

        while True:
            profile = Profile(motifs)
            motifs = most(profile, Dna, k)
            current_score = Score(motifs)

            if current_score < best_score:
                best_score = current_score
                best_motifs = motifs
            else:
                break

    return best_motifs

iteration = 2000
result = randomized(Dna, k, t, iteration)

for motif in result:
    print(motif)
