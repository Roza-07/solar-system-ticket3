# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet


def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """
    objects = []
    
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            
            parts = line.split()
            if len(parts) < 8:
                continue
                
            object_type = parts[0].lower()
            
            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("Unknown space object:", object_type)

    return objects


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.
    Формат: Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    """
    parts = line.split()
    if len(parts) >= 8:
        star.R = int(parts[1])
        star.color = parts[2]
        star.m = float(parts[3])
        star.x = float(parts[4])
        star.y = float(parts[5])
        star.Vx = float(parts[6])
        star.Vy = float(parts[7])


def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Формат: Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    """
    parts = line.split()
    if len(parts) >= 8:
        planet.R = int(parts[1])
        planet.color = parts[2]
        planet.m = float(parts[3])
        planet.x = float(parts[4])
        planet.y = float(parts[5])
        planet.Vx = float(parts[6])
        planet.Vy = float(parts[7])


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.
    Формат: Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    """
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        out_file.write("# Solar System - Ticket #3\n")
        out_file.write("# Format: Type R color mass x y Vx Vy\n\n")
        
        for obj in space_objects:
            if obj.type == 'star':
                line = f"Star {obj.R} {obj.color} {obj.m} {obj.x} {obj.y} {obj.Vx} {obj.Vy}\n"
            elif obj.type == 'planet':
                line = f"Planet {obj.R} {obj.color} {obj.m} {obj.x} {obj.y} {obj.Vx} {obj.Vy}\n"
            else:
                continue
            out_file.write(line)


if __name__ == "__main__":
    print("This module is not for direct call!")