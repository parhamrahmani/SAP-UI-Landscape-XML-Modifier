import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from ui.ui_utils import clear_frame, create_exit_restart_back_buttons
from utils.xml_utils import select_xml_file


def remove_system_window(menu_frame):
    # Clear the main window
    clear_frame(menu_frame)

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
    from ui.menu import show_red_warning

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

    def proceed_to_next():
        if xml_path_entry.get() == "" or not xml_path_entry.get().endswith(".xml"):
            messagebox.showerror("Error", "Please enter a path to your XML file")
            return
        else:
            clear_frame(menu_frame)  # Clear the menu_frame

            # create a label for selecting connection type
            connection_type_label = tk.Label(menu_frame, text=f"Please select connection type: ",
                                             font=("Arial", 12, "bold"), fg="black", bg="white")
            connection_type_label.pack(pady=10)

            # create radio buttons for choosing the connection type
            connection_type = tk.IntVar()

            radio_button_frame = tk.Frame(menu_frame, bg="white")
            radio_button_frame.pack(pady=5, anchor='center')

            radiobutton_1 = tk.Radiobutton(radio_button_frame, bg="white", fg="black",
                                           text="1. Custom Application Server",
                                           font=("Arial", 12, "bold"), variable=connection_type,
                                           value=1)
            radiobutton_1.grid(row=0, column=0, padx=10)  # pack replaced with grid

            radiobutton_2 = tk.Radiobutton(radio_button_frame, bg="white", fg="black", text="2. Group/Server Selection",
                                           font=("Arial", 12, "bold"), variable=connection_type,
                                           value=2)
            radiobutton_2.grid(row=0, column=1, padx=10)
            # Create a separate frame to contain the form
            form_frame = tk.Frame(menu_frame, bg='white')
            form_frame.pack(pady=40)

            # Create the form fields
            application_server_entry = tk.Entry(form_frame, bg='white', fg='black', font=("Arial", 12))
            application_server_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
            application_server_label = tk.Label(form_frame, text="Application Server", bg='white', fg='black',
                                                font=("Arial", 12))
            application_server_label.grid(row=0, column=0, padx=5, pady=5)

            instance_number_entry = tk.Entry(form_frame, bg='white', fg='black', font=("Arial", 12))
            instance_number_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
            instance_number_label = tk.Label(form_frame, text="Instance Number", bg='white', fg='black',
                                             font=("Arial", 12))
            instance_number_label.grid(row=1, column=0, padx=5, pady=5)

            system_id_entry = tk.Entry(form_frame, bg='white', fg='black', font=("Arial", 12))
            system_id_entry.grid(row=2, column=1, padx=5, pady=5, sticky='we')
            system_id_label = tk.Label(form_frame, text="System ID", bg='white', fg='black', font=("Arial", 12))
            system_id_label.grid(row=2, column=0, padx=5, pady=5)

            # Configuring the column's weight to ensure they take up the full space
            form_frame.grid_columnconfigure(1, weight=1)

            # Create a button to send information to the next function
            next_button = tk.Button(form_frame, text="Find SAP System", background="black", foreground="white",
                                    width=40, height=2)
            next_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='we')

            # Initially hide the form
            form_frame.pack_forget()

            def on_connection_type_change(*args):
                """
                   Adjusts the GUI based on the user's chosen connection type.
                   If the user chooses the first type of connection (represented by 1),
                   a form is displayed and the "Next" button is configured to retrieve SAP system information.
                   If the user chooses the second type of connection (represented by 2), the form is hidden
                   and the "Next" button's action is removed.
                   """
                if connection_type.get() == 1:
                    form_frame.pack()  # Show the form
                    # Modify the button command to pass menu_frame as an argument
                    next_button.config(command=lambda: get_sap_system(menu_frame))

                elif connection_type.get() == 2:
                    form_frame.pack_forget()  # Hide the form
                    next_button.config(command=None)

        # Attach the handler to the radio button selection variable
        connection_type.trace("w", on_connection_type_change)

        # Create a frame for 'Exit' and 'Back' buttons
        button_frame = tk.Frame(menu_frame)
        button_frame.pack(side="bottom")
        # Create 'Exit' and 'Back' buttons in the button_frame
        create_exit_restart_back_buttons(button_frame)

        # Attach the handler to the radio button selection variable
        connection_type.trace("w", on_connection_type_change)

    next_button = tk.Button(menu_frame, text="Next", background="black", foreground="white", width=10, height=2,
                            command=proceed_to_next)
    next_button.pack(pady=10)

    create_exit_restart_back_buttons(menu_frame)
