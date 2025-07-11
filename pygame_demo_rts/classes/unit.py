class Unit:
    def __init__(self, x, y, grid, team='player'):
        self.x = x
        self.y = y
        self.grid = grid
        self.team = team
        self.hp = 10
        self.attack_range = 1
        self.can_act = True

    def move_to(self, x, y):
        if self.grid.get_tile(x, y):
            self.x, self.y = x, y

    def is_alive(self):
        return self.hp > 0
