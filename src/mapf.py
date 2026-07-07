#!/usr/bin/env python3
from graph import Graph


class Drone:
    def __init__(self, drone_id: int, path: list[str]) -> None:
         self.id = drone_id 
         self.path = path
         self.position_index = -1


class ReservationTable:
    def __init__(self) -> None:
        self.node_reservations: dict[tuple[str, int], list[int]] = {}
        self.edge_reservations: dict[tuple[str, str, int], list[int]] = {}

    def reserve_node(self, node: str, time: int, drone_id: int) -> None:
        self.node_reservations[(node, time)] = drone_id

    def is_node_free(self, node: str, time: int) -> bool:
        return (node, time) not in self.node_reservations
    
    def reserve_edge(
            self, 
            a: str, 
            b: str, 
            time: int, 
            drone_id: int
            ) -> None:
        self. edge_reservations[(a, b, time)] = drone_id

    def is_edge_free(self, a: str, b: str, time: int) -> bool:
        return (a, b, time) not in self.edge_reservations
    
    # should also add methods to handle capacities here?

class Scheduler:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.reservations = ReservationTable()

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
