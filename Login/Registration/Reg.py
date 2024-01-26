from tkinter import *
import ttkbootstrap as tb
import subprocess
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox


conn = sqlite3.connect('voter_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS voters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
''')
conn.commit()

def forward():
    name = my_entry.get()
    if not name:

        return

    cursor.execute('SELECT * FROM voters WHERE name = ?', (name,))
    existing_entry = cursor.fetchone()

    if existing_entry:

        messagebox.showinfo("Already Registered", f"{name} is already registered.")
        subprocess.run(["python", "log.py"])
    else:

        cursor.execute('INSERT INTO voters (name) VALUES (?)', (name,))
        conn.commit()
        messagebox.showinfo("Registration Successful", f"{name} has been registered successfully.")

        subprocess.run(["python", "log.py"])


root = tb.Window(themename="litera", iconphoto=None)
root.configure(bg="#f5f5f5")
root.attributes('-fullscreen', True)


registration_label = tb.Label(root, text="Voter Registration", font=("Roboto", 40, "bold"))
registration_label.pack(pady=(50,0))
registration_label.configure(style="Primary.TLabel") 

my_frame = LabelFrame(root, font=("Roboto", 16, "bold"), background="#00FFFF", padx=100, pady=100)
my_frame.place(relx=0.5, rely=0.5, anchor='center')

my_entry = tb.Entry(my_frame, font=("Roboto", 16), width=30)
my_entry.pack(pady=20, padx=20) 

my_button = tb.Button(my_frame, text="Register Now ➡️", bootstyle="success", command=forward)
my_button.pack(side=BOTTOM, pady=(100, 10))

original_image = Image.open("emblem.png")
resized_image = original_image.resize((90, 90))
logo_image = ImageTk.PhotoImage(resized_image)

logo_label = tb.Label(root, image=logo_image, anchor='s')
logo_label.place(relx=0.5, rely=1.0, anchor='s', y=-30)

root.option_add("*Font", "Roboto")

style = tb.Style()
style.configure("Primary.TLabel", background="#f5f5f5")

root.mainloop()
