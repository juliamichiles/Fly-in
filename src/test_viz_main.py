#!/usr/bin/env python3
from parser import Parser
from graph import Graph
from path_finding import PathFinding
from mapf import Drone, Scheduler
from viz_pygame import visualize # or viz_matplotlib

def main():
    parser = Parser("../maps/hard/02_capacity_hell.txt")
    map_info = parser.parse_map()

    graph = Graph(map_info.zones, map_info.connections)

    pf = PathFinding()
    start = graph.get_start()
    end = graph.get_end()

    path, cost = pf.dijkstra(graph, start, end)

    drones = [
        Drone(i, path)
        for i in range(map_info.nb_drones)
    ]

    scheduler = Scheduler(graph)
    scheduler.schedule(drones)

    visualize(graph, drones)

if __name__ == "__main__":
    main()
