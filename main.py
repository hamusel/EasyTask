import atexit
import os
import tkinter as tk
from tkinter import messagebox
from datetime import date
from db import DB
from tkinter import ttk

# create database by instantiating a new db Object
database = DB()

#Functions
def write_record():
    fhandler = open('record.txt', 'w')
    fhandler.write(str(database.current_oid))
    fhandler.close()

def delete_check():
    global delete_button
    if database.current_oid == 0:
        delete_button.config(state='disabled')

def add_entry():
    if not name_entry.get() or not difficulty_entry.get():
        name_entry.delete(0, tk.END)
        difficulty_entry.delete(0, tk.END)
        messagebox.showerror('Error', 'The fields can\'t be empty!')
        raise Exception('wrong entry!')
    try:
        int(difficulty_entry.get())
    except:
        messagebox.showerror("Error", 'The \'Difficulty\' must be a number!')
        raise Exception("insert number!")
    if len(name_entry.get()) > 20:
        messagebox.showerror("Error", "Your entry is too long!")
        raise Exception("too many characters")
    if database.current_oid>100:
        messagebox.showerror('Error', 'Limit of entries achieved!')
        raise Exception('limit achieved')
    else:
        database.insert(name_entry.get(), difficulty_entry.get())
        name_entry.delete(0, tk.END)
        difficulty_entry.delete(0, tk.END)
        database.current_oid += 1
        if database.current_oid > 0:
            delete_button.config(state="active")
        show_entry()

show_d = dict()
def show_entry():
    now = date.today()
    database.fetch_one()
    show_d[f'myLbl{database.current_oid}'] = tk.Label(frame, text=f'{database.e[0]} {database.e[1]} @ {now}')
    show_d[f'myLbl{database.current_oid}'].grid(column=0, row=database.current_oid + 3, columnspan=2)
                                                #sticky='w')

def show_all():
    now = date.today()
    database.fetch_all()
    counter = 1
    for entry in database.entries:
        show_d[f'myLbl{counter}'] = tk.Label(frame, text=f'{entry[0]} {entry[1]} @ {now}')
        show_d[f'myLbl{counter}'].grid(column=0, row=counter + 3, columnspan=2)
                                       #, sticky='w')
        counter += 1

def delete_entry():
    try:
        show_d['myLbl' + str(database.current_oid)].destroy()
    except:
        print("no entries to delete")
    database.current_oid -= 1
    if database.current_oid >= 0:
        database.delete_last_entry(database.current_oid)
        delete_check()

#GUI
root = tk.Tk()
root.title("EasyTask")
root.geometry("402x400")
root.resizable(False, False)

outside_frame = tk.Frame(root)
outside_frame.pack(fill=tk.BOTH, expand =1)

canvas = tk.Canvas(outside_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scroll_bar = ttk.Scrollbar(outside_frame, orient=tk.VERTICAL, command=canvas.yview)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scroll_bar.set)

frame = tk.Frame(canvas)

canvas.create_window((0,0), window=frame, anchor='nw')
frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

task_name = tk.Label(frame, text='Task name')
task_name.grid(column=0, row=0)
difficulty = tk.Label(frame, text='Difficulty')
difficulty.grid(column=0, row=1)

name_entry = tk.Entry(frame, width=30)
name_entry.grid(column=1, row=0)
difficulty_entry = tk.Entry(frame, width=10)
difficulty_entry.grid(column=1, row=1, sticky='w')

add_button = tk.Button(frame, text="Add entry", command=add_entry, width=25)
add_button.grid(column=1, row=2, columnspan=1)
delete_button = tk.Button(frame, text="Delete last entry", command=delete_entry, width=25)
delete_button.grid(column=1, row=3, columnspan=1)

#Functions for starting
delete_check()
if os.path.isfile('record.txt'):
    show_all()

atexit.register(write_record)
root.mainloop()
