#!/usr/bin/env python3
import sys
from parser import Parser
from errors import MapError
from graph import Graph
from path_finding import PathFinding
from mapf import Drone, Scheduler
from gui import Vizualizer


def print_map(map_info):
    print("\n=== MAP CONTENT ===")
    for name, info in map_info.zones.items():
        print(
            f"{name}: {info['type']} "
            f"at ({info['x']}, {info['y']}) "
            f"[{info['metadata'].get('color', 'none')}]"
        )


def simulate(graph, paths, nb_drones):
    print("\n=== ASSIGNING DRONES ===")
    pf = PathFinding()
    drone_paths = pf.assign_drones(paths, nb_drones)

    drones = [
        Drone(i, path)
        for i, path in enumerate(drone_paths)
    ]

    for d in drones:
        print(f"Drone {d.id}: {d.path}")

    print("\n=== SIMULATION ===")
    scheduler = Scheduler(graph)
    scheduler.schedule(drones)
    viz = Vizualizer(graph, drones)
    viz.run()

    for d in drones:
        print(f"Drone {d.id} final position index: {d.position_index}")


def main():
    if len(sys.argv) < 2:
        print("Usage: ./main.py <map_file> [k_paths]")
        return

    filename = sys.argv[1]

    try:
        parser = Parser(filename)
        map_info = parser.parse_map()

        print("✔ Map parsed successfully")
        print_map(map_info)

        print("\n=== BUILDING GRAPH ===")
        graph = Graph(map_info.zones, map_info.connections)

        start = graph.get_start()
        end = graph.get_end()

        print(f"Start: {start}")
        print(f"End:   {end}")

        pf = PathFinding()

        # ---- Single shortest path ----
        if len(sys.argv) == 2:
            path, cost = pf.dijkstra(graph, start, end)

            if path is None:
                print("No path found.")
                return

            print("\n=== SHORTEST PATH ===")
            print(f"Path: {path}")
            print(f"Cost: {cost}")

            simulate(graph, [(path, cost)], map_info.nb_drones)

        # ---- K shortest paths ----
        else:
            try:
                k = abs(int(sys.argv[2]))
            except ValueError:
                print("Second argument must be a number")
                return

            print(f"\n=== FINDING {k} PATHS ===")
            paths = pf.k_short_paths(graph, start, end, k)

            if not paths:
                print("No paths found.")
                return

            for i, (p, c) in enumerate(paths):
                print(f"{i+1}. Path: {p} | Cost: {c}")

            simulate(graph, paths, map_info.nb_drones)

    except MapError as e:
        print(f"Map error: {e}")


if __name__ == "__main__":
    main()
