from tkinter import *
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

root = tb.Window(themename="litera", iconphoto=None)
root.configure(bg="#f5f5f5")

root.attributes('-fullscreen', True)

root.title("Log In ")

registration_label = tb.Label(root, text="Login", font=("Roboto", 40, "bold"))
registration_label.pack(pady=(50,0))
registration_label.configure(style="Primary.TLabel")

my_frame = LabelFrame(root ,font=("Roboto", 16, "bold"), background="#00FFFF", padx=100, pady=100)
my_frame.place(relx=0.5, rely=0.5, anchor='center')

my_entry1 = tb.Entry(my_frame, font=("Roboto", 16), width=30)
my_entry1.insert(0, "Election ID")
my_entry1.pack(pady=15, padx=20)

my_entry2 = tb.Entry(my_frame, font=("Roboto", 16), width=30)
my_entry2.insert(0, "Date of Birth")
my_entry2.pack(pady=15, padx=20)

my_button = tb.Button(my_frame, text="Log In →", bootstyle="success", command=checker)
my_button.pack(pady=(60,0), padx=20)

var1 = IntVar()
my_check = tb.Checkbutton(my_frame, bootstyle="primary", text="Remember Me", variable=var1, onvalue=1, offvalue=0)
my_check.pack(pady=(70,0))

original_image = Image.open("india.png")
resized_image = original_image.resize((90, 90))
logo_image = ImageTk.PhotoImage(resized_image)

logo_label = tb.Label(root, image=logo_image, anchor='s')
logo_label.place(relx=0.5, rely=1.0, anchor='s', y=-30)

root.option_add("*Font", "Roboto")
root.option_add("*Entry.highlightcolor", "#54a0ff")

create_table()

root.mainloop()
