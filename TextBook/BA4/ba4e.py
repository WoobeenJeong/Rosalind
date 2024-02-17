### Cyclopeptide Sequencing
### Integer mass가 주어지고, 가능한 Cyclopeptide를 모두 출력하기
### 다행히 Integer table은 필요없는게, protein seq로 바꾸는 것은 아직 요구X
### -> 하지만 쓰면 할 수 있음

###################################################
### integer mass list

integer_mass_table = { 'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 
                      'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114, 
                      'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 
                      'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186 }

###################################################

def cycloseq(spectrum):

    cyclopeps = []
    peptides = list(integer_mass_table.values())
    
    while len(peptides) > 0:
        to_remove = []
        for i, pep01 in enumerate(peptides):
            for j, pep02 in enumerate(peptides):
                if i != j:
                    if pep01 in spectrum and pep02 in spectrum:
                        if pep01 + pep02 in spectrum:
                            cyclopeps.append(pep01)
                            cyclopeps.append(pep02)
                            to_remove.extend([i, j])
                    elif pep01 not in spectrum and pep02 not in spectrum:
                        to_remove.extend([i, j])
                        
        to_remove = list(set(to_remove))
        to_remove.sort(reverse=True)
        for index in to_remove:
            peptides.pop(index)
    
    ### peptides의 원소를 사용해서 max(spectrum)을 만들 수 있는 조합 코드
    ### 이걸로 cyclopeps를 만들어야 함
    
    current = 0
    path = []
    for each in cyclopeps:
        while current < max(spectrum):
            if current + each in spectrum:
                current += each
                path.append(each)
            else:
                break

    return path

# ###################################################
# ### permutation을 이용한 모든 가능한 peptide sequence 찾기

# def permutation(cyclopeptide):
#     def backtrack(used, remaining):
#         if len(used) == len(cyclopeptide):
#             permutations.add('-'.join(map(str, used)))
#             return
#         for i in range(len(remaining)):
#             next_element = remaining[i]
#             backtrack(used + [next_element], remaining[:i] + remaining[i+1:])

#     permutations = set()
#     backtrack([], cyclopeptide)
#     return sorted(permutations, reverse=True)

# ###################################################

with open('bioinfo2/sample.txt', 'r') as f:
    spectrum = list(map(int, f.readline().strip().split()))
    
print(spectrum)

cyclopep = cycloseq(spectrum)
print(cyclopep)
# result = permutation(cyclopep)
# print(*result, sep=' ')
