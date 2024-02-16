### count gc content

import pandas as pd

def count_gc(raw):
    raw["count"] = raw["seq"].apply(lambda x: x.count("G") + x.count("C"))
    raw["GCcontents"] = raw["count"]/raw["seq"].apply(lambda x: len(x))*100
    target = raw[raw["GCcontents"] == raw["GCcontents"].max()]
    result = f"{target['name'].values[0]}\n{target['GCcontents'].values[0]}"

    return result

###################################################

raw = []        # [] 이건 list를 만드는 것
name = ""

with open('bioinfo2/rosalind_gc.txt',"r") as file:
    for line in file:
        line = line.strip()     # line으로 읽을 때, 불필요한 /n이나 /t 존재 제거 (특정 문자를 제거하고 싶으면 .strip(">")도 가능)
        if line.startswith(">"):
            if name:
                raw.append({"name":name,"seq":seq})     # .append로 지정해주지 않으면, 값이 최신 값으로 갱신되어 저장됨 즉, 마지막 줄만 보여줌
            name = line[1:]
            seq = ""
        else:
            seq += line

if name:
    raw.append({"name":name,"seq":seq})     # 위에 말했던 것처럼, 처음부터 읽어서 마지막줄만 넣어줌
    raw = pd.DataFrame(raw)

print(count_gc(raw))
