_This project has been created as part of the 42 curriculum by juliatav_

## Description: 
---
- SUBJECT: section that clearly presents the project, including its goal and a brief overview.

This project's goal is to design a routting system able to navigate a fleet of drones efficiently from a given starting base to a target location in the fewest possible simulation turns while respecting a series of contraints and avoiding deadlocks.


## Algorithm:
---
- SUBJECT: A detailed description of your algorithm choices and implementation strategy must also be included.

The simulation uses a Prioritized Planning architecture combined with a Space-Time Dijkstra inspired search algorithm to resolve complex routing constraints for multiple drones simultaneously. 
In this strategy, agents are scheduled sequentially (from Drone 1 to N). As each drone successfully plots its path, its occupied nodes and edges are registered into a shared global Reservation Table across specific time ticks (t). Subsequent drones treat these reserved space-time coordinates as dynamic obstacles, forcing them to route around or wait for prior agents to clear bottlenecks, narrow gates, and capacity-limited zones.

Unlike standard spatial pathfinding, the state space encompasses both topological graph nodes and time indices, denoted as tuples of (node, time).

To handle heavily restricted topological layouts—such as single-file entry gates and convergence traps—the search implements a hard time-step cutoff ($1,000$ ticks). If a valid conflict-free sequence cannot be found due to saturation, a PathError is raised, cleanly identifying deadlocks without risking infinite execution loops.

## Visualization:
---
- SUBJECT: Documentation of the visual representation features and how they enhance the user
experience.

The Visualizer built with Pygame transforms multi-agent drone paths into an interactive, real-time graphical simulation. Key features include:
 - Dynamic Map Scaling & Auto-Fit: Automatically measures map bounding coordinates  and compares them against current desktop display resolutions. If a map exceeds screen dimensions, it automatically scales down the pixel 'cell_size'  and abbreviates zone labels to prevent window clipping.

- SUBJECT: Example input and expected output demonstrating the program’s functionality
# TODO: make this prettier:
Easy Level 2: Simple fork with two paths
example map:
nb_drones: 4

start_hub: start 0 0 [color=green]
hub: junction 1 0 [color=yellow max_drones=2]
hub: path_a 2 1 [color=blue]
hub: path_b 2 -1 [color=blue]
end_hub: goal 3 0 [color=red max_drones=3]

connection: start-junction [max_link_capacity=2]
connection: junction-path_a
connection: junction-path_b
connection: path_a-goal
connection: path_b-goal

Expected terminal output:
D1-junction D2-junction
D1-path_a D2-path_b D3-junction D4-junction
D1-goal D2-goal D3-path_a D4-path_b
D3-goal D4-goal

--- Performance Statistics ---
Average turns per drone: 3.50
Average drones moved per turn: 3.00

Expected visualization:
#TODO: ADD SCREENSHOT OF THIS MAP

## Instructions:
---
- SUBJECT: section containing any relevant information about compilation,
installation, and/or execution.
*To create/activate virtual environment:*
'make venv'
'source .venv/bin/activate'

*To install depencencies:*
'make install'

*To run (with default map):*
'make run'
*or (with specified map):*
'make run ARGS=<path to map file>'

*to debug:*
'make debug'

*to run linters:*
'make lint'
'make lint-strict'

*to cleanup:*
'make clean'
*or (to remove .venv):*
'make fclean'

## Resources:
---
- SUBJECT: section listing classic references related to the topic (documentation, articles, tutorials, etc.), as well as a description of how AI was used —
specifying for which tasks and which parts of the project.

https://brandonkindred.medium.com/mastering-pathfinding-the-essentials-of-dijkstra-and-a-algorithms-691b226e71c4

https://medium.com/@singhatul1155/dijkstras-algorithm-navigating-the-shortest-path-how-to-use-it-and-its-importance-8924295fe690

## Mini Glossary:
- 'Zones': places
- 'Connections': paths
- 'Graph': the map
- 'Drones': moving agents
- 'Turns': time steps
- 'Goal': move all drones in the fewest turns possible
