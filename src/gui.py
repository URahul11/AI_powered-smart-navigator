import streamlit as st
from graph import load_graph
from algorithms import dijkstra, a_star, greedy_best_first, tsp
from ml_model import TrafficPredictor
from visualization import visualize_graph

def main():
    st.title("AI Smart Navigator")
    
    # Load traffic predictor
    predictor = TrafficPredictor('data/traffic_data.csv')
    
    # Sidebar inputs
    st.sidebar.header("Route Parameters")
    hour = st.sidebar.slider("Hour (0-23)", 0, 23, 8)
    day_of_week = st.sidebar.selectbox("Day of Week", 
                                       options=[1, 2, 3, 4, 5], 
                                       format_func=lambda x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][x-1])
    start = st.sidebar.selectbox("Start City", options=['A', 'B', 'C', 'D', 'E'])
    end = st.sidebar.selectbox("End City", options=['A', 'B', 'C', 'D', 'E'])
    algo = st.sidebar.selectbox("Algorithm", options=['dijkstra', 'a_star', 'greedy', 'tsp'])
    
    intermediates = []
    if algo == 'tsp':
        intermediates_input = st.sidebar.text_input("Intermediate Cities (comma-separated, e.g., B,C)", "")
        if intermediates_input:
            intermediates = [city.strip() for city in intermediates_input.split(',')]
    
    # Load graph
    G, heuristics = load_graph('data/cities_graph.json', predictor, hour, day_of_week)
    
    # Run algorithm
    if st.sidebar.button("Find Route"):
        if algo == 'dijkstra':
            path, distance = dijkstra(G, start, end)
        elif algo == 'a_star':
            path, distance = a_star(G, start, end, heuristics)
        elif algo == 'greedy':
            path, distance = greedy_best_first(G, start, end, heuristics)
        elif algo == 'tsp':
            path, distance = tsp(G, start, end, intermediates)
        
        # Display results
        if path:
            st.write(f"**Path**: {path}")
            st.write(f"**Total Distance (adjusted for traffic)**: {distance:.2f} km")
            visualize_graph(G, path, title=f"{algo.capitalize()} Path with Traffic")
        else:
            st.write(f"No path from {start} to {end}")

if __name__ == "__main__":
    main()