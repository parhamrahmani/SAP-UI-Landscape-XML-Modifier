import tkinter as tk
import tkinter.filedialog as filedialog
import xml.etree.ElementTree as ET
from tkinter import ttk
import customtkinter

from gui.main_menu import *


def show_stats_window(menu_frame, description_label, menu_label):
    clear_frame(menu_frame)

    file_path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
    if file_path:
        get_stats(file_path)
        item_list = get_stats(file_path).items()
        try:
            stats_frame = tk.Frame(menu_frame, bg="white")
            stats_frame.pack(pady=20)

            stats_label = tk.Label(stats_frame, text="Statistics", font=("Arial", 16, "bold"), bg="white")
            stats_label.pack(pady=10)

            style = ttk.Style()
            style.configure("Treeview", font=("Arial", 12), rowheight=30)
            style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

            stats_table = ttk.Treeview(stats_frame, columns=("Category", "Count"), show="headings", height=10,
                                       style="Treeview")
            stats_table.column("Category", width=300)
            stats_table.column("Count", width=150)
            stats_table.heading("Category", text="Category", anchor=tk.CENTER)
            stats_table.heading("Count", text="Count", anchor=tk.CENTER)

            for category, count in item_list:
                stats_table.insert("", "end", values=(category, count))

            stats_table.pack()

            def go_back():
                clear_frame(stats_frame)

            def exit_program():
                root_tk.destroy()

            # Create the back button
            back_button = customtkinter.CTkButton(
                master=stats_frame,
                fg_color=("black", "black"),
                text="Back",
                command=go_back
            )
            back_button.pack(side=tk.LEFT, padx=10, pady=10)

            # Create the exit button
            exit_button = customtkinter.CTkButton(
                master=stats_frame,
                fg_color=("black", "black"),
                text="Exit",
                command=exit_program
            )
            exit_button.pack(side=tk.RIGHT, padx=10, pady=10)

        except Exception as e:
            error_label = tk.Label(menu_frame, text=f"An error occurred while processing the XML file:\n{str(e)}",
                                   font=("Arial", 12), bg="white")
            error_label.pack(pady=20)

    # Remove the description and menu options
    description_label.pack_forget()
    menu_label.pack_forget()