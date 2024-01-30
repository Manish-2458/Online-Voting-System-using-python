from tkinter import *
import tkinter as tk
import ttkbootstrap as tb
import sqlite3
import datetime
from tkinter import IntVar
from PIL import Image, ImageTk

def create_table():
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    election_id TEXT,
                    date_of_birth DATE
                )
                ''')
    conn.commit()
    conn.close()

def insert_data(election_id, date_of_birth):
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (election_id, date_of_birth) VALUES (?, ?)', (election_id, date_of_birth))
    conn.commit()
    conn.close()

def checker():
    election_id = my_entry1.get()
    date_of_birth = my_entry2.get()

    try:
        datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please enter date in YYYY-MM-DD format.")
        return

    insert_data(election_id, date_of_birth)

def on_entry_click(event, entry_widget, default_text):
    if entry_widget.get() == default_text:
        entry_widget.delete(0, tk.END)
        entry_widget.config(fg='black')

def on_focus_out(event, entry_widget, default_text):
    if entry_widget.get() == "":
        entry_widget.insert(0, default_text)
        entry_widget.config(fg='grey')
root = tb.Window(themename="litera", iconphoto=None)
root.configure(bg="#f5f5f5")

root.attributes('-fullscreen', True)

root.title("Log In ")

registration_label = tb.Label(root, text="Login", font=("Roboto", 40, "bold"))
registration_label.pack(pady=(50,0))
registration_label.configure(style="Primary.TLabel")

my_frame = LabelFrame(root ,font=("Roboto", 16, "bold"), background="#00FFFF", padx=100, pady=100)
my_frame.place(relx=0.5, rely=0.5, anchor='center')

entry_election_id = tk.Entry(my_frame, font=("Roboto", 16), width=30, fg='grey')
entry_election_id.insert(0, "Election ID")
entry_election_id.bind("<FocusIn>", lambda event: on_entry_click(event, entry_election_id, "Election ID"))
entry_election_id.bind("<FocusOut>", lambda event: on_focus_out(event, entry_election_id, "Election ID"))
entry_election_id.pack(pady=15, padx=20)

# Entry for Date of Birth
entry_dob = tk.Entry(my_frame, font=("Roboto", 16), width=30, fg='grey')
entry_dob.insert(0, "Date of Birth")
entry_dob.bind("<FocusIn>", lambda event: on_entry_click(event, entry_dob, "Date of Birth"))
entry_dob.bind("<FocusOut>", lambda event: on_focus_out(event, entry_dob, "Date of Birth"))
entry_dob.pack(pady=15, padx=20)

my_button = tb.Button(my_frame, text="Log In →", bootstyle="success", command=checker)
my_button.pack(pady=(60,0), padx=20)

var1 = IntVar()
my_check = tb.Checkbutton(my_frame, bootstyle="primary", text="Remember Me", variable=var1, onvalue=1, offvalue=0)
my_check.pack(pady=(70,0))

original_image = Image.open("emblem.png")
resized_image = original_image.resize((90, 90))
logo_image = ImageTk.PhotoImage(resized_image)

logo_label = tb.Label(root, image=logo_image, anchor='s')
logo_label.place(relx=0.5, rely=1.0, anchor='s', y=-30)

root.option_add("*Font", "Roboto")
root.option_add("*Entry.highlightcolor", "#54a0ff")

create_table()

root.mainloop()