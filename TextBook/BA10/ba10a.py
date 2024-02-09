### Hidden path problem
### p(pi) = p(pi1) * p(pi2|pi1) * p(pi3|pi2) * ... * p(piL|piL-1) 즉, 이전 확률에 현재 확률을 곱해나가는 것

### Array 사용버전 ###

import numpy as np

def transition_prob(string, states, transition_matrix):
    prob = 1/len(states)
    for i in range(len(string)-1):
        prob *= transition_matrix[states.index(string[i])][states.index(string[i+1])]   #이 부분이 array버전에서는 [][]로 표현
    return prob
    
    
with open ('bioinfo2/rosalind_ba10a.txt','r') as f:
    dataset = f.readlines()
    string = dataset[0].strip()
    states = dataset[2].strip().split()                 # array나 matrix나 상관없으려나? 어느게 더 편할까
    transition_matrix = np.array([list(map(float, line.strip().split()[1:])) for line in dataset[5:5+len(states)]])

# print(string, states, len(states), transition_matrix, sep='\n')

# print(states.index('A'), states.index('B'))

########################################################################################
### Matrix 사용버전 ###

import numpy as np

def transition_prob(string, states, transition_matrix):
    prob = 1/len(states)
    for i in range(len(string)-1):
        prob *= transition_matrix[states.index(string[i]), states.index(string[i+1])]
    return prob

with open('bioinfo2/rosalind_ba10a.txt', 'r') as f:
    dataset = f.readlines()
    string = dataset[0].strip()
    states = dataset[2].strip().split()
    transition_matrix = np.matrix([list(map(float, line.strip().split()[1:])) for line in dataset[5:5+len(states)]])

# print(string, states, len(states), transition_matrix, sep='\n')
# print(states.index('A'), states.index('B'))

print(transition_prob(string, states, transition_matrix))


########################################################################################

### ba5b.py의 manhattan문제 기반 viterbi algo. 활용 Longest path 얻는것 활용아님!!!!!! 이건 p(pi)아냐!!!!


# def make_manhattan(string,state):
#     matrix = np.zeros((len(state),len(string)))
#     matrix[0][0] = 1
#     matrix[1][0] = 1
#     return matrix

# def viterbi(string, states, transition_matrix):
#     matrix = make_manhattan(string, states)
#     initial_weight = 1/len(states)
    
#     print(f'[0][0]',transition_matrix[0,0],f'[0][1]',transition_matrix[0,1],f'[1][0]',transition_matrix[1,0],f'[1][1]',transition_matrix[1,1])
    
#     for i in range(1,len(string)):
#         for j in range(len(states)):
#             matrix[j][i] = max(matrix[0][i-1]*transition_matrix[0,j],matrix[1][i-1]*transition_matrix[1,j])
    
#         print(f'[{j}][{i}]',matrix[j][i])
#     return matrix

# print(make_manhattan(string,states))

# print(viterbi(string,states,transition_matrix))
