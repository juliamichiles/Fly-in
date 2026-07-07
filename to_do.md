# Next:
- [ ] Update ReservationTable to handle capacities - see chat
    (Graph already has helper methods to get zone/connection capacities)

# Parser:
- Parses map file in a data structure and partially validates it so far
- [X] fixed most issues I hope...
- [X] missing parse_connections
- [X] parse_map is not storing data in the dict properly
- [x] implement the rest of parse_map
- [X] Reestructure Parser:
    - [X] Create Map object and store map data there instead of in Parser 
    - [X] Modify Parser so that it returns a Map object
- [X] Run more tests with the invalid and valid maps
- [ ] Should I actually print 'MapError' on my error messages?
- Might need fixing:
    - [X] Check for dashes AND SPACES on zone names! 
    - [X] Check for repeated names while parsing? Bc the dict might simply 
        replace an old key if I try to add one with a repeated name?
    - [X] Ensure zones are listed before connections - I think I've fixed it (?)
    - [X] Check for closing brackets in parse_metadata
- [X] re-write the entire thing to look pretty? 

# Validation:
- [X] Create a separate Validate module to further validate Map object
- [ ] Move some validation logic from Parser to Validate
     (keep in parser only what is necessary for it to work)
- [X] implement validate_connections
- [X] finish validate_zones
- [X] call validate inside parse_map
- [X] test everything
- [ ] more tests with even more invalid maps
- [ ] doesn't handle multiple brackets well
- FIXME:
    - [X] printing line twice for some errors
    - [ ] not printing line for duplicte zone name and invalid zone name 
    - [ ] prints the wrong error message:
        - [ ] multiple brackets maps -> connection to unknown zone 
        - [ ] empty file -> missing nb_drones

# Graph:
- [X] Created graph - tested

# Pathfinding
- [X] Implemented Dijkstra
- [X] Apparently working - see chat for minor fixes
- [X] More tests
- [X] Implement multiple "shortest paths"
- [ ] Notes on assign dones
- [ ] Implement simulation + notes on it 
- [ ] Ver chat

# Later:
- [ ] Visualization
- [ ] Traffic simulation
- [ ] Create a main file so we can just update it as the project grows

# General
- [ ] think about project structure:
    - What should be a package with init?
    - How to organize directories?
- [X] choose algorithm(s)
- [X] decide graph's structure
- [X] stardef multi-agent path finding
- [ ] DOCSTRINGS!!!
- [ ] Mypy + flake8
- [ ] README
- [ ] Re-name files, Reestructure them and maybe redistribute classes
- Traffic simulation
- Visualization
- Makefile

# Notes on:
- [ ] "Draw" all data structures
- [ ] mapf file methods
