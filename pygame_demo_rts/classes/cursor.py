class Cursor:
    def __init__(self, grid):
        self.grid = grid
        self.x = 0
        self.y = 0

    def move(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if self.grid.get_tile(nx, ny):
            self.x, self.y = nx, ny

