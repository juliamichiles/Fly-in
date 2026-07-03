#!/usr/bin/env python3
from heapq import heappop, heappush
from typing import Optional
from graph import Graph


class PathFinding:

    # more stuff? An init? variables? Otherwise move this to graph

    @staticmethod
    def dijkstra(
        graph: Graph,
        start: str,
        end: str
        ) -> tuple[Optional[list[str]], float]: 
        to_explore: list[tuple[int, str, list[str]]] = [(0, start, [])]
        distances: dict[str, int] = {start: 0}

        while to_explore:
            cost, node, path = heappop(to_explore)

            # Ignore outdated paths
            if cost > distances.get(node, float("inf")):
                continue

            path = path + [node]

            if node == end:
                return path, cost

            # loop through each neighbor
            for neighbor, move_cost, metadata in graph.neighbors(node):
                if graph.is_blocked(neighbor):
                    continue

                new_cost: int = cost + move_cost

                if new_cost < distances.get(neighbor, float("inf")):
                    distances[neighbor] = new_cost
                    heappush(to_explore, (new_cost, neighbor, path))

        return None, float("inf")


if __name__ == "__main__":

    import sys
    from pprint import pprint
    from parser import Parser
    from errors import MapError

    argc: int = len(sys.argv)
    if argc == 2:
        try:
            parser = Parser(sys.argv[1])
            map_info = parser.parse_map()
            print("Success parsing map!\n")
            print("=== MAP CONTENT ===")
            print("\n".join(
                f"{name}: {info['type']} at ({info['x']}, {info['y']}) "
                f"[{info['metadata'].get('color', 'none')}]"
                for name, info in map_info.zones.items()
                )
            )
            # print("\n\nThe actual strcture:\nZones:\n")
            # pprint(map_info.zones)
            # print("\nConnections:\n")
            # pprint(map_info.connections)
            # print(f"Number of drones: {map_info.nb_drones}")
            # print(f"Zones: {map_info.zones}")
            # print(f"Connections: {map_info.connections}")
            print("Generating graph...")
            graph = Graph(map_info.zones, map_info.connections)
            print("[WARNING] nb_drones will be ignored for now")
            start = graph.get_start()
            end = graph.get_end()
            pprint(f"Found shortest path: {PathFinding.dijkstra(graph, start, end)}")
        except MapError as e:
            print(e)
    elif argc < 2:
        print("If you don't give me a file name, I can't open it...")

    else:
        print("Too many files! One at a time please...")

