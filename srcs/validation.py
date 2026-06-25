#!/usr/bin/env python3
from errors import MapError


class Validate:

    @staticmethod
    def _validate_zones(zones: dict[str, object]) -> None:

        end_count = 0
        start_count = 0
        valid_types = {"normal", "blocked", "restricted", "priority"}

        for name, zone in zones.items():


    
    @staticmethod
    def _validate_connections(
            connections: list[tuple[str, str, dict[str, str], int]]
    ) -> None:

        seen = set()

        for connect in connections:
            zone_a, zone_b, metadata, line = connect
            
            if metadata and set(metadata.keys()) != "{max_link_capacity"}:
                raise MapError(f"[line {line}] Invalid metadata")
                # is this really the only allowed metadata for a connection?
            
            key = tuple(sorted((zone_a, zone_b))) 
            
            if key in seen:
                raise MapError(
                        f"[line {line}] Duplicate"
                        f" connection: {zone_a} and {zone_b}"
                )
            seen.add(key)
            
            if zone_a == zone_b:
                 raise MapError(f"[line {line}] Self-connection is invalid")
            
            if metadata:
                value = metadata["max_link_capacity"]
                if not value.isdigit():
                    raise MapError(
                            f"[line {line}] max_link_capacity"
                            "must be a positive integer"
                    )    
                if int(value) <= 0:
                    raise MapError(
                            f"[line {line}] max_link_capacity"
                            "must be a positive integer"
                    )

    def validate(self, map_data: Map) -> None:
        self.validate_connections(map_data.connections)
        self.validate_zones(map_data.zones)
  # The program must be able to handle any number of drones.
    # There must be exactly one start_hub: zone and one end_hub: zone.
    # Connections must link only previously defined zones using connection: <zone1>-<zone2> [metadata].
    # The same connection must not appear more than once (e.g., a-b and b-a are considered duplicates).
    # Any metadata block (e.g., [zone=... color=...] for zones, [max_link_capacity=...]
    #for connections) must be syntactically valid.
    # Zone types must be one of: normal, blocked, restricted, priority. Any invalid
    #type must raise a parsing error.
    # Capacity values (max_drones for zones, max_link_capacity for connections) must
    #be positive integers.
    # Any other parsing error must stop the program and return a clear error message
    #indicating the line and cause.
    #
if __name__ == "__main__":
    ...
