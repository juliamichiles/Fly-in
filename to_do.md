# Next:
- DOCSTRINGS
- Remove unnecessary comments
- README
- [ ] fix Makefile
- [ ] Ensure all subject requirements are matched now
- [ ] A bunch of tests
- [ ] Write a testing script that reads terminal simulation
- [ ] NOTES:
        - [X] mapf
        - [ ] parser

# IMPORTANT QUESTIONS:
- How makefile runs main.py with/without a map?
- Can I really have subdirectories? Or all my files must be loose in the root 
- Should I have python 3.10^ in my requirements?

# Fixed:
- [X] GUI was counting an extra turn
- [X] possibly has even more errors... see browser's chat
- [X] simulation_log() possibly has issues (not printing connection name right)
- [X] Fix visualization: zone names are unreadable for large maps
- [X] Ensure terminal simulation is being printed correctly
- [X] run test_parser! Its passing a few invalid maps
- [X] Move all files to the root of the repo
- [X] After everything is trully working, linters!!

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
- [X] Move some validation logic from Parser to Validate
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
- [X] Notes on assign dones
- [X] Implement simulation + notes on it 
- [X] More notes on actual workflow of assign_drones and simulation
- [ ] More tests, with a bunch of different maps
- [ ] Print more stages of the simulation - for testing purposes
- [X] Notes on simulation and ReservationTable
- [X] Modify the rest of the code to match new mapf algorithm
- [X] Update ReservationTable to handle capacities - see chat
    (Graph already has helper methods to get zone/connection capacities)

# GUI:
- [X] Minimal vizualization - hard to read, needs fixing
- [ ] Some of it doesn't match subject requirements - fix it 
- [ ] take notes 
- [X] Create a new chat and start Visualization probably?
    (give it all files so far for context)

# Later:
- [X] Starrted visualization
- [X] Traffic simulation
- [X] Create a main file so we can just update it as the project grows
- [ ] Create test programs to verify project functionality (not submitted or
        graded). Use frameworks like pytest or unittest for unit tests, covering 
        ege cases.
- [ ] Is algorithm too naif? Maybe improve mapf algorithm

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
- [X] tui simulation
- [X] fixed a bunch of subject missmatches
- [X] new main file
- Traffic simulation
- Visualization
- Makefile

# Notes on:
- [X] "Draw" all data structures
- [ ] mapf file methods
- [ ] GUI + pygame
