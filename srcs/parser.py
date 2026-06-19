#!/usr/bin/env python3
from errors import MapError


class Parser():

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.lines = []
        self.nb_drones = None
        self.zones = {}
        self.connections = []

    def _clean_map(self) -> list[str]:
        try:
            with open() self.filename as file:
                lines = file.readlines()
        except (FileNotFoundError, PermissionError) as e:
            raise MapError(f"Couldn't read map '{self.filename}': {e}")
        
        clear_map = []
        # should be in a try/except? Bc lines won't exist if there was an error 
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            clear_map.append(line)
        return clear_map
    
    def parse_drones(self): 
        #  The first line defines the number of drones using nb_drones: <number>.
        # do I even need this? 
    
    def parse_zone(self):
    # Zone definition on each line using type prefixes:
        # start_hub: <name> <x> <y> [metadata] marks the starting zone.
        # end_hub: <name> <x> <y> [metadata] marks the end zone.
        # hub: <name> <x> <y> [metadata] defines a regular zone.
        # The connection syntax forbids dashes in zone names (see below).
        # Zone types:
            #  normal – Standard zone with 1 turn movement cost (default)
            #  blocked – Inaccessible zone. Drones must not enter or pass 
            #    through this zone. Any path using it is invalid.
            #  restricted – A sensitive or dangerous zone. Movement to this 
            #    zone costs 2 turns.
            #  priority – A preferred zone. Movement to this zone costs 1 turn 
            #    but should be prioritized in pathfinding.
    
    
    def parse_connection(self):
    # Connections are defined using connection: <name1>-<name2> [metadata]:
        #  Define a bidirectional connection (edge) between two zones.
        #  The connection syntax forbids dashes in zone names.
        #  Optional metadata can be specified in brackets [...]:
        #  max_link_capacity=<number> (default: 1) - Maximum drones that
        #    can traverse this connection simultaneously
    
    def parse_metadata(self):
    # All metadata is optional and enclosed in brackets [...] with default values:
        #  zone=<type> (default: normal)
        #  color=<value> (default: none)
        #  max_drones=<number> (default: 1) - Maximum drones that can
        #  occupy this one simultaneously
        #  Tags inside brackets can appear in any order.
    
    # TODO: add return type
    def parse_map(self):
        self.lines = parse_lines()


if __name__ == "__main__":
    ...
