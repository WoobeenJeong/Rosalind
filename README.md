# Rosalind

- Textbook Track

## Textbook Track 

### [BA1]
<details>
<summary>Hamming distance</summary>
<div markdown="1">

The minimum number of **substitutions(Errors)** required to change one string into the other.

--> check [BA5] Edit distance (= Levenshtein distance, Wagner–Fischer algorithm)

</div>
</details>

<details>
<summary>Brute Force algorithm</summary>
<div markdown="1">

(= exhaustive search, generate and test)
(= nondeterministic Turing machines)

Systematically checking all possible candidates for whether or not each candidate satisfies the problem's statement.
   <p align="left">
  <img src="https://github.com/WoobeenJeong/Rosalind/assets/132027211/d1047568-3dc4-4223-9bc3-309ac5c9d51f" alt="image" width="auto" height="200">
   </p>
   
sliding window : n(string) - m(pattern) + 1

complexity : O(mn)

</div>
</details>

<details>
<summary>GC skew</summary>
<div markdown="1">

In some bacterial genomes, there is an enrichment of guanine over cytosine, because of cytosine deamination on okazaki fragement.

GC skew = (G - C)/(G + C)

```
def min_gc_skew(string):
    min_skew_list = [0]
    skew = 0
    min_skew = 0
    
    for i in range(len(string)):    
        if string[i] == C면 -1, G면 +1 로 skew 계산

        if 현재 누적skew가 min_skew보다 작으면
            min_skew = skew
            min_skew_list에 해당 위치 추가
            
    return min_skew_list
```

</div>
</details>

### [BA2]

<details>
<summary>Greedy search</summary>
<div markdown="1">

The problem-solving heuristic algorithm of making the locally optimal choice at each stage.

: greedy choice -> feasibility check -> update solution (local) -> repeat -> optimality check (global)

- same as DP : "heuristic, calculate all possible"
- differ from DP : "does not reconsider the choice, previous decision doesn't affect after works"

- limitations : NOT an optimal solution, local optimization
   <p align="left">
  <img src="https://github.com/WoobeenJeong/Rosalind/assets/132027211/dc4f095a-9384-4ef7-bbbc-8a4f93764c4b" alt="image" width="auto" height="100">
   </p>

</div>
</details>

<details>
<summary>Gibbs sampler</summary>
<div markdown="1">
= Markov Chain Monte Carlo(MCMC) based algorithm by Bayesian inference, 
   
   that randomly starts -> determine and restart from initial as EM algorithm process

-> more efficient than greedy search but slow

</div>
</details>

<details>
<summary>Pseudo count (Laplacian smoothing)</summary>
<div markdown="1">
= Laplace smoothing, Additive smoothing = Lidstone smoothing

A technique used to smooth count data, eliminating issues caused by certain values having 0 occurrences.

("pseudocount" α > 0 is a smoothing parameter. α = 0 corresponds to no smoothing.)

   <p align="left">
  <img src="https://github.com/WoobeenJeong/Rosalind/assets/132027211/aa61935f-301e-46b7-8828-70bb053e09e1" alt="image" width="auto" height="100">
   </p>


</div>
</details>

<details>
<summary>Median string</summary>
<div markdown="1">
= Commonly found kmer motif(pattern) from all strings(DNAs,...) with the least distance.

   <p align="left">
  <img src="https://github.com/WoobeenJeong/Rosalind/assets/132027211/703ed468-6c44-4cad-9f87-25959bf3dd05" alt="image" width="auto" height="200">
   </p>

</div>
</details>

### [BA3]
<details>
<summary>Graph </summary>
<div markdown="1">

G=(V,E)

example : 1-2-3

V,v for nodes(vertices(from vertex)) = {1,2,3}

E,u for edges = {(1,2),(2,3)}

- Hamming graph
- De bruijn graph
- Kautz graph

</div>
</details>

<details>
<summary>De Bruijn Graph (DBG) </summary>
<div markdown="1">

n-dimensional m-symbol **directed** graph $((1,2)\neq(2,1))$

- $m^n$ vertices(nodes)
- each nodes has $m$ income and outcome edges
- all possible length-n sequences allows multiple m-symbols appear
- each DBG follows Eulerian or Hamiltonian cycle.

   <p align="left">
  <img src="https://github.com/WoobeenJeong/Rosalind/assets/132027211/e73a6e51-32a6-40a1-acf4-ac8e699250c4" alt="image" width="auto" height="100">
   </p>
   
strong : speedy
weak : indel error, naive DBG spend lot of times

</div>
</details>

<details>
<summary>Eulerian/Hamiltonian cycle </summary>
<div markdown="1">
   
= cycle, circuit (start=end) / path, trail(start≠end) / distance(as scored)
___

**Eulerian** : **finite** graph that visits every edge exactly once. (can be found in both "directed/undirected")

= Konigsberg's bridge problem

= euler's theorem 

= all nodes have an even(2,4,6...) degree(edge numbers) 

