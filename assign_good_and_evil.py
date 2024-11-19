import dsc40graph
from collections import deque

def assign_good_and_evil(graph):
    if not graph:
        return None
    status = {node:'undefined' for node in graph.nodes}
    for u in graph.nodes:
        if status[u] == 'undefined':
            status[u] = 'good'
            if graph.neighbors(u):
                queue = deque([u])
                while(queue):
                    current = queue.popleft()
                    for neighbor in graph.neighbors(current):
                        if status[neighbor] == 'undefined':
                            status[neighbor] = 'evil' if status[current] == 'good' else 'good'
                            queue.append(neighbor)
                        elif status[neighbor] == status[current]:
                            return None
    return status
