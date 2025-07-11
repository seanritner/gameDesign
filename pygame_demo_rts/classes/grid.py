class Resource:
    def __init__(self, resource_type="grass"):
        self.resource_type = resource_type

class Grid(Resource):
    def __init__(self, width, height, default_tile):
        super().__init__("grid")
        self.width = width
        self.height = height
        self.tiles = [[default_tile for _ in range(width)] for _ in range(height)]

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None
    