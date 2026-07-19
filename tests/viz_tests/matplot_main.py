#!/usr/bin/env python3
import matplotlib
from viz_matplotlib import visualize
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ---- MINIMAL GRAPH MOCK ----
class Graph:
    def __init__(self):
        self.zones = {
            "start": {
                "position": (0, 0),
                "metadata": {"zone": "start_hub"},
            },
            "A": {
                "position": (2, 1),
                "metadata": {"zone": "normal"},
            },
            "B": {
                "position": (4, 0),
                "metadata": {"zone": "restricted"},
            },
            "C": {
                "position": (2, -2),
                "metadata": {"zone": "waiting"},
            },
            "goal": {
                "position": (6, 0),
                "metadata": {"zone": "end_hub"},
            },
        }

        self.connections = [
            ("start", "A"),
            ("A", "B"),
            ("A", "C"),
            ("B", "goal"),
            ("C", "goal"),
        ]


# ---- MINIMAL DRONE MOCK ----
class Drone:
    def __init__(self, history):
        self.history = history


def main():
    graph = Graph()

    drones = [
        Drone(["start", "A", "B", "goal"]),
        Drone(["start", "A", "C", "goal"]),
        Drone(["start", "A", "B", "goal"]),
    ]

    visualize(graph, drones)


if __name__ == "__main__":
    main()
