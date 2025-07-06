def generate_trajectory(wall_width, wall_height, obstacles=[]):
    path = []
    step = 0.25  # 25cm step
    y = 0
    toggle = False
    while y < wall_height:
        row = []
        x = 0
        while x < wall_width:
            if not any(ox <= x <= ox+ow and oy <= y <= oy+oh for ox, oy, ow, oh in obstacles):
                row.append((x, y))
            x += step
        path.extend(row if not toggle else reversed(row))
        y += step
        toggle = not toggle
    return path
