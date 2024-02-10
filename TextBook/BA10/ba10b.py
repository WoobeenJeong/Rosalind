### 이번엔 잘 생각해야 하는게, trans-emit matrix에서 계산해야 함 = 고로, trans prob를 구할 일은 없기 때문에 괜찮
### 저번 ba10a.py에서 구한건 trans prob를 구하는 것 / 이번엔 emit prob를 구하는 것

import numpy as np

def emission_prob(trans_string, emit_string,trans_states,emit_states,matrix):
    emit_prob = 1
    if len(trans_string) != len(emit_string):
        return 'Error:Some states are missing'
    else:
        for i in range(len(emit_string)):
            emit_prob *= trans_emit_matrix[emit_states.index(emit_string[i]),trans_states.index(trans_string[i])]
            print(emit_string[i],trans_string[i],emit_prob)
        
    return emit_prob
    

with open('bioinfo2/rosalind_ba10b.txt', 'r') as f:
    dataset = f.readlines()
    trans_string = dataset[0].strip()
    trans_states = dataset[2].strip().split()
    emit_string = dataset[4].strip()
    emit_states = dataset[6].strip().split()
    trans_emit_matrix = np.matrix([list(map(float, line.strip().split()[1:])) for line in dataset[9:9+len(trans_states)]])
    
print(trans_states,trans_string)
print(emit_states,emit_string)
# print(trans_emit_matrix)
# print(len(trans_string),len(emit_string))

# print(trans_string[2],trans_states.index('z'))
# print(emit_string[2],emit_states.index('B'))

print(emission_prob(trans_string, emit_string,trans_states,emit_states,trans_emit_matrix))
