import random
import numpy as np
import warnings

def build_randomized_tutte_matrix(n, edges, random_range=(1, 10**9)):
    matrix = np.zeros((n, n), dtype=np.float64)
    variables = {} 

    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError(f"Vertices ({u}, {v}) out of bounds for n={n}")
        if u == v:
            raise ValueError(f"Self-loops ({u}, {v}) are not supported in this context.")

        i, j = min(u, v), max(u, v)

        if (i, j) not in variables:
            variables[(i, j)] = float(random.randint(random_range[0], random_range[1]))

        random_val = variables[(i, j)]
        matrix[i, j] = random_val
        matrix[j, i] = -random_val

    return matrix

def get_maximum_matching_size_randomized(n, edges, random_range=(1, 10**9)):
    if n == 0:
        return 0
    if not edges and n > 0:
        return 0
    if n > 0 and not edges:
        return 0

    try:
        tutte_matrix = build_randomized_tutte_matrix(n, edges, random_range)
    except ValueError as e:
        print(f"Error building Tutte matrix: {e}")
        return -1 

    rank = np.linalg.matrix_rank(tutte_matrix)

    if rank % 2 != 0:
        warnings.warn(f"Calculated rank ({rank}) is odd. This is unexpected for a Tutte matrix "
                      f"and might indicate numerical precision issues. Rounding down.")

    max_matching_size = rank // 2

    return max_matching_size

def has_perfect_matching_randomized(n, edges, random_range=(1, 10**9)):
    if n % 2 != 0:
        return False
    if n == 0:
        return True

    max_matching_size = get_maximum_matching_size_randomized(n, edges, random_range)

    if max_matching_size < 0:
        print("Could not determine perfect matching due to error in size calculation.")
        return None

    return max_matching_size == n // 2


print("--- Randomized Tutte Matrix Algorithms ---")

n1 = 4
edges1 = [(0, 1), (1, 2), (2, 3), (3, 0)]
print(f"\nGraph 1: Square (n={n1}, edges={edges1})")
size1 = get_maximum_matching_size_randomized(n1, edges1)
pm1 = has_perfect_matching_randomized(n1, edges1)
print(f"  Est. Max Matching Size: {size1} (Expected: 2)")
print(f"  Likely has Perfect Matching? {pm1} (Expected: True)")
if pm1 is not None:
    print(f"  Consistency Check: {pm1 == (size1 == n1 // 2)}")

n2 = 3
edges2 = [(0, 1), (1, 2)]
print(f"\nGraph 2: Path P3 (n={n2}, edges={edges2})")
size2 = get_maximum_matching_size_randomized(n2, edges2)
pm2 = has_perfect_matching_randomized(n2, edges2)
print(f"  Est. Max Matching Size: {size2} (Expected: 1)")
print(f"  Likely has Perfect Matching? {pm2} (Expected: False)")

n3 = 4
edges3 = [(0, 1), (1, 2), (2, 3)]
print(f"\nGraph 3: Path P4 (n={n3}, edges={edges3})")
size3 = get_maximum_matching_size_randomized(n3, edges3)
pm3 = has_perfect_matching_randomized(n3, edges3)
print(f"  Est. Max Matching Size: {size3} (Expected: 2)")
print(f"  Likely has Perfect Matching? {pm3} (Expected: True)")
if pm3 is not None:
    print(f"  Consistency Check: {pm3 == (size3 == n3 // 2)}")

n4 = 4
edges4 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
print(f"\nGraph 4: Complete K4 (n={n4}, edges={edges4})")
size4 = get_maximum_matching_size_randomized(n4, edges4)
pm4 = has_perfect_matching_randomized(n4, edges4)
print(f"  Est. Max Matching Size: {size4} (Expected: 2)")
print(f"  Likely has Perfect Matching? {pm4} (Expected: True)")
if pm4 is not None:
    print(f"  Consistency Check: {pm4 == (size4 == n4 // 2)}")

n5 = 4
edges5 = [(0, 1), (0, 2), (0, 3)]
print(f"\nGraph 5: Claw K1,3 (n={n5}, edges={edges5})")
size5 = get_maximum_matching_size_randomized(n5, edges5)
pm5 = has_perfect_matching_randomized(n5, edges5)
print(f"  Est. Max Matching Size: {size5} (Expected: 1)")
print(f"  Likely has Perfect Matching? {pm5} (Expected: False)")
if pm5 is not None:
    print(f"  Consistency Check: {pm5 == (size5 == n5 // 2)}")

n6 = 10
edges6 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
          (5, 7), (7, 9), (9, 6), (6, 8), (8, 5),
          (0, 5), (1, 6), (2, 7), (3, 8), (4, 9)] 
print(f"\nGraph 6: Petersen Graph (n={n6})")
size6 = get_maximum_matching_size_randomized(n6, edges6)
pm6 = has_perfect_matching_randomized(n6, edges6)
print(f"  Est. Max Matching Size: {size6} (Expected: 5)")
print(f"  Likely has Perfect Matching? {pm6} (Expected: True)")
if pm6 is not None:
    print(f"  Consistency Check: {pm6 == (size6 == n6 // 2)}")

n7 = 4
edges7 = []
print(f"\nGraph 7: Empty Graph (n={n7})")
size7 = get_maximum_matching_size_randomized(n7, edges7)
pm7 = has_perfect_matching_randomized(n7, edges7)
print(f"  Est. Max Matching Size: {size7} (Expected: 0)")
print(f"  Likely has Perfect Matching? {pm7} (Expected: False)") 
if pm7 is not None:
     print(f"  Consistency Check: {pm7 == (size7 == n7 // 2)}")

n8 = 4
edges8 = [(0,1)] 
print(f"\nGraph 8: Isolated Vertices (n={n8}, edges={edges8})")
size8 = get_maximum_matching_size_randomized(n8, edges8)
pm8 = has_perfect_matching_randomized(n8, edges8)
print(f"  Est. Max Matching Size: {size8} (Expected: 1)")
print(f"  Likely has Perfect Matching? {pm8} (Expected: False)")
if pm8 is not None:
     print(f"  Consistency Check: {pm8 == (size8 == n8 // 2)}")
