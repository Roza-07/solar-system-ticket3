# coding: utf-8
# license: GPLv3

"""Модуль визуализации."""

header_font = "Arial-16"

window_width = 1000
window_height = 800

scale_factor = None
show_orbits = True


def calculate_scale_factor(max_distance):
    global scale_factor
    scale_factor = 0.4 * min(window_height, window_width) / max_distance
    print('Scale factor:', scale_factor)


def scale_x(x):
    return int(x * scale_factor) + window_width // 2


def scale_y(y):
    return int(-y * scale_factor) + window_height // 2


def create_star_image(space, star):
    x = scale_x(star.x)
    y = scale_y(star.y)
    r = star.R
    star.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=star.color)


def create_planet_image(space, planet):
    x = scale_x(planet.x)
    y = scale_y(planet.y)
    r = planet.R
    planet.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=planet.color)


def toggle_orbits():
    global show_orbits
    show_orbits = not show_orbits
    print(f"Орбиты: {'включены' if show_orbits else 'выключены'}")


def update_system_name(space, system_name):
    space.create_text(30, 80, tag="header", text=system_name, font=header_font)


def update_object_position(space, body):
    x = scale_x(body.x)
    y = scale_y(body.y)
    r = body.R
    
    if x + r < 0 or x - r > window_width or y + r < 0 or y - r > window_height:
        space.coords(body.image, window_width + r, window_height + r,
                     window_width + 2*r, window_height + 2*r)
    else:
        space.coords(body.image, x - r, y - r, x + r, y + r)


if __name__ == "__main__":
    print("This module is not for direct call!")