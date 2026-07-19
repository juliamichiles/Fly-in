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
        
        if "-" in node:
            return True

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

    @staticmethod
    def path_finding(
            graph: Graph,
            reservations: ReservationTable,
            start: str,
            end: str,
            start_time: int = 0
            ) -> tuple[list[str] | None, int | float]:

        # list of (path_weight, time_cost, current_node, path_history)
        to_explore = [(0.0, start_time, start, [])]
        # tracks both node and time
        visited: set[tuple[str, int]] = set()
        time_limit = 1000

        while to_explore:
            weight, time, node, path = heappop(to_explore)

            if time > time_limit:
                break
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
                heappush(
                        to_explore, 
                        (weight + 1.0, time + 1, node, current_path)
                )
                
            for neighbor, move_cost, _ in graph.neighbors(node):
                if graph.is_blocked(neighbor):
                    continue

                time_elapsed = 2 if move_cost == 2 else 1
                if time_elapsed == 1:
                    if reservations.is_edge_free(node, neighbor, time) and \
                            reservations.is_node_free(neighbor, time + 1):
                        # adds move_cost to weight, but exactly 1 to time
                        heappush(to_explore, (
                            weight + move_cost,
                            time + 1, 
                            neighbor,
                            current_path
                        ))
                elif time_elapsed == 2:
                    free_0 = reservations.is_edge_free(node, neighbor, time)
                    free_1 = reservations.is_edge_free(node, neighbor, time + 1)
                    free_2 = reservations.is_node_free(neighbor, time + 2)
                    if free_0 and free_1 and free_2:
                        conn_name = (
                                f"{min(node, neighbor)}-"
                                f"{max(node, neighbor)}"
                        )
                        dummy_path = current_path + [conn_name]
                        # adds move_cost (2) to weight, and exactly 2 to time
                        heappush(to_explore, (
                            weight + move_cost,
                            time + 2,
                            neighbor,
                            dummy_path
                        ))

        return None, float("inf")


class Scheduler:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.reservations = ReservationTable(graph)

    def schedule(self, 
                 nb_drones: int,
                 start: str,
                 end: str
        ) -> list[Drone]:
        
        drones = []
        
        for i in range(1, nb_drones + 1):
            path, cost = PathFinding.path_finding(
                    self.graph, self.reservations, start, end, start_time=0
                    )
            if not path:
                print(f"Warning: No path found for Drone {i} (Deadlock)")
                # should I really print this? Or stop execution?
                continue
            for time_tick, location in enumerate(path):
                if "-" in location:
                    u, v = location.split("-")
                    self.reservations.reserve_edge(u, v, time_tick - 1, i)
                    self.reservations.reserve_edge(u, v, time_tick, i)
                else:
                    self.reservations.reserve_node(location, time_tick, i)
                    # Reserve normal 1-turn transitions
                    if time_tick > 0:
                        prev_location = path[time_tick - 1]
                        if "-" not in prev_location:
                            self.reservations.reserve_edge(
                                    prev_location, 
                                    location, 
                                    time_tick - 1, 
                                    i
                            )
                                
            drone = Drone(i, path)
            drone.history = path
            drones.append(drone)

        return drones

    @staticmethod
    def simulation_log(drones: list[Drone], end_hub: str) -> None:
        if not drones:
            return

        total_turns = max(len(d.history) for d in drones)

        for t in range(1, total_turns):
            turn_moves = []
            for d in drones:
                
                if t >= len(d.history):
                    continue
                
                prev_loc = d.history[t - 1]
                curr_loc = d.history[t]
                
                if prev_loc == end_hub:
                    continue
                if curr_loc != prev_loc:
                    turn_moves.append(f"D{d.id}-{curr_loc}")
            if turn_moves:
                print(" ".join(turn_moves))


if __name__ == "__main__":
    ...
