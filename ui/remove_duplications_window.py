import tkinter as tk

from ui.ui_utils import show_red_warning, clear_frame, create_exit_restart_back_buttons
from utils.xml_utils import remove_duplicates, select_xml_file


def remove_duplications_window(menu_frame):
    """
       Function to create a GUI window for removing duplications from an XML file.

       The function presents a brief description, a warning message, and file selection option
       to the user. On clicking "Submit", the remove_duplicates function from xml_utils is invoked.

       Args:
           menu_frame (tkinter.Frame): Frame widget in which the remove duplication UI is built.
       """
    # Clear the main window

    clear_frame(menu_frame)

    description_label = tk.Label(
        menu_frame,
        text="Warnings:\n\n"
             "1. This function will remove duplications in your landscape files\n\n"
             "2. Parameters to recognize the duplications (if all true simultaneously):\n"
             " -Duplicate Application Server and Instance Number\n"
             " -Duplicate System ID\n"
             "\n3. This function will take up to several minutes to process depending on your system.\n",
        font=("Arial", 10, "bold"),
        bg="white",
        anchor='w',
        justify='left'
    )
    description_label.pack(pady=10)

    show_red_warning(menu_frame)
    file_label = tk.Label(menu_frame, text="\n\nPlease enter your local XML file",
                          font=("Arial", 10, "bold"),
                          bg="white")
    file_label.pack(pady=10)
    entry_frame = tk.Frame(menu_frame)
    entry_frame.pack(pady=10)
    xml_path_entry = tk.Entry(entry_frame, width=50)  # Entry widget to input XML file path
    xml_path_entry.pack(side='left')
    browse_button = tk.Button(entry_frame, text="Browse", command=lambda: select_xml_file(xml_path_entry),
                              background="black",
                              foreground="white")
    browse_button.pack(side='left', padx=5)

    remove_duplications_button = tk.Button(entry_frame, text="Submit",
                                           command=lambda: remove_duplicates(xml_path_entry.get()),
                                           background="black",
                                           foreground="white")
    remove_duplications_button.pack(side='left', padx=5)

    create_exit_restart_back_buttons(menu_frame)
