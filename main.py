from tkinter import *
from tkinter import messagebox
from datetime import date
import atexit
import os
import db

# create DataBase by instantiating a new db Object
database = db.DB()

#Functions
def write_record():
    fhandler = open('record.txt', 'w')
    fhandler.write(str(database.current_oid))
    fhandler.close()


def delete_check():
    global current_oid
    current_oid = database.current_oid
    global delete_button
    if database.current_oid == 0:
        delete_button.config(state='disabled')


def add_entry():
    global current_oid
    current_oid = database.current_oid

    try:
        int(difficulty_entry.get())
    except:
        messagebox.showerror("Error", 'The \'difficulty\' must be a number!')
        raise Exception("insert number!")

    if len(name_entry.get()) > 20:
        messagebox.showerror("Error", "Your entry is too long!")
        raise Exception("too many characters")

    if database.current_oid>10:
        messagebox.showerror('Error', 'Limit of entries achieved!')
        raise Exception('limit achieved')

    if not name_entry.get() or not difficulty_entry.get():
        name_entry.delete(0, END)
        difficulty_entry.delete(0, END)
        messagebox.showerror('Error', 'The fields can\'t be empty!')
        raise Exception('wrong entry!')

    else:
        database.cur.execute("INSERT INTO tasks(name, difficulty) VALUES (?,?)", (name_entry.get(), difficulty_entry.get()))
        name_entry.delete(0, END)
        difficulty_entry.delete(0, END)
        database.conn.commit()
        database.current_oid += 1
        if database.current_oid > 0:
            delete_button.config(state="active")
        show_entry()


d = dict()
def show_entry():
    now = date.today()
    database.cur.execute("SELECT * FROM tasks WHERE oid=" + str(database.current_oid))
    e = database.cur.fetchone()
    d[f'myLbl{database.current_oid}'] = Label(frame, text=f'{e[0]} {e[1]} {now}')
    d[f'myLbl{database.current_oid}'].grid(column=0, row=database.current_oid + 3, columnspan=2, sticky='w')


def show_all():
    global current_oid
    current_oid = database.current_oid
    now = date.today()
    database.cur.execute("SELECT * FROM tasks")
    entries = database.cur.fetchall()
    counter = 1
    for entry in entries:
        d[f'myLbl{counter}'] = Label(frame, text=f'{entry[0]} {entry[1]} {now}')
        d[f'myLbl{counter}'].grid(column=0, row=counter + 3, columnspan=2, sticky='w')
        counter += 1


def delete_entry():
    global delete_button
    global current_oid
    current_oid = database.current_oid
    try:
        d['myLbl' + str(database.current_oid)].destroy()
    except:
        print("no entries to delete")
    database.current_oid -= 1

    if database.current_oid >= 0:
        database.cur.execute("DELETE FROM tasks WHERE oid=(SELECT MAX(oid) FROM tasks)")
        database.conn.commit()
        delete_check()

#GUI
root = Tk()
root.title("EasyTask")
root.geometry("400x400+1000+300")
frame = Frame(root)
frame.pack(pady=10)


labelNames = ["task name", "difficulty"] #should be a dic

labelNamesCounter = 0
for label in labelNames:
    label = Label(frame, text=label)
    label.grid(column=0, row=labelNamesCounter)
    labelNamesCounter += 1

name_entry = Entry(frame)
name_entry.grid(column=1, row=0)
difficulty_entry = Entry(frame)
difficulty_entry.grid(column=1, row=1)

add_button = Button(frame, text="Add entry", command=add_entry, width=25)
add_button.grid(column=0, row=2, columnspan=2)
delete_button = Button(frame, text="Delete last entry", command=delete_entry, width=25)
delete_button.grid(column=0, row=3, columnspan=2)


#Functions for starting
delete_check()
if os.path.isfile('record.txt'):
    show_all()

atexit.register(write_record)
root.mainloop()

