from .pathfinder import Pathfinder

class UnitPath:
    def __init__(self, unit, grid):
        self.unit = unit
        self.grid = grid
        self.pathfinder = Pathfinder(grid)
        self.path = []

    def set_destination(self, x, y):
        self.path = self.pathfinder.find_path((self.unit.x, self.unit.y), (x, y))

    def follow_path(self):
        if self.path:
            next_tile = self.path.pop(0)
            self.unit.move_to(*next_tile)

