from kandinsky import *


def fast_print(image, sizes, coordinates: tuple[int, int]):
    x = 0
    y = 0
    line_count = 0

    for shape in image:
        if len(shape) == 3:
            fill_rect(coordinates[0] + x, coordinates[1] + y, shape[0], shape[1], shape[-1])
            line_count = shape[1] - 1
            x += shape[0]

        elif len(shape) == 2:
            fill_rect(coordinates[0] + x, coordinates[1] + y, shape[0], line_count + 1, shape[-1])
            x += shape[0]

        else:
            set_pixel(coordinates[0] + x, coordinates[1] + y, shape[-1])
            x += 1

        if x == sizes[0]:
            x = 0
            y += line_count + 1
            line_count = 0


fast_print([(100, 1, (255, 0, 0)), (1, 19, (0, 38, 255)), (99, 19, (255, 255, 255))], (100, 20), (0, 0))
