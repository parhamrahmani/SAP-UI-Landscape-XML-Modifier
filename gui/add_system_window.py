import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter

from utils.xml_utils import add_custom_system_type


def add_system_window(menu_frame):
    def select_source_xml_file():
        xml_file_path = filedialog.askopenfilename(initialdir="/", title="Select source XML file",
                                                   filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
        if xml_file_path:
            xml_path_entry.delete(0, tk.END)  # Clear the entry field
            xml_path_entry.insert(tk.END, xml_file_path)  # Insert the selected file path

    def select_destination_xml_file():
        xml_file_path = filedialog.askopenfilename(initialdir="/", title="Select destination XML file",
                                                   filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
        if xml_file_path:
            xml_path_entry2.delete(0, tk.END)  # Clear the entry field
            xml_path_entry2.insert(tk.END, xml_file_path)  # Insert the selected file path

    def proceed_to_next():
        source_xml_path = xml_path_entry.get()
        destination_xml_path = xml_path_entry2.get()

        if not source_xml_path.endswith('.xml') or not destination_xml_path.endswith('.xml'):
            messagebox.showwarning("Invalid File Warning", "Please enter valid XML file paths.")
        else:
            clear_frame(menu_frame)  # Clear the menu_frame

            # create a label for source file
            source_file_label = tk.Label(menu_frame, text=f"Please select connection type: ",
                                         font=("Arial", 12, "bold"), fg="black", bg="white")
            source_file_label.pack(pady=10)

            # create radio buttons for choosing the connection type
            connection_type = tk.IntVar()
            radiobutton_1 = tk.Radiobutton(menu_frame, bg="white",fg="black", text="1. Custom Application Server",font=("Arial", 12, "bold") , variable=connection_type,
                                           value=1)
            radiobutton_1.pack(pady=5,  anchor='center')
            radiobutton_2 = tk.Radiobutton(menu_frame,bg="white",fg="black",  text="2. Group/Server Selection", font=("Arial", 12, "bold") ,variable=connection_type,
                                           value=2)
            radiobutton_2.pack(pady=5,  anchor='center')

            # Create a separate frame to contain the form
            form_frame = tk.Frame(menu_frame, bg='white')
            form_frame.pack(pady=40)

            # Create the form fields
            applicationServer_entry = tk.Entry(form_frame, bg='white', fg='black', font=("Arial", 12))
            applicationServer_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
            applicationServer_label = tk.Label(form_frame, text="Application Server", bg='white', fg='black',
                                               font=("Arial", 12))
            applicationServer_label.grid(row=0, column=0, padx=5, pady=5)

            instanceNumber_entry = tk.Entry(form_frame, bg='white', fg='black', font=("Arial", 12))
            instanceNumber_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
            instanceNumber_label = tk.Label(form_frame, text="Instance Number", bg='white', fg='black',
                                            font=("Arial", 12))
            instanceNumber_label.grid(row=1, column=0, padx=5, pady=5)

            systemID_entry = tk.Entry(form_frame, bg='white', fg='black', font=("Arial", 12))
            systemID_entry.grid(row=2, column=1, padx=5, pady=5, sticky='we')
            systemID_label = tk.Label(form_frame, text="System ID", bg='white', fg='black', font=("Arial", 12))
            systemID_label.grid(row=2, column=0, padx=5, pady=5)

            # Configuring the column's weight to ensure they take up the full space
            form_frame.grid_columnconfigure(1, weight=1)

            # Create a button to send infroamtion to the next function
            next_button = tk.Button(form_frame, text="Next", background="black", foreground="white", width=40, height=2)
            next_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='we')

            # Initially hide the form
            form_frame.pack_forget()

            def on_connection_type_change(*args):
                if connection_type.get() == 1:
                    form_frame.pack()  # Show the form
                    next_button.config(command=lambda: add_custom_system_type(source_xml_path, destination_xml_path,
                                                                              applicationServer_entry.get(),
                                                                              instanceNumber_entry.get(),
                                                                              systemID_entry.get()))
                elif connection_type.get() == 2:
                    form_frame.pack_forget()  # Hide the form
                    next_button.config(command=None)

            # Attach the handler to the radio button selection variable
            connection_type.trace("w", on_connection_type_change)

            # Create a frame for 'Exit' and 'Back' buttons
            button_frame = tk.Frame(menu_frame)
            button_frame.pack(side="bottom")
            # Create 'Exit' and 'Back' buttons in the button_frame
            create_exit_restart_buttons(button_frame)

    from gui.menu import clear_frame, create_exit_restart_buttons
    # Clear the main window
    clear_frame(menu_frame)

    description_label = tk.Label(
        menu_frame,
        text="Warnings:\n\n"
             "1. This function will add a system from your existing SAP Logon XML file\n to another XML file."
             "\n\n2. Please make sure that the system you want to add is already added to your \nexisting XML file by SAP Logon,"
             " and the destination XML file has the right structure."
             "\n\n3. Always make a backup of your XML files before using this function.",
        font=("Arial", 10, "bold"),
        bg="white",
        anchor='w',
        justify='left'
    )
    description_label.pack(pady=10)

    file_label = tk.Label(menu_frame, text="\n\nPlease put the address of your source XML file",
                          font=("Arial", 10, "bold"),
                          bg="white")
    file_label.pack(pady=10)
    entry_frame = tk.Frame(menu_frame)
    entry_frame.pack(pady=10)
    xml_path_entry = tk.Entry(entry_frame, width=50)  # Entry widget to input XML file path
    xml_path_entry.pack(side='left')
    browse_button = tk.Button(entry_frame, text="Browse", command=select_source_xml_file, background="black",
                              foreground="white")
    browse_button.pack(side='left', padx=5)

    file_label2 = tk.Label(menu_frame, text="\n\nPlease put the address of your destination XML file",
                           font=("Arial", 10, "bold"),
                           bg="white")
    file_label2.pack(pady=10)
    second_entry_frame = tk.Frame(menu_frame)
    second_entry_frame.pack(pady=10)
    xml_path_entry2 = tk.Entry(second_entry_frame, width=50)  # Entry widget to input XML file path
    xml_path_entry2.pack(side='left')
    browse_button2 = tk.Button(second_entry_frame, text="Browse", command=select_destination_xml_file,
                               background="black",
                               foreground="white")
    browse_button2.pack(side='left', padx=5)

    next_button = tk.Button(menu_frame, text="Next", background="black", foreground="white", width=10, height=2,
                            command=proceed_to_next)
    next_button.pack(pady=10)

    create_exit_restart_buttons(menu_frame)
