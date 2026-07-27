#!/usr/bin/env python3
from graph import Graph
from heapq import heappop, heappush
from errors import PathError
from typing import Set, List, Dict, Tuple


class Drone:
    """Represent an individual drone agent within the simulation
            environment.
    """
    def __init__(self, drone_id: int, path: List[str]) -> None:
        """Initialize a Drone instance.

        Args:
            drone_id: Unique integer identifier for the drone.
            path: Sequence of zone or connection names representing the
                scheduled route.
        """
        self.id = drone_id
        self.path = path
        self.position_index = -1
        self.history: List[str] = []


class ReservationTable:
    """Space-time reservation table to prevent node and edge collisions
            between agents.
    """
    def __init__(self, graph: Graph) -> None:
        """Initialize the ReservationTable instance with map graph references.

        Args:
            graph: The Graph instance containing zone and connection
                capacities.
        """
        self.node_reservations: Dict[Tuple[str, int], List[int]] = {}
        self.edge_reservations: Dict[Tuple[str, str, int], List[int]] = {}
        self.graph = graph

    def reserve_node(self, node: str, time: int, drone_id: int) -> None:
        """Reserve a zone node for a specific drone at a given time tick.

        Args:
            node: Name of the zone node to reserve.
            time: Time tick index.
            drone_id: Identifier of the drone making the reservation.

        Returns:
            None
        """
        self.node_reservations.setdefault((node, time), []).append(drone_id)

    def is_node_free(self, node: str, time: int) -> bool:
        """Check whether a zone node has available capacity at a specific time
            tick.

        Args:
            node: Zone node name to inspect.
            time: Time tick index.

        Returns:
            True if remaining node capacity permits another drone, False zone
                otherwise.
        """
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
        """Reserve a connection edge between two nodes at a specific time tick.

        Args:
            a: First node connected by the edge link.
            b: Second node connected by the edge link.
            time: Time tick index.
            drone_id: Identifier of the drone making the edge reservation.

        Returns:
            None
        """
        key = self._edge_key(a, b, time)
        self.edge_reservations.setdefault(key, []).append(drone_id)

    def is_edge_free(self, a: str, b: str, time: int) -> bool:
        """Check whether an edge connection has available capacity at a given
            time tick.

        Args:
            a: First node connected by the edge.
            b: Second node connected by the edge.
            time: Time tick index.

        Returns:
            True if edge capacity permits traversal, False otherwise.
        """
        capacity = self.graph.connection_capacity(a, b)
        key = self._edge_key(a, b, time)
        current = self.edge_reservations.get(key, [])
        return len(current) < capacity

    def _edge_key(self, a: str, b: str, time: int) -> Tuple[str, str, int]:
        """Construct an undirected canonical key for edge lookup in reservation
            dictionaries.

        Args:
            a: First node name.
            b: Second node name.
            time: Time tick index.

        Returns:
            A tuple of sorted node names and time index: (min_node, max_node,
                time).
        """
        return (min(a, b), max(a, b), time)


class PathFinding:
    """Container class for space-time search algorithms."""

    @staticmethod
    def path_finding(
            graph: Graph,
            reservations: ReservationTable,
            start: str,
            end: str,
            start_time: int = 0
            ) -> Tuple[List[str] | None, int | float]:
        """Find a conflict-free path from start to end in space-time using
                priority search.

        Args:
            graph: Graph instance representing grid topology.
            reservations: ReservationTable tracking existing drone
                reservations.
            start: Name of the starting hub node.
            end: Name of the destination end hub node.
            start_time: Initial time tick index to begin search from. Defaults
                to 0.

        Returns:
            A tuple containing:
                - List of visited locations (nodes/transit links) if found,
                    else None.
                - Final time tick integer if path exists, otherwise
                    float("inf").
        """
        # List of (path_weight, time_cost, current_node, path_history)
        to_explore: List[Tuple[
            float,
            int,
            str,
            List[str]
            ]] = [(0.0, start_time, start, [])]

        # tracks both node and time
        visited: Set[Tuple[str, int]] = set()
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
                    free_1 = reservations.is_edge_free(
                            node,
                            neighbor,
                            time + 1
                            )
                    free_2 = reservations.is_node_free(neighbor, time + 2)
                    if free_0 and free_1 and free_2:
                        conn_name = graph.get_connection_name(node, neighbor)
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
    """Orchestrate priority-based path scheduling for multiple drone agents."""

    def __init__(self, graph: Graph) -> None:
        """Initialize the Scheduler instance.

        Args:
            graph: Graph representation of the simulation map.
        """
        self.graph = graph
        self.reservations = ReservationTable(graph)

    def schedule(
            self,
            nb_drones: int,
            start: str,
            end: str
    ) -> List[Drone]:
        """Sequentially plan conflict-free paths for all drones from start to
                end hub.

        Args:
            nb_drones: Total number of drone agents to schedule.
            start: Starting hub name.
            end: Target end hub name.

        Returns:
            A list of scheduled Drone instances populated with path histories.

        Raises:
            PathError: If pathfinding fails to find a valid route for any drone
                (deadlock).
        """
        drones = []

        for i in range(1, nb_drones + 1):
            path, cost = PathFinding.path_finding(
                    self.graph, self.reservations, start, end, start_time=0
                    )
            if not path:
                raise PathError(f"No path found for Drone {i} (Deadlock)")
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
    def simulation_log(drones: List[Drone], end_hub: str) -> None:
        """Print step-by-step turn execution logs to stdout.

        Args:
            drones: List of scheduled Drone instances.
            end_hub: Name of the destination hub node.

        Returns:
            None
        """
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

    @staticmethod
    def print_statistics(drones: List[Drone], end_hub: str) -> None:
        """Calculate and output simulation performance metrics to standard
                output.

        Args:
            drones: List of scheduled Drone instances.
            end_hub: Target end hub node name.

        Returns:
            None
        """
        if not drones:
            return

        print("\n--- Performance Statistics ---")
        total_sim_turns = max(len(d.history) for d in drones) - 1
        if total_sim_turns <= 0:
            return

        total_drone_turns = sum(len(d.history) - 1 for d in drones)
        avg_turns = total_drone_turns / len(drones)
        print(f"Average turns per drone: {avg_turns:.2f}")

        total_moves = 0
        for d in drones:
            for t in range(1, len(d.history)):
                if d.history[t] != d.history[t - 1] \
                        and d.history[t - 1] != end_hub:
                    total_moves += 1

        avg_moves_per_turn = total_moves / total_sim_turns
        print(f"Average drones moved per turn: {avg_moves_per_turn:.2f}")


if __name__ == "__main__":
    ...
