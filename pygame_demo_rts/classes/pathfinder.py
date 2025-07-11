class Pathfinder:
    def __init__(self, grid):
        self.grid = grid

    def find_path(self, start, goal):
        # Dummy straight line path
        path = []
        x0, y0 = start
        x1, y1 = goal
        while x0 != x1 or y0 != y1:
            if x0 < x1: x0 += 1
            elif x0 > x1: x0 -= 1
            elif y0 < y1: y0 += 1
            elif y0 > y1: y0 -= 1
            path.append((x0, y0))
        return path

