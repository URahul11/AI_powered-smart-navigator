import networkx as nx
from itertools import permutations

def dijkstra(G, start, end, weight='adjusted_distance'):
    try:
        path = nx.dijkstra_path(G, start, end, weight=weight)
        total_distance = nx.dijkstra_path_length(G, start, end, weight=weight)
        return path, total_distance
    except nx.NetworkXNoPath:
        return None, float('inf')

def a_star(G, start, end, heuristics, weight='adjusted_distance'):
    try:
        path = nx.astar_path(G, start, end, 
                            heuristic=lambda n, goal: heuristics.get(n, float('inf')), 
                            weight=weight)
        total_distance = nx.astar_path_length(G, start, end, 
                                             heuristic=lambda n, goal: heuristics.get(n, float('inf')), 
                                             weight=weight)
        return path, total_distance
    except nx.NetworkXNoPath:
        return None, float('inf')

def greedy_best_first(G, start, end, heuristics, weight='adjusted_distance'):
    try:
        def greedy_heuristic(n):
            return heuristics.get(n, float('inf'))
        
        path = []
        visited = set()
        current = start
        while current != end:
            if current in visited:
                return None, float('inf')
            path.append(current)
            visited.add(current)
            neighbors = list(G.neighbors(current))
            if not neighbors:
                return None, float('inf')
            current = min(neighbors, key=lambda n: greedy_heuristic(n) if n not in visited else float('inf'))
        path.append(end)
        total_distance = sum(G[path[i]][path[i+1]][weight] for i in range(len(path)-1))
        return path, total_distance
    except:
        return None, float('inf')

def tsp(G, start, end, intermediates, weight='adjusted_distance'):
    try:
        cities = [start] + intermediates + [end]
        n = len(cities)
        if n < 2:
            return None, float('inf')

        min_dist = float('inf')
        min_path = None
        for perm in permutations(intermediates):
            current_path = [start] + list(perm) + [end]
            full_path = []
            current_dist = 0
            valid = True
            for i in range(len(current_path) - 1):
                try:
                    segment_path = nx.dijkstra_path(G, current_path[i], current_path[i+1], weight=weight)
                    segment_dist = nx.dijkstra_path_length(G, current_path[i], current_path[i+1], weight=weight)
                    full_path.extend(segment_path[:-1] if i < len(current_path) - 2 else segment_path)
                    current_dist += segment_dist
                except nx.NetworkXNoPath:
                    valid = False
                    break
            if valid and current_dist < min_dist:
                min_dist = current_dist
                min_path = full_path

        return min_path, min_dist
    except:
        return None, float('inf')

# Test all algorithms
if __name__ == "__main__":
    from graph import load_graph
    from ml_model import TrafficPredictor
    predictor = TrafficPredictor('data/traffic_data.csv')
    G, heuristics = load_graph('data/cities_graph.json', predictor, hour=8, day_of_week=1)
    start, end = 'A', 'E'
    intermediates = ['B', 'C']
    
    # Test Dijkstra
    path, distance = dijkstra(G, start, end, weight='adjusted_distance')
    print(f"Dijkstra: Path = {path}, Distance = {distance}")
    
    # Test A*
    path, distance = a_star(G, start, end, heuristics, weight='adjusted_distance')
    print(f"A*: Path = {path}, Distance = {distance}")
    
    # Test Greedy
    path, distance = greedy_best_first(G, start, end, heuristics, weight='adjusted_distance')
    print(f"Greedy: Path = {path}, Distance = {distance}")
    
    # Test TSP
    path, distance = tsp(G, start, end, intermediates, weight='adjusted_distance')
    print(f"TSP (visit {intermediates}): Path = {path}, Distance = {distance}")