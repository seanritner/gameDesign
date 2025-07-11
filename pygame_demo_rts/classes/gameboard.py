from .grid import Grid, Resource
from .cursor import Cursor
from .unit import Unit
from .overlay import UnitOverlay
from .unitpath import UnitPath

import pygame

class GameBoard:
    def __init__(self):
        self.grid = Grid(15, 12, Resource())
        self.cursor = Cursor(self.grid)
        self.units = [
            Unit(3, 3, self.grid, "player"),
            Unit(7, 7, self.grid, "enemy")
        ]
        self.overlay = UnitOverlay(self.grid)
        self.paths = [UnitPath(u, self.grid) for u in self.units]
        self.current_unit_index = 0

    def update(self):
        unit = self.get_active_unit()
        if unit and unit.can_act:
            self.overlay.show_move_range(unit, 3)
            path = self.paths[self.current_unit_index]
            path.follow_path()

    def handle_input(self, key):
        unit = self.get_active_unit()
        if key == pygame.K_LEFT:
            self.cursor.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.cursor.move(1, 0)
        elif key == pygame.K_UP:
            self.cursor.move(0, -1)
        elif key == pygame.K_DOWN:
            self.cursor.move(0, 1)
        elif key == pygame.K_SPACE:
            # move active unit
            path = self.paths[self.current_unit_index]
            path.set_destination(self.cursor.x, self.cursor.y)
        elif key == pygame.K_RETURN:
            unit.can_act = False
            self.next_turn()

    def get_active_unit(self):
        if self.units:
            return self.units[self.current_unit_index]
        return None

    def next_turn(self):
        for u in self.units:
            u.can_act = True
        self.current_unit_index = (self.current_unit_index + 1) % len(self.units)