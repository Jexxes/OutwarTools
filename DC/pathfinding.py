from collections import defaultdict
from collections import deque

def create_graph(rooms):
    graph = defaultdict(list)
    for room in rooms:
        room_id = room['Id']
        if room['North'] != 0: graph[room_id].append(room['North'])
        if room['South'] != 0: graph[room_id].append(room['South'])
        if room['East'] != 0: graph[room_id].append(room['East'])
        if room['West'] != 0: graph[room_id].append(room['West'])
    return graph

def bfs(graph, start, end, teleportable_rooms):
    queue = deque([[start]])
    visited = set([start])

    # Add all teleportable rooms to the queue
    for room in teleportable_rooms:
        if room != start:  # Avoid adding the start room again
            queue.append([start, room])
            visited.add(room)

    while queue:
        path = queue.popleft()
        current = path[-1]
        if current == end:
            return path
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    return None





#test = bfs(graph, 4, 4417)
#print(test)


