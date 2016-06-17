from PIL import Image, ImageDraw, ImageFilter
from collections import defaultdict
from pprint import pprint


def colorizer1(val):
    if val <= 85:
        return 0
    elif val <= 170:
        return 127
    elif val <= 255:
        return 255


def colorizer2(val):
    if val < 128:
        return 0
    return 255


def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


class Maze(object):
    def __init__(self, img,
                 entrance_color=(0, 255, 0),
                 exit_color=(255, 0, 0),
                 path_color=None):
        super(Maze, self).__init__()
        self.raw_img = img
        self.img = img.filter(ImageFilter.BLUR)
        self.img = self.img.filter(ImageFilter.SMOOTH_MORE)
        self.img = self.img.point(colorizer1)
#        self.img = self.img.resize
        self.img.save('display.png', 'png')
        self.entrance_color = entrance_color
        self.exit_color = exit_color
        self._pixels = self.img.getdata()
        if path_color:
            self.path_color = path_color
        else:
            self.path_color = self.analyze_background()
        self.brush = ImageDraw.Draw(self.raw_img)

    def get_thing(self, color):
        dict_x = defaultdict(int)
        dict_y = defaultdict(int)
        total_weight = 0
        for j in range(self.img.height):
            for i in range(self.img.width):
                p = self._pixels[i + self.img.width * j]
                distance = (
                    (p[0] - color[0])**2 +
                    (p[1] - color[1])**2 +
                    (p[2] - color[2])**2
                    ) ** 0.5
                if distance < 16:
                    dict_x[i] += 1
                    dict_y[j] += 1
                    total_weight += 1
        if not total_weight:
            raise Exception('There is nothing with that color')

        g = [0, 0]

        for x in dict_x:
            g[0] += (0.5 + x) * dict_x[x]
        for y in dict_y:
            g[1] += (0.5 + y) * dict_y[y]

        g[0] = int(g[0] / total_weight - 0.5)
        g[1] = int(g[1] / total_weight - 0.5)
        return tuple(g)

    def neighbours(self, p, stepsize):
        return ([p[0], p[1] - stepsize],
                [p[0] + stepsize, p[1]],
                [p[0], p[1] + stepsize],
                [p[0] - stepsize, p[1]],
                [p[0] + int(stepsize * 0.7), p[1] - int(stepsize * 0.7)],
                [p[0] + int(stepsize * 0.7), p[1] + int(stepsize * 0.7)],
                [p[0] - int(stepsize * 0.7), p[1] + int(stepsize * 0.7)],
                [p[0] - int(stepsize * 0.7), p[1] - int(stepsize * 0.7)])


    def valid_neighbours(self, neighbours):
        valid_colors = (self.entrance_color,
                        self.exit_color,
                        self.path_color)
        valid_list = []
        for x, y in neighbours:
            if not any((x >= self.img.width,
                        y >= self.img.height,
                        x < 0, y < 0)):
                try:
                    if self._pixels[x + self.img.width * y] in valid_colors:
                        valid_list.append((x, y))
                except:
                    print(x, y, 'AVAST!')
                    raise Exception('SIKINTI!')

        return valid_list

    def solve(self, stepsize, pencil_color):
        entrance = self.get_thing(self.entrance_color)
        pix = self.img.load()
        paths = [[entrance]]
        point_dict = {}

        while paths and not all([pix[p[-1][0], p[-1][1]] == self.exit_color
                                 for p in paths]):

            pivot_path = paths.pop(0)
            if pix[pivot_path[-1][0], pivot_path[-1][1]] == self.exit_color:
                paths.append(pivot_path)
            neighbours = self.neighbours(pivot_path[-1], stepsize)
            valid_neighbours = self.valid_neighbours(neighbours)
            for v in valid_neighbours:
                if v not in point_dict:
                    paths.append(pivot_path + [v])
                    point_dict[v] = 0
                if pix[v[0], v[1]] == self.exit_color:
                    self.draw_path(pivot_path + [v], pencil_color)
                    return self.raw_img

    def analyze_background(self):
        color_frequency = defaultdict(int)
        for p in self._pixels:
            if p not in (self.entrance_color, self.exit_color):
                color_frequency[p] += 1
        background_color = max(color_frequency.items(), key=lambda x: x[1])[0]
        return background_color

    def draw_path(self, path, pencil_color):
        for i in range(len(path) - 1):
            self.brush.line(path[i]+path[i+1], fill=pencil_color, width=7)
        self.raw_img.save('test.png')
        self.raw_img.show()

if __name__ == '__main__':
    raw_img = Image.open('deneme.jpg')
    m = Maze(raw_img)
    print(m.entrance_color, m.exit_color, m.path_color)
    solution = m.solve(12, pencil_color=(255, 255, 0))

    # brush.line(g+g, fill=(255, 0, 0))
    # neighbours = neighbours(g, 10)
    # valids = valid_neighbours(img, neighbours, (0, 0, 0))
    # for p in valids:
    #     brush.line(p+g, fill=(255, 0, 0))

    # img.save('sonuc.png', 'png')
    # colorized_image.save('c.png', 'png')
