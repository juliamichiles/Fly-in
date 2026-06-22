#!/usr/bin/env python3

class Map:
      def __init__(
              self,
              nb_drones: int,
              zones: dict,
              connections: list[tuple]
      ) -> None:

          self.nb_drones = nb_drones
          self.zones = zones
          self.connections = connections


if __name__ == "__main__":
    ...
