#!/usr/bin/env python3
import sys
from parser import Parser
from errors import MapError
from graph import Graph
from mapf import Drone, Scheduler, PathFinding
from gui import Vizualizer


def print_map(map_info):
    print("\n=== MAP CONTENT ===")
    for name, info in map_info.zones.items():
        print(
            f"{name}: {info['type']} "
            f"at ({info['x']}, {info['y']}) "
            f"[{info['metadata'].get('color', 'none')}]"
        )

def main():
    if len(sys.argv) < 2:
        print("Usage: ./main.py <map_file> [k_paths]")
        return

    filename = sys.argv[1]

    try:
        print("[1] Loading and validating map...")
        parser = Parser(filename)
        map_info = parser.parse_map()

        print("Map parsed successfully")
        print_map(map_info)

        print("\n=== BUILDING GRAPH ===")
        graph = Graph(map_info.zones, map_info.connections)

        start = graph.get_start()
        end = graph.get_end()

        print(f"Start: {start}")
        print(f"End:   {end}")

        print("[2] Running Multi-Agent Scheduler...")
        pf = PathFinding()
        print("\n=== MAPF SCHEDULING ===")
        scheduler = Scheduler(graph)
        drones = scheduler.schedule(map_info.nb_drones, start, end)

        for d in drones:
            print(f"Drone {d.id} Path: {d.history}")

        print("\n=== SIMULATION ===")
        print("[3] Launching Pygame...")
        viz = Vizualizer(graph, drones)
        viz.run()

    except MapError as e:
        print(f"Map error: {e}")


if __name__ == "__main__":
    main()
