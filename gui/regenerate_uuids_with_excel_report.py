from tkinter import filedialog
import logging
from tkinter import ttk
import tkinter as tk

from gui.menu import clear_frame
from utils.xml_utils import regenerate_uuids_export_excel


def regenerate_uuids_with_excel_report(menu_frame):
    def select_xml_file():
        xml_file_path = filedialog.askopenfilename(initialdir="/", title="Select source XML file",
                                                   filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
        if xml_file_path:
            xml_path_entry.delete(0, tk.END)  # Clear the entry field
            xml_path_entry.insert(tk.END, xml_file_path)  # Insert the selected file path

    # Clear the main window
    clear_frame(menu_frame)

    description_label = tk.Label(
        menu_frame,
        text="Warnings:\n\n"
             "1. This function will regenerate the uuids of services and items\n"
             "in your SAP UI Local Landscape Files (XML files), In order to make\n"
             "to make it usable as a Global Landscape File (XML file).\n\n"
             "2. This function will also remove any inclusions of SAPUIGlobalLandscape.xml\n"
             "in your output file, in order to make it usable as a global/central file and avoid errors \n\n"
             "3. This function will also generate an excel report of the changes made to the XML file\n\n"
             "4. Make sure to backup your XML file before using this function\n\n",
        font=("Arial", 10, "bold"),
        bg="white",
        anchor='w',
        justify='left'
    )
    description_label.pack(pady=10)
    file_label = tk.Label(menu_frame, text="\n\nPlease put a copy of your local XML file",
                          font=("Arial", 10, "bold"),
                          bg="white")
    file_label.pack(pady=10)
    entry_frame = tk.Frame(menu_frame)
    entry_frame.pack(pady=10)
    xml_path_entry = tk.Entry(entry_frame, width=50)  # Entry widget to input XML file path
    xml_path_entry.pack(side='left')
    browse_button = tk.Button(entry_frame, text="Browse", command=select_xml_file, background="black",
                              foreground="white")
    browse_button.pack(side='left', padx=5)

    xml_file_path = xml_path_entry.get()

    regenerate_uuids_button = tk.Button(entry_frame, text="Submit",
                                        command=lambda: regenerate_uuids_export_excel(xml_path_entry.get()),
                                        background="black", foreground="white")

    regenerate_uuids_button.pack(side="left", pady=5)
