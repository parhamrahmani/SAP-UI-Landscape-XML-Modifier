import tkinter as tk
import tkinter.filedialog as filedialog
import xml.etree.ElementTree as ET
import customtkinter
import tkinter as tk
import tkinter.font as tkfont
import tkinter as tk
from tkinter import filedialog, messagebox

from gui.add_system_window import add_system_window
from gui.stats_pad import show_stats_window
from utils.excel_utils import export_excel
from utils.xml_utils import extract_from_nodes, remove_duplicates, regenerate_uuids_export_excel, \
    get_stats

BUTTON_WIDTH = 30
BUTTON_HEIGHT = 2
BUTTON_FONT_SIZE = 12


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def customize_button(button):
    # Increase the height of the button
    button.configure(height=BUTTON_HEIGHT)

    # Make the text bold and adjust font size
    button_font = tkfont.Font(size=BUTTON_FONT_SIZE)
    button.configure(font=button_font)


def create_exit_back_buttons(frame):
    back_button = tk.Button(
        master=frame,
        text="Main Menu",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: go_back_to_main(frame)
    )
    customize_button(back_button)
    back_button.pack(side='right', anchor='se', padx=5, pady=5)

    exit_button = tk.Button(
        master=frame,
        text="Exit",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=frame.quit
    )
    customize_button(exit_button)
    exit_button.pack(side='right', anchor='se', padx=5, pady=5)


def create_main_menu_buttons(menu_frame):
    add_system_button = tk.Button(
        master=menu_frame,
        text="Add a new system from your existing XML file to another XML file",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: add_system_window(menu_frame)  # replace with your function
    )
    customize_button(add_system_button)
    add_system_button.pack(pady=10, fill='both')

    regenerate_uuids_button = tk.Button(
        master=menu_frame,
        text="Regenerate UUIDs and export Excel Reports",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: regenerate_uuids_export_excel()  # replace with your function
    )
    customize_button(regenerate_uuids_button)
    regenerate_uuids_button.pack(pady=10, fill='both')

    remove_duplications_button = tk.Button(
        master=menu_frame,
        text="Remove duplications",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: remove_duplicates()  # replace with your function
    )
    customize_button(remove_duplications_button)
    remove_duplications_button.pack(pady=10, fill='both')

    export_excel_button = tk.Button(
        master=menu_frame,
        text="Export Excel Reports",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: export_excel()  # replace with your function
    )
    customize_button(export_excel_button)
    export_excel_button.pack(pady=10, fill='both')
    show_stats_button = tk.Button(
        master=menu_frame,
        text="Show the statistics of your XML file",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: show_stats_window(menu_frame)
    )
    customize_button(show_stats_button)
    show_stats_button.pack(pady=10, fill='both')
    extract_button = tk.Button(
        master=menu_frame,
        text="Destruct XML file structure into one simple list of items in one workspace",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: extract_from_nodes()  # replace with your function
    )
    customize_button(extract_button)
    extract_button.pack(pady=10, fill='both')

    create_exit_back_buttons(menu_frame)


def go_back_to_main(menu_frame):
    clear_frame(menu_frame)
    create_main_menu_buttons(menu_frame)
