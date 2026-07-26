#!/usr/bin/env python3
from errors import ConnectionError
from typing import Any, List, Dict, Tuple


class Graph:
    """Represent the simulation map as a weighted, capacity-constrained graph."""

    def __init__(self,
                 zones: Dict[str, Dict[str, Any]],
                 connections: List[Tuple[str, str, Dict[str, str], int]]
                 ) -> None:
        """Initialize the Graph instance.

        Args:
            zones: Mapping of zone names to their attributes and metadata.
            connections: List of tuples defining connection edges between hubs.
        """
        self.zones: Dict[str, Dict[str, Any]] = zones
        self.connections = connections
        self.connection_info = {
            (min(a, b), max(a, b)): metadata
            for a, b, metadata, _ in connections
        }
        self.connection_names: Dict[Tuple[str, str], str] = {}

        for a, b, _, _ in connections:
            og_name = f"{a}-{b}"
            self.connection_names[(a, b)] = og_name
            self.connection_names[(b, a)] = og_name

        self.graph: Dict[str, List[Tuple[
            str,
            float,
            Dict[str, str]
            ]]] = self._build_graph(connections)

    def get_connection_name(self, a: str, b: str) -> str:
        """Retrieve the canonical formatted connection name string between two
        hubs.

        Args:
            a: Name of the first zone.
            b: Name of the second zone.

        Returns:
            The raw connection string formatted as defined in the source file.
        """ 
        return self.connection_names.get((a, b), f"{a}-{b}")

    @staticmethod
    def _get_cost(zone: Dict[str, Any]) -> float | None:
        """Calculate movement weight/cost based on the destination zone type.

        Args:
            zone: Attribute dictionary of the destination zone.

        Returns:
            The numerical travel cost multiplier (2.0 for restricted, 0.9 for
            priority, 1.0 for normal), or None if the zone is blocked.
        """
        zone_type = zone["metadata"].get("zone", "normal")

        if zone_type == "blocked":
            return None
        elif zone_type == "restricted":
            return 2.0
        elif zone_type == "priority":
            return 0.9
        else:
            return 1.0

    def _build_graph(
            self,
            connections: List[Tuple[str, str, Dict[str, str], int]]
            ) -> Dict[str, List[Tuple[str, float, Dict[str, str]]]]:
        """Construct the internal adjacency list graph representation.

        Args:
            connections: List of connection tuple definitions from the map 
                parser.

        Returns:
            An adjacency dictionary mapping hub names to lists of neighbor
            tuples (neighbor_name, move_cost, metadata).
        """
        graph: Dict[str, List[Tuple[
            str,
            float,
            Dict[str, str]
            ]]] = {name: [] for name in self.zones}

        for hub_a, hub_b, metadata, _ in connections:
            cost_to_b = self._get_cost(self.zones[hub_b])
            cost_to_a = self._get_cost(self.zones[hub_a])
            if cost_to_b is not None:
                graph[hub_a].append((hub_b, cost_to_b, metadata))
            if cost_to_a is not None:
                graph[hub_b].append((hub_a, cost_to_a, metadata))
        return graph

    def neighbors(self, node: str) -> List[Tuple[
                str,
                float,
                Dict[str, str]
            ]]:
        """Retrieve all accessible neighboring hubs for a given node.

        Args:
            node: The zone name to query.

        Returns:
            A list of neighbor tuples (neighbor_name, move_cost, metadata).
        """
        return self.graph[node]

    def is_blocked(self, node: str) -> bool:
        """Check whether a zone is marked as blocked.

        Args:
            node: Zone name to check.

        Returns:
            True if zone metadata indicates 'blocked', False otherwise.
        """
        zone_md = self.zones[node]["metadata"].get("zone")
        return bool(zone_md == "blocked")

    def is_restricted(self, node: str) -> bool:
        """Check whether a zone is marked as restricted.

        Args:
            node: Zone name to check.

        Returns:
            True if zone metadata indicates 'restricted', False otherwise.
        """
        zone_md = self.zones[node]["metadata"].get("zone")
        return bool(zone_md == "restricted")

    def is_priority(self, node: str) -> bool:
        """Check whether a zone is marked as priority.

        Args:
            node: Zone name to check.

        Returns:
            True if zone metadata indicates 'priority', False otherwise.
        """
        zone_md = self.zones[node]["metadata"].get("zone")
        return bool(zone_md == "priority")

    def zone_capacity(self, node: str) -> int | float:
        """Determine maximum drone occupancy for a given zone.

        Args:
            node: Zone name to query.

        Returns:
            Infinity (`float("inf")`) for start/end hubs, or the integer
            `max_drones` capacity (defaults to 1).
        """
        zone_type = self.zones[node].get("type")
        if zone_type in ("start_hub", "end_hub"):
            return float("inf")
        capacity = self.zones[node]["metadata"].get("max_drones", 1)
        return int(capacity)

    def connection_capacity(self, a: str, b: str) -> int:
        """Retrieve link capacity between two connected hubs.

        Args:
            a: Name of first hub.
            b: Name of second hub.

        Returns:
            Integer max link capacity (defaults to 1 if unspecified).

        Raises:
            ConnectionError: If no edge exists between nodes a and b.
        """
        key = (min(a, b), max(a, b))
        try:
            metadata = self.connection_info[key]
        except KeyError:
            raise ConnectionError(f"No connection between {a} and {b}")
        return int(metadata.get("max_link_capacity", 1))

    def get_end(self) -> str | None:
        """Locate and return the end hub zone name.

        Returns:
            Name string of the end_hub, or None if missing.
        """
        for name, zone in self.zones.items():
            if zone["type"] == "end_hub":
                return name
        return None

    def get_start(self) -> str | None:
        """Locate and return the start hub zone name.

        Returns:
            Name string of the start_hub, or None if missing.
        """
        for name, zone in self.zones.items():
            if zone["type"] == "start_hub":
                return name
        return None


if __name__ == "__main__":
    ...
