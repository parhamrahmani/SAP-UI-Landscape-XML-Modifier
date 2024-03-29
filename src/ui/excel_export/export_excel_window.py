import tkinter as tk

from src.ui.ui_components.dialog_boxes import DialogBoxes
from src.ui.ui_components.ui_utils import UiUtils
from src.utils.excel_utils.excel_utils import export_excel


def export_excel_window(menu_frame):
    """
              This function creates a gui window for user to the export excel sheets from Landscape Files.

           Args:
               menu_frame (tk.Frame): The frame where the uuid regeneration window will be displayed.
           """

    # Clear the main window
    UiUtils.clear_frame(menu_frame)

    description_label = tk.Label(
        menu_frame,
        text="Warnings:\n\n"
             "1. This function will export excel sheets from a SAP UI Landscape File.\n\n"
             "2. This function won't edit anything in the xml file and only makes a spreadsheet.\n\n"
             "3. This function will also generate an excel spreadsheet of system duplications in your file\n\n",
        font=("Arial", 10, "bold"),
        bg="white",
        anchor='w',
        justify='left'
    )
    description_label.pack(pady=10)
    UiUtils.show_red_warning(menu_frame)

    file_label = tk.Label(menu_frame, text="\n\nPlease enter your local XML file",
                          font=("Arial", 10, "bold"),
                          bg="white")
    file_label.pack(pady=10)
    entry_frame = tk.Frame(menu_frame)
    entry_frame.pack(pady=10)
    xml_path_entry = tk.Entry(entry_frame, width=50)  # Entry widget to input XML file path
    xml_path_entry.pack(side='left')
    browse_button = tk.Button(entry_frame, text="Browse", command=lambda: DialogBoxes.xml_selection(xml_path_entry,
                                                                                                    "Select XML File"),
                              background="black",
                              foreground="white")
    browse_button.pack(side='left', padx=5)
    export_button = tk.Button(entry_frame, text="Submit", command=lambda: export_excel(xml_path_entry.get()),
                              background="black", foreground="white")
    export_button.pack(side="left", pady=5)

    UiUtils.create_exit_restart_back_buttons(menu_frame)
