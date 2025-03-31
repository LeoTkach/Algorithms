class TarjanSCC:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.index = 0
        self.stack = []
        self.indices = [-1] * n
        self.lowlink = [-1] * n
        self.on_stack = [False] * n
        self.sccs = []

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def strongconnect(self, v):
        self.indices[v] = self.index
        self.lowlink[v] = self.index
        self.index += 1
        self.stack.append(v)
        self.on_stack[v] = True
        
        for w in self.graph[v]:
            if self.indices[w] == -1:
                self.strongconnect(w)
                self.lowlink[v] = min(self.lowlink[v], self.lowlink[w])
            elif self.on_stack[w]:
                self.lowlink[v] = min(self.lowlink[v], self.indices[w])
        
        if self.lowlink[v] == self.indices[v]:
            scc = []
            while True:
                w = self.stack.pop()
                self.on_stack[w] = False
                scc.append(w)
                if w == v:
                    break
            self.sccs.append(scc)

    def find_sccs(self):
        for v in range(self.n):
            if self.indices[v] == -1:
                self.strongconnect(v)
        return self.sccs

if __name__ == "__main__":
    n, m = map(int, input().split())
    tarjan = TarjanSCC(n)
    for _ in range(m):
        u, v = map(int, input().split())
        tarjan.add_edge(u, v)
    sccs = tarjan.find_sccs()
    for scc in sccs:
        print(" ".join(map(str, scc)))