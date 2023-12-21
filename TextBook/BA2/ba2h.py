
## distance between pattern and string

import numpy as np

def hamming(pattern1, pattern2):
    total = 0

    for i in range(len(pattern1)):
        if pattern1[i] != pattern2[i]:
            total += 1

    return total


def sum_hamming(pattern, string):
    k = len(pattern)
    distance = 0

    for i in range(len(string)):
        hamming_distance = k + 1
        for j in range(len(string[i]) - k + 1):
            if hamming_distance > hamming(pattern, string[i][j:j+k]):
                hamming_distance = hamming(pattern, string[i][j:j+k])
        distance += hamming_distance
        # print(hamming_distance)
    
    return distance
    

with open('bioinfo2/rosalind_ba2h.txt') as input:
    all = input.readlines()
    pattern = all[0].strip()
    text = all[1].strip().split(' ')
    
# print(pattern)
# print(text)

print(sum_hamming(pattern, text))