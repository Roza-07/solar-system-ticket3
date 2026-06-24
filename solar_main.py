# coding: utf-8
# license: GPLv3

import tkinter
from tkinter.filedialog import *
from solar_vis import *
from solar_model import *
from solar_input import *

perform_execution = False
physical_time = 0
displayed_time = None
time_step = None
space_objects = []


def execution():
    global physical_time
    global displayed_time
    
    recalculate_space_objects_positions(space_objects, time_step.get())
    for body in space_objects:
        update_object_position(space, body)
    
    physical_time += time_step.get()
    displayed_time.set("%.1f" % physical_time + " seconds gone")
    
    if perform_execution:
        space.after(101 - int(time_speed.get()), execution)


def start_execution():
    global perform_execution
    perform_execution = True
    start_button['text'] = "Pause"
    start_button['command'] = stop_execution
    execution()
    print('Started execution...')


def stop_execution():
    global perform_execution
    perform_execution = False
    start_button['text'] = "Start"
    start_button['command'] = start_execution
    print('Paused execution.')


def open_file_dialog():
    global space_objects
    global perform_execution
    
    perform_execution = False
    for obj in space_objects:
        if hasattr(obj, 'image') and obj.image:
            space.delete(obj.image)
    
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    if not in_filename:
        return
    
    space_objects = read_space_objects_data_from_file(in_filename)
    
    if not space_objects:
        print("No objects loaded!")
        return
    
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space_objects])
    calculate_scale_factor(max_distance)
    
    for obj in space_objects:
        if obj.type == 'star':
            create_star_image(space, obj)
        elif obj.type == 'planet':
            create_planet_image(space, obj)
    
    print(f"Loaded {len(space_objects)} objects")


def save_file_dialog():
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    if out_filename:
        write_space_objects_data_to_file(out_filename, space_objects)


def main():
    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    
    print('Modelling started!')
    physical_time = 0
    
    root = tkinter.Tk()
    root.title("Solar System - Ticket #3")
    root.geometry("1000x900")
    
    space = tkinter.Canvas(root, width=1000, height=800, bg="black")
    space.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
    
    frame = tkinter.Frame(root, height=60)
    frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    frame.pack_propagate(False)
    
    start_button = tkinter.Button(frame, text="Start", command=start_execution, width=8)
    start_button.pack(side=tkinter.LEFT, padx=5, pady=10)
    
    time_step = tkinter.DoubleVar()
    time_step.set(1)
    time_step_entry = tkinter.Entry(frame, textvariable=time_step, width=5)
    time_step_entry.pack(side=tkinter.LEFT, padx=5, pady=10)
    
    time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(frame, variable=time_speed, orient=tkinter.HORIZONTAL, length=100)
    scale.pack(side=tkinter.LEFT, padx=5, pady=10)
    
    load_file_button = tkinter.Button(frame, text="Open file...", command=open_file_dialog, width=12)
    load_file_button.pack(side=tkinter.LEFT, padx=5, pady=10)
    
    save_file_button = tkinter.Button(frame, text="Save to file...", command=save_file_dialog, width=12)
    save_file_button.pack(side=tkinter.LEFT, padx=5, pady=10)
    
    toggle_orbits_button = tkinter.Button(frame, text="Toggle Orbits", command=toggle_orbits, width=12)
    toggle_orbits_button.pack(side=tkinter.LEFT, padx=5, pady=10)
    
    displayed_time = tkinter.StringVar()
    displayed_time.set("0.0 seconds gone")
    time_label = tkinter.Label(frame, textvariable=displayed_time, width=20)
    time_label.pack(side=tkinter.RIGHT, padx=10, pady=10)
    
    root.mainloop()
    print('Modelling finished!')


if __name__ == "__main__":
    main()