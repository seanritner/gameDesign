class UnitOverlay:
    def __init__(self, grid):
        self.grid = grid
        self.highlighted_tiles = []

    def show_move_range(self, unit, move_range):
        self.highlighted_tiles.clear()
        for dx in range(-move_range, move_range + 1):
            for dy in range(-move_range, move_range + 1):
                x = unit.x + dx
                y = unit.y + dy
                if self.grid.get_tile(x, y):
                    self.highlighted_tiles.append((x, y))

