import json
import networkx as nx
from ml_model import TrafficPredictor

def load_graph(file_path, traffic_predictor=None, hour=None, day_of_week=None):
    # Load JSON data
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes (cities)
    for node in data['nodes']:
        G.add_node(node)
    
    # Add edges with adjusted weights
    for edge in data['edges']:
        distance = edge['distance']
        # Adjust distance by traffic multiplier
        if traffic_predictor and hour is not None and day_of_week is not None:
            traffic = traffic_predictor.predict(hour, day_of_week)
            adjusted_distance = distance * traffic
        else:
            adjusted_distance = distance  # Fallback to raw distance
        G.add_edge(edge['from'], edge['to'], 
                  distance=distance,
                  adjusted_distance=adjusted_distance,
                  traffic=edge['traffic'],
                  tolls=edge['tolls'],
                  safety=edge['safety'])
    
    # Get heuristics
    heuristics = data.get('heuristics', {})
    
    return G, heuristics

# Test loading the graph
if __name__ == "__main__":
    predictor = TrafficPredictor('data/traffic_data.csv')
    G, heuristics = load_graph('data/cities_graph.json', predictor, hour=8, day_of_week=1)
    print("Nodes:", G.nodes())
    print("Edges:", G.edges(data=True))
    print("Heuristics:", heuristics)