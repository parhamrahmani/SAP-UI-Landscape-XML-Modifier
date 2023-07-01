import tkinter as tk
import tkinter.filedialog as filedialog
import xml.etree.ElementTree as ET
from tkinter import ttk
import customtkinter

from gui.stats_pad import *
from utils.xml_utils import *
from utils.excel_utils import *
from utils.console import *


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


if __name__ == "__main__":
    root_tk = tk.Tk()
    root_tk.geometry("600x600")
    root_tk.resizable(False, False)
    root_tk.configure(bg="white")
    root_tk.title("SAP UI Landscape XML Modifier")

    # Create a title label
    title_label = tk.Label(root_tk, text="SAP UI Landscape XML Modifier", font=("Arial", 18, "bold"), bg="white")
    title_label.pack(pady=20)

    # Create a description label
    description_text = "This program allows you to modify SAP UI Landscape XML files by regenerating UUIDs for workspaces,\n" \
                       "nodes, services, and items. It also provides the option to remove includes and rename workspaces,\n" \
                       "in order to make them usable as central files."

    description_label = tk.Label(root_tk, text=description_text, font=("Arial", 10), bg="white")
    description_label.pack(pady=10)

    # Create a label for menu options
    menu_label = tk.Label(root_tk, text="Menu Options", font=("Arial", 14, "bold"), bg="white")
    menu_label.pack(pady=20)

    # Create a frame for the menu options buttons
    menu_frame = tk.Frame(root_tk, bg="white")
    menu_frame.pack()

    # Create the "Destruct XML file structure into one simple list of items in one workspace" button
    extract_button = customtkinter.CTkButton(
        master=menu_frame,
        fg_color=("black", "black"),
        text="Destruct XML file structure into one simple list of items in one workspace"
    )
    extract_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Create the "Export Excel Reports" button
    export_excel_button = customtkinter.CTkButton(
        master=menu_frame,
        fg_color=("black", "black"),
        text="Export Excel Reports"
    )
    export_excel_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # Create the "Remove duplications" button
    remove_duplications_button = customtkinter.CTkButton(
        master=menu_frame,
        fg_color=("black", "black"),
        text="Remove duplications (still in development)"
    )
    remove_duplications_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    # Create the "Regenerate UUIDs and export Excel Reports" button
    regenerate_uuids_button = customtkinter.CTkButton(
        master=menu_frame,
        fg_color=("black", "black"),
        text="Regenerate UUIDs and export Excel Reports"
    )
    regenerate_uuids_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    # Create the "Add a new system from your existing XML file to another XML file" button
    add_system_button = customtkinter.CTkButton(
        master=menu_frame,
        fg_color=("black", "black"),
        text="Add a new system from your existing XML file to another XML file"
    )
    add_system_button.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

    # Create the "Show Statistics" button
    show_stats_button = customtkinter.CTkButton(
        master=menu_frame,
        fg_color=("black", "black"),
        text="Show the statistics of your XML file",
        command=lambda: show_stats_window(menu_frame,description_label, menu_label)
    )
    show_stats_button.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

    # Configure the column weight to center the buttons
    menu_frame.columnconfigure(0, weight=1)

    root_tk.mainloop()
