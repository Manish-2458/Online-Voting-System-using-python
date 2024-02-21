import tkinter as tk
import subprocess
import ttkbootstrap as tb
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

class Marquee(tk.Canvas):
    def __init__(self, parent, text, margin=2, delay=4):
        tk.Canvas.__init__(self, parent, highlightthickness=0, bg="#f5f5f5")
        self.parent = parent
        self.delay = delay
        self.margin = margin
        self.text = text
        self.text_id = None
        self.width = 0
        self.bind("<Configure>", self.on_resize)
        self.draw_text()

    def draw_text(self):
        self.delete("all")
        self.text_id = self.create_text(self.width + self.margin, self.margin, anchor="nw", text=self.text,
                                        font=("Roboto", 40, "bold"), fill="black")
        self.animate()

    def on_resize(self, event):
        self.width = event.width
        self.delete("all")
        self.draw_text()

    def animate(self):
        self.move(self.text_id, -1, 0)
        x1, y1, x2, y2 = self.bbox(self.text_id)
        if x2 < 0:
            self.move(self.text_id, self.width + self.margin * 2, 0)
        self.after(self.delay, self.animate)

def auth(file):
    pswd = "admin123"
    admin_password = simpledialog.askstring("Enter Password", "Enter admin password", show='*')
    if admin_password == pswd:
        root.destroy()
        subprocess.run(["python", file])
    else:
        messagebox.showwarning("Invalid Password", "Incorrect admin password.")

def move1():
    root.destroy()
    subprocess.run(["python", "candidate_reg.py"])

def move2():
    root.destroy()
    subprocess.run(["python", "log.py"])

def move3():
    auth("results.py")

root = tb.Window(themename="litera", iconphoto=None)
root.attributes('-fullscreen', True)
root.title("Log In ")

marquee = Marquee(root, "Be Bright, Vote for the right!")
marquee.place(relx=0.5, rely=0.1, anchor='center', relwidth=1, y=130)

# Create a frame for the two-column layout
columns_frame = tk.Frame(root, bg="#f5f5f5")
columns_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=1, relheight=0.6)

# Left column for video player
left_column = tk.Frame(columns_frame, bg="red", width=400)
left_column.pack(side="left", fill="both", expand=True)

# Load and display the GIF file
gif_image = Image.open("Voting.gif")
gif_photo = ImageTk.PhotoImage(gif_image)
gif_label = tk.Label(left_column, image=gif_photo)
gif_label.pack(expand=True)

# Right column for frame
right_column = tk.Frame(columns_frame, bg="blue", width=1200)
right_column.pack(side="right", fill="both", expand=True, padx=20, pady=100)  # Add padding here

my_style = tb.Style()
my_style.configure('success.Outline.TButton', font=("Helvetica", 25))

my_button1 = tb.Button(right_column, text="Candidate Registration", bootstyle="success", style="success.Outline.TButton", width=30, command=move1)
my_button1.pack(pady=(20, 0), padx=20)

my_button2 = tb.Button(right_column, text="Voting Interface", bootstyle="success", style="success.Outline.TButton", width=30, command=move2)
my_button2.pack(pady=(60, 0), padx=20)

my_button3 = tb.Button(right_column, text="Results", bootstyle="success", style="success.Outline.TButton", width=30, command=move3)
my_button3.pack(pady=(60, 0), padx=20)

# Create a frame for the emblem image
emblem_frame = tk.Frame(root, bg="#f5f5f5")
emblem_frame.place(relx=0.5, rely=1.0, anchor='s')

original_image = Image.open("./emblem.png")
resized_image = original_image.resize((90, 90))
logo_image = ImageTk.PhotoImage(resized_image)

logo_label = tb.Label(emblem_frame, image=logo_image, anchor='center')
logo_label.pack()

root.option_add("*Font", "Roboto")
root.option_add("*Entry.highlightcolor", "#54a0ff")

root.mainloop()
