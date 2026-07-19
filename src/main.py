#!/usr/bin/env python3
import sys
from parser import Parser
from errors import MapError, VizualizationError
from graph import Graph
from mapf import Scheduler


def main() -> None:

    if len(sys.argv) < 2:
        print("Usage: ./main.py <map_file> [k_paths]")
        return

    filename = sys.argv[1]

    try:
        parser = Parser(filename)
        map_info = parser.parse_map()

        graph = Graph(map_info.zones, map_info.connections)
        start = graph.get_start()
        end = graph.get_end()

        scheduler = Scheduler(graph)
        drones = scheduler.schedule(map_info.nb_drones, start, end)
        scheduler.simulation_log(drones, end)

        from gui import Vizualizer

        viz = Vizualizer(graph, drones)
        viz.run()

    except MapError as e:
        print(f"Map error: {e}")

    except VizualizationError as e:
        print("[WARNING] GUI Vizualizer currently unavaliable.")
        print(f"VizualizationError: {e}")


if __name__ == "__main__":
    main()
