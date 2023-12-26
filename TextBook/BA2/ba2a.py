### k, d motif enumeration
### Brute Force algorithm 활용

def mutate(pattern, d):
    def helper(input, n, remaining_d):                     # helper함수가 재귀식이 가능토록 함
        if remaining_d == 0:                               # d번 변형을 순차적으로 할 것이므로, d번 이상/이하로 변형 안되도록
            if input != pattern:                           # 변형된 값이 기존 pattern이랑 달라야 함
                mutants.add(input)                         # d번 변형 완료 시, mutants에 input저장 (modify가 아닌 이유는 마지막에 modify를 input으로 받음)
            return
        
        if n == len(pattern):                              # pattern의 길이와 변형할 위치가 같아지면 (예: 3자리 유전자 n=3번째 자리 도착) 끝내기
            return                                         # 이 두번째 if문은 위의 첫번째 if문이 True여야 진행함
        
        for char in "ACGT":                                # A,C,G,T 중 1개로 변형할 것임
            modify = input[:n] + char + input[n+1:]        # modify에 n번째 이전까지 문자열 + 변형n번째 + n번째 이후 문자열로 변형된 문자 저장
            helper(modify, n+1, remaining_d-1)             # n+1은 똑같은 자리X 다른 자리를 바꾸기 위해, remain_d는 얼마나 변형 남았는지 횟수, 위로 다시 올라가 for반복
        helper(input, n+1, remaining_d)                    # remain_d가 0일때, 즉 XXOO, XOXO, XOOX (X=바뀐자리)가 완료되면 OXXO와 OXOX를 위해 위로 올려보내기
        
    mutants = set()                                        # 이제 modify의 결과가 이동 된 "input"을 저장할 공간 만들어서
    helper(pattern, 0, d)                                  # 초기에 n="0" 즉 첫번째 문자열 위치부터 시작하기

    # print(f"{pattern}: {sorted(set(mutants))}")           # 실제로 print해보면 k-mer 패턴 별로 d개씩 치환된 set={ , , ...,}을 확인 가능함
    return mutants  

def hamming(str01,str02):
    count = sum([1 for i in range(len(str01)) if str01[i] != str02[i]])
    return count

def motif_enumeration(Dna, k, d):
    patterns = set()

    for string in Dna:
        for i in range(len(string) - k + 1):
            pattern = string[i:i + k]
            pattern_mutants = mutate(pattern, d)

            for mutant in pattern_mutants:
                count = 0
                for sequence in Dna:
                    for j in range(len(sequence) - k + 1):
                        kmer = sequence[j:j + k]
                        if hamming(mutant, kmer) <= d:
                            count += 1
                            break
                if count == len(Dna):
                    patterns.add(mutant)

    return list(patterns)

with open("bioinfo2/rosalind_ba2a.txt", "r") as file:
    lines = file.readlines()
    k, d = map(int, lines[0].split())
    Dna = [line.strip() for line in lines[1:]]
    
result = motif_enumeration(Dna, k, d)
print(" ".join(result))
