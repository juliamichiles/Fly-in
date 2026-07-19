#!/usr/bin/env python3
import pygame
import math

WIDTH, HEIGHT = 800, 600
BG_COLOR = (5, 5, 5)

ZONE_COLORS = {
    "start_hub": (0, 255, 159),
    "end_hub": (0, 255, 159),
    "restricted": (255, 60, 60),
    "waiting": (60, 150, 255),
    "priority": (0, 229, 255),
    "normal": (180, 180, 180),
}

DRONE_COLOR = (255, 255, 100)

def draw_glow(surface, pos, color, radius):
    for r in range(radius, 0, -3):
        alpha = int(255 * (r / radius) * 0.2)
        glow = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*color, alpha), (r, r), r)
        surface.blit(glow, (pos[0]-r, pos[1]-r))

def visualize(graph, drones):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Normalize positions
    raw_pos = {
        name: (zone["x"], zone["y"])
        for name, zone in graph.zones.items()
    }
    xs = [p[0] for p in raw_pos.values()]
    ys = [p[1] for p in raw_pos.values()]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    def transform(p):
        x = int((p[0] - min_x) / (max_x - min_x + 1e-5) * (WIDTH - 100) + 50)
        y = int((p[1] - min_y) / (max_y - min_y + 1e-5) * (HEIGHT - 100) + 50)
        return x, y

    pos = {k: transform(v) for k, v in raw_pos.items()}

    max_time = max(len(d.history) for d in drones)
    time = 0

    running = True
    while running:
        clock.tick(5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        # --- Radar sweep ---
        angle = (time * 5) % 360
        cx, cy = WIDTH // 2, HEIGHT // 2
        length = 1000
        end_x = cx + length * math.cos(math.radians(angle))
        end_y = cy + length * math.sin(math.radians(angle))
        pygame.draw.line(screen, (0, 255, 100), (cx, cy), (end_x, end_y), 1)

        # --- Draw edges ---
        for a, b, *_ in graph.connections:
            pygame.draw.line(screen, (40, 40, 40), pos[a], pos[b], 1)

        # --- Draw nodes ---
        for name, zone in graph.zones.items():
            zone_type = zone["metadata"].get("zone", "normal")
            color = ZONE_COLORS.get(zone_type, (200, 200, 200))
            draw_glow(screen, pos[name], color, 12)
            pygame.draw.circle(screen, color, pos[name], 4)

        # --- Draw drones ---
        for d in drones:
            if time < len(d.history):
                node = d.history[time]
                if node:
                    draw_glow(screen, pos[node], DRONE_COLOR, 10)
                    pygame.draw.circle(screen, DRONE_COLOR, pos[node], 5)

        pygame.display.flip()
        time += 1
        if time >= max_time:
            time = max_time - 1  # stop at last frame

    pygame.quit()

if __name__ == "__main__":
    ...
