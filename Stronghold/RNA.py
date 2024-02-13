### foward transcription DNA -> mRNA

def transcription01(dna):
    for i in range(len(dna)):
        if dna[i] == 'T':
            dna = dna[:i] + 'U' + dna[i+1:]
        
    return dna

def transcription02(dna):
    return dna.replace('T', 'U')

with open('bioinfo2/rosalind_rna.txt', 'r') as file:
    dna = file.read().replace('\n', '')

# print(transcription01(dna))
print(transcription02(dna))
