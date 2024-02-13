import os
import tkinter as tk
import sqlite3
from PIL import Image, ImageTk

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voting Interface Module")
        self.root.attributes("-fullscreen", True)

        # self.folder_path = "Party_Symbols"
        self.folder_path = os.path.join(os.path.dirname(__file__), "Party_Symbols")

        self.image_files = [f for f in os.listdir(self.folder_path) if f.endswith(('.png'))]

        self.images = []
        self.labels = []

        self.connection = sqlite3.connect("votes.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                party_name TEXT
            )
        ''')
        self.connection.commit()

        self.canvas = None

        self.create_widgets()
        self.bind_mouse_scroll()  # Bind mouse scroll event after canvas creation

    def create_widgets(self):
        header_label = tk.Label(self.root, text="Choose Political Party for Parliament", font=("Helvetica", 18), pady=20, fg="blue")
        header_label.pack()

        self.canvas = tk.Canvas(self.root, height=self.root.winfo_screenheight())
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.root, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=frame, anchor=tk.NW)

        self.frame_width = 300
        self.frame_height = 300

        widgets_in_row = 4
        row_count = 0
        for i, file_name in enumerate(self.image_files):
            image_path = os.path.join(self.folder_path, file_name)
            img = Image.open(image_path)
            img = img.resize((self.frame_width - 20, self.frame_height - 50))
            img = ImageTk.PhotoImage(img)

            padx_value = 40
            pady_value = 30
            column_value = i % widgets_in_row

            button = tk.Button(frame, image=img, text=file_name.split('.')[0], compound=tk.TOP, command=lambda f=file_name: self.button_click(f))
            button.image = img

            button["font"] = ("Helvetica", 12)

            button.grid(row=row_count, column=column_value, padx=padx_value, pady=pady_value)

            self.images.append(img)
            self.labels.append(file_name.split('.')[0])

            if (i + 1) % widgets_in_row == 0:
                row_count += 1

        frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def bind_mouse_scroll(self):
        self.root.bind("<MouseWheel>", self.on_mouse_scroll)

    def on_mouse_scroll(self, event):
        if self.canvas:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def button_click(self, file_name):
        print(f"Button clicked for {file_name}")

        self.cursor.execute("INSERT INTO votes (party_name) VALUES (?)", (file_name.split('.')[0],))
        self.connection.commit()

        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="Thanks for voting!", font=("Helvetica", 24), pady=50)
        label.pack(fill=tk.BOTH, expand=True)

    def __del__(self):
        self.connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
