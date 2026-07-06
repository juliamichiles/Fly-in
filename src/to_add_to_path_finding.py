def assign_drones(
    paths: list[tuple[list[str], int]],
    nb_drones: int
) -> list[list[list[str]]]:
    """
    Returns list of drone paths:
    [
        [path1, path1, path2, ...],  # each drone assigned a path
    ]
    """

    # how many drones per path
    assigned: list[int] = [0] * len(paths)

    drone_paths: list[list[str]] = []

    for _ in range(nb_drones):

        # choose best path
        best_index = min(
            range(len(paths)),
            key=lambda i: len(paths[i][0]) + assigned[i]
        )

        assigned[best_index] += 1
        drone_paths.append(paths[best_index][0])

    return drone_paths
