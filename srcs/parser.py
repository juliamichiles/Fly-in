#!/usr/bin/env python3
from errors import MapError
from typing import Optional, Dict
#FIXME: be consistent with returning a value or assigning directly inside method
# as in, return nb_drones vs. self.nb_drones = nb_drones (inside method)
# crate a Map object and store all that info there, not in Parser?

# " parsing error must stop the program and return a clear error 
# message indicating the line and cause."
# FIXME: turn self.lines into a list of tuples where each line is paired to its
# original number from the map file (considering empty lines/comments) so we can # print error messages with line number


class Parser():

    def __init__(self, filename: str) -> None:
        
        #TODO: add typehints
        self.filename = filename
        self.lines = []
        self.nb_drones = None
        self.zones = {}
        self.connections: list[tuple] = []

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
        else:
            parts = body.split()
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
            raise MapError(f"Found duplicate zone name: '{name}'")
        
        metadata = {}
        if md_str:
            metadata = self._parse_metadata(md_str)
        
        return name, {
            "type": hub_type,
            "x": x,
            "y": y,
            "metadata": metadata
        }

    
    def _parse_connection(self, connect_str: str) -> tuple:
        
        metadata = {}
        
        prexif, body = connect_str.split(":", 1)
        if '[' in body:
            clear_body, md_str = body.split('[', 1)
        if clear_body:
            body = clear_body
        if '-' not in body:
            raise MapError(
                    "Invalid connection: "
                    " 'connect_str', must contain '-'"
                    )
        connection = body.split('-')
        
        if md_str:
            metadata = _parse_metadata(md_str)

        return connection, metadata
    
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
        # Should add a try/except here?
        for line in self.lines[1::]:
            if line.startswith(("hub:", "start_hub:", "end_hub:")):
                name, zone_data = self._parse_zone(line)
                self.zones[name] = zone_data
            elif line.startswith("connection:"):
                connection = self._parse_connection(line)
                self.connections.append(connection)


if __name__ == "__main__":
    ...
