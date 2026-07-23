#!/usr/bin/env python3
import sys
from parser import Parser
from errors import MapError, PathError, VisualizationError
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

        if not start or not end:
            # this won't ever be prited since map wa already validated
            # it's only here bc of mypy
            raise MapError("Missing start or end hub")
        scheduler = Scheduler(graph)
        drones = scheduler.schedule(map_info.nb_drones, start, end)
        scheduler.simulation_log(drones, end)
        scheduler.print_statistics(drones, end)

        from gui import Visualizer

        viz = Visualizer(graph, drones)
        viz.run()

    except MapError as e:
        print(f"Map error: {e}")
    except PathError as e:
        print(f"PathError: {e}")
    except VisualizationError as e:
        print("[WARNING] GUI Visualizer currently unavaliable.")
        print(f"VisualizationError: {e}")


if __name__ == "__main__":
    main()
