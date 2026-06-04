class Window:
    pass

    def __init__(self, row: int, col: int):
        self.grid = [[]]
        self.make_grid(row, col)

    def make_grid(self, row: int, col: int):
        row_list = []
        for i in range(row):
            col_list = []
            for j in range(col):
                col_list.append(None) # TODO: base widget class? specific widget for blank window in grid?
            row_list.append(col_list)
        
        self.grid = row_list

    def get_at(self, row: int, col: int):
        if (row >= len(self.grid)) or (col >= len(self.grid[row])):
            raise IndexError
        
        return self.grid[row][col]

    def set_at(self, row: int, col: int, widget):
        if (row >= len(self.grid)) or (col >= len(self.grid[row])):
            raise IndexError
        
        self.grid[row][col] = widget
