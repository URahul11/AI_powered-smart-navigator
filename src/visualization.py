import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

# Set interactive backend
matplotlib.use('TkAgg')  # Use Tkinter backend for Windows

def visualize_graph(G, path=None, title="City Graph"):
    # Create figure
    plt.figure(figsize=(8, 6))
    
    # Define positions for nodes (simple layout)
    pos = nx.spring_layout(G)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    
    # Draw all edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1)
    
    # Highlight path if provided
    if path:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=12)
    
    # Draw edge labels (adjusted distances)
    edge_labels = {(u, v): f"{d['adjusted_distance']:.1f}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    
    plt.title(title)
    plt.axis('off')
    plt.show()  # Should now display

# Test visualization
if __name__ == "__main__":
    from graph import load_graph
    from ml_model import TrafficPredictor
    predictor = TrafficPredictor('data/traffic_data.csv')
    G, _ = load_graph('data/cities_graph.json', predictor, hour=8, day_of_week=1)
    visualize_graph(G, path=['A', 'B', 'C', 'D', 'E'], title="TSP Path with Traffic")