
import numpy as np

def score(ref, alt1, alt2):
    n, m, k = len(ref), len(alt1), len(alt2)
    matrix = np.zeros((n + 1, m + 1, k + 1), dtype=int)
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            for l in range(1, k + 1):
                if ref[i - 1] == alt1[j - 1] == alt2[l - 1]:
                    matrix[i][j][l] = matrix[i - 1][j - 1][l - 1] + 1
                else:
                    matrix[i][j][l] = max(matrix[i - 1][j][l], matrix[i][j - 1][l], matrix[i][j][l - 1])
    
    maximum = matrix[n][m][k]
                    
    return matrix, maximum

# print(score(ref, alt1, alt2))

def traceback(ref, alt1, alt2):
    
    matrix, maximum = score(ref, alt1, alt2)
    seq = [""] * 3
    i, j, k = len(ref), len(alt1), len(alt2)
    
    while i > 0 and j > 0 and k > 0:
        if ref[i - 1] == alt1[j - 1] == alt2[k - 1]:
            seq[0] = ref[i - 1] + seq[0]
            seq[1] = alt1[j - 1] + seq[1]
            seq[2] = alt2[k - 1] + seq[2]
            i -= 1
            j -= 1
            k -= 1
        elif matrix[i][j][k] == matrix[i - 1][j][k]:
            seq[0] = ref[i - 1] + seq[0]
            seq[1] = "-" + seq[1]
            seq[2] = "-" + seq[2]
            i -= 1
        elif matrix[i][j][k] == matrix[i][j - 1][k]:
            seq[0] = "-" + seq[0]
            seq[1] = alt1[j - 1] + seq[1]
            seq[2] = "-" + seq[2]
            j -= 1
        elif matrix[i][j][k] == matrix[i][j][k - 1]:
            seq[0] = "-" + seq[0]
            seq[1] = "-" + seq[1]
            seq[2] = alt2[k - 1] + seq[2]
            k -= 1
        else:
            break
    
    while i > 0:
        seq[0] = ref[i - 1] + seq[0]
        seq[1] = "-" + seq[1]
        seq[2] = "-" + seq[2]
        i -= 1
    while j > 0:
        seq[0] = "-" + seq[0]
        seq[1] = alt1[j - 1] + seq[1]
        seq[2] = "-" + seq[2]
        j -= 1
    while k > 0:
        seq[0] = "-" + seq[0]
        seq[1] = "-" + seq[1]
        seq[2] = alt2[k - 1] + seq[2]
        k -= 1
        
    return maximum, seq

with open("bioinfo2/rosalind_ba5m.txt",'r') as file:
    read = file.readlines()
    ref = read[0].strip()
    alt1 = read[1].strip()
    alt2 = read[2].strip()

maximum, seq = traceback(ref, alt1, alt2)

print(maximum)
for line in seq:
    print(line)