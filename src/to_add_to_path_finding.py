from heapq import heappop, heappush
from typing import List, Tuple


""" Modified Dijkstra """
class PathFinding:

    @staticmethod
    def _is_too_similar(
        path1: List[str],
        path2: List[str],
        threshold: float = 0.7
    ) -> bool:
        set1 = set(path1)
        set2 = set(path2)

        common = len(set1 & set2)
        similarity = common / max(len(set1), 1)

        return similarity > threshold

    @staticmethod
    def k_shortest_paths(
        graph: Graph,
        start: str,
        end: str,
        k: int
    ) -> List[Tuple[List[str], int]]:

        heap: List[Tuple[int, str, List[str]]] = [(0, start, [])]
        results: List[Tuple[List[str], int]] = []

        while heap:
            cost, node, path = heappop(heap)

            path = path + [node]

            # stop cycles
            if len(path) != len(set(path)):
                continue

            # goal reached
            if node == end:

                # reject similar paths
                is_similar = any(
                    PathFinding._is_too_similar(path, existing_path)
                    for existing_path, _ in results
                )

                if not is_similar:
                    results.append((path, cost))

                if len(results) == k:
                    return results

                continue

            # explore neighbors
            for neighbor, move_cost, metadata in graph.neighbors(node):
                if graph.is_blocked(neighbor):
                    continue

                if neighbor in path:  # prevent loops
                    continue

                new_cost = cost + move_cost
                heappush(heap, (new_cost, neighbor, path))

        return results
