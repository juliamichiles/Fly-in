_This project has been created as part of the 42 curriculum by juliatav._

# Fly-in

## Description

This project's goal is to design a routing system that efficiently routes a fleet of drones from a starting base to a target location while minimizing the total number of simulation turns. The system must strictly respect zone and connection capacity constraints, movement rules, and avoid deadlocks to ensure a valid and efficient simulation.

Drawing from concepts in **multi-agent path-finding (MAPF)** and **traffic simulation and management**, the project coordinates multiple autonomous agents moving through a shared network with limited resources. It combines graph algorithms, path planning, and turn-based scheduling to maximize throughput while maintaining safe and collision-free drone movement.

---

## Algorithm

The simulation uses a **Prioritized Planning** architecture combined with a **Space-Time Dijkstra-inspired** search algorithm to resolve routing constraints for multiple drones simultaneously.

Agents are planned sequentially (from Drone 1 to Drone N). Once a drone successfully computes a path, every occupied node and traversed connection is recorded in a global **Reservation Table** indexed by simulation time. Subsequent drones treat these reserved space-time coordinates as dynamic obstacles, forcing them to either reroute or strategically wait for previously planned drones to clear bottlenecks, narrow passages, and capacity-limited zones.

Unlike traditional shortest-path algorithms that search only across graph vertices, the search state is represented as **(node, time)** tuples, allowing the planner to reason about both space and time simultaneously.

To prevent infinite searches on highly constrained maps, the algorithm enforces a hard limit of **1,000 simulation ticks**. If no conflict-free solution can be found within this horizon, a `PathError` is raised, cleanly detecting unschedulable scenarios without risking infinite execution.

### Planning Workflow

Each drone is planned sequentially using a shared **Reservation Table**. Once a valid path is found, every occupied node and traversed connection is reserved at the corresponding simulation time. These reservations become dynamic obstacles for all subsequently planned drones.

```text
                    +----------------------+
                    |   Drone i (1..N)     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Space-Time Dijkstra  |
                    | Search (node, time)  |
                    +----------+-----------+
                               |
                     Path found?| 
                     +-----+----+
                     |          |
                   Yes         No
                     |          |
                     v          v
        +------------------+   PathError
        | Reserve Nodes &  |
        | Reserve Edges    |
        | in Time Table    |
        +---------+--------+
                  |
                  v
        +------------------+
        | Next Drone (i+1) |
        +---------+--------+
                  |
                  v
          Repeat until all
        drones are scheduled
```

---

## Visualization

The project includes an interactive visualizer built with **Pygame** that displays the simulation in real time. It provides a clear representation of drone movements, occupied zones, and overall traffic flow throughout the network.

Current features include:

- **Automatic map scaling** based on the user's display resolution.
- **Automatic node label shortening** when space is limited.
- **Color-coded zones** using metadata from the input map.
- **Real-time drone movement animation** synchronized with the simulation.

### Example map

```text
Easy Level 2: Simple fork with two paths

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
```

### Expected terminal output

```text
D1-junction D2-junction
D1-path_a D2-path_b D3-junction D4-junction
D1-goal D2-goal D3-path_a D4-path_b
D3-goal D4-goal

--- Performance Statistics ---
Average turns per drone: 3.50
Average drones moved per turn: 3.00
```

### Expected visualization

> *Placeholder: insert a screenshot of the visualizer running the example map.*

---

## Instructions

The project includes a `Makefile` that automates the most common development tasks.

### Create and activate a virtual environment

```bash
make venv
source .venv/bin/activate
```

### Install dependencies

```bash
make install
```

### Run the project

Run using the default map:

```bash
make run
```

Run using a specific map:

```bash
make run ARGS=<path-to-map-file>
```

### Debug

```bash
make debug
```

### Linting

```bash
make lint
make lint-strict
```

### Cleanup

```bash
make clean
```

Remove the virtual environment as well:

```bash
make fclean
```

---

## Resources

### Multi-Agent Path Finding (MAPF)

- https://www.youtube.com/watch?v=EFg3u_E6eHU

### Graph Algorithms

- https://brandonkindred.medium.com/mastering-pathfinding-the-essentials-of-dijkstra-and-a-algorithms-691b226e71c4
- https://medium.com/@singhatul1155/dijkstras-algorithm-navigating-the-shortest-path-how-to-use-it-and-its-importance-8924295fe690

### Python Regular Expressions

- https://realpython.com/ref/stdlib/re/

### Pygame

- https://www.pygame.org/docs/
- https://www.youtube.com/watch?v=blLLtdv4tvo&t=559s

---

## AI Usage

AI tools were used as development assistants throughout the project. Their contributions included:

- generating additional valid and invalid test maps;
- explaining algorithms and Python language features;
- helping debug edge cases;
- polishing and reviewing documentation for clarity and grammar;
- assisting in the development of helper scripts for testing.

All architectural decisions, algorithm design, implementation, and final validation were completed manually. Every AI-generated suggestion was reviewed, understood, and adapted before being incorporated into the project.
