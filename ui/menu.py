import os
import tkinter.font as tkfont
import tkinter as tk
from ui.add_system_window import add_system_window
from ui.remove_duplications_window import remove_duplications_window
from ui.show_stats_window import show_stats_window

from utils.excel_utils import export_excel
from utils.xml_utils import extract_from_nodes
import sys


def restart_program():
    """
        Restarts the current python program by re-executing the current Python script with the same arguments.
        """
    python = sys.executable
    os.execl(python, python, *sys.argv)


BUTTON_WIDTH = 30
BUTTON_HEIGHT = 2
BUTTON_FONT_SIZE = 12


def clear_frame(frame):
    """
        Removes all widgets from the given frame and any nested frames.

        Args:
            frame (tk.Frame): The frame from which to remove all widgets.
        """
    for widget in frame.winfo_children():
        widget.destroy()

    # If form_frame and button_frame are present, clear them as well
    if hasattr(frame, 'form_frame'):
        for widget in frame.form_frame.winfo_children():
            widget.destroy()
        del frame.form_frame  # Remove the reference to form_frame from frame
    if hasattr(frame, 'button_frame'):
        for widget in frame.button_frame.winfo_children():
            widget.destroy()
        del frame.button_frame  # Remove the reference to button_frame from frame
    if hasattr(frame, 'next_button_frame'):
        for widget in frame.next_button_frame.winfo_children():
            widget.destroy()
        del frame.next_button_frame  # Remove the reference to button_frame from frame


def customize_button(button):
    """
       Customizes the given button by adjusting its height and font.

       Args:
           button (tk.Button): The button to customize.
       """
    # Increase the height of the button
    button.configure(height=BUTTON_HEIGHT)

    # Make the text bold and adjust font size
    button_font = tkfont.Font(size=BUTTON_FONT_SIZE)
    button.configure(font=button_font)


def create_exit_restart_buttons(frame):
    """
       Creates Exit and Restart buttons and adds them to the given frame.

       Args:
           frame (tk.Frame): The frame where the buttons will be added.
       """
    back_button = tk.Button(
        master=frame,
        text="Restart",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: restart_program()
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
    """
        Creates the main menu buttons and adds them to the given frame.

        Args:
            menu_frame (tk.Frame): The frame where the buttons will be added.
        """
    add_system_button = tk.Button(
        master=menu_frame,
        text="Add a system from your existing Landscape file to another Landscape file",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: add_system_window(menu_frame)  # replace with your function
    )
    customize_button(add_system_button)
    add_system_button.pack(pady=10, fill='both')

    from ui.regenerate_uuids_with_excel_report import regenerate_uuids_with_excel_report
    regenerate_uuids_button = tk.Button(
        master=menu_frame,
        text="Regenerate UUIDs and export Excel Reports",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: regenerate_uuids_with_excel_report(menu_frame)  # replace with your function
    )
    customize_button(regenerate_uuids_button)
    regenerate_uuids_button.pack(pady=10, fill='both')

    remove_duplications_button = tk.Button(
        master=menu_frame,
        text="Remove duplications in your Landscape file",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: remove_duplications_window(menu_frame)  # replace with your function
    )
    customize_button(remove_duplications_button)
    remove_duplications_button.pack(pady=10, fill='both')

    export_excel_button = tk.Button(
        master=menu_frame,
        text="Export Excel Reports of your Landscape file",
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
        text="Show the statistics of your Landscape file",
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
        text="Destruct Landscape file structure into one simple list of items in one workspace",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: extract_from_nodes()  # replace with your function
    )
    customize_button(extract_button)
    extract_button.pack(pady=10, fill='both')

    footer_warning_frame = tk.Frame(menu_frame, bg="white")
    footer_warning_frame.pack(side='bottom', fill='both', expand=True)

    important_warning = tk.Label(footer_warning_frame,
                                 text="IMPORTANT: Please make sure to use a copy your XML file before"
                                      "using",
                                 font=("Arial", 10, "bold"),
                                 bg="white",
                                 fg="red",
                                 anchor='w',
                                 justify='left')
    important_warning.pack(pady=10)
    create_exit_restart_buttons(menu_frame)
