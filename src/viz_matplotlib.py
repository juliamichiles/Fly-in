#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ---- COLOR MAPPING ----
ZONE_COLORS = {
    "start_hub": "#00ff9f",
    "end_hub": "#00ff9f",
    "restricted": "#ff3b3b",
    "waiting": "#3ba7ff",
    "priority": "#00e5ff",
    "normal": "#aaaaaa",
}

DRONE_COLOR = "#ffff00"

# ---- MAIN FUNCTION ----
def visualize(graph, drones):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor("#050505")
    ax.set_facecolor("#050505")

    # Extract positions
    pos = {name: zone["position"] for name, zone in graph.zones.items()}

    # Draw edges
    for a, b, *_ in graph.connections:
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        ax.plot([x1, x2], [y1, y2], color="#222222", linewidth=1)

    # Draw nodes
    for name, zone in graph.zones.items():
        x, y = pos[name]
        zone_type = zone["metadata"].get("zone", "normal")
        color = ZONE_COLORS.get(zone_type, "#aaaaaa")
        ax.scatter(x, y, color=color, s=50, zorder=2)

    # Prepare drone scatter
    drone_scatter = ax.scatter([], [], color=DRONE_COLOR, s=80, zorder=3)

    max_time = max(len(d.history) for d in drones)

    def update(frame):
        xs, ys = []
        for d in drones:
            if frame < len(d.history):
                node = d.history[frame]
                if node:
                    x, y = pos[node]
                    xs.append(x)
                    ys.append(y)
        drone_scatter.set_offsets(list(zip(xs, ys)))
        return (drone_scatter,)

    ax.set_xticks([])
    ax.set_yticks([])

    ani = animation.FuncAnimation(
        fig, update, frames=max_time, interval=500, repeat=False
    )

    plt.show()

if __name__ == "__main__":
    ...
