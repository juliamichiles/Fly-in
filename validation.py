#!/usr/bin/env python3
from errors import MapError
from map_data import Map
from typing import Any, List, Dict, Tuple


class Validation:
    """Validate semantic correctness and constraint rules for parsed map data."""

    @staticmethod
    def _validate_zones(zones: Dict[str, Dict[str, Any]]) -> None:
        """Validate zone configuration rules, hub counts, and metadata fields.

        Args:
            zones: A dictionary mapping zone names to their parsed attribute 
                dictionaries.

        Returns:
            None

        Raises:
            MapError: If hub types are unrecognized, hub counts are invalid
                (not exactly one start_hub and one end_hub), metadata keys/values
                are invalid, or start and end hubs share identical coordinates.
        """
        end_count = 0
        start_count = 0
        valid_types = {"normal", "blocked", "restricted", "priority"}
        allowed_metadata_keys = {"zone", "max_drones", "color"}

        for _, zone in zones.items():

            zone_type = zone["type"]
            metadata = zone["metadata"]
            line = zone.get("line", "?")

            if zone_type == "start_hub":
                start_count += 1
            elif zone_type == "end_hub":
                end_count += 1
            elif zone_type != "hub":
                raise MapError(
                        f"[line {line}] Invalid hub type '{zone_type}'"
                )
            if end_count > 1 or start_count > 1:
                raise MapError(
                          f"[line {line}] Map must have exactly one end_hub"
                          " and exactly one start_hub "
                )

            if metadata:
                for key in metadata:
                    if key not in allowed_metadata_keys:
                        raise MapError(
                            f"[line {line}] Invalid metadata key '{key}' "
                            "for zone.\nAllowed keys:"
                            "'zone', 'max_drones' 'color'"
                        )
                if "zone" in metadata:
                    value = metadata["zone"]
                    if value not in valid_types:
                        raise MapError(
                                f"[line {line}] Invalid zone type '{value}'")

                if "max_drones" in metadata:
                    value = metadata["max_drones"]

                    if not value.isdigit() or int(value) <= 0:
                        raise MapError(
                                f"[line {line}] max_drones must "
                                "be a positive integer"
                        )
                if "color" in metadata:
                    value = metadata["color"]
                    if not value.isalpha():
                        raise MapError(
                                f"[line {line}] Invalid color '{value}'")
        if start_count == 0 or end_count == 0:
            raise MapError(
                    "[invalid map file] Missing end_hub or start_hub"
                    )

        start: Dict[str, Any] | None = None
        end: Dict[str, Any] | None = None

        for zone in zones.values():
            if zone["type"] == "start_hub":
                start = zone
            elif zone["type"] == "end_hub":
                end = zone
        if start and end:
            if start["x"] == end["x"] and start["y"] == end["y"]:
                line = start["line"]
                raise MapError(
                    f"[line {line}] start_hub and end_hub"
                    " must have different coordinates"
                )

    @staticmethod
    def _validate_connections(
            connections: List[Tuple[str, str, Dict[str, str], int]]
    ) -> None:
        """Validate connection metadata, edge uniqueness, and self-connection
        constraints.

        Args:
            connections: A list of tuples containing zone_a, zone_b,
                metadata dictionary, and original line number.

        Returns:
            None

        Raises:
            MapError: If duplicate connections exist, a hub connects to itself,
                unsupported metadata keys are present, or max_link_capacity is 
                invalid.
        """
        seen = set()

        for connect in connections:
            zone_a, zone_b, metadata, line = connect

            if metadata and set(metadata.keys()) != {"max_link_capacity"}:
                raise MapError(f"[line {line}] Invalid metadata")

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
                            " must be a positive integer"
                    )
                if int(value) <= 0:
                    raise MapError(
                            f"[line {line}] max_link_capacity"
                            " must be a positive integer"
                    )

    def validate(self, map_data: Map) -> None:
        """Execute all map validation routines on a given Map object.

        Args:
            map_data: The Map dataclass/object containing parsed zones and 
                connections.

        Returns:
            None

        Raises:
            MapError: If any zone or connection constraint rule is violated.
        """
        self._validate_connections(map_data.connections)
        self._validate_zones(map_data.zones)


if __name__ == "__main__":
    ...
