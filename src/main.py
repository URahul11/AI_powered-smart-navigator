from graph import load_graph
from algorithms import dijkstra, a_star, greedy_best_first, tsp
from ml_model import TrafficPredictor

def main():
    # Load traffic predictor
    predictor = TrafficPredictor('data/traffic_data.csv')
    
    # Get time inputs
    try:
        hour = int(input("Enter hour (0-23): ").strip())
        day_of_week = int(input("Enter day of week (1=Monday, ..., 5=Friday): ").strip())
    except ValueError:
        print("Invalid hour or day. Using default traffic.")
        hour, day_of_week = None, None
    
    # Load graph with traffic adjustments
    G, heuristics = load_graph('data/cities_graph.json', predictor, hour, day_of_week)
    print("Available cities:", G.nodes())
    
    # Get user input
    start = input("Enter start city: ").strip()
    end = input("Enter end city: ").strip()
    algo = input("Choose algorithm (dijkstra, a_star, greedy, tsp): ").strip().lower()
    
    # For TSP, get intermediate cities
    intermediates = []
    if algo == 'tsp':
        intermediates_input = input("Enter intermediate cities (comma-separated, e.g., B,C): ").strip()
        if intermediates_input:
            intermediates = [city.strip() for city in intermediates_input.split(',')]
    
    # Run selected algorithm
    if algo == 'dijkstra':
        path, distance = dijkstra(G, start, end, weight='adjusted_distance')
    elif algo == 'a_star':
        path, distance = a_star(G, start, end, heuristics, weight='adjusted_distance')
    elif algo == 'greedy':
        path, distance = greedy_best_first(G, start, end, heuristics, weight='adjusted_distance')
    elif algo == 'tsp':
        path, distance = tsp(G, start, end, intermediates, weight='adjusted_distance')
    else:
        print("Invalid algorithm! Choose dijkstra, a_star, greedy, or tsp.")
        return
    
    # Display result
    if path:
        if algo == 'tsp':
            print(f"TSP path from {start} to {end} visiting {intermediates}: {path}")
        else:
            print(f"{algo.capitalize()} path from {start} to {end}: {path}")
        print(f"Total distance (adjusted for traffic): {distance} km")
    else:
        print(f"No path from {start} to {end}")

if __name__ == "__main__":
    main()