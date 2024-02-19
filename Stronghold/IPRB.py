# (k,m,n) input counts of homozygous dominant(k), heterozygous(m), homozygous recessive(n) organisms
    
def IPRB(AA, Aa, aa):
    
    if AA == 0 and Aa == 0 and aa == 0:
        return 0.0
    elif AA == 0 and Aa == 0:
        return 1.0
    elif AA == 0 and aa == 0:
        return 1.0
    else:
        return 1.0 - (aa*(aa-1) + aa*Aa*0.5 + Aa*aa*0.5 + Aa*(Aa-1)*0.25) / ((AA+Aa+aa) * (AA+Aa+aa-1))      # 1 - probability of no dominant allele

    # aa와 aa가 만나면 무조건 aa가 나옴
    # aa와 Aa가 만나면 0.5확률로 aa가 나옴 (근데, (Aa,aa)와 (aa,Aa)는 다른 경우임)
    # Aa와 Aa가 만나면 0.25확률로 aa가 나옴

with open('rosalind_iprb.txt', 'r') as f:
    k, m, n = map(int, f.readline().split())
    print(IPRB(k,m,n))

