import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.cm as cm

def load_excel_data(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error loading Excel data: {e}")
        return None

def update_display():
    selected_Position = Position_var.get()
    filtered_df = original_df.copy()
    if selected_Position != "All":
        filtered_df = filtered_df[filtered_df['Position'] == selected_Position]

    update_treeview(filtered_df)

    statistical_analysis_button["state"] = tk.NORMAL

def update_treeview(data_frame):
    for item in tree.get_children():
        tree.delete(item)

    for index, row in data_frame.iterrows():
        tree.insert("", "end", values=list(row))

def show_statistical_analysis():
    selected_Position = Position_var.get()

    filtered_df = original_df.copy()
    if selected_Position != "All":
        filtered_df = filtered_df[filtered_df['Position'] == selected_Position]

    plt.figure(figsize=(8, 6))

    if 'Party_representation' not in filtered_df.columns:
        print("Error: 'Party_representation' column not found in filtered DataFrame.")
        return

    parties = filtered_df['Party_representation']
    votes = filtered_df['Votes']

    colors = cm.get_cmap('viridis', len(parties))

    for Party_representation, vote, color in zip(parties, votes, colors(range(len(parties)))):
        plt.bar(Party_representation, vote, label=f'{vote}', color=color, edgecolor='black', linewidth=0.5, alpha=0.7, align='center')
        plt.text(Party_representation, vote + 0.1, str(vote), ha='center', va='bottom')

    plt.xlabel('Parties')
    plt.ylabel('Votes')
    plt.title('Statistical Analysis: Parties vs Votes')

    plt.legend()

    canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_frame)
    canvas.draw()

    if hasattr(statistical_analysis_button, 'canvas_widget'):
        statistical_analysis_button.canvas_widget.get_tk_widget().destroy()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    statistical_analysis_button.canvas_widget = canvas

def exit_program():
    root.attributes('-fullscreen', False)
    root.destroy()

root = tk.Tk()
root.title("Excel Data Viewer")
root.resizable(False, False)

root.attributes('-fullscreen', True)

window_width = root.winfo_screenwidth()
left_column_width = int(0.4 * window_width)
right_column_width = window_width - left_column_width

left_column = tk.Frame(root, width=left_column_width)
left_column.pack_propagate(False)
left_column.pack(side=tk.LEFT, fill=tk.BOTH)

emblem_path = "emblem.png"  
emblem_image = Image.open(emblem_path)
emblem_image = emblem_image.convert("RGBA")
emblem_image.putalpha(100) 

emblem_photo = ImageTk.PhotoImage(emblem_image)
emblem_label = tk.Label(left_column, image=emblem_photo)
emblem_label.pack(fill=tk.BOTH, expand=True)

right_column = tk.Frame(root, bg='#f2f2f2') 
right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

file_path = "sample.xlsx"
original_df = load_excel_data(file_path)

if original_df is None:
    print("Error: Failed to load Excel data.")
    exit_program()

localities = ["All"] + original_df['Position'].unique().tolist()

Position_var = tk.StringVar(root)
Position_var.set("All")

Position_menu = ttk.Combobox(right_column, textvariable=Position_var, values=localities)

apply_filter_button = tk.Button(right_column, text="Apply Filter", command=update_display)
statistical_analysis_button = tk.Button(right_column, text="Statistical Analysis", state=tk.DISABLED, command=show_statistical_analysis)
exit_button = tk.Button(right_column, text="Exit", command=exit_program)

font_style = ('Helvetica', 12)
Position_menu.config(font=font_style)
apply_filter_button.config(font=font_style)
statistical_analysis_button.config(font=font_style)
exit_button.config(font=font_style)

Position_menu.pack(pady=20)
apply_filter_button.pack(pady=10)

tree_columns = original_df.columns.tolist()
tree = ttk.Treeview(right_column, columns=tree_columns, show="headings")

for col in tree_columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(pady=20)
statistical_analysis_button.pack(pady=10)
exit_button.pack(pady=10)

graph_frame = tk.Frame(right_column, bg='#f2f2f2')
graph_frame.pack(fill=tk.BOTH, expand=True)

update_display()

def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()