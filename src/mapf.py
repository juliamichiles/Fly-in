#!/usr/bin/env python3
from graph import Graph
import graph


class Drone:
    def __init__(self, drone_id: int, path: list[str]) -> None:
         self.id = drone_id 
         self.path = path
         self.position_index = -1


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
        self.edge_reservations.setdefault((a, b, time), []).append(drone_id)
    
    def is_edge_free(self, a: str, b: str, time: int) -> bool:
        capacity = self.graph.connection_capacity(a, b)
        current = self.edge_reservations.get((a, b, time), [])
        return len(current) < capacity
    
    # should also add methods to handle capacities here?

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
                            next_node, current_node, time
                            ):
                        continue
                drone.position_index = next_pos
                self.reservations.reserve_node(next_node, time, drone.id)
                if current_node is not None:
                    self.reservations.reserve_edge(
                            current_node, next_node, time, drone.id
                            )
            time += 1

if __name__ == "__main__":
    ...
