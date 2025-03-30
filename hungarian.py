import numpy as np

def hungarian_algorithm(cost_matrix):
    
    cost_matrix = np.array(cost_matrix, dtype=float)
    original_cost_matrix = cost_matrix.copy()
    n, m = cost_matrix.shape
    
    if n > m:
        cost_matrix = np.hstack([cost_matrix, np.zeros((n, n-m))])
        m = n
    
    cost_matrix = cost_matrix - cost_matrix.min(axis=1).reshape(-1, 1)
    
    cost_matrix = cost_matrix - cost_matrix.min(axis=0)
    
    line_count = 0
    k = min(n, m)
    
    row_ind, col_ind = np.array([-1] * n), np.array([-1] * m)
    
    while line_count < k:
        marked_rows, marked_cols = mark_matrix(cost_matrix)
        line_count = len(marked_rows) + len(marked_cols)
        
        if line_count < k:
            min_val = float('inf')
            for i in range(n):
                if i not in marked_rows:
                    for j in range(m):
                        if j not in marked_cols:
                            min_val = min(min_val, cost_matrix[i, j])
            for i in range(n):
                for j in range(m):
                    if i not in marked_rows and j not in marked_cols:
                        cost_matrix[i, j] -= min_val
                    elif i in marked_rows and j in marked_cols:
                        cost_matrix[i, j] += min_val
    assign_rows_cols(cost_matrix, row_ind, col_ind)
    
    return row_ind, col_ind[:len(original_cost_matrix[0])]

def mark_matrix(matrix):
    
    n, m = matrix.shape
    
    row_ind, col_ind = np.array([-1] * n), np.array([-1] * m)
    assign_rows_cols(matrix, row_ind, col_ind)
    
    marked_rows = set()
    marked_cols = set()
    rows_with_assignments = set(np.where(row_ind >= 0)[0])
    
    unassigned_rows = set(range(n)) - rows_with_assignments
    
    new_marked_rows = unassigned_rows.copy()
    
    while new_marked_rows:
        marked_rows.update(new_marked_rows)
        new_marked_cols = set()
        
        for row in new_marked_rows:
            for col in range(m):
                if matrix[row, col] == 0 and col not in marked_cols:
                    new_marked_cols.add(col)
        
        marked_cols.update(new_marked_cols)
        new_marked_rows = set()
        
        for col in new_marked_cols:
            for row in range(n):
                if col == col_ind[row] and row not in marked_rows:
                    new_marked_rows.add(row)
    
    return (set(range(n)) - marked_rows), marked_cols

def assign_rows_cols(cost_matrix, row_ind, col_ind):
    
    n, m = cost_matrix.shape
    
    row_ind[:] = -1
    col_ind[:] = -1
    
    for i in range(n):
        for j in range(m):
            if cost_matrix[i, j] == 0 and row_ind[i] == -1 and col_ind[j] == -1:
                row_ind[i] = j
                col_ind[j] = i
    
    done = False
    while not done:
        done = True
        for i in range(n):
            if row_ind[i] == -1:  
                visited_cols = set()
                if find_augmenting_path(cost_matrix, i, row_ind, col_ind, visited_cols):
                    done = False
    
def find_augmenting_path(cost_matrix, start_row, row_ind, col_ind, visited_cols):
    
    n, m = cost_matrix.shape
    
    for j in range(m):
        if cost_matrix[start_row, j] == 0 and j not in visited_cols:
            visited_cols.add(j)
            
            if col_ind[j] == -1 or find_augmenting_path(cost_matrix, col_ind[j], row_ind, col_ind, visited_cols):
                row_ind[start_row] = j
                col_ind[j] = start_row
                return True
    
    return False

if __name__ == "__main__":
    cost_matrix = np.array([
        [7, 5, 9, 8],
        [9, 4, 3, 7],
        [9, 9, 5, 6]
    ])
    
    row_indices, col_indices = hungarian_algorithm(cost_matrix)
    
    print("Assignments (worker -> job):")
    total_cost = 0
    for i in range(len(row_indices)):
        j = row_indices[i]
        print(f"Worker {i} -> Job {j} (Cost: {cost_matrix[i, j]})")
        total_cost += cost_matrix[i, j]
    
    print(f"Total cost: {total_cost}")