___

**Hamiltonian** : graph that visits each nodes exactly once. (can be found in both "directed/undirected")

= **traceable path**

= manhattan tour problem, traveling salesman problem(TSP)

= NP complete problem -> as Brute Force

</div>
</details>

<details>
<summary>NP complete(NPC), NP hard problem </summary>
<div markdown="1">

nondeterministic polynomial-time complete

___

(nondeterministic Turing machines(NTM) = Brute force search algorithm)

(polynomial-time -> deterministic algorithm / linear programming)

$2^{O(\log \ n)} = poly(n)$

-> possible (yes/no = P/NP) for n times

$Let \ L \ as \ text, \ \forall L' \in NP \ and \ L' {\leq}_p L, \ then \ LP-hard$

-> $\subset$ halting problem

</div>
</details>

<details>
<summary> Fleury/Hierholzer algorithm </summary>
<div markdown="1">

= algorithm for finding Eulerian path
  (E = # of edges)
  
- Fleury : O(E^2)
  1. start node = #E:odd or random(if all #E same) 
  2. no brige for edge
  3. choose -> erase edge

- Hierholzer : O(E)
  1. start node = random
  2. choose -> erase edge

</div>
</details>

<details>
<summary> Depth first search (DFS) </summary>
<div markdown="1">

= find path(cycle) of tree, DAG, maze


DFS algorithm : O(|V|+|E|)

- V = # of nodes

- E = # of edges


```
DFS(node,Graph):
    if node in Graph:
    for all directed edges from v(node) to w(neighbor) that are in G.adjacentEdges(v) do
        if vertex w is not labeled as discovered then
            recursively call DFS(G, w)

### [Example] ###

def dfs(node):
    if node in graph:
        for neighbor in graph[node]:
            if (node, neighbor) not in visited_edges:
                visited_edges.add((node, neighbor))
                dfs(neighbor)
    path.append(node)
```

</div>
</details>

<details>
<summary> In/Out-degree, Source/Sink </summary>
<div markdown="1">
= For direted graph(path/cycle even tree),  

$Let \  G=(V,E), v \in V (v \ for\  nodes) \ \sum_{v \in V}{deg^- (v)} + \sum_{v \in V}{deg^+ (v)}=|A|$

$If \ A=0, balanced \ directed \ graph$

${deg^- (v)}$ = Indegree = Source : start point of matrix : inward edges < outward edges

${deg^+ (v)}$ = Outdegree = Sink : end point of matrix : inward edges > outward edges


</div>
</details>

### [BA5]
<details>
<summary> Dynamic Programing (DP) problems </summary>
<div markdown="1">
by : Richard Bellman (1950s) 

= Mathematical optimization method with recursive sub-problems

Source : start (0,0)

Sink : end (m,n)

traceback (optimization) : Sink to Source

1. Fibonacci Sequence
2. Change making Problem
3. Longest Increasing Subsequence, LIS
4. Matrix Chain Multiplication
5. 0/1 Knapsack Problem
6. Shortest Path Problem
7. Subset Sum Problem

</div>
</details>

<details>
<summary> Wagner–Fischer algorithm </summary>
<div markdown="1">

   <p align="left">
  <img src="https://github.com/WoobeenJeong/Rosalind/assets/132027211/7b0ed8ce-f0e6-44da-b239-32eaeb4f7b12" alt="image" width="auto" height="100">
   </p>
   
= Edit distance

= Levenshtein distance

The minimum number of **single character edit(insertion, deletion, substitutions)** required to change one string into the other.

</div>
</details>

<details>
<summary> Needleman-Wunch algorithm </summary>
<div markdown="1">

= Global alignment

$H_{k,l} =0$

$(1 < k \leq i < n, \ 1 < l \leq j < m)$

$H(x)=$

   - $H_{i-1,j-1} + s(a,b) \max_{k\geq 1} (H_{i-k,j} - \sigma_k)$

   - $max_{k\geq 1}(\{H_{i-k,j}-\sigma_k\})$

   - $max_{l\geq 1}(\{H_{i,j-l}-\sigma_l\})$

</div>
</details>

<details>
<summary> Smith-Waterman algorithm </summary>
<div markdown="1">

= Local alignment

$H_{k,0} = H_{0,l} =0$

$(1 < k \leq i < n, \ 1 < l \leq j < m)$

$H(x)=$

   - $H_{i-1,j-1} + s(a,b) \max_{k\geq 1} (H_{i-k,j} - \sigma_k)$

   - $max_{k\geq 1}(\{H_{i-k,j}-\sigma_k\})$

   - $max_{l\geq 1}(\{H_{i,j-l}-\sigma_l\})$

   - $0$

</div>
</details>

<details>
<summary> BLOSUM, PAM </summary>
<div markdown="1">


BLOSUM = BLOcks SUbstitution Matrix

         The matrix built from blocks with less than r% of similarity

PAM = Point Accepted Mutation

      Relating the number of mutated amino acids per 100 A.A


|  BLOSUM  |    PAM   |
|----------|----------|
| BLOSUM90 |  PAM100  |
| BLOSUM89 |  PAM120  |
| BLOSUM62 |  PAM160  |
| BLOSUM52 |  PAM200  |
| BLOSUM45 |  PAM250  |

</div>
</details>

<details>
<summary> Modified alignments </summary>
<div markdown="1">

- Semi-Global alignment:

      AAAAABBBBBCCCCCD

         AABB---CC---D

- Fitting alignment:

      AAAAABBBBBCCCCC
  
             BB-CC
  
- Overlap alignment:

       AAABBBCCC
  
           BB-CCDD
  
- Affine gap alignment:
- Multiple Sequence alignment (MSA):

</div>
</details>

### [BA7]
<details>
<summary>Tree, Adjacency matrix</summary>
<div markdown="1">

**Definition of "Tree"**
1. graph without cycle (graph = node + edge --> check [BA3] Graph)
2. leaf node (degree=1) : without any child nodes = external node = terminal node = outer node
3. internal node (degree>1) : with any child nodes = internal node = inner node = inode
4. if # of node > 2, each internal node have > 1 edges.
5. total (n) nodes have (n-1) edge(s).   

- unrooted tree : consist of leaf nodes(degree=1) and internal nodes(degree>1).
- rooted tree : have root node(degree=2), so that makes leaf(degree=1), internal(degree>2).
- simple tree : # of node > 2, 1 pair of leaf in each inner nodes(=parent node).


**Adjacency matrix**

= To indicate graph into matrix, pair of nodes(verticles) are adjacent or not.

= If the graph is **undiredted**, = adjacency matrix is **symmetric**

--> check [BA3] DFS

</div>
</details>

<details>
<summary>Additive/Fitted/Distance matrix</summary>
<div markdown="1">



</div>
</details>


<details>
<summary>Limb length</summary>
<div markdown="1">


      A \       / E
          C -- D  
      B /       \ F

$CE = [(AC+CE)+(BC+CE)-(AC+BC)]/2$

$so, AC = AE - (AE+BE-AB)/2$

in here, AC = limb length

for A and B, is neighbor node

**limb length**
= distance between leaf node and parent node

</div>
</details>


### [BA8]
<details>
<summary>K-center cluster</summary>
<div markdown="1">

1. Maximal distance
   - Farthest First Traversal
   - $min\sum(data-center) \ and \ max\sum(center-center)$
2. K-means based on "Center of gravity theorem"
   - Squared Error Distortion
   - $Distortion(Data,Centers) = (1/n) min \sum(Euclidian dist(Data, Centers))\times2$


</div>
</details>

<details>
<summary>K-means vs KNN cluster</summary>
<div markdown="1">

**K-means** : k refers **# of classes** (unsupervised)
- clustering

**KNN** : k refers **# of nearest neighbors** (supervised, class already selected) 
- classifying, regression

</div>
</details>

<details>
<summary>Lloyd algorithm</summary>
<div markdown="1">

=

</div>
</details>

___

## Hint

<details>
<summary> ba2d </summary>
<div markdown="1">

   <p align="left">
  <img src="https://github.com/WoobeenJeong/Rosalind/assets/132027211/0583e5ae-0ddc-45a0-874c-79588cb7b196" alt="image" width="auto" height="100">
   </p>

</div>
</details>

<details>
<summary> ba3e, ba3j </summary>
<div markdown="1">

   <p align="left">
  <img src="https://github.com/WoobeenJeong/Rosalind/assets/132027211/8f57c10f-14e9-42d6-9cee-6d918e3a0d19" alt="image" width="auto" height="100">
   </p>

   <p align="left">
  <img src="https://github.com/WoobeenJeong/Rosalind/assets/132027211/719de066-c7a1-4754-83f3-ae5c3baa4222" alt="image" width="auto" height="100">
   </p>

</div>
</details>

<details>
<summary> ba3h </summary>
<div markdown="1">

- ba3e + ba3g (pattern -> DBG -> DAG)

```
def overlap(patterns):
   ### for max length overlapping { prefix : [suffix] } by using count_overlap
   return DBG
   
def count_overlap(prefix,suffix)
   return overlap_length

def find_end(DBG):
   return start_node

def eulerian(DBG):
   def dfs_stack(start_node):
      stack.append(start_node)
      while stack:
         path.append
   dfs_stack(start_node)
   return path[::-1]

def stringmake(path)
   ### result += every single suffix[overlap_length:] by using count_overlap
   return

```

</div>
</details>

<details>
<summary> ba5k </summary>
<div markdown="1">

   <p align="left">
  <img src="https://github.com/WoobeenJeong/Rosalind/assets/132027211/11414ff6-9e1e-46e8-a64e-d24a4b266725" alt="image" width="auto" height="100">
   </p>

</div>
</details>
