### 목적은 모든 문자열에서 hamming distance가 가장 적은 kmer를 찾는 것
### 이를 위해서는 1. 각 stirng에서 가능한 모든 kmer pattern 만들기 2. pattern이 갖는 hamming distance계산하기 (string별로) 3. 해당 distance의 합이 가장 적은 경우 4. kmer pattern반환

def hamm(pattern1, pattern2):
    total = 0

    for i in range(len(pattern1)):
        if pattern1[i] != pattern2[i]:
            total += 1

    return total

def least(dna, k):
    min_dist = float('inf')
    common = ""

    for i in range(4**k):
        pattern = ""
        index = i

        for j in range(k):
            pattern += "ACGT"[index % 4]
            index //= 4

        # print(f'{pattern}:{index}')

        sum_min_dist = 0

        for text in dna:
            distance = float('inf')

            for i in range(len(text) - k + 1):
                exist_kmer = text[i:i+k]
                current_distance = hamm(pattern, exist_kmer)

                if current_distance < distance:
                    distance = current_distance

            sum_min_dist += distance

        if sum_min_dist < min_dist:
            min_dist = sum_min_dist
            common = pattern

    return common

############################################

with open("bioinfo2/sample.txt", "r") as file:
    lines = file.readlines()

k = int(lines[0].split()[0])
Dna = [line.strip() for line in lines[1:]]

# for line in lines:
#     print(line.strip())

target = least(Dna,k)
print(target)