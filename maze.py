MAZE = ('#E................##\n'
        '#.######.########.##\n'
        '#.######.########.##\n'
        '#.######.########.##\n'
        '#.######.....e###.##\n'
        '#.######.########.##\n'
        '#.###....####e###.##\n'
        '#.######......###.##\n'
        '#.#########.#####.##\n'
        '#.###############.##\n'
        '#.................##\n'
        '######.#######.#####\n'
        '######.#######.#####\n'
        '######.#######.#####\n'
        '###....###.....#####\n'
        '######.###.###.#####\n'
        '####...###..##.#####\n'
        '######.###.###....##\n'
        '######.#######.#####\n'
        '######.........#####\n')


class Maze(object):
    def __init__(self, s, entrance_char='E', exit_char='e',
                 path_char='.', solid_chars='#', delimiter='/'):
        super(Maze, self).__init__()
        self.tiles = s.strip(delimiter).split(delimiter)
        self.entrance_char = entrance_char
        self.exit_char = exit_char
        self.solid_chars = solid_chars

    def __getitem__(self, coords):
        try:
            return self.tiles[coords[1]][coords[0]]
        except IndexError:
            return None

    @property
    def entrance(self):
        for y, t in enumerate(self.tiles):
            x = t.find(self.entrance_char)
            if x != -1:
                return (x, y)

    @property
    def exit(self):
        for y, t in enumerate(self.tiles):
            x = t.find(self.exit_char)
            if x != -1:
                return (x, y)

    def neighbors(self, cell):
        neighbors = []
        width = len(self.tiles[0])
        height = len(self.tiles)
        potentials = (
            (cell[0]-1, cell[1]),
            (cell[0], cell[1]+1),
            (cell[0]+1, cell[1]),
            (cell[0], cell[1]-1))

        for c in potentials:
            if 0 <= c[0] < width and 0 <= c[1] < height:
                if self[c] and self[c] not in self.solid_chars:
                    neighbors.append(c)
        return neighbors

    def solutions(self):
        path_stack = [[self.entrance]]
        while path_stack and not all([self[p[-1]] == self.exit_char for p in path_stack]):
            pivot_path = path_stack.pop(0)
            if self[pivot_path[-1]] == self.exit_char:
                path_stack.append(pivot_path)
                continue
            ns = self.neighbors(pivot_path[-1])
            for n in ns:
                if n not in pivot_path:
                    if self[n] == '.':
                        path_stack.append(pivot_path + [n])
                    elif self[n] == self.exit_char:
                        path_stack.append(pivot_path + [n])
        return path_stack

    def optimal_solution(self):
        ss = self.solutions()
        try:
            optimal = min(ss, key=lambda x: len(x))
        except ValueError:
            raise Exception('No exit points.')
        return optimal

    def draw_path(self, path, mark):
        path_map = self.tiles[:]
        for point in path:
            tile = list(path_map[point[1]])
            tile[point[0]] = mark
            tile = ''.join(tile)
            path_map[point[1]] = tile
        for tile in path_map:
            print(tile)

if __name__ == '__main__':
    m = Maze(MAZE, delimiter='\n')
    print('Entrance:', m.entrance)
    print('Exit:', m.exit)
    ss = m.solutions()
    # for s in ss:
    #     print(s)
    optimum = m.optimal_solution()
    print('Optimum:', optimum)
    m.draw_path(optimum[1:-1], 'o')
