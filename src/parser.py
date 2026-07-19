#!/usr/bin/env python3
from errors import MapError
from map_data import Map
from validation import Validation
import re


class Parser:

    # FIXME: Can I have this uppercase variables?
    DRONE_PAT = re.compile(r"^nb_drones:\s*(\d+)$")
    # Matches: <type>: <name> <x> <y> [metadata]
    # Captures: type, name, x, y, and optional metadata string
    ZONE_PAT = re.compile(
        r"^(hub|start_hub|end_hub):\s*"  # type
        r"([^\s\[\-]+)\s+"               # name
        r"(-?\d+)\s+"                    # x
        r"(-?\d+)"                       # y
        r"(?:\s*\[(.*)\])?$"             # optional metadata
    )
    # Matches: connection: <name>-<name> [metadata]
    # Captures: node_a, node_b, and optional metadata string
    CONN_PAT = re.compile(
            r"^connection:\s*([^\s\[\-]+)-([^\s\[\-]+)(?:\s*\[(.*)\])?$"
            )
    # Matches: key=value
    META_PAT = re.compile(r"([^\s=]+)=([^\s=]+)")

    def __init__(self, filename: str) -> None:

        self.filename: str = filename
        self.lines: list[tuple[int, str]] = []

    def _clean_map(self) -> list[tuple[int, str]]:

        try:
            with open(self.filename, "r") as file:
                lines = file.readlines()
        except (
                FileNotFoundError,
                PermissionError,
                IsADirectoryError
        ) as e:
            raise MapError(f"[invalid map file] Couldn't read map file:\n{e}")

        clear_map = []
        for line_num, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            clear_map.append((line_num, line))

        return clear_map

    def _parse_drones(self) -> int:

        n, first_line = self.lines[0]
        match = self.DRONE_PAT.match(first_line)

        if not match:
            raise MapError(f"[line {n}] undefined number of drones")

        nb_drones = int(match.group(1))
        if nb_drones <= 0:
            raise MapError(
                    f"[line {n}] 'nb_drones' must be a positive number."
            )

        return nb_drones

    def _parse_zone(self,
                    line: str,
                    n: int) -> tuple[str, dict[str, object]]:

        match = self.ZONE_PAT.match(line)
        if not match:
            raise MapError(
                    f"[line {n}]: Invalid zone syntax"
                    "Expected '<hub_type>: <name> <x> <y> [metadata]'"
            )

        hub_type, name, x_str, y_str, md_str = match.groups()
        metadata = self._parse_metadata(md_str)
        return name, {
            "type": hub_type,
            "x": int(x_str),
            "y": int(y_str),
            "metadata": metadata,
            "line": n
        }

    def _parse_connection(self, line: str, n: int) -> tuple[
            str,
            str,
            dict[str, str],
            int
            ]:

        match = self.CONN_PAT.match(line)
        if not match:
            raise MapError(
                    f"[line {n}] Invalid connection syntax"
                    "Expected 'connection: <A>-<B> [metadata]'"
                    )

        a, b, md_str = match.groups()
        metadata = self._parse_metadata(md_str)
        return a, b, metadata, n

    def _parse_metadata(self, md_str: str) -> dict[str, str]:

        metadata = {}

        if not md_str:
            return metadata

        tokens = md_str.strip().split()

        for token in tokens:
            match = self.META_PAT.match(token)
            if not match:
                raise MapError(
                        f"Invalid metadata format: '{token}'"
                        " must be in 'key=value' format."
                )
            key, value = match.groups()
            metadata[key] = value

        return metadata

    def parse_map(self) -> Map:

        self.lines = self._clean_map()

        if not self.lines:
            raise MapError("[invalid map file] map is empty")

        zones: dict[str, dict[str, object]] = {}
        connections: list[tuple[str, str, dict[str, str]]] = []
        nb_drones = self._parse_drones()
        seen_connection = False

        """ parse from the second line onwards """
        for line_num, line in self.lines:

            if line.startswith(("hub:", "start_hub:", "end_hub:")):

                if seen_connection:
                    raise MapError(
                            f"[line {line_num}] Zones must "
                            "be defined before connections"
                    )
                name, zone_data = self._parse_zone(line, line_num)

                if name in zones:
                    raise MapError(f"[line {line_num}] duplicate zone name!")

                zones[name] = zone_data

            elif line.startswith("connection:"):
                seen_connection = True
                connection = self._parse_connection(line, line_num)
                a, b, _, _ = connection

                if a not in zones or b not in zones:
                    raise MapError(
                            f"[line {line_num}] connection"
                            " to unknown zone!")
                connections.append(connection)

            elif not line.startswith((
                "nb_drones:",
                "hub:",
                "start_hub:",
                "end_hub:",
                "connection:"
            )):
                raise MapError(f"[line {line_num}] unknown syntax")

        if not connections:
            raise MapError(
                    "[invalid map file] map must have connections"
            )

        map_info = Map(nb_drones, zones, connections)
        valid = Validation()
        valid.validate(map_info)

        return map_info


if __name__ == "__main__":

    import sys
    from pprint import pprint

    argc: int = len(sys.argv)
    if argc == 2:
        try:
            parser = Parser(sys.argv[1])
            map_info = parser.parse_map()
            print("Success parsing map!\n")
            print("=== MAP CONTENT ===")
            print("\n".join(
                f"{name}: {info['type']} at ({info['x']}, {info['y']}) "
                f"[{info['metadata'].get('color', 'none')}]"
                for name, info in map_info.zones.items()
                )
            )
            print("\n\nThe actual strcture:\nZones:\n")
            pprint(map_info.zones)
            print("\nConnections:\n")
            pprint(map_info.connections)
            # print(f"Number of drones: {map_info.nb_drones}")
            # print(f"Zones: {map_info.zones}")
            # print(f"Connections: {map_info.connections}")
        except MapError as e:
            print(e)
    elif argc < 2:
        print("If you don't give me a file name, I can't open it...")

    else:
        print("Too many files! One at a time please...")
