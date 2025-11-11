# graph_2 = [[0, 1, 0, 1, 0], [], [], [], []]

# также, графы могут быть представлены в виде матрицы вида (0 1 0 1 0), (0 0 1 0 0), где 0 - не можем пойти в данный узел, 1 - можем, - однонаправленный цикличный граф

from collections import deque
import time
import threading
from functools import wraps

def measure_time(func):
    # Используем threading.local для потокобезопасности
    local_data = threading.local()

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Инициализируем флаг измерения для текущего потока
        if not hasattr(local_data, 'is_measuring'):
            local_data.is_measuring = False

        # Если уже измеряем время (рекурсивный вызов) - просто выполняем функцию
        if local_data.is_measuring:
            return func(*args, **kwargs)

        # Первый вызов - начинаем измерение
        local_data.is_measuring = True
        start_time = time.perf_counter()

        try:
            result = func(*args, **kwargs)
            execution_time = time.perf_counter() - start_time
            print(f"Функция {func.__name__} выполнена за {execution_time:.6f} секунд")
            return result
        finally:
            # Сбрасываем флаг независимо от того, было ли исключение
            local_data.is_measuring = False

    return wrapper


class Graph:
    def __init__(self):
        self.vertices = {
        "a": ["b", "d"],
        "b": ["c"],
        "c": ["f", "a"],
        "d": ["f"],
        "f": []
        }

    @measure_time
    def breadth_first_search(self, start_verticy, end_verticy):
        queue = deque([start_verticy])
        parent = {start_verticy: None}

        while queue:
            verticy = queue.popleft()

            for neighbor in self.vertices[verticy]:
                if neighbor not in parent:
                    parent[neighbor] = verticy

                    if neighbor == end_verticy:
                        print(f"мы нашли {end_verticy}")

                        path = []
                        step = neighbor

                        while step is not None:
                            print(step)
                            path.append(step)
                            step = parent[step]

                        path.reverse()
                        return path

                    queue.append(neighbor)

        return None

our_graph = Graph()
print(our_graph.breadth_first_search('a', 'f'))


@measure_time
def dfs_shortest_path(graph, start, goal):
    """
    Находит кратчайший путь от start до goal с помощью DFS (полный перебор).
    Работает, но неэффективен по сравнению с BFS.

    :param graph: dict, список смежности
    :param start: начальная вершина
    :param goal:  конечная вершина
    :return: список — кратчайший путь, или None, если недостижим
    """

    def dfs_recursive(current, goal, visited, path, all_paths):
        if current == goal:
            all_paths.append(list(path))  # сохраняем копию пути
            return

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs_recursive(neighbor, goal, visited, path, all_paths)
                path.pop()  # backtracking
                visited.remove(neighbor)

    if start == goal:
        return [start]

    all_paths = []
    visited = {start}
    dfs_recursive(start, goal, visited, [start], all_paths)

    if not all_paths:
        return None

    # Находим путь минимальной длины
    shortest = min(all_paths, key=len)
    return shortest


our_graph = Graph
dfs_shortest_path(our_graph.vertices, "a", "f")


import heapq
from ctypes.macholib.dyld import dyld_image_suffix_search


def dijkstra(_graph, start):
    distances = {node: float('inf') for node in _graph}
    distances[start] = 0

    pq = [(0, start)] # расстояние до вершины и сама вершина
    while pq:
        current_dist, u = heapq.heappop(pq)

        if current_dist > distances[u]:
            continue

        for v, weight in _graph.get(u, []):
            new_dist = current_dist + weight

            if new_dist < distances[v]:
                distances[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return distances


def dijkstra_v1(_graph, start, end):
    distances = {node: float('inf') for node in _graph}
    parent = {node: None for node in graph}
    distances[start] = 0

    pq = [(0, start)]

    while pq:
        current_dist, u = heapq.heappop(pq)

        if u == end:
            path = []
            while u is not None:
                path.append(u)
                u = parent[u]
            return path[::-1], distances[end]

        if current_dist > distances[u]:
            continue

        for v, weight in _graph.get(start, []):
            new_dist = current_dist + weight

            if new_dist < distances[v]:
                distances[v] = new_dist
                parent[v] = u
                heapq.heappush(pq, (new_dist, v))
    return distances


def bellow_ford_all(graph, start, vertices):
    dist = {v: float('info') for v in vertices}
    parent = {v: None for v in vertices}
    dist[start] = 0

    for _ in range(len(vertices) - 1):
        updated = False
        for u, v, w in graph:
            if dist[u] == float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = updated = True
        if not updated:
                break

        for  u, v, w in graph:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                print('отрицательный цикл')
                return None, None




def adj_to_adges(adj_graph):
    edges = []
    for u in adj_graph[u]:
        edges.append((u, v, m))
    return edges

graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 1), ('D', 5)],
    'C': [('D', 8), ('E', 10)],
    'D': [('E', 2)],
    'E': [],
}

print(adj_to_adges(graph))
print()
print(dijkstra(graph, 'A'))
print(dijkstra_v1(graph, 'A', 'E'))
print()
print(bellow_ford_all(adj_to_adges(graph), 'A', graph.keys()))

# сечение вероятности для шахмат



