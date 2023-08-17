import os
import tkinter as tk
from tkinter import filedialog


class DialogBoxes:
    @staticmethod
    def xml_selection(xml_path_entry, title):  #
        """
                   Opens a dialog to select a source XML file, and updates 'xml_path_entry' with the file path.
                   """
        xml_file_path = filedialog.askopenfilename(initialdir="/", title=title,
                                                   filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
        if xml_file_path:
            xml_path_entry.delete(0, tk.END)  # Clear the entry field
            xml_path_entry.insert(tk.END, xml_file_path)  # Insert the selected file path

    @staticmethod
    def open_folder_containing_file(xml_file_path):
        folder_path = os.path.dirname(xml_file_path)
        os.startfile(folder_path)
