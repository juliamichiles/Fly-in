"""Custom exception modules for the simulation engine."""


class MapError(Exception):
    """Exception raised when map parsing or structure validation fails."""
    ...


class PathError(Exception):
    """Exception raised when pathfinding fails or a drone route cannot be
        scheduled.
    """
    ...


class ConnectionError(Exception):
    """Exception raised for invalid connection topologies."""
    ...


class VisualizationError(Exception):
    """Exception raised when the graphical interface encounters a dependency
        error.
    """
    ...
