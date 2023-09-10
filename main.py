from tkinter import *
import sqlite3
from datetime import date

# SQL Connexion
conn = sqlite3.connect("EasyTask.db")
cur = conn.cursor()

# Create main table
cur.execute("DROP TABLE IF EXISTS tasks")
cur.execute("CREATE TABLE tasks(name TEXT, difficulty INTEGER)")

# GUI
root = Tk()
root.title("EasyTask")
root.geometry("400x400+1000+300")
frame = Frame(root)
frame.pack(pady=10)

current_oid=0
def addEntry():
    global current_oid
    if nameEntry.get()=="" or difficultyEntry=="":
        nameEntry.delete(0,END)
        difficultyEntry.delete(0,END)
        raise Exception('wrong entry!')

    elif type(int(difficultyEntry.get()))!=int:
         raise Exception("insert number!")

    else:
        cur.execute("INSERT INTO tasks(name, difficulty) VALUES (?,?)", (nameEntry.get(), difficultyEntry.get()))
        nameEntry.delete(0,END)
        difficultyEntry.delete(0,END)
        conn.commit()
        current_oid+=1
        if current_oid>0:
            deleteButton.config(state="active")
        showEntry()

d = dict()
def showEntry():
    now = date.today()
    global current_oid
    cur.execute("SELECT * FROM tasks WHERE oid="+str(current_oid))
    e = cur.fetchone()
    d['myLbl{}'.format(current_oid)] = Label(frame, text=str(e[0]) + " " + str(e[1]) + " " + str(now))
    d['myLbl{}'.format(current_oid)].grid(column=0, row=current_oid + 3, columnspan=2, sticky='w')


def deleteEntry():
    global deleteButton
    global current_oid
    try:
        d['myLbl'+str(current_oid)].destroy()
    except:
        print("no entries to delete")
    current_oid -= 1

    if current_oid>=0:
        cur.execute("DELETE FROM tasks WHERE oid=(SELECT MAX(oid) FROM tasks)")
        conn.commit()
        if current_oid==0:
            deleteButton.config(state="disabled")


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

deleteButton= Button(frame, text="Delete last entry", command=deleteEntry, width=25, state="disabled")
deleteButton.grid(column=0, row=3, columnspan=2)


root.mainloop()
