#!/usr/bin/env python3
from heapq import heappop, heappush
from typing import Optional
from graph import Graph


class PathFinding:

    # more stuff? An init? variables? Otherwise move this to graph
    # TODO: Actually remove this? Keep just the k_paths
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
    
    def _check_similarity(
            self,
            path_a: list[str], 
            path_b: list[str], 
            threshold: float
            ) -> bool:
        set_a = set(path_a)
        set_b = set(path_b)
        
        common = len(set_a & set_b)
        similarity = common / max(len(set_a), 1)

        return similarity > threshold

    def k_short_paths(self, graph, start, end, k):
        to_explore = [(0, start, [])]
        results: list[tuple[list[str], int]] = []
    
        while to_explore:
            cost, current, path = heappop(to_explore)
            path = path + [current]
    
            if current == end:
                is_similar = any(
                    self._check_similarity(other_path, path, 0.7)
                    for other_path, _ in results
                )
                if not is_similar:
                    results.append((path, cost))
                if len(results) == k:
                    return results
                continue
    
            for neighbor, move_cost, metadata in graph.neighbors(current):
                if graph.is_blocked(neighbor):
                    continue
                if neighbor in path:
                    continue
    
                new_cost = cost + move_cost
                heappush(to_explore, (new_cost, neighbor, path))
    
        return results
    
    @staticmethod
    def assign_drones(
            paths: list[tuple[list[str], int]],
            nb_drones: int
            ) -> list[list[list[str]]]:
        
        assigned: list[int] = [0] * len(paths)
        drone_paths: list[list[str]] = []

        for _ in range(nb_drones):
            best_index = min(
                    range(len(paths)),
                    key=lambda i: len(paths[i][0]) + assigned[i]
                    )
            assigned[best_index] += 1
            drone_paths.append(paths[best_index][0])
        return drone_paths

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
    elif argc == 3:
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
        print("Generating graph...")
        graph = Graph(map_info.zones, map_info.connections)
        print("[WARNING] nb_drones will be ignored for now")
        start = graph.get_start()
        end = graph.get_end()
        try:
            k = int(sys.argv[2])
            if k < 0:
                k = k * -1
            pprint(f"Trying to find up to {k} shortest paths...")
            p_finding = PathFinding()
            pprint(p_finding.k_short_paths(graph, start, end, k))
        except ValueError as e:
            print(f"{e}: second argument must be a numeric value")
    elif argc < 2:
        print("If you don't give me a file name, I can't open it...")

    else:
        print("Too many files! One at a time please...")

