# coding: utf-8
# license: GPLv3

# Главный модуль - создает окно, кнопки и управляет программой

import tkinter
from tkinter.filedialog import *
from solar_vis import *
from solar_model import *
from solar_input import *

perform_execution = False  # Флаг: запущена симуляция или нет
physical_time = 0          # Текущее физическое время
displayed_time = None      # Переменная для отображения времени в интерфейсе
time_step = None           # Шаг времени (dt)
time_speed = None          # Скорость симуляции
space = None               # Холст для рисования
start_button = None        # Кнопка Start/Pause
space_objects = []         # Список всех объектов (звезды + планеты)


def execution():
    """Основной цикл симуляции - вызывается каждую итерацию"""
    global physical_time
    global displayed_time
    
    # Пересчитываем координаты всех объектов
    recalculate_space_objects_positions(space_objects, time_step.get())
    
    # Обновляем их положение на экране
    for body in space_objects:
        update_object_position(space, body)
    
    # Увеличиваем время
    physical_time += time_step.get()
    displayed_time.set("%.1f" % physical_time + " seconds gone")
    
    # Если симуляция запущена - планируем следующий вызов
    if perform_execution:
        space.after(101 - int(time_speed.get()), execution)


def start_execution():
    """Запускает симуляцию"""
    global perform_execution
    perform_execution = True
    start_button['text'] = "Pause"  # Меняем текст кнопки
    start_button['command'] = stop_execution  # Меняем действие кнопки
    execution()
    print('Started execution...')


def stop_execution():
    """Останавливает симуляцию"""
    global perform_execution
    perform_execution = False
    start_button['text'] = "Start"
    start_button['command'] = start_execution
    print('Paused execution.')


def open_file_dialog():
    """Загружает данные из файла"""
    global space_objects
    global perform_execution
    
    perform_execution = False  # Останавливаем симуляцию
    
    # Удаляем старые изображения с холста
    for obj in space_objects:
        if hasattr(obj, 'image') and obj.image:
            try:
                space.delete(obj.image)
            except:
                pass  # Если объект уже удален - игнорируем ошибку
    
    # Удаляем старые орбиты
    for line in orbit_lines:
        try:
            space.delete(line)
        except:
            pass
    orbit_lines.clear()
    
    # Открываем диалог выбора файла
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    if not in_filename:
        print("File not selected!")
        return
    
    print(f"Loading file: {in_filename}")
    
    # Читаем объекты из файла
    space_objects = read_space_objects_data_from_file(in_filename)
    
    # Проверяем, что объекты загрузились
    if not space_objects:
        print("NO OBJECTS! Check file format!")
        return
    
    print(f"Objects loaded: {len(space_objects)}")
    for obj in space_objects:
        print(f"   - {obj.type}: x={obj.x}, y={obj.y}, R={obj.R}, color={obj.color}")
    
    # Находим максимальное расстояние от центра
    max_distance = 1  # Стартовое значение, чтобы избежать деления на ноль
    for obj in space_objects:
        dist = max(abs(obj.x), abs(obj.y))
        if dist > max_distance:
            max_distance = dist
    
    print(f"Max distance: {max_distance}")
    
    # Вычисляем масштаб
    calculate_scale_factor(max_distance)
    print(f"Scale factor: {scale_factor}")
    
    # Создаем изображения всех объектов
    for obj in space_objects:
        if obj.type == 'star':
            create_star_image(space, obj)
        elif obj.type == 'planet':
            create_planet_image(space, obj)
            # Рисуем орбиту планеты (вокруг первой попавшейся звезды)
            for star in space_objects:
                if star.type == 'star':
                    draw_orbit(space, star, obj)
                    break  # Рисуем орбиту только вокруг первой звезды
        else:
            print(f"Unknown type: {obj.type}")
    
    print("All objects created!")


def save_file_dialog():
    """Сохраняет текущее состояние в файл"""
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    if out_filename:
        write_space_objects_data_to_file(out_filename, space_objects)


def main():
    """Главная функция - создает окно и интерфейс"""
    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    
    print('Modelling started!')
    physical_time = 0
    
    # Создаем главное окно
    root = tkinter.Tk()
    root.title("Solar System - Ticket #3")
    root.geometry("1000x900")
    
    # Создаем холст для рисования (черный фон)
    space = tkinter.Canvas(root, width=1000, height=800, bg="black")
    space.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
    
    # Создаем панель с кнопками внизу
    frame = tkinter.Frame(root, height=60)
    frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    frame.pack_propagate(False)  # Фиксируем высоту панели
    
    # Кнопка Start/Pause
    start_button = tkinter.Button(frame, text="Start", command=start_execution, width=8)
    start_button.pack(side=tkinter.LEFT, padx=5, pady=10)
    
    # Поле для ввода шага времени
    time_step = tkinter.DoubleVar()
    time_step.set(1)
    time_step_entry = tkinter.Entry(frame, textvariable=time_step, width=5)
    time_step_entry.pack(side=tkinter.LEFT, padx=5, pady=10)
    
    # Ползунок скорости
    time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(frame, variable=time_speed, orient=tkinter.HORIZONTAL, length=100)
    scale.pack(side=tkinter.LEFT, padx=5, pady=10)
    
    # Кнопка открытия файла
    load_file_button = tkinter.Button(frame, text="Open file...", command=open_file_dialog, width=12)
    load_file_button.pack(side=tkinter.LEFT, padx=5, pady=10)
    
    # Кнопка сохранения файла
    save_file_button = tkinter.Button(frame, text="Save to file...", command=save_file_dialog, width=12)
    save_file_button.pack(side=tkinter.LEFT, padx=5, pady=10)
    
    # Кнопка включения/выключения орбит
    toggle_orbits_button = tkinter.Button(frame, text="Toggle Orbits", command=toggle_orbits, width=12)
    toggle_orbits_button.pack(side=tkinter.LEFT, padx=5, pady=10)
    
    # Отображение времени
    displayed_time = tkinter.StringVar()
    displayed_time.set("0.0 seconds gone")
    time_label = tkinter.Label(frame, textvariable=displayed_time, width=20)
    time_label.pack(side=tkinter.RIGHT, padx=10, pady=10)
    
    # Запускаем главный цикл tkinter
    root.mainloop()
    print('Modelling finished!')


if __name__ == "__main__":
    main()