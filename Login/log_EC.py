from tkinter import *
import tkinter as tk
import subprocess
import ttkbootstrap as tb
from tkinter import IntVar
from PIL import Image, ImageTk
from tkinter import messagebox

def checker():
    election_id = entry_election_id.get()
    date_of_birth = entry_dob.get()

    if election_id == "12345" and date_of_birth == "18062004":
        open_select_window()
    else:

        display_message("Credentials do not match!")

def open_select_window():
    subprocess.run(["python", "select1.py"])

def display_message(message):
    messagebox.showinfo("Message", message)

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
registration_label.pack(pady=(50, 0))
registration_label.configure(style="Primary.TLabel")

my_frame = LabelFrame(root, font=("Roboto", 16, "bold"), background="#00FFFF", padx=100, pady=100)
my_frame.place(relx=0.5, rely=0.5, anchor='center')

entry_election_id = tk.Entry(my_frame, font=("Roboto", 16), width=30, fg='grey')
entry_election_id.insert(0, "Username")
entry_election_id.bind("<FocusIn>", lambda event: on_entry_click(event, entry_election_id, "Username"))
entry_election_id.bind("<FocusOut>", lambda event: on_focus_out(event, entry_election_id, "Username"))
entry_election_id.pack(pady=15, padx=20)

entry_dob = tk.Entry(my_frame, font=("Roboto", 16), width=30, fg='grey')
entry_dob.insert(0, "Password")
entry_dob.bind("<FocusIn>", lambda event: on_entry_click(event, entry_dob, "Password"))
entry_dob.bind("<FocusOut>", lambda event: on_focus_out(event, entry_dob, "Password"))
entry_dob.pack(pady=15, padx=20)

my_button = tb.Button(my_frame, text="Log In →", bootstyle="success", command=checker)
my_button.pack(pady=(60, 0), padx=20)

var1 = IntVar()
my_check = tb.Checkbutton(my_frame, bootstyle="primary", text="Remember Me", variable=var1, onvalue=1, offvalue=0)
my_check.pack(pady=(70, 0))

original_image = Image.open("emblem.png")
resized_image = original_image.resize((90, 90))
logo_image = ImageTk.PhotoImage(resized_image)

logo_label = tb.Label(root, image=logo_image, anchor='s')
logo_label.place(relx=0.5, rely=1.0, anchor='s', y=-30)

root.option_add("*Font", "Roboto")
root.option_add("*Entry.highlightcolor", "#54a0ff")

root.mainloop()
