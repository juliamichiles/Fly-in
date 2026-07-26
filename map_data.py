#!/usr/bin/env python3
from typing import List, Dict, Tuple


class Map:
    def __init__(
        self,
        nb_drones: int,
        zones: Dict[str, Dict[str, object]],
        connections: List[Tuple[str, str, Dict[str, str], int]]
    ) -> None:
        self.nb_drones = nb_drones
        self.zones = zones
        self.connections = connections


if __name__ == "__main__":
    ...
