### cyclic peptides에서 spectrum을 만족하는 peptide 찾기
### Cyclopeptide Sequencing
### Integer mass가 주어지고, 가능한 Cyclopeptide를 모두 출력하기
### 다행히 Integer table은 필요없는게, protein seq로 바꾸는 것은 아직 요구X
### -> 하지만 쓰면 할 수 있음

############################################

peptides = [57, 71, 87, 97, 99, 101, 103, 113, 113, 114, 115, 128, 128, 129, 131, 137, 147, 156, 163, 186]

############################################

def find_cyclopep(spectrum, peptides):
    ref = []
    listed = []
    original = spectrum.copy()

    for subpeps in original:
        if subpeps in peptides:
            ref.append(subpeps)
            spectrum.remove(subpeps)

    if 0 in spectrum:
        spectrum.remove(0)

    for ref01 in ref:
        for ref02 in ref:
            if ref01 + ref02 in spectrum:
                listed.append((ref01, ref02))
                listed.append((ref02, ref01))
                spectrum.remove(ref01 + ref02)

    print(listed)

    if len(ref) == len(set(ref)):
        stopper = len(ref)
    else:
        stopper = len(ref) - (len(ref) - len(set(ref)))

    while len(listed[0]) < stopper:
        new_list = []
        for each in listed:
            eachsum = sum(each)
            # print(eachsum)
            for ref00 in ref:
                if ref00 not in each and ref00 + eachsum in spectrum:
                    new_list.append(each + (ref00,))
                    new_list.append((ref00,) + each)
                        
                    for each in new_list:
                        if each[::-1][:-1] not in new_list:
                            new_list.remove(each)

        listed.clear()
        listed.extend(new_list)
        
        print(listed)
        print(new_list)

    return listed, ref

def adjust(spectrum, peptides):
    
    listed, ref = find_cyclopep(spectrum, peptides)
    cycle = []

    for each in ref:
        for imperfect in listed:
            if sum(imperfect) == max(spectrum):
                cycle = imperfect
            elif sum(imperfect) + each == max(spectrum):
                cycle = imperfect + (each,)
            else:
                cycle = imperfect
    
    return cycle

def rolling(spectrum, peptides):
    cycle = adjust(spectrum, peptides)
    reverse = cycle[::-1]
    total = []
    
    for i in range(len(cycle)):
        cycle_shifted = cycle[i:] + cycle[:i]
        reverse_shifted = reverse[i:] + reverse[:i]
        total.append(cycle_shifted)
        total.append(reverse_shifted)

    return total    

############################################

with open('bioinfo2/rosalind_ba4e.txt', 'r') as f:
    spectrum = list(map(int, f.readline().split()))
    print(spectrum)

possibles = rolling(spectrum, peptides)

for tuple_element in possibles:
    print("-".join(map(str, tuple_element)), end=" ")
