#!/usr/bin/env python3
from map_data import Map
# TODO: add typehints

class Graph:

    def __init__(self) -> None:
        pass
    
    @staticmethod
    def _get_cost(zone) -> int:
        # cost depends on the destination node, not the connection.
        zone_type = zone["metadata"].get("zone", "normal")

        if zone_type == "blocked":
            return None
        elif zone_type == "restricted":
            return 2
        else:
            return 1  # bc priority and normal have the same cost

    def build_graph(self, zones, connections) -> dict[str, list[tuple]]:
        # turns map into a graph 
        graph = {name: [] for name in zones}

        for hub_a, hub_b, metadata, _ in connections:
            cost_to_b = _get_cost(zones[hub_b])
            cost_to_a = _get_cost(zones[hub_a])

            if cost_to_b is not None:
                graph[hub_a].append((hub_b, cost_to_b, metadata))

            if cost_to_a is not None:
                graph[hub_b].append((hub_a, cost_to_a, metadata))
        
        return graph


if __name__ == "__main__":
    ...
