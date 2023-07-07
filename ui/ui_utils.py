import os
import sys
import tkinter.font as tkfont
import tkinter as tk
from tkinter import messagebox

BUTTON_WIDTH = 30
BUTTON_HEIGHT = 2
BUTTON_FONT_SIZE = 12


def show_red_warning(frame):
    important_warning = tk.Label(frame, text="IMPORTANT: Please make sure to backup your XML file before\n and"
                                             " use a copy of it for this function ",
                                 font=("Arial", 10, "bold"),
                                 bg="white",
                                 fg="red",
                                 anchor='w',
                                 justify='left')
    important_warning.pack(pady=10)


def restart_program():
    """
        Restarts the current python program by re-executing the current Python script with the same arguments.
        """
    python = sys.executable
    os.execl(python, python, *sys.argv)


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


def create_exit_restart_back_buttons(frame):

    """
       Creates Exit and Restart buttons and adds them to the given frame.

       Args:
           frame (tk.Frame): The frame where the buttons will be added.
       """
    from ui.menu import create_main_menu_buttons

    back_button = tk.Button(
        master=frame,
        text="Restart",
        background="black",
        foreground="white",
        width=25,
        height=BUTTON_HEIGHT,
        command=lambda: restart_program()
    )
    back_button.pack(side='right', anchor='se', padx=5, pady=5)

    exit_button = tk.Button(
        master=frame,
        text="Exit",
        background="black",
        foreground="white",
        width=25,
        height=BUTTON_HEIGHT,
        command=frame.quit
    )
    exit_button.pack(side='right', anchor='se', padx=5, pady=5)

    main_menu_button = tk.Button(master=frame, text="Back To Main Menu", background="black",
                                 foreground="white",
                                 width=25,
                                 height=BUTTON_HEIGHT,
                                 command=lambda: create_main_menu_buttons(frame),
                                 )
    main_menu_button.pack(side='right', anchor='se', padx=5, pady=5)
