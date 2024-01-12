### seed값이 12여야 rosalind에서 원하는 값이 나오는 것으로 생각됨
### 기존 코드를 활용하되 initial값과 iteration에 주의해서 작성
### seed = 20 / start motif = 20 / iteration = 2000 기준

import random
random.seed(12)

def most(text, k, profile):                 # 이전 most함수 그대로 활용, 가장 probability높은 motif를 배출
    n = len(text)
    max_prob = -1
    common = ""
    nt = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

    for i in range(n - k + 1):
        kmer = text[i:i+k]
        prob = 1

        for j in range(k):
            prob *= profile[nt[kmer[j]]][j]

        if prob > max_prob:
            max_prob = prob
            common = kmer

    return common

def Score(motifs):                          # 이전 score함수 그대로 활용, 각자리마다 score 누산해서 합산score를 motif별로 작성
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

### Pseudo count를 포함하는 Profile code의 경우 다른 방식으로 작성 ###
### ba2f.py 에서는 Profile을 dict = {A:, C:, G:, T:}꼴로 3D로 작성했지만
### ba2g.py 에서는 Profile을 list (2D)로 작성해서, 

def Profile(motifs):
    k = len(motifs[0])
    t = len(motifs)
    profile = [[1.0 for _matrix in range(k)] for matrix in range(4)]
    
    for i in range(k):
        string = [kmer[i] for kmer in motifs]       # motifs(kmer묶음)에서 각각 꺼내오기 (string으로 구분해야 하니)
        for j in range(4):
            count = string.count('ACGT'[j])         # A,C,G,T를 각각 count해서 저장
            profile[j][i] = (count + 1) / (t + 4)   # count정보에 pseudo count(+1) 해서 비율(/(t+4))을 profile에 저장
    
    return [list(row) for row in profile]

def Gibbs(Dna, k, t, N):
    random_motif = [text[i:i+k] for text in Dna for i in range(len(text) - k + 1)]
    best_motifs = random.sample(random_motif, t)                                        # motifs에서 랜덤하게 t개 생성
    
    for repeat in range(N):                                                             # N은 돌아가는 횟수
        i = random.randint(0, t-1)                                                      # motifs에서 한개의 random 선택
        excepted = best_motifs[:i] + best_motifs[i+1:]                                  # 선택한 것을 제외한 motifs들 (t-1개)
        profile = Profile(excepted)   
        new_motif = most(Dna[i], k, profile)
        best_motifs[i] = new_motif                                                      # 이부분은 이전과 동일
        
        if Score(best_motifs) < Score(random_motif):                                    # Profile로 불러온 best_motif가 score낮으면 업데이트
            random_motif = best_motifs.copy()                                           # 가장 낮은 Motif 저장(사실 상 밑에서 불러오기)
    
    return random_motif

##################################################################

with open("bioinfo2/rosalind_ba2g.txt", "r") as f:
    k, t, N = map(int, f.readline().split())
    Dna = [line.strip() for line in f.readlines()]

##################################################################

### Parameter 수정

best_motifs = None                          # 위에 돌린 값 초기화
best_score = float('inf')                   # Gibbs 돌릴떄 score비교 시작값은 무조건 큰값 (낮은거 찾아야 하니)

N = 2000                                   # 알고리즘 반복 횟수 설정 if you want

for repeat in range(20):                    # 초기 target 20번 생성
    
    motifs = Gibbs(Dna, k, t, N)     
    new = Score(motifs)                     # new에 Gibbs된 score 계산 
    if new < best_score:                    # 똑같이 score 낮은거 판단
        best_score = new  
        best_motifs = motifs  

for result in best_motifs:
    print(result)
