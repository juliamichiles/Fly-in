#!/usr/bin/env python3
from erros import MapError
# unsure how to organize this... 
# one big validate function with encolosed helpers?
# one validate class with methods?
# c-style individual functions and a main that calls the other ones? 



class Parser():
# suggested structure:

    def __init__(self, filename: str) -> None:
       self.filename = filename

    def parse_lines(self):
        try:
            with open self.filename as map:
                lines = map.readlines()
        except (FileNotFoundError, PermissionError) as e:
            raise MapError(f"Couldn't read map '{filename}': {e}")
        
        
        #  The first line defines the number of drones using nb_drones: <number>.
        # Comments start with ’#’ and are ignored.
        # Empty lines should be ignored
        # How abt lines containing only wtspc chars?
    
    def parse_drones(self):
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


if __name__ == "__main__":
    ...
