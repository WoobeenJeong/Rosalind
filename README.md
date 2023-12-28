# Rosalind

- Textbook Track

## Textbook Track 

### [BA1]
<details>
<summary>Hamming distance</summary>
<div markdown="1">

The minimum number of substitutions(Errors) required to change one string into the other.

</div>
</details>

<details>
<summary>Brute Force algorithm</summary>
<div markdown="1">

(= exhaustive search, generate and test)
(= nondeterministic Turing machines)

Systematically checking all possible candidates for whether or not each candidate satisfies the problem's statement.
   <p align="left">
  <img src="https://github.com/WoobeenJeong/Rosalind/assets/132027211/d1047568-3dc4-4223-9bc3-309ac5c9d51f" alt="image" width="auto" height="100">
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

___

## Hint

<details>
<summary> ba3e </summary>
<div markdown="1">

   <p align="left">
  <img src="https://github.com/WoobeenJeong/Rosalind/assets/132027211/09223752-ec87-4ce5-8e69-ae5fa425d917" alt="image" width="auto" height="100">
   </p>

</div>
</details>


