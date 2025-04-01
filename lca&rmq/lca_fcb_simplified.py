import math

class LCA_FCB_Simplified:
    def __init__(self, adj, root=0):
        self.n = len(adj)
        self.adj = adj
        self.root = root

        self.euler_tour = []
        self.depths = []
        self.first_occurrence = [-1] * self.n
        self._current_depth = 0

        self._dfs(root, -1)

        self.tour_len = len(self.depths)
        self.log_tour_len = self.tour_len.bit_length() - 1

        self.st = [[0] * (self.log_tour_len + 1) for _ in range(self.tour_len)]

        self._build_sparse_table()

    def _dfs(self, u, parent):
        current_index = len(self.euler_tour)
        self.euler_tour.append(u)
        self.depths.append(self._current_depth)
        if self.first_occurrence[u] == -1:
            self.first_occurrence[u] = current_index

        for v in self.adj[u]:
            if v != parent:
                self._current_depth += 1
                self._dfs(v, u)
                self._current_depth -= 1
                self.euler_tour.append(u)
                self.depths.append(self._current_depth)

    def _build_sparse_table(self):
        for i in range(self.tour_len):
            self.st[i][0] = i

        for k in range(1, self.log_tour_len + 1):
            for i in range(self.tour_len - (1 << k) + 1):
                idx1 = self.st[i][k - 1]
                idx2 = self.st[i + (1 << (k - 1))][k - 1]
                self.st[i][k] = idx1 if self.depths[idx1] <= self.depths[idx2] else idx2

    def _query_sparse_table(self, l, r):
        length = r - l + 1
        k = length.bit_length() - 1

        idx1 = self.st[l][k]
        idx2 = self.st[r - (1 << k) + 1][k]

        return idx1 if self.depths[idx1] <= self.depths[idx2] else idx2

    def query(self, u, v):
        idx_u = self.first_occurrence[u]
        idx_v = self.first_occurrence[v]

        l = min(idx_u, idx_v)
        r = max(idx_u, idx_v)

        min_depth_index = self._query_sparse_table(l, r)

        return self.euler_tour[min_depth_index]

if __name__ == "__main__":
    n_nodes = 8
    adj = [[] for _ in range(n_nodes)]

    def add_edge(u, v):
        adj[u].append(v)
        adj[v].append(u)

    add_edge(0, 1)
    add_edge(0, 2)
    add_edge(0, 3)
    add_edge(1, 4)
    add_edge(1, 5)
    add_edge(2, 6)
    add_edge(5, 7)

    lca_solver = LCA_FCB_Simplified(adj, root=0)

    print(f"LCA(4, 7) = {lca_solver.query(4, 7)}")
    print(f"LCA(4, 6) = {lca_solver.query(4, 6)}")
    print(f"LCA(3, 7) = {lca_solver.query(3, 7)}")
    print(f"LCA(5, 7) = {lca_solver.query(5, 7)}")
    print(f"LCA(0, 0) = {lca_solver.query(0, 0)}")
    print(f"LCA(6, 6) = {lca_solver.query(6, 6)}")
