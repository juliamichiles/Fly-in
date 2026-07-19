#!/usr/bin/env python3
import sys
import re

def parse_map(map_path: str) -> tuple[int, str, str, dict[str, int], set[tuple[str, str]], dict[tuple[str, str], int]]:
    """Parses the map file to extract constraints and topology."""
    nb_drones = 0
    start_hub = ""
    end_hub = ""
    zone_capacities: dict[str, int] = {}
    connections: set[tuple[str, str]] = set()
    link_capacities: dict[tuple[str, str], int] = {}

    with open(map_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Parse drone count
            if line.startswith('nb_drones:'):
                nb_drones = int(line.split(':')[1].strip())
                continue

            # Parse hubs/zones
            if any(line.startswith(prefix) for prefix in ['start_hub:', 'end_hub:', 'hub:']):
                parts = line.split()
                zone_name = parts[1]
                
                if line.startswith('start_hub:'):
                    start_hub = zone_name
                elif line.startswith('end_hub:'):
                    end_hub = zone_name

                # Extract max_drones capacity (default: 1)
                max_drones = 1
                cap_match = re.search(r'max_drones=(\d+)', line)
                if cap_match:
                    max_drones = int(cap_match.group(1))
                
                zone_capacities[zone_name] = max_drones
                continue

            # Parse connections
            if line.startswith('connection:'):
                conn_part = line.split()[1]
                z1, z2 = conn_part.split('-')
                edge = tuple(sorted((z1, z2)))
                connections.add((z1, z2))
                connections.add((z2, z1)) # Bidirectional

                # Extract max_link_capacity (default: 1)
                max_link = 1
                link_match = re.search(r'max_link_capacity=(\d+)', line)
                if link_match:
                    max_link = int(link_match.group(1))
                
                link_capacities[edge] = max_link

    return nb_drones, start_hub, end_hub, zone_capacities, connections, link_capacities


def validate_simulation(map_path: str, sim_output_path: str) -> bool:
    """Validates the simulation output against the parsed map constraints."""
    # Load map rules
    nb_drones, start, end, zone_caps, connections, link_caps = parse_map(map_path)
    
    # Track current positions: Drone ID -> Zone/Connection Name
    drone_positions: dict[str, str] = {f"D{i}": start for i in range(1, nb_drones + 1)}
    
    with open(sim_output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    for turn_idx, line in enumerate(lines, start=1):
        moves = line.split()
        turn_moves: dict[str, str] = {} # drone_id -> destination
        link_usage: dict[tuple[str, str], int] = {}

        # 1. Parse individual movements for this turn
        for move in moves:
            if '-' not in move or not move.startswith('D'):
                print(f"[Error Turn {turn_idx}]: Invalid format '{move}'")
                return False
            drone_id, dest = move.split('-', 1)
            if drone_id not in drone_positions:
                print(f"[Error Turn {turn_idx}]: Unknown drone '{drone_id}'")
                return False
            turn_moves[drone_id] = dest

            # 2. Check path connectivity and link capacities
        for drone_id, dest in turn_moves.items():
            src = drone_positions[drone_id]
            
            # Determine the physical edge being used for link capacity tracking
            if '-' in dest: # Entering a restricted transit connection (e.g., "micro_gate1-overflow_hell1")
                z1, z2 = dest.split('-')
                if src != z1:
                    print(f"[Error Turn {turn_idx}]: {drone_id} tried to enter connection {dest} from {src}")
                    return False
                if (z1, z2) not in connections:
                    print(f"[Error Turn {turn_idx}]: Invalid connection {dest} for {drone_id}")
                    return False
                edge = tuple(sorted((z1, z2)))
                
            elif '-' in src: # Landing from a restricted connection (e.g., src is "micro_gate1-overflow_hell1")
                z1, z2 = src.split('-')
                if dest != z2:
                    print(f"[Error Turn {turn_idx}]: {drone_id} must land at {z2}, tried {dest}")
                    return False
                edge = tuple(sorted((z1, z2)))
                
            else: # Standard move between normal zones
                if (src, dest) not in connections:
                    print(f"[Error Turn {turn_idx}]: Disconnected move {src} -> {dest} for {drone_id}")
                    return False
                edge = tuple(sorted((src, dest)))

            # Track and validate link capacity
            if edge in link_caps:
                link_usage[edge] = link_usage.get(edge, 0) + 1
                if link_usage[edge] > link_caps[edge]:
                    print(f"[Error Turn {turn_idx}]: Link capacity exceeded on connection {edge}")
                    return False

        # 3. Simulate state change & evaluate zone capacity
        next_positions = drone_positions.copy()
        for drone_id, dest in turn_moves.items():
            next_positions[drone_id] = dest

        # Count occupants per zone (ignoring start/end hubs and transit lines)
        zone_counts: dict[str, int] = {}
        for d_id, pos in next_positions.items():
            if pos != start and pos != end and '-' not in pos: 
                zone_counts[pos] = zone_counts.get(pos, 0) + 1

        for zone, count in zone_counts.items():
            if count > zone_caps.get(zone, 1):
                print(f"[Error Turn {turn_idx}]: Zone '{zone}' exceeded capacity (Contains {count} drones)")
                return False


# 4. Final Goal Check
    undelivered = [d for d, pos in drone_positions.items() if pos != end]
    if undelivered:
        print(f"[Validation Failed]: Drones left behind: {undelivered}")
        return False

    print(f"Success! Solution verified valid in {len(lines)} turns.")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python validate.py <map_file> <simulation_output_file>")
        sys.exit(1)
    
    success = validate_simulation(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)

