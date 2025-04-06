import random
import numpy as np
import warnings

def greedy_maximal_matching(vertices, edges):
    matching = set()
    covered_vertices = set()
    
    for u, v in edges:
        if u not in covered_vertices and v not in covered_vertices:
            matching.add(frozenset([u, v]))
            covered_vertices.add(u)
            covered_vertices.add(v)
            
    matching_list = [tuple(sorted(list(edge))) for edge in matching]
    return matching_list

num_vertices_1 = 5
vertices_1 = list(range(num_vertices_1))
edges_1 = [(0, 1), (1, 2), (2, 3), (3, 4)]
greedy_m1 = greedy_maximal_matching(vertices_1, edges_1)
print(f"Graph 1 (P5): Edges={edges_1}")
print(f"  Greedy Maximal Matching: {greedy_m1}")
print(f"  Size: {len(greedy_m1)}")

num_vertices_2 = 5
vertices_2 = list(range(num_vertices_2))
edges_2_ordered = [(0, 1), (2, 3), (4, 0), (1, 2), (3, 4), (0, 2)]
greedy_m2a = greedy_maximal_matching(vertices_2, edges_2_ordered)
print(f"\nGraph 2 (C5 + (0,2)): Edges={edges_2_ordered}")
print(f"  Greedy Maximal Matching: {greedy_m2a}")
print(f"  Size: {len(greedy_m2a)}") 

edges_2_ordered_b = [(0, 2), (3, 4), (0, 1), (1, 2), (2, 3), (4, 0) ] 
greedy_m2b = greedy_maximal_matching(vertices_2, edges_2_ordered_b)
print(f"\nGraph 2 (C5 + (0,2)): Edges={edges_2_ordered_b}")
print(f"  Greedy Maximal Matching: {greedy_m2b}")
print(f"  Size: {len(greedy_m2b)}") 

num_vertices_3 = 6
vertices_3 = list(range(num_vertices_3)) 
edges_3 = []
for i in range(3):
    for j in range(3, 6):
        edges_3.append((i, j))
greedy_m3 = greedy_maximal_matching(vertices_3, edges_3)
print(f"\nGraph 3 (K3,3): Edges={edges_3}")
print(f"  Greedy Maximal Matching: {greedy_m3}")
print(f"  Size: {len(greedy_m3)}")
