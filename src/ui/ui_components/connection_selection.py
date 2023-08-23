import logging
import tkinter as tk
from tkinter import messagebox

from src.ui.system_addition.adding_system_final_tab import system_adding_tab
from src.ui.system_modification.modifying_system_final_tab import system_modification_tab
from src.ui.system_removal.removing_system_final_tab import system_removal_tab
from src.utils.xml_utils.xml_query import XMLQuery


def radio_buttons_creation(frame, font, variable, texts):
    for i, text in enumerate(texts):
        radio_button_name = "radio_button_" + str(i)
        radio_button_name = tk.Radiobutton(frame, text=text, variable=variable, value=i, font=font,
                                           bg="white", fg="black", )
        radio_button_name.grid(row=0, column=i, sticky='w')


def create_sap_finder_button(frame, connection_types, row, column):
    for connection_type in connection_types:
        button_name = "button_" + connection_type
        button_name = tk.Button(frame, text="Find SAP System", font=("Arial", 10, "bold"), bg="white", fg="black")
        button_name.grid(row=row, column=column, columnspan=2, sticky='we', padx=5, pady=5)


def get_custom_sap_system(frame, source_xml_path, server_address_entry, sys_id_entry,
                          destination_xml_path, task):
    """
    Fetches details of an SAP system based on input parameters and asks for user confirmation. If the SAP
    system is found, it fetches the details and presents it to the user in a dialog box. User is asked to
    confirm if this is the SAP system they want to add. If confirmed, the system is then added to the
    system adding tab. In case of any exception during this process, it displays a warning message with
    exception details.
    """
    try:
        sap_system = XMLQuery.find_custom_system(source_xml_path,
                                                 server_address_entry,
                                                 sys_id_entry)
        if task == "addition":

            if sap_system is not None:
                system_info = f"Description: {sap_system.get('name')}\n\n" \
                              f"Server Address: {sap_system.get('server')}\n\n" \
                              f"System ID: {sap_system.get('systemid')}\n\n"

                dialog_text = f"Is this the SAP System you want to add?\n\n{system_info}"
                dialog_title = "Confirm System Details"

                if messagebox.askyesno(dialog_title, dialog_text):
                    system_adding_tab(frame, sap_system, source_xml_path, destination_xml_path)
                    return True, sap_system

            else:
                messagebox.showinfo("No matching system found", "Please check your inputs and try again.")
        elif task == "removal":
            if sap_system is not None:
                system_info = f"Description: {sap_system.get('name')}\n\n" \
                              f"Server Address: {sap_system.get('server')}\n\n" \
                              f"System ID: {sap_system.get('systemid')}\n\n"

                dialog_text = f"Is this the SAP System you want to remove?\n\n{system_info}"
                dialog_title = "Confirm System Details"

                if messagebox.askyesno(dialog_title, dialog_text):
                    system_removal_tab(frame, sap_system, source_xml_path)
                    pass
        elif task == "modification":
            if sap_system is not None:
                system_info = f"Description: {sap_system.get('name')}\n\n" \
                              f"Server Address: {sap_system.get('server')}\n\n" \
                              f"System ID: {sap_system.get('systemid')}\n\n"

                dialog_text = f"Is this the SAP System you want to modify?\n\n{system_info}"
                dialog_title = "Confirm System Details"

                if messagebox.askyesno(dialog_title, dialog_text):
                    system_modification_tab(frame, sap_system, source_xml_path)
                    pass
            else:
                messagebox.showinfo("No matching system found", "Please check your inputs and try again.")

    except Exception as e:
        messagebox.showwarning("Error in get_custom_sap_system():", str(e))
        logging.error(f"Error in get_custom_sap_system(): {str(e)}")


def get_fnwbc_system(frame, source_xml_path, fiori_nwbc_urls_entry,
                     destination_xml_path, task):
    try:
        sap_system = XMLQuery.find_fiori_nwbc_system(source_xml_path, fiori_nwbc_urls_entry)
        if task == "addition":
            if sap_system is not None:
                system_info = f"Description: {sap_system.get('name')}\n\n" \
                              f"URL: {sap_system.get('url')}\n\n"
                dialog_text = f"Is this the SAP System you want to add?\n\n{system_info}"
                dialog_title = "Confirm System Details"

                if messagebox.askyesno(dialog_title, dialog_text):
                    system_adding_tab(frame, sap_system, source_xml_path, destination_xml_path)
            else:
                messagebox.showinfo("No matching system found", "Please check your inputs and try again.")
        elif task == "removal":
            if sap_system is not None:
                system_info = f"Description: {sap_system.get('name')}\n\n" \
                              f"URL: {sap_system.get('url')}\n\n"
                dialog_text = f"Is this the SAP System you want to remove?\n\n{system_info}"
                dialog_title = "Confirm System Details"

                if messagebox.askyesno(dialog_title, dialog_text):
                    system_removal_tab(frame, sap_system, source_xml_path)
                    pass
        elif task == "modification":
            if sap_system is not None:
                system_info = f"Description: {sap_system.get('name')}\n\n" \
                              f"URL: {sap_system.get('url')}\n\n"
                dialog_text = f"Is this the SAP System you want to modify?\n\n{system_info}"
                dialog_title = "Confirm System Details"

                if messagebox.askyesno(dialog_title, dialog_text):
                    system_modification_tab(frame, sap_system, source_xml_path)
                    pass

            else:
                messagebox.showinfo("No matching system found", "Please check your inputs and try again.")
    except Exception as e:
        messagebox.showwarning("Error in get_fnwbc_system():", str(e))
        logging.error(f"Error in get_fnwbc_system(): {str(e)}")
