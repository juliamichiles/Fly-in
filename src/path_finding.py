#!/usr/bin/env python3
from heapq import heappop, heappush
from graph import Graph


class PathFinding:

    # more stuff? An init? variables? Otherwise move this to graph

    @staticmethod
    def dijkstra(
            graph: Graph,
            start: str,
            end: str
            ) -> tuple[list, int | float]:
        
        # (total_cost, current_node, path)
        heap = [(0, start, [])]
        visited: set[str] = set()

        while heap:
            cost, node, path = heappop(heap)
            
            if node in visited:
                continue
            visited.add(node)
            
            path = path + [node]
            
            if node == end:
                return path, cost
            
            for neighbor, move_cost, metadata in graph.neighbors(node):
                if graph.is_blocked(neighbor):
                    continue
                item = (cost + move_cost, neighbor, path)
                heappush(heap, item)

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

