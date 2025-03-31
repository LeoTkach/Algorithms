def edmonds_blossom(graph):
    """
    Implements Edmonds' Blossom Algorithm for finding maximum cardinality matching in general graphs.
    
    Parameters:
    graph: Dictionary representing an undirected graph where keys are vertices and values are
           lists of adjacent vertices
    
    Returns:
    A dictionary representing the matching, where keys and values are matched vertices
    """

    matching = {}

    def find_augmenting_path(v, visited, path):
        visited.add(v)
        
        for neighbor in graph[v]:
            # Skip if we've already visited this neighbor
            if neighbor in visited:
                continue

            if neighbor not in matching or (neighbor in matching and matching[neighbor] == v):
                if v not in matching or (v in matching and matching[v] != neighbor):
                    path.append((v, neighbor))
                    return True

            if neighbor in matching:
                matched_to = matching[neighbor]
                if matched_to not in visited:
                    path.append((v, neighbor))
                    path.append((neighbor, matched_to))
                    if find_augmenting_path(matched_to, visited, path):
                        return True

                    path.pop()
                    path.pop()
        
        return False

    def contract_blossom(blossom, v, blossom_base):

        contracted_graph = {}
        for vertex in graph:
            if vertex in blossom and vertex != blossom_base:
                continue
            contracted_graph[vertex] = []
            for neighbor in graph[vertex]:
                if neighbor in blossom:
                    if blossom_base not in contracted_graph[vertex]:
                        contracted_graph[vertex].append(blossom_base)
                else:
                    contracted_graph[vertex].append(neighbor)
        
        return contracted_graph

    def find_blossom(v, visited, parent):
        visited.add(v)
        
        for neighbor in graph[v]:
            if neighbor == parent:
                continue
                
            if neighbor in visited:

                blossom = [neighbor, v]
                current = v
                while current != neighbor:
                    current = parent[current]
                    blossom.append(current)
                return blossom
            
            parent[neighbor] = v
            result = find_blossom(neighbor, visited, parent)
            if result:
                return result
        
        return None

    while True:

        augmenting_path = []
        visited = set()

        found_path = False
        for v in graph:
            if v not in matching:
                if find_augmenting_path(v, visited, augmenting_path):
                    found_path = True
                    break
        
        if not found_path:

            for v in graph:
                blossom = find_blossom(v, set(), {v: None})
                if blossom:

                    blossom_base = blossom[0]
                    contracted_graph = contract_blossom(blossom, v, blossom_base)

                    temp_matching = edmonds_blossom(contracted_graph)

                    for a, b in temp_matching.items():
                        if a == blossom_base:

                            for blossom_vertex in blossom:
                                if b in graph[blossom_vertex]:
                                    matching[blossom_vertex] = b
                                    matching[b] = blossom_vertex
                                    break
                        elif b == blossom_base:

                            for blossom_vertex in blossom:
                                if a in graph[blossom_vertex]:
                                    matching[a] = blossom_vertex
                                    matching[blossom_vertex] = a
                                    break
                        else:
                            matching[a] = b
                            matching[b] = a
                    
                    return matching

            break

        for i in range(0, len(augmenting_path), 2):
            u, v = augmenting_path[i]

            if u in matching:
                del matching[matching[u]]
                del matching[u]

            if v in matching:
                del matching[matching[v]]
                del matching[v]

            matching[u] = v
            matching[v] = u
    
    return matching

if __name__ == "__main__":

    graph = {
        0: [1, 2],
        1: [0, 2, 3],
        2: [0, 1, 3, 4],
        3: [1, 2, 5],
        4: [2, 5],
        5: [3, 4]
    }
    
    matching = edmonds_blossom(graph)
    print("Maximum matching:", matching)
