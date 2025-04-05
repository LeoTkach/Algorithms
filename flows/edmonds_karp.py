from collections import deque

INF = float('inf')

def bfs(graph, s, t, parent):
    visited = {node: False for node in graph}
    queue = deque()

    queue.append(s)
    visited[s] = True
    parent[s] = -1

    while queue:
        u = queue.popleft()
        if u in graph:
            for v, capacity in graph[u].items():
                if not visited.get(v, False) and capacity > 0: # Используем get для безопасности
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == t:
                        return True
    return False

def edmonds_karp(capacity_graph, source, sink):
    residual_graph = {u: dict(neighbors) for u, neighbors in capacity_graph.items()}
    nodes = set(residual_graph.keys())

    # Сбор всех уникальных узлов и инициализация обратных ребер
    nodes_to_process = list(capacity_graph.keys())
    processed_nodes = set()
    while nodes_to_process:
        u = nodes_to_process.pop(0)
        if u in processed_nodes:
            continue
        processed_nodes.add(u)
        nodes.add(u)
        if u in capacity_graph: # Убеждаемся, что узел есть в исходном графе
            for v in list(capacity_graph[u].keys()): # Используем list для безопасной итерации
                 nodes.add(v)
                 if v not in residual_graph:
                     residual_graph[v] = {}
                 if u not in residual_graph.get(v, {}): # Безопасная проверка и добавление обратного ребра
                     residual_graph[v][u] = 0
                 if v not in processed_nodes and v not in nodes_to_process:
                      nodes_to_process.append(v) # Добавляем соседа для обработки

    parent = {node: -1 for node in nodes}
    max_flow = 0

    while bfs(residual_graph, source, sink, parent):
        path_flow = INF
        s = sink
        while s != source:
            # Проверяем наличие parent[s] и ребра в residual_graph перед доступом
            if parent[s] == -1: # Не должно случаться при успешном BFS, но для безопасности
                 break
            if parent[s] not in residual_graph or s not in residual_graph[parent[s]]:
                 # Обработка возможной ошибки отсутствия ребра в остаточном графе
                 # Это может указывать на проблему в логике BFS или обновлении графа
                 print(f"Ошибка: Отсутствует ожидаемое ребро в остаточном графе: {parent[s]} -> {s}")
                 # Можно выбрать стратегию: прервать или пропустить обновление
                 path_flow = 0 # Установить поток в 0, чтобы не менять max_flow
                 break
            path_flow = min(path_flow, residual_graph[parent[s]][s])
            s = parent[s]
        
        if path_flow == 0: # Если произошла ошибка на этапе поиска path_flow
             break # Прерываем основной цикл

        max_flow += path_flow

        v = sink
        while v != source:
            u = parent[v]
            if u == -1: # Должно быть обработано ранее, но для страховки
                 break
            # Проверяем наличие ребер перед обновлением
            if u in residual_graph and v in residual_graph[u]:
                 residual_graph[u][v] -= path_flow
            # Убедимся что v есть в residual_graph перед доступом к residual_graph[v]
            if v not in residual_graph:
                residual_graph[v] = {}
            # Увеличиваем пропускную способность обратного ребра
            residual_graph[v][u] = residual_graph[v].get(u, 0) + path_flow

            v = parent[v]

    return max_flow

# --- Пример использования ---
if __name__ == "__main__":
    graph_capacities = {
        's': {'a': 10, 'b': 10},
        'a': {'c': 4, 'd': 8},
        'b': {'a': 2, 'd': 9},
        'c': {'t': 10},
        'd': {'c': 6, 't': 10},
        't': {}
    }

    source_node = 's'
    sink_node = 't'

    max_flow_value = edmonds_karp(graph_capacities, source_node, sink_node)
    print(f"Максимальный поток из '{source_node}' в '{sink_node}': {max_flow_value}")