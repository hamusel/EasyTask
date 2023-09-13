from tkinter import *
import os
import sqlite3
from datetime import date
import atexit

# SQL Connexion
if not os.path.isfile('EasyTask.db'):
    current_oid = 0
    conn = sqlite3.connect("EasyTask.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE tasks(name TEXT, difficulty INTEGER)")
else:
    conn = sqlite3.connect("EasyTask.db")
    cur = conn.cursor()
    fhandler1 = open('record.txt', 'r')
    current_oid = int(fhandler1.read())


root = Tk()
root.title("EasyTask")
root.geometry("400x400+1000+300")
frame = Frame(root)
frame.pack(pady=10)

def write_record():
    fhandler = open('record.txt', 'w')
    fhandler.write(str(current_oid))
    fhandler.close()

def delete_check():
    global current_oid
    global deleteButton
    if current_oid == 0:
        deleteButton.config(state='disabled')


def addEntry():
    global current_oid
    if not nameEntry.get() or not difficultyEntry.get():
        nameEntry.delete(0, END)
        difficultyEntry.delete(0, END)
        raise Exception('wrong entry!')

    elif type(int(difficultyEntry.get())) != int:
        raise Exception("insert number!")

    else:
        cur.execute("INSERT INTO tasks(name, difficulty) VALUES (?,?)", (nameEntry.get(), difficultyEntry.get()))
        nameEntry.delete(0, END)
        difficultyEntry.delete(0, END)
        conn.commit()
        current_oid += 1
        if current_oid > 0:
            deleteButton.config(state="active")
        showEntry()


d = dict()
def showEntry():
    now = date.today()
    # global current_oid
    cur.execute("SELECT * FROM tasks WHERE oid=" + str(current_oid))
    e = cur.fetchone()
    d[f'myLbl{current_oid}'] = Label(frame, text=f'{e[0]} {e[1]} {now}')
    d[f'myLbl{current_oid}'].grid(column=0, row=current_oid + 3, columnspan=2, sticky='w')


def show_all():
    global current_oid
    now = date.today()
    cur.execute("SELECT * FROM tasks")
    entries = cur.fetchall()
    counter = 1
    for entry in entries:
        d[f'myLbl{counter}'] = Label(frame, text=f'{entry[0]} {entry[1]} {now}')
        d[f'myLbl{counter}'].grid(column=0, row=counter + 3, columnspan=2, sticky='w')
        counter += 1


def deleteEntry():
    global deleteButton
    global current_oid
    print(current_oid)
    try:
        d['myLbl' + str(current_oid)].destroy()
    except:
        print("no entries to delete")
    current_oid -= 1

    if current_oid >= 0:
        cur.execute("DELETE FROM tasks WHERE oid=(SELECT MAX(oid) FROM tasks)")
        conn.commit()
        delete_check()


labelNames = ["task name", "difficulty"]

labelNamesCounter = 0
for label in labelNames:
    label = Label(frame, text=label)
    label.grid(column=0, row=labelNamesCounter)
    labelNamesCounter += 1

nameEntry = Entry(frame)
nameEntry.grid(column=1, row=0)
difficultyEntry = Entry(frame)
difficultyEntry.grid(column=1, row=1)

addButton = Button(frame, text="Add entry", command=addEntry, width=25)
addButton.grid(column=0, row=2, columnspan=2)

deleteButton = Button(frame, text="Delete last entry", command=deleteEntry, width=25, state="active")
deleteButton.grid(column=0, row=3, columnspan=2)

delete_check()
if os.path.isfile('record.txt'):
    show_all()
atexit.register(write_record)

root.mainloop()
