import math

class LCA_RMQ_Solver:

    def __init__(self, adj, root=0):
        self.n = len(adj)
        self.adj = adj
        self.root = root
        
        self.euler_tour = []
        self.depths = []
        self.first_occurrence = [-1] * self.n
        
        self.visited = [False] * self.n
        self._dfs(self.root, 0)
        
        self.tour_len = len(self.depths)
        self._build_sparse_table()

    def _dfs(self, u, depth):
        self.visited[u] = True
        if self.first_occurrence[u] == -1:
            self.first_occurrence[u] = len(self.euler_tour)
        
        self.euler_tour.append(u)
        self.depths.append(depth)
        
        for v in self.adj[u]:
            if not self.visited[v]:
                self._dfs(v, depth + 1)
                self.euler_tour.append(u)
                self.depths.append(depth)

    def _build_sparse_table(self):
        if not self.depths:
            self.st = []
            self.logs = []
            return

        max_k = int(math.log2(self.tour_len))
        self.st = [[0] * (max_k + 1) for _ in range(self.tour_len)]

        for i in range(self.tour_len):
            self.st[i][0] = i 

        for k in range(1, max_k + 1):
            for i in range(self.tour_len - (1 << k) + 1):
                idx1 = self.st[i][k - 1]
                idx2 = self.st[i + (1 << (k - 1))][k - 1]
                if self.depths[idx1] < self.depths[idx2]:
                    self.st[i][k] = idx1
                else:
                    self.st[i][k] = idx2
        
        self.logs = [0] * (self.tour_len + 1)
        for i in range(2, self.tour_len + 1):
            self.logs[i] = self.logs[i // 2] + 1

    def _query_rmq_index(self, l, r):
         if l > r : 
             l, r = r, l # Ensure l <= r
         if l < 0 or r >= self.tour_len:
              raise IndexError("RMQ query indices out of bounds")
         
         k = self.logs[r - l + 1]
         idx1 = self.st[l][k]
         idx2 = self.st[r - (1 << k) + 1][k]
         
         if self.depths[idx1] < self.depths[idx2]:
             return idx1
         else:
             return idx2

    def query_lca(self, u, v):
        if not (0 <= u < self.n and 0 <= v < self.n):
             raise ValueError("Nodes out of range")
        if self.first_occurrence[u] == -1 or self.first_occurrence[v] == -1:
             raise ValueError("One or both nodes not reachable from the root")

        idx_u = self.first_occurrence[u]
        idx_v = self.first_occurrence[v]
        
        l = min(idx_u, idx_v)
        r = max(idx_u, idx_v)
        
        min_depth_idx_in_tour = self._query_rmq_index(l, r)
        return self.euler_tour[min_depth_idx_in_tour]

# --- Example Usage ---
if __name__ == '__main__':
    # Example Tree:
    #       0
    #      /|\
    #     1 2 3
    #    /|   |\
    #   4 5   6 7
    #           |
    #           8
    n_nodes = 9
    adj_list = [[] for _ in range(n_nodes)]
    edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 4), (1, 5),
        (3, 6), (3, 7),
        (7, 8)
    ]

    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)

    lca_solver = LCA_RMQ_Solver(adj_list, root=0)

    print(f"Euler Tour: {lca_solver.euler_tour}")
    print(f"Depths:     {lca_solver.depths}")
    print(f"First Occ:  {lca_solver.first_occurrence}")

    node1, node2 = 4, 5
    lca_result = lca_solver.query_lca(node1, node2)
    print(f"LCA({node1}, {node2}) = {lca_result}") # Expected: 1

    node1, node2 = 4, 8
    lca_result = lca_solver.query_lca(node1, node2)
    print(f"LCA({node1}, {node2}) = {lca_result}") # Expected: 0

    node1, node2 = 6, 8
    lca_result = lca_solver.query_lca(node1, node2)
    print(f"LCA({node1}, {node2}) = {lca_result}") # Expected: 3
    
    node1, node2 = 5, 2
    lca_result = lca_solver.query_lca(node1, node2)
    print(f"LCA({node1}, {node2}) = {lca_result}") # Expected: 0

    node1, node2 = 0, 4
    lca_result = lca_solver.query_lca(node1, node2)
    print(f"LCA({node1}, {node2}) = {lca_result}") # Expected: 0