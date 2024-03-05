class Node(object):

    def __init__(current):
        current.suffix_node = -1   

    def __repr__(current):
        return "Node(suffix link: %d)"%current.suffix_node

class Edge(object):
    def __init__(current, start, end, internal, tail):
        current.start = start
        current.end = end
        current.internal = internal
        current.tail = tail
        
    @property
    def length(current):
        return current.end - current.start

    def __repr__(current):
        return 'Edge(%d, %d, %d, %d)'% (current.internal, current.tail 
                                        ,current.start, current.end )


class Suffix(object):
    def __init__(current, internal, start, end):
        current.internal = internal
        current.start = start
        current.end = end
        
    @property
    def length(current):
        return current.end - current.start
                
    def explicit(current):
        return current.start > current.end
    
    def implicit(current):
        return current.end >= current.start

        
class SuffixTree(object):

    def __init__(current, string):
        current.string = string
        current.N = len(string) - 1
        current.nodes = [Node()]
        current.edges = {}
        current.active = Suffix(0, 0, -1)
        
        for i in range(len(string)):
            current._add_prefix(i)
    
    def __repr__(current):
        curr_index = current.N
        memory = ""
        values = list(current.edges.values())
        values.sort(key=lambda x: x.internal)
        for edge in values:
            if edge.internal == -1:
                continue
            
            top = min(curr_index, edge.end)
            memory += current.string[edge.start:top+1] + "\n"
        return memory
            
    def _add_prefix(current, end):
        last_parent_node = -1
        while True:
            parent_node = current.active.internal
            if current.active.explicit():
                if (current.active.internal, current.string[end]) in current.edges:
                    break
            else:
                index = current.edges[current.active.internal, current.string[current.active.start]]
                if current.string[index.start + current.active.length + 1] == current.string[end]:
                    break
                parent_node = current._split_edge(index, current.active)

            current.nodes.append(Node())
            index = Edge(end, current.N, parent_node, len(current.nodes) - 1)
            current._insert_edge(index)
            
            if last_parent_node > 0:
                current.nodes[last_parent_node].suffix_node = parent_node
            last_parent_node = parent_node
            
            if current.active.internal == 0:
                current.active.start += 1
            else:
                current.active.internal = current.nodes[current.active.internal].suffix_node
            current._canonize_suffix(current.active)
        if last_parent_node > 0:
            current.nodes[last_parent_node].suffix_node = parent_node
        current.active.end += 1
        current._canonize_suffix(current.active)
        
    def _insert_edge(current, edge):
        current.edges[(edge.internal, current.string[edge.start])] = edge
        
    def _remove_edge(current, edge):
        current.edges.pop((edge.internal, current.string[edge.start]))
        
    def _split_edge(current, edge, suffix):
        current.nodes.append(Node())
        index = Edge(edge.start, edge.start + suffix.length, suffix.internal, len(current.nodes) - 1)
        current._remove_edge(edge)
        current._insert_edge(index)
        current.nodes[index.tail].suffix_node = suffix.internal  ### need to add node for each edge
        edge.start += suffix.length + 1
        edge.internal = index.tail
        current._insert_edge(edge)
        return index.tail

    def _canonize_suffix(current, suffix):

        if not suffix.explicit():
            index = current.edges[suffix.internal, current.string[suffix.start]]
            if index.length <= suffix.length:
                suffix.start += index.length + 1
                suffix.internal = index.tail
                current._canonize_suffix(suffix)

    def find_substring(current, substring):
        if not substring:
            return -1
        if current.case_insensitive:
            substring = substring.lower()
        curr_node = 0
        i = 0
        while i < len(substring):
            edge = current.edges.get((curr_node, substring[i]))
            if not edge:
                return -1
            ln = min(edge.length + 1, len(substring) - i)
            if substring[i:i + ln] != current.string[edge.start:edge.start + ln]:
                return -1
            i += edge.length + 1
            curr_node = edge.tail
        return edge.start - len(substring) + ln
        
    def has_substring(current, substring):
        return current.find_substring(substring) != -1

with open('ba9c_output.txt', 'w') as out:
    with open('bioinfo2/rosalind_ba9c.txt', 'r') as f:
        text = f.readline()
        tree = SuffixTree(text)
        out.write(tree.__repr__())
