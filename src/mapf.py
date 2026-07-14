#!/usr/bin/env python3
from graph import Graph
from heapq import heappop, heappush
import graph


class Drone:
    def __init__(self, drone_id: int, path: list[str]) -> None:
        self.id = drone_id 
        self.path = path
        self.position_index = -1
        self.history: list[str | None] = []

class ReservationTable:
    def __init__(self, graph: Graph) -> None:
        self.node_reservations: dict[tuple[str, int], list[int]] = {}
        self.edge_reservations: dict[tuple[str, str, int], list[int]] = {}
        self.graph = graph

    def reserve_node(self, node: str, time: int, drone_id: int) -> None:
        self.node_reservations.setdefault((node, time), []).append(drone_id)

    def is_node_free(self, node: str, time: int) -> bool:
        capacity = self.graph.zone_capacity(node)
        current = self.node_reservations.get((node, time), [])
        return len(current) < capacity
    
    def reserve_edge(
            self, 
            a: str, 
            b: str, 
            time: int, 
            drone_id: int
            ) -> None:
        key = self._edge_key(a, b, time)
        self.edge_reservations.setdefault(key, []).append(drone_id)
    
    def is_edge_free(self, a: str, b: str, time: int) -> bool:
        capacity = self.graph.connection_capacity(a, b)
        key = self._edge_key(a, b, time)
        current = self.edge_reservations.get(key, [])
        return len(current) < capacity
    
    def _edge_key(self, a: str, b: str, time: int) -> tuple[str, str, int]:
        return (min(a, b), max(a, b), time)


class PathFinding:
    # TODO: Merge scheduler into this class??

    @staticmethod
    def cooperative_dijkstra(
            graph: Graph,
            reservations: ReservationTable,
            start: str,
            end: str,
            start_time: int = 0
            ) -> tuple[list[str] | None, int]:
        
        # list of (path_weigt, time_cost, current_node, path_history)
        to_explore = [(0.0, start_time, start, [])]
        # tracks both node and time 
        visited: set[tuple[str, int]] = set()
        
        while to_explore:
            weight, time, node, path = heappop(to_explore)

            if (node, time) in visited:
                continue
            visited.add((node, time))
            current_path = path + [node]
            if node == end:
                return current_path, time

            # drone waits in place, if that zone has free capacity at time + 1
            if reservations.is_node_free(node, time + 1):
                # Waiting adds 1.0 to weight (so moving forward is preferred)
                # and 1 to time
                heappush(to_explore, (weight + 1.0, time + 1, node, current_path))
            for neighbor, move_cost, _ in graph.neighbors(node):
                if graph.is_blocked(neighbor):
                    continue
                
                time_elapsed = 2 if move_cost == 2 else 1 
                if time_elapsed == 1:
                    if reservations.is_edge_free(node, neighbor, time) and \
                            reservations.is_node_free(neighbor, time + 1):
                               # We add move_cost to weight, 
                               # but exactly 1 to time
                                heappush(to_explore, (
                                    weight + move_cost, 
                                    time + 1, neighbor, 
                                    current_path
                                    ))
                    elif time_elapsed == 2:
                        if reservations.is_edge_free(node, neighbor, time) and \
                                reservations.is_node_free(neighbor, time + 2):
                                    conn_name = f"{min(node, neighbor)}-"
                                                f"{max(node, neighbor)}"
                        dummy_path = current_path + [conn_name]
                        # We add move_cost (2) to weight, and exactly 2 to time
                        heappush(to_explore, (
                            weight + move_cost, 
                            time + 2, 
                            neighbor, 
                            dummy_path
                            ))

            return None, float("inf") # no path found


class Scheduler:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.reservations = ReservationTable(graph)

    def schedule(self, drones: list[Drone]) -> None:
        active = True
        time = 0

        while active:
            active = False
            
            for drone in drones:
                next_pos = drone.position_index + 1
                if next_pos >= len(drone.path):
                    continue
                active = True
                if drone.position_index >= 0:
                    current_node = drone.path[drone.position_index]
                else:
                    current_node = None
                next_node = drone.path[next_pos]

                if not self.reservations.is_node_free(next_node, time):
                    continue
                if current_node is not None:
                    if not self.reservations.is_edge_free(
                            current_node, next_node, time
                            ):
                        continue
                drone.position_index = next_pos
                self.reservations.reserve_node(next_node, time, drone.id)
                if current_node is not None:
                    self.reservations.reserve_edge(
                            current_node, next_node, time, drone.id
                            )
            for drone in drones:
                if drone.position_index >= 0:
                    drone.history.append(drone.path[drone.position_index])
                else:
                    drone.history.append(None)

            time += 1

if __name__ == "__main__":
    ...
