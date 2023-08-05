def array_dimensions(arr):
    outer_dim = 0
    inner_dim = 0

    if isinstance(arr, list):
        outer_dim = len(arr)

        if arr and isinstance(arr[0], list):
            inner_dim = len(arr[0])

    return outer_dim, inner_dim
