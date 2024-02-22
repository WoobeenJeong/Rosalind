### convolution of cyclic peptides spectrum
### 스펙트럼에서 가장 많이 나타나는 mass 차이를 찾아내서
### 가장 많이 나타나는 mass 차이 (multiplicity)를 가진 peptide를 찾아내는 문제

### 문제 예시도 그렇고, matrix로 만들어 풀면 시각화에 좋을것

import numpy as np

integer_mass_table = { 'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 
                      'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114, 
                      'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 
                      'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186 }

mass_only = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]

#####################################################

def convolution(spectrum):

    spectrum.sort()
    diff = np.zeros((len(spectrum)-1, len(spectrum)-1))
    for i in range(len(spectrum)):
        for j in range(i + 1, len(spectrum)):
            diff[i-j, j - 1] = spectrum[j] - spectrum[i]
    # print(diff)
            
    convoluted = []
    elements = diff[diff != 0].flatten()                            # 매트릭스 0아닌 요소를 1차원으로 변환
    uniq_elems, counts = np.unique(elements, return_counts=True)    # 중복된 요소와 횟수 찾기
    sorted_elems = np.argsort(-counts)                              # 중복 횟수를 기준으로 내림차순 정렬
    # sorted_elems = np.lexsort((-uniq_elems, -counts))             # 중복 횟수를 기준으로 오름차순 정렬
    for index in sorted_elems:
        convoluted.extend([uniq_elems[index]] * counts[index])      # 정렬된 순서대로 결과 리스트에 추가
    
    return convoluted

#####################################################

with open('bioinfo2/rosalind_ba4h.txt', 'r') as f:
    spectrum = list(map(int, f.readline().strip().split()))
# print(spectrum)

result = convolution(spectrum)

for each in result:
    print(int(each), end=' ')
    oneline = str(int(each)) + ' '

with open('ba4h_output.txt', 'w') as f:
    f.write(oneline)
