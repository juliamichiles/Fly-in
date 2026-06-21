#!/usr/bin/env python3
from errors import MapError
from typing import Optional, Dict
#FIXME: be consistent with returning a value or assigning directly inside method
# as in, return nb_drones vs. self.nb_drones = nb_drones (inside method)


class Parser():

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.lines = []
        self.nb_drones = None
        self.zones = {}
        self.connections = []

    def _clean_map(self) -> list[str]:
        try:
            with open(self.filename, "r") as file:
                lines = file.readlines()
        except (FileNotFoundError, PermissionError) as e:
            raise MapError(f"Couldn't read map '{self.filename}': {e}")
        
        clear_map = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            clear_map.append(line)
        return clear_map
    
    def _parse_drones(self): 
        first_line = self.lines[0]
        
        if not first_line.startswith("nb_drones:"):
            raise MapError(
                    "First line must define the number of"
                    " drones using 'nb_drones: <positive_integer>'."
            )
        try:
            nb_drones = int(first_line.split(":", 1)[1].strip())
            if nb_drones <= 0:
                raise MapError("'nb_drones' must be a positive integer.")
        except ValueError:
            raise MapError("'nb_drones' must be a positive integer.")

        return nb_drones
    
    def _parse_zone(self, line: str) -> tuple[str, int, int, Optional]:
        
        hub_type, body = line.split(":", 1)
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
        if name in self.zones:
            raise MapError("Found duplicate zone name: '{name}'")
        
        metadata = {}
        if md_str:
            metadata = _parse_metadata(md_str)
        
        return hub_type, name, x, y, metadata

    
    def _parse_connection(self):
    # Connections are defined using connection: <name1>-<name2> [metadata]:
        #  Define a bidirectional connection (edge) between two zones.
        #  The connection syntax forbids dashes in zone names.
        #  Optional metadata can be specified in brackets [...]:
        #  max_link_capacity=<number> (default: 1) - Maximum drones that
        #    can traverse this connection simultaneously
    
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
                # Should I really raise an error here?
        
        return metadata

    def parse_map(self):
        self.lines = self._clean_map()

        if not self.lines:
            raise MapError("Map file is empty.")
        try:
            self.nb_drones = self._parse_drones()
        except MapError:
            raise MapError()
            # Also strange, why would I raise the same error again?
        
        """ parse from the second line onwards """
        for line in self.lines[1::]:
            if line.startswith(("hub:", "start_hub:", "end_hub:")):
                zone = self._parse_zone(line) # will return a tuple
                self.zones.update(zone)
            elif line.startswith()


if __name__ == "__main__":
    ...
