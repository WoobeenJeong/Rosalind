### overlap kmers into adjacency list
### k-1 prefix suffix

def overlaps(kmers, window):
    
    overlap_dict = {}
    
    for prefix in kmers:
        for suffix in kmers:
            if prefix != suffix and prefix[window:] == suffix[:-window]:
                if prefix not in overlap_dict:
                    overlap_dict[prefix] = suffix
                else:
                    overlap_dict[prefix].append(suffix)
    # print(overlap_dict)
    result = sorted(overlap_dict.items(), key=lambda x: x[0])    
    
    return result

with open ('bioinfo2/rosalind_ba3c.txt', 'r') as f:
    kmers = [line.strip() for line in f]
    window = 1

# print(kmers, window)

result = overlaps(kmers, window)

for each in result:
    print(each[0], '->', each[1])
