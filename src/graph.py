#!/usr/bin/env python3
from errors import ConnectionError


class Graph:

    def __init__(self,
                 zones: dict[str, dict[str, object]],
                 connections: list[tuple[str, str, dict[str, str], int]]
                 ) -> None:
        self.zones = zones
        self.connections = connections
        self.connection_info = {
            (min(a, b), max(a, b)): metadata
            for a, b, metadata, _ in connections
        }
        self.connection_names = {}
        for a, b, _, _ in connections:
            og_name = f"{a}-{b}"
            self.connection_names[(a, b)] = og_name
            self.connection_names[(b, a)] = og_name
        self.graph = self._build_graph(connections)

    def get_connection_name(self, a: str, b: str) -> str:
        return self.connection_names.get((a, b), f"{a}-{b}")

    @staticmethod
    def _get_cost(zone: dict[str, object]) -> float | None:
        # cost depends on the destination node, not the connection.
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
            connections: list[tuple[str, str, dict[str, str], int]]
            ) -> dict[str, list[tuple[str, int, dict[str, str]]]]:

        graph = {name: [] for name in self.zones}

        for hub_a, hub_b, metadata, _ in connections:
            cost_to_b = self._get_cost(self.zones[hub_b])
            cost_to_a = self._get_cost(self.zones[hub_a])
            if cost_to_b is not None:
                graph[hub_a].append((hub_b, cost_to_b, metadata))
            if cost_to_a is not None:
                graph[hub_b].append((hub_a, cost_to_a, metadata))
        return graph

    def neighbors(self, node: str) -> list[tuple]:
        return self.graph[node]

    def is_blocked(self, node: str) -> bool:
        zone_md = self.zones[node]["metadata"].get("zone")
        return zone_md == "blocked"

    def is_restricted(self, node: str) -> bool:
        zone_md = self.zones[node]["metadata"].get("zone")
        return zone_md == "restricted"

    def is_priority(self, node: str) -> bool:
        zone_md = self.zones[node]["metadata"].get("zone")
        return zone_md == "priority"

    def zone_capacity(self, node: str) -> int | float:
        zone_type = self.zones[node].get("type")
        if zone_type in ("start_hub", "end_hub"):
            return float("inf")
        capacity = self.zones[node]["metadata"].get("max_drones", 1)
        return int(capacity)

    def connection_capacity(self, a: str, b: str) -> int:
        key = (min(a, b), max(a, b))
        try:
            metadata = self.connection_info[key]
        except KeyError:
            raise ConnectionError(f"No connection between {a} and {b}")
        return int(metadata.get("max_link_capacity", 1))

    def get_end(self) -> str | None:
        for name, zone in self.zones.items():
            if zone["type"] == "end_hub":
                return name

    def get_start(self) -> str | None:
        for name, zone in self.zones.items():
            if zone["type"] == "start_hub":
                return name


if __name__ == "__main__":
    ...
