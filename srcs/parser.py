#!/usr/bin/env python3
from errors import MapError
from typing import Optional, Dict
from map_data import Map

class Parser:

    def __init__(self, filename: str) -> None:

        # TODO: add typehints
        self.filename = filename
        self.lines = []
   
    def _clean_map(self) -> list[str]:
   
        try:
            with open(self.filename, "r") as file:
                lines = file.readlines()
        except (FileNotFoundError, PermissionError) as e:
            raise MapError(f"Couldn't read map '{self.filename}': {e}")

        clear_map = []
        line_num = -1  # haven't decided if the 1st line is 1 or 0
        for line in lines:
            line_num += 1
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            clear_map.append((line_num, line))
        return clear_map

    def _parse_drones(self):
        line_num, first_line = self.lines[0]

        if not first_line.startswith("nb_drones:"):
            raise MapError(
                    f"[line {line_num}] must define the number of"
                    " drones using 'nb_drones: <positive_integer>'."
            )
        try:
            nb_drones = int(first_line.split(":", 1)[1].strip())
            if nb_drones <= 0:
                raise MapError("'nb_drones' must be a positive integer.")
        except ValueError:
            raise MapError("'nb_drones' must be a positive integer.")

        return nb_drones

    def _parse_zone(self, line: str) -> tuple[str, dict]:
        md_str = None
        hub_type, body = line.split(":", 1)
        body = body.strip()
        hub_type = hub_type.strip()
        clear_body = body
        if '[' in body:
            clear_body, md_str = body.split('[', 1)
        parts = clear_body.split()
        if len(parts) < 3:
            raise MapError(
                    f"'{hub_type}' zone missing "
                    " required name or coordinates."
            )
        try:
            name = parts[0]
            x = int(parts[1])
            y = int(parts[2])
        except ValueError:
            raise MapError("Invalid coordinates: must be a numeric value.")

        # Not sure I want to check this here or in a validate method
        if '-' in name:
            raise MapError("Zone names cannot contain dashes.")

        metadata = {}
        if md_str:
            metadata = self._parse_metadata(md_str)

        return name, {
            "type": hub_type,
            "x": x,
            "y": y,
            "metadata": metadata
        }

    def _parse_connection(
            self, 
            connect_str: str
    ) -> tuple[str, str, Dict[str, str]]:
   
        md_str = None
        metadata: Dict[str, str] = {}

        _, body = connect_str.split(":", 1)
        body = body.strip()
        connection_part = body

        if '[' in body:
            connection_part, md_str = body.split('[', 1)

        connection_part = connection_part.strip()

        if '-' not in connection_part:
            raise MapError("Invalid connection: must contain '-'")

        parts = connection_part.split('-')
        if len(parts) != 2:
            raise MapError("Invalid connection: must be in format 'A-B'")

        a, b = parts[0].strip(), parts[1].strip()

        if md_str:
            metadata = self._parse_metadata(md_str)

        return a, b, metadata
    
    def _parse_metadata(self, md_str: str) -> Dict[str, str]:

        metadata: Dict[str, str] = {}

        if not md_str:
            return metadata

        content = md_str.strip("[]")
        tokens = content.split()
        for token in tokens:
            if "=" in token:
                key, value = token.split("=", 1)
                metadata[key.strip()] = value.strip()
            else:
                raise MapError("Invalid metadata format.")

        return metadata

    def parse_map(self) -> Map:
        
        self.lines = self._clean_map()

        if not self.lines:
            raise MapError("Map file is empty.")
        
        zones = {}
        connections = []
        nb_drones = self._parse_drones()
    
        """ parse from the second line onwards """
        for line_num, line in self.lines[1::]:
            if line.startswith(("hub:", "start_hub:", "end_hub:")):
                name, zone_data = self._parse_zone(line)
                zones[name] = zone_data
            elif line.startswith("connection:"):
                connection = self._parse_connection(line)
                connections.append(connection)
       
        map_info = Map(nb_drones, zones, connections)
        return map_info


if __name__ == "__main__":
    ...
