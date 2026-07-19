#!/usr/bin/env python3
import sys
from graph import Graph
from mapf import Drone
from errors import VizualizationError
try:
    import os
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    import pygame
except (ImportError, ModuleNotFoundError) as e:
    raise VizualizationError(e)


class Vizualizer:

    def __init__(
            self,
            graph: Graph,
            drones: list[Drone],
            cell_size: int = 120,
            padding: int = 100
    ) -> None:

        self.bg_color = (10, 16, 10) # Ultra-dark green/black
        self.connect_color = (51, 102, 0)
        self.drone_color = (255, 255, 255)
        
        pygame.init()
        self.graph = graph
        self.drones = drones
        self.cell_size = cell_size
        self.padding = padding
        self.font = pygame.font.SysFont("monospace", 18, bold=True)

        self.total_turns = max(len(d.history) for d in drones) if drones else 0
        self.current_turn = 0

        x_coords = [int(z["x"]) for z in graph.zones.values()]
        y_coords = [int(z["y"]) for z in graph.zones.values()]

        self.min_x, self.max_x = min(x_coords), max(x_coords)
        self.min_y, self.max_y = min(y_coords), max(y_coords)

        width = (self.max_x - self.min_x) * cell_size + (padding * 2)
        height = (self.max_y - self.min_y) * cell_size + (padding * 2)

        # Fallback for 1D or small maps
        self.screen = pygame.display.set_mode(
                (max(width, 800), max(height, 600))
        )
        pygame.display.set_caption("Fly-in")
        self.clock = pygame.time.Clock()

    def _get_color(self, color_str: str) -> tuple[int, int, int]:
        try:
            return tuple(pygame.Color(color_str))[:3]
        except (ValueError, TypeError):
            return (200, 200, 200)  # grey as default

    def _to_screen_coords(self, x: int, y: int) -> tuple[int, int]:
        """Maps map coordinates to Pygame window pixels."""
        screen_x = self.padding + (x - self.min_x) * self.cell_size
        screen_y = self.padding + (y - self.min_y) * self.cell_size
        return screen_x, screen_y

    def draw(self):
        self.screen.fill(self.bg_color)

        # Draw connections
        for u, v, metadata, _ in self.graph.connections:
            if u in self.graph.zones and v in self.graph.zones:
                u_x = int(self.graph.zones[u]["x"])
                u_y = int(self.graph.zones[u]["y"])
                v_x = int(self.graph.zones[v]["x"])
                v_y = int(self.graph.zones[v]["y"])
                pos_u = self._to_screen_coords(u_x, u_y)
                pos_v = self._to_screen_coords(v_x, v_y)
                pygame.draw.line(
                        self.screen,
                        self.connect_color,
                        pos_u,
                        pos_v,
                        2)
        # Draw zones
        zone_occupants: dict[
                str,
                list[int]
        ] = {name: [] for name in self.graph.zones}
        transit_occupants: dict[str, list[int]] = {}
        
        for drone in self.drones:
            if self.current_turn < len(drone.history):
                loc = drone.history[self.current_turn]
                if loc:
                    if "-" in loc:
                        transit_occupants.setdefault(loc, []).append(drone.id)
                    elif loc in zone_occupants:
                        zone_occupants[loc].append(drone.id)

        for name, zone in self.graph.zones.items():
            x, y = int(zone["x"]), int(zone["y"])
            px, py = self._to_screen_coords(x, y)
            
            color_str = zone["metadata"].get("color", "none")
            rgb_color = self._get_color(color_str)
            pygame.draw.circle(self.screen, rgb_color, (px, py), 18, 2)

            if len(name) > 10:
                name = name[:10]
            lbl = self.font.render(name, True, self.connect_color)
            self.screen.blit(lbl, (px - lbl.get_width() // 2, py - 35))

            occupants = zone_occupants[name]
            if occupants:
                drone_txt = ",".join(str(d_id) for d_id in occupants)
                d_lbl = self.font.render(drone_txt, True, self.drone_color)

                box_w, box_h = d_lbl.get_width() + 6, d_lbl.get_height() + 4
                pygame.draw.rect(
                        self.screen,
                        self.bg_color,
                        (px - box_w // 2, py - box_h // 2, box_w, box_h)
                )
                pygame.draw.rect(
                        self.screen,
                        self._get_color("green"),
                        (px - box_w // 2, py - box_h // 2, box_w, box_h),
                        1
                )
                self.screen.blit(
                        d_lbl,
                        (px - d_lbl.get_width() // 2, py - d_lbl.get_height() // 2)
                )
        # Draw transit zones
        for conn, occupants in transit_occupants.items():
            u, v = conn.split("-")
            u_x, u_y = int(self.graph.zones[u]["x"]),\
                    int(self.graph.zones[u]["y"])
            v_x, v_y = int(self.graph.zones[v]["x"]),\
                    int(self.graph.zones[v]["y"])
            
            # Calculate midle of connection 
            px, py = self._to_screen_coords((u_x + v_x) / 2, (u_y + v_y) / 2)
            
            drone_txt = ",".join(str(d_id) for d_id in occupants)
            d_lbl = self.font.render(drone_txt, True, self.drone_color)
            box_w, box_h = d_lbl.get_width() + 6, d_lbl.get_height() + 4

            pygame.draw.rect(
                        self.screen, 
                        self.bg_color, 
                    (px - box_w // 2, py - box_h // 2, box_w, box_h)
            )
            pygame.draw.rect(
                    self.screen, 
                    self._get_color("yellow"), 
                    (px - box_w // 2, py - box_h // 2, box_w, box_h), 
                    1
            )
            self.screen.blit(
                    d_lbl, 
                    (px - d_lbl.get_width() // 2, py - d_lbl.get_height() // 2)
            ) 
        hud_txt = (
                f"TURN: {self.current_turn + 1}/{self.total_turns}"
                "[Left/Right Arrow to Step]"
        )
        hud_lbl = self.font.render(hud_txt, True, self._get_color("green"))
        self.screen.blit(hud_lbl, (20, 20))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.current_turn < self.total_turns - 1:
                            self.current_turn += 1
                    elif event.key == pygame.K_LEFT:
                        if self.current_turn > 0:
                            self.current_turn -= 1
            self.clock.tick(30)


if __name__ == "__main__":
    ...
