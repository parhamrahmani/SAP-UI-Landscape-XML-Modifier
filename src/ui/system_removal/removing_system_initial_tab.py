import tkinter as tk
from tkinter import messagebox

from src.ui.ui_components.connection_selection import radio_buttons_creation, get_custom_sap_system, \
    get_fnwbc_system
from src.ui.ui_components.dialog_boxes import DialogBoxes
from src.ui.ui_components.forms import create_custom_system_form, create_fiori_nwbc_form
from src.ui.ui_components.ui_utils import UiUtils

DEFAULT_FONT_BOLD = ("Arial", 8, "bold")


def remove_system_window(menu_frame):
    # Clear the main window
    UiUtils.clear_frame(menu_frame)

    description_label = tk.Label(
        menu_frame,
        text="Warnings:\n\n"
             "1. This function will remove a sap system from your  SAP UI Landscape file    \n "
             "\n\n2. Please make sure to use a copy of your landscape file and never edit a\n"
             "landscape file directly!\n\n",

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

    def proceed_to_next():
        xml_path = xml_path_entry.get()  # Retrieve the value from the entry widget when needed
        if xml_path == "" or not xml_path.endswith(".xml"):
            messagebox.showerror("Error", "Please enter a path to your XML file")
            return
        else:
            UiUtils.clear_frame(menu_frame)  # Clear the menu_frame

            # create a label for selecting connection type
            connection_type_label = tk.Label(menu_frame, text=f"Please select connection type: ",
                                             font=("Arial", 12, "bold"), fg="black", bg="white")
            connection_type_label.pack(pady=10)

            # create radio buttons for choosing the connection type
            connection_type = tk.IntVar()

            radio_button_frame = tk.Frame(menu_frame, bg="white")
            radio_button_frame.pack(pady=5, anchor='center')
            texts = ["1. Custom Application Server", "2. FIORI/NWBC System"]

            radio_buttons_creation(radio_button_frame, DEFAULT_FONT_BOLD, connection_type, texts)
            server_address_entry, name_entry, sys_id_entry, custom_system_form_frame = create_custom_system_form(
                xml_path,
                menu_frame)

            fiori_nwbc_name, fiori_nwbc_urls, fiori_nwbc_frame = create_fiori_nwbc_form(xml_path,
                                                                                        menu_frame)

            # Configuring the column's weight to ensure they take up the full space
            custom_system_form_frame.grid_columnconfigure(1, weight=1)

            # Create a button to send information to the next function
            # The command associated with this button is determined by def on_connection_type_change(*args)
            next_button_custom = tk.Button(custom_system_form_frame, text="Find SAP System", background="black",
                                           foreground="white",
                                           command=lambda: get_custom_sap_system(menu_frame, xml_path,
                                                                                 server_address_entry.get(),
                                                                                 sys_id_entry.get()
                                                                                 , None, "removal"),
                                           width=40, height=2)
            next_button_custom.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='we')

            # The command associated with this button is determined by def on_connection_type_change(*args)
            next_button_fnwbc = tk.Button(fiori_nwbc_frame, text="Find SAP System", background="black",
                                          foreground="white",
                                          width=40, height=2)
            next_button_fnwbc.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='we')

            # Initially hide the form
            custom_system_form_frame.pack()
            fiori_nwbc_frame.pack_forget()

            def on_connection_type_change(*args):
                if connection_type.get() == 0:
                    custom_system_form_frame.pack()  # Show the custom system form
                    fiori_nwbc_frame.pack_forget()

                    next_button_custom.config(command=lambda: get_custom_sap_system(menu_frame, xml_path,
                                                                                    server_address_entry.get(),
                                                                                    sys_id_entry.get()
                                                                                    , None, "removal"))

                elif connection_type.get() == 1:
                    custom_system_form_frame.pack_forget()
                    fiori_nwbc_frame.pack()

                    next_button_fnwbc.config(command=lambda: get_fnwbc_system(menu_frame, xml_path,
                                                                              fiori_nwbc_urls.get(),
                                                                              None, "removal"))

                # Attach the handler to the radio button selection variable

            connection_type.trace("w", on_connection_type_change)

            # Create a frame for 'Exit' and 'Back' buttons
            button_frame = tk.Frame(menu_frame)
            button_frame.pack(side="bottom")
            # Create 'Exit' and 'Back' buttons in the button_frame
            back_button = tk.Button(
                master=button_frame,
                text="Restart",
                background="black",
                foreground="white",
                width=25,
                height=2,
                command=lambda: UiUtils.restart_program()
            )
            back_button.pack(side='right', anchor='se', padx=5, pady=5)

            exit_button = tk.Button(
                master=button_frame,
                text="Exit",
                background="black",
                foreground="white",
                width=25,
                height=2,
                command=menu_frame.quit
            )
            exit_button.pack(side='right', anchor='se', padx=5, pady=5)
            main_menu_button = tk.Button(master=button_frame, text="Back", background="black",
                                         foreground="white",
                                         width=25,
                                         height=2,
                                         command=lambda: remove_system_window(menu_frame),
                                         )
            main_menu_button.pack(side='right', anchor='se', padx=5, pady=5)
            # Attach the handler to the radio button selection variable
            connection_type.trace("w", on_connection_type_change)

    next_button = tk.Button(menu_frame, text="Next", background="black", foreground="white", width=10, height=2,
                            command=proceed_to_next)
    next_button.pack(pady=10)

    UiUtils.create_exit_restart_back_buttons(menu_frame)
