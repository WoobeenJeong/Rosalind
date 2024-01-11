### Profile most probable kmer
### 주어진 kmer windoe로 kmer window 지나가며 profile정리
### 해당 profile을 기반으로 가장 발생가능서 높은 kmer반환 

def most1(string, k, input_matrix):
    maxium = 0
    most = ""

    nt_dict = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

    for i in range(len(string)-k+1):
        kmer = string[i:i+k]
        probability = 1
        for j in range(k):
            nt = kmer[j]
            nt_matrix = nt_dict[nt]
            probability *= input_matrix[nt_matrix][j]

        # print(nt_matrix)
        # print(input_matrix)
        # print(probability)
        
        if probability > maxium:
            maxium = probability
            most = kmer

    return most

def most2(string, k, profile):
    max = 0
    most = ""

    for i in range(len(string) - k + 1):
        kmer = string[i:i + k]
        probability = 1
        for j in range(k):
            nt = kmer[j]
            probability *= profile[nt][j]

        if probability > max:
            max = probability
            most = kmer

    return most

########################################

with open("bioinfo2/rosalind_ba2c.txt", "r") as file:
    lines = file.readlines()

dna = lines[0].strip()
k = int(lines[1].strip())

matrix = []
for line in lines[2:]:
    row = [float(val) for val in line.split()]
    matrix.append(row)

nt = ['A', 'C', 'G', 'T']
profile = {}
for i in range(len(nt)):
    nucleotide = nt[i]
    each = matrix[i]
    profile[nucleotide] = each

print(dna,"\n",k,"\n",profile)


result1 = most1(dna,k,matrix)
result2 = most2(dna,k,profile)
print(result1)
print(result2)
