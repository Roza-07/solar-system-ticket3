# coding: utf-8
# license: GPLv3

# Модуль визуализации - отвечает за рисование объектов на экране

header_font = "Arial-16"

window_width = 1000
window_height = 800

scale_factor = None  # Коэффициент масштабирования (пикселей на метр)

show_orbits = True   # Показывать орбиты или нет
orbit_lines = []     # Список линий орбит на холсте


def calculate_scale_factor(max_distance):
    """Вычисляет масштаб: сколько пикселей в одном метре"""
    global scale_factor
    if max_distance == 0:
        scale_factor = 1  # Защита от деления на ноль
    else:
        scale_factor = 0.35 * min(window_height, window_width) / max_distance
    print('Scale factor:', scale_factor)


def scale_x(x):
    """Переводит физическую координату X в экранную"""
    return int(x * scale_factor) + window_width // 2


def scale_y(y):
    """Переводит физическую координату Y в экранную.
       Ось Y перевернута: в физике Y вверх, на экране Y вниз"""
    return window_height // 2 - int(y * scale_factor)


def create_star_image(space, star):
    """Создает изображение звезды на холсте"""
    x = scale_x(star.x)  # физическая координата -> экранная
    y = scale_y(star.y)
    r = star.R  # радиус звезды в пикселях
    
    # Отладочный вывод - проверяем, что звезда создается
    print(f"Star: ({star.x}, {star.y}) -> screen ({x}, {y}), R={r}")
    
    # Создаем круг на холсте
    star.image = space.create_oval([x - r, y - r], [x + r, y + r], 
                                   fill=star.color, outline=star.color)


def create_planet_image(space, planet):
    """Создает изображение планеты на холсте"""
    x = scale_x(planet.x)
    y = scale_y(planet.y)
    r = planet.R
    
    # Отладочный вывод - проверяем, что планета создается
    print(f"Planet: ({planet.x}, {planet.y}) -> screen ({x}, {y}), R={r}")
    
    planet.image = space.create_oval([x - r, y - r], [x + r, y + r], 
                                     fill=planet.color, outline=planet.color)


def toggle_orbits():
    """Включает/выключает отображение орбит"""
    global show_orbits
    global orbit_lines
    show_orbits = not show_orbits
    if not show_orbits:
        for line in orbit_lines:
            space.delete(line)  # Удаляем все линии орбит
        orbit_lines = []
    print(f"Orbits: {'ON' if show_orbits else 'OFF'}")


def draw_orbit(space, star, planet):
    """Рисует орбиту планеты как окружность вокруг звезды"""
    global orbit_lines
    if not show_orbits:
        return
    
    # Вычисляем радиус орбиты по расстоянию от звезды до планеты
    dx = planet.x - star.x
    dy = planet.y - star.y
    radius = (dx**2 + dy**2)**0.5
    if radius == 0:
        return
    
    # Центр орбиты - звезда
    x = scale_x(star.x)
    y = scale_y(star.y)
    r = int(radius * scale_factor)
    
    # Рисуем окружность
    line = space.create_oval(x - r, y - r, x + r, y + r, 
                             outline='gray', width=1, tags="orbit")
    orbit_lines.append(line)


def update_system_name(space, system_name):
    """Показывает название системы на холсте"""
    space.create_text(30, 80, tag="header", text=system_name, font=header_font, fill='white')


def update_object_position(space, body):
    """Перемещает объект на холсте при его движении"""
    x = scale_x(body.x)
    y = scale_y(body.y)
    r = body.R
    
    # Если объект ушел за экран - прячем его
    if x + r < 0 or x - r > window_width or y + r < 0 or y - r > window_height:
        space.coords(body.image, window_width + r, window_height + r,
                     window_width + 2*r, window_height + 2*r)
    else:
        # Перемещаем объект в новые координаты
        space.coords(body.image, x - r, y - r, x + r, y + r)


if __name__ == "__main__":
    print("This module is not for direct call!")