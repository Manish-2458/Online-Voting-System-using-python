import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from PIL import Image, ImageTk
from ttkbootstrap import Style
from openpyxl import Workbook, load_workbook
import os
import subprocess

class CandidateManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Candidate Management System")

        #self.style = Style("lumen")
        self.root.attributes("-fullscreen", True)
        self.candidates = []
        self.admin_username = "admin"
        self.admin_password = "admin123"
        self.ec_mode = False

        tk.Label(root, text="Candidate Management System", font=('Helvetica', 18, 'bold')).grid(row=0, column=1, columnspan=6, pady=10, sticky='nsew')

        self.create_add_delete_candidate_section()
        self.create_table_section()
        self.create_ec_view_modify_section()
        self.load_candidates_from_excel() 
        for i in range(8):
            self.root.grid_columnconfigure(i, weight=1)

        for i in range(13):
            self.root.grid_rowconfigure(i, weight=1)

        tk.Label(root, text="").grid(row=13, column=0)

        self.headers = ["ID", "Party Name", "Position", "Party"]

        # Add a dictionary to keep track of sorting directions
        self.sort_directions = {
            "ID": True,
            "Name": True,
            "Position": True,
            "Party": True
        }

        # Bind the heading click events to the sorting function
        self.candidate_tree.heading("ID", command=lambda: self.sort_column("ID"))
        self.candidate_tree.heading("Name", command=lambda: self.sort_column("Name"))
        self.candidate_tree.heading("Position", command=lambda: self.sort_column("Position"))
        self.candidate_tree.heading("Party", command=lambda: self.sort_column("Party"))

        # tk.Button(root, text="Exit", command=root.destroy, font=('Helvetica', 12)).grid(row=14, column=0, columnspan=8, pady=10)
        
        
    def sort_column(self, column):
        candidates = self.candidates[:]

        if column == "ID":
            candidates.sort(key=lambda x: self.candidates.index(x) + 1)
        else:
            candidates.sort(key=lambda x: x[self.headers.index(column)], reverse=self.sort_directions[column])

        # Change the sorting direction
        if column != "ID":
            self.sort_directions[column] = not self.sort_directions[column]

        # Clear the existing table
        for item in self.candidate_tree.get_children():
            self.candidate_tree.delete(item)

        # Repopulate the table with sorted data
        for i, candidate_info in enumerate(candidates, start=1):
            self.candidate_tree.insert("", tk.END, iid=i, values=(i, candidate_info[0], candidate_info[3], candidate_info[1]))



   
    def save_candidates_to_excel(self):
        wb = Workbook()
        ws = wb.active
        ws.append(["Party", "Party Symbol", 0,"Position","Name"])
        for candidate in self.candidates:
            ws.append(candidate)
        wb.save("sample.xlsx")


    def load_candidates_from_excel(self):
        if not os.path.exists("sample.xlsx"):
            self.save_candidates_to_excel()  # Create the file if it doesn't exist

        try:
            wb = load_workbook("sample.xlsx")
            ws = wb.active
            for row in ws.iter_rows(min_row=2, values_only=True):
                self.candidates.append(row)
            self.update_treeview()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_add_delete_candidate_section(self):
        tk.Label(self.root, text="Candidate Name:", font=('Helvetica', 12)).grid(row=3, column=1, padx=5, pady=2, sticky=tk.E)
        self.name_entry = tk.Entry(self.root, font=('Helvetica', 12))
        self.name_entry.grid(row=3, column=2, padx=5, pady=2, columnspan=4, sticky=tk.W + 'nsew')

        tk.Label(self.root, text="Party Affiliation:", font=('Helvetica', 12)).grid(row=4, column=1, padx=5, pady=2, sticky=tk.E)
        self.party_entry = tk.Entry(self.root, font=('Helvetica', 12))
        self.party_entry.grid(row=4, column=2, padx=5, pady=2, columnspan=4, sticky=tk.W + 'nsew')

        tk.Label(self.root, text="Party Symbol", font=('Helvetica', 12)).grid(row=5, column=1, padx=5, pady=2, sticky=tk.E)
        self.bio_entry = tk.Entry(self.root, font=('Helvetica', 12))
        self.bio_entry.grid(row=5, column=2, padx=5, pady=2, columnspan=4, sticky=tk.W + 'nsew')

        tk.Label(self.root, text="Position:", font=('Helvetica', 12)).grid(row=6, column=1, padx=5, pady=2, sticky=tk.E)
        self.position_var = tk.StringVar()
        self.position_entry = ttk.Combobox(self.root, textvariable=self.position_var,
                                           values=["MLA", "MP"], font=('Helvetica', 12))
        self.position_entry.grid(row=6, column=2, padx=5, pady=2, columnspan=4, sticky=tk.W + 'nsew')

        tk.Label(self.root, text="Candidate Photo:", font=('Helvetica', 12)).grid(row=7, column=1, padx=5, pady=2, sticky=tk.E)
        self.candidate_photo_path = tk.StringVar()
        tk.Entry(self.root, textvariable=self.candidate_photo_path, font=('Helvetica', 12)).grid(row=7, column=2, padx=5, pady=2, columnspan=3, sticky=tk.W + 'nsew')
        tk.Button(self.root, text="Browse", command=self.browse_candidate_photo, font=('Helvetica', 12)).grid(row=7, column=5, padx=5, pady=2, sticky=tk.W + 'nsew')

        tk.Label(self.root, text="Party Symbol:", font=('Helvetica', 12)).grid(row=8, column=1, padx=5, pady=2, sticky=tk.E)
        self.party_symbol_path = tk.StringVar()
        tk.Entry(self.root, textvariable=self.party_symbol_path, font=('Helvetica', 12)).grid(row=8, column=2, padx=5, pady=2, columnspan=3, sticky=tk.W + 'nsew')
        tk.Button(self.root, text="Browse", command=self.browse_party_symbol, font=('Helvetica', 12)).grid(row=8, column=5, padx=5, pady=2, sticky=tk.W + 'nsew')

        # Buttons
        tk.Button(self.root, text="Add Candidate", command=self.add_candidate, font=('Helvetica', 12)).grid(row=11, column=1,  padx=5, pady=2, sticky='nsew')
        tk.Button(self.root, text="Delete Candidate", command=self.delete_candidate, font=('Helvetica', 12)).grid(row=11, column=6, padx=5, pady=2, sticky='nsew')

    def create_table_section(self):
        table_frame = tk.Frame(self.root)
        table_frame.grid(row=12, column=1, columnspan=6, pady=5, sticky="nsew")

        self.candidate_tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Position", "Party"), show="headings", style="mystyle.Treeview")
        self.candidate_tree.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.candidate_tree.yview)
        scrollbar.pack(side="right", fill="y")

        self.candidate_tree.config(yscrollcommand=scrollbar.set)


        self.candidate_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.candidate_tree.heading("Name", text="Name", anchor=tk.CENTER)
        self.candidate_tree.heading("Position", text="Position", anchor=tk.CENTER)
        self.candidate_tree.heading("Party", text="Party", anchor=tk.CENTER)

        self.candidate_tree.column("ID", anchor=tk.CENTER, width=30)
        self.candidate_tree.column("Name", anchor=tk.CENTER, width=150)
        self.candidate_tree.column("Position", anchor=tk.CENTER, width=100)
        self.candidate_tree.column("Party", anchor=tk.CENTER, width=150)

        for i in range(1, 7):
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(10, weight=1)

    def exit_application(self):
        self.root.destroy()
        subprocess.run(["python", "main.py"])
    
    def create_ec_view_modify_section(self):
        self.mode_var = tk.IntVar()
        tk.Checkbutton(self.root, text="Election Commissioner Mode", variable=self.mode_var, command=self.toggle_ec_mode, font=('Helvetica', 12)).grid(row=13, column=1, columnspan=6, pady=5, sticky=tk.W)

        # Buttons
        tk.Button(self.root, text="View Details", command=self.view_details, font=('Helvetica', 12)).grid(row=15, column=1,  padx=4, pady=2, sticky='nsew')
        tk.Button(self.root, text="Modify Details", command=self.modify_details, font=('Helvetica', 12)).grid(row=15, column=6, padx=5, pady=2, sticky='nsew')

        tk.Button(self.root, text="Exit", command=self.exit_application, font=('Helvetica', 12)).grid(row=14, column=0, columnspan=8, pady=10)
        

        for i in range(1, 7):
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(11, weight=1)
        self.root.grid_rowconfigure(12, weight=1)
    def browse_candidate_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.candidate_photo_path.set(file_path)

    def browse_party_symbol(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.party_symbol_path.set(file_path)

    def toggle_ec_mode(self):
        '''self.ec_mode = not self.ec_mode
        if self.ec_mode:
            messagebox.showinfo("Election Commissioner Mode", "Enter Election Commissioner credentials to access exclusive features.")'''
        admin_password = simpledialog.askstring("Switch Mode", "Enter admin password:", show='*')

        if admin_password == self.admin_password:
            self.ec_mode = not self.ec_mode
            if self.ec_mode:
                messagebox.showinfo("Election Commissioner Mode", "Election Commissioner mode activated.\n")
        else:
            messagebox.showwarning("Invalid Password", "Incorrect admin password. Switching to Candidate mode.")
            self.ec_mode = False
            self.mode_var.set(0)

    def add_candidate(self):
        if self.ec_mode:        
            self.ec_mode_add_candidate()
            self.save_candidates_to_excel()
        else:
            messagebox.showwarning("Access Denied!","Please select ec mode.")


    def ec_mode_add_candidate(self):
        name = self.name_entry.get()
        party = self.party_entry.get()
        symbol = self.bio_entry.get()
        position = self.position_var.get()
        candidate_photo = self.candidate_photo_path.get()
        party_symbol = self.party_symbol_path.get()
        if name and party and symbol and position and candidate_photo and party_symbol:
            if self.authenticate_ec():
                candidate_info = (party, symbol, 0, position, name )
                self.candidates.append(candidate_info)
                self.update_treeview()
                self.clear_entries()
            else:
                messagebox.showwarning("Invalid Credential", "Incorrect password.")
        else:
            messagebox.showwarning("Incomplete Information", "Please fill in all fields.")

    def delete_candidate(self):
        if self.ec_mode:
            self.ec_mode_delete_candidate()
            self.save_candidates_to_excel()
        else:
            messagebox.showwarning("Access Denied!","Please select ec mode.")

    def ec_mode_delete_candidate(self):
        if self.authenticate_ec():
            selected_index = self.candidate_tree.selection()
            if selected_index:
                deleted_candidate = self.candidates.pop(int(selected_index[0]) - 1)
                messagebox.showinfo("Deleted", f"Candidate {deleted_candidate[0]} has been deleted.")
                self.update_treeview()
            else:
                messagebox.showwarning("No Candidate Selected", "Please select a candidate to delete.")

    def view_details(self):
        selected_index = self.candidate_tree.selection()
        if selected_index:
            index_as_int = int(selected_index[0])
            candidate = self.candidates[index_as_int - 1]
            '''if self.ec_mode:
                self.show_candidate_details(candidate)
            else:
                messagebox.showwarning("Access Denied!","Please select ec mode.")'''
            self.show_candidate_details(candidate)
        else:
            messagebox.showwarning("No Candidate Selected", "Please select a candidate to view details.")


    def show_candidate_details(self, candidate):
        details_window = tk.Toplevel(self.root)
        details_window.title("Candidate Details")
        details_window.attributes('-toolwindow', True)
        details_window.resizable(width=False, height=False)
        
        tk.Label(details_window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        tk.Label(details_window, text="Party:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        tk.Label(details_window, text="Bio:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        tk.Label(details_window, text="Position:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        tk.Label(details_window, text="Photo:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        tk.Label(details_window, text="Symbol:").grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)

        tk.Label(details_window, text=candidate[0]).grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        tk.Label(details_window, text=candidate[1]).grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        tk.Label(details_window, text=candidate[2]).grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        tk.Label(details_window, text=candidate[3]).grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)


        candidate_photo = Image.open(candidate[4])
        candidate_photo = candidate_photo.resize((100, 100))
        candidate_photo = ImageTk.PhotoImage(candidate_photo)
        tk.Label(details_window, image=candidate_photo).grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
        tk.Label(details_window, image=candidate_photo).image = candidate_photo 


        party_symbol = Image.open(candidate[5])
        party_symbol = party_symbol.resize((100, 100))
        party_symbol = ImageTk.PhotoImage(party_symbol)
        tk.Label(details_window, image=party_symbol).grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)
        tk.Label(details_window, image=party_symbol).image = party_symbol
        details_window.wait_window()
    def modify_details(self):
        if self.ec_mode:
            self.ec_mode_modify_details()
            self.save_candidates_to_excel()
        else:
            messagebox.showwarning("Access Denied!","Please select ec mode.")

    def ec_mode_modify_details(self):
        if self.authenticate_ec():
            selected_index = self.candidate_tree.selection()
            if selected_index:
                self.modify_candidate_details(int(selected_index[0]) - 1)
            else:
                messagebox.showwarning("No Candidate Selected", "Please select a candidate to delete.")

    def modify_candidate_details(self, index):
        details_window = tk.Toplevel(self.root)
        details_window.title("Modify Details")
        details_window.attributes('-toolwindow', True)
        details_window.resizable(width=False, height=False)

        tk.Label(details_window, text="Candidate Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        name_entry = tk.Entry(details_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=2)
        name_entry.insert(0, self.candidates[index][0])

        tk.Label(details_window, text="Party Affiliation:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        party_entry = tk.Entry(details_window)
        party_entry.grid(row=1, column=1, padx=10, pady=5, columnspan=3)
        party_entry.insert(0, self.candidates[index][1])

        tk.Label(details_window, text="Candidate Bio:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        bio_entry = tk.Entry(details_window)
        bio_entry.grid(row=2, column=1, padx=10, pady=5, columnspan=3)
        bio_entry.insert(0, self.candidates[index][2])

        tk.Label(details_window, text="Position:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        position_var = tk.StringVar()
        position_entry = ttk.Combobox(details_window, textvariable=position_var, values=["MP", "MLA"])
        position_entry.grid(row=3, column=1, padx=10, pady=5, columnspan=3, sticky=tk.W)
        position_entry.set(self.candidates[index][3])

        tk.Label(details_window, text="Candidate Photo:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        candidate_photo_path_var = tk.StringVar()
        tk.Entry(details_window, textvariable=candidate_photo_path_var).grid(row=4, column=1, padx=10, pady=5, columnspan=2)
        tk.Button(details_window, text="Browse", command=lambda: self.photo_modify(candidate_photo_path_var)).grid(row=4, column=3, padx=10, pady=5)

        tk.Label(details_window, text="Party Symbol:").grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)
        party_symbol_path_var = tk.StringVar()
        tk.Entry(details_window, textvariable=party_symbol_path_var).grid(row=5, column=1, padx=10, pady=5, columnspan=2)
        tk.Button(details_window, text="Browse", command=lambda: self.browse_party_symbol_modify(party_symbol_path_var)).grid(row=5, column=3, padx=10, pady=5)


        candidate_photo_path_var.set(self.candidates[index][4])
        party_symbol_path_var.set(self.candidates[index][5])


        tk.Button(details_window, text="Save Changes", command=lambda: self.save_changes(index, name_entry.get(), party_entry.get(), bio_entry.get(), position_var.get(), candidate_photo_path_var.get(), party_symbol_path_var.get()), font=('Helvetica', 12)).grid(row=6, column=0, columnspan=4, pady=10)

    def photo_modify(self, photo_path_var):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        photo_path_var.set(file_path)

    def browse_party_symbol_modify(self, symbol_path_var):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        symbol_path_var.set(file_path)

    def save_changes(self, index, name, party, bio, position, candidate_photo, party_symbol):
        if name and party and bio and position and candidate_photo and party_symbol:
            self.candidates[index] = (name, party, bio, position, candidate_photo, party_symbol)
            messagebox.showinfo("Changes Saved", "Candidate details have been successfully modified.")
            self.update_treeview()
        else:
            messagebox.showwarning("Incomplete Information", "Please fill in all fields.")

    def update_treeview(self):
        for item in self.candidate_tree.get_children():
            self.candidate_tree.delete(item)

        for i, candidate_info in enumerate(self.candidates, start=1):
            self.candidate_tree.insert("", tk.END, iid=i, values=(i, candidate_info[0], candidate_info[3], candidate_info[1]))

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.party_entry.delete(0, tk.END)
        self.bio_entry.delete(0, tk.END)
        self.position_entry.set("")
        self.candidate_photo_path.set("")
        self.party_symbol_path.set("")

    def authenticate_ec(self):
        password = simpledialog.askstring("Election Commissioner Mode", "Enter admin password:", show='*')
        if password == self.admin_password:
            return True
        else:
            messagebox.showwarning("Invalid Credentials", "Incorrect password.")
            return False


if __name__ == "__main__":
    root = tk.Tk()
    app = CandidateManagementSystem(root)
    root.mainloop()

