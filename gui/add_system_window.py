import logging
from tkinter import ttk
import tkinter as tk

from tkinter import filedialog, messagebox
import customtkinter
from tkinter import simpledialog
from utils.xml_utils import find_custom_system, find_router, list_all_workspaces, \
    list_nodes_of_workspace, add_custom_system



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
            radiobutton_2.grid(row=0, column=1, padx=10)  # pack replaced with grid

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
            next_button = tk.Button(form_frame, text="Find SAP System", background="black", foreground="white",
                                    width=40, height=2)
            next_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='we')

            # Initially hide the form
            form_frame.pack_forget()


            def system_adding_tab(frame, sap_system):

                # Clear the frame
                clear_frame(frame)

                workspaces = list_all_workspaces(destination_xml_path)
                system_to_add = sap_system
                router_bool = False

                if sap_system.get('routerid') is not None:
                    router_bool = True

                # Create a Frame for the tab
                tab_frame = tk.Frame(frame, bg='white')
                tab_frame.pack(pady=10)

                selected_workspace = tk.StringVar(tab_frame)
                selected_node = tk.StringVar(tab_frame)

                if router_bool:
                    # Create a frame to contain the labels

                    router_address = find_router(source_xml_path, sap_system.get('routerid')).get('name')
                    # Create labels for each piece of information
                    sap_system_name_label = tk.Label(tab_frame, text=f"Selected SAP System: ",
                                                     font=("Arial", 10, "bold"), fg="black", bg="white")
                    sap_system_name_value = tk.Label(tab_frame, text=f"{system_to_add.get('name')}", font=("Arial", 10),
                                                     fg="black", bg="white")

                    server_address_label = tk.Label(tab_frame, text=f"Server Address: ", font=("Arial", 10, "bold"),
                                                    fg="black", bg="white")
                    server_address_value = tk.Label(tab_frame, text=f"{system_to_add.get('server')}",
                                                    font=("Arial", 10), fg="black", bg="white")

                    system_id_label = tk.Label(tab_frame, text=f"System ID: ", font=("Arial", 10, "bold"), fg="black",
                                               bg="white")
                    system_id_value = tk.Label(tab_frame, text=f"{system_to_add.get('systemid')}", font=("Arial", 10),
                                               fg="black", bg="white")

                    router_string_label = tk.Label(tab_frame, text=f"Router String: ", font=("Arial", 10, "bold"),
                                                   fg="black", bg="white")
                    router_string_value = tk.Label(tab_frame, text=f"{router_address}", font=("Arial", 10), fg="black",
                                                   bg="white")

                    # Grid placement of the labels
                    sap_system_name_label.grid(row=0, column=0, sticky='w')
                    sap_system_name_value.grid(row=0, column=1, sticky='w')

                    server_address_label.grid(row=1, column=0, sticky='w')
                    server_address_value.grid(row=1, column=1, sticky='w')

                    system_id_label.grid(row=2, column=0, sticky='w')
                    system_id_value.grid(row=2, column=1, sticky='w')

                    router_string_label.grid(row=3, column=0, sticky='w')
                    router_string_value.grid(row=3, column=1, sticky='w')
                else:
                    sap_system_name_label = tk.Label(tab_frame, text=f"Selected SAP System: ",
                                                     font=("Arial", 10, "bold"), fg="black", bg="white")
                    sap_system_name_value = tk.Label(tab_frame, text=f"{system_to_add.get('name')}", font=("Arial", 10),
                                                     fg="black", bg="white")

                    server_address_label = tk.Label(tab_frame, text=f"Server Address: ", font=("Arial", 10, "bold"),
                                                    fg="black", bg="white")
                    server_address_value = tk.Label(tab_frame, text=f"{system_to_add.get('server')}",
                                                    font=("Arial", 10), fg="black", bg="white")

                    system_id_label = tk.Label(tab_frame, text=f"System ID: ", font=("Arial", 10, "bold"), fg="black",
                                               bg="white")
                    system_id_value = tk.Label(tab_frame, text=f"{system_to_add.get('systemid')}", font=("Arial", 10),
                                               fg="black", bg="white")
                    # Grid placement of the labels
                    sap_system_name_label.grid(row=0, column=0, sticky='w')
                    sap_system_name_value.grid(row=0, column=1, sticky='w')

                    server_address_label.grid(row=1, column=0, sticky='w')
                    server_address_value.grid(row=1, column=1, sticky='w')

                    system_id_label.grid(row=2, column=0, sticky='w')
                    system_id_value.grid(row=2, column=1, sticky='w')

                # Create a label for source file
                tab_label = tk.Label(tab_frame,
                                     text=f"Please select which Workspace and Node You want to add the system to: ",
                                     font=("Arial", 10, "bold"), fg="black", bg="white")
                tab_label.grid(row=4, column=0, columnspan=2, pady=10)

                # Create a label and dropdown menu for the workspaces
                workspace_label = tk.Label(tab_frame, text="Workspace: ", font=("Arial", 10, "bold"), fg="black",
                                           bg="white")
                workspace_label.grid(row=6, column=0, sticky='w')

                workspace_options = [ws.get('name') for ws in workspaces]
                workspace_combobox = ttk.Combobox(tab_frame, textvariable=selected_workspace, values=workspace_options,
                                                  state='readonly')
                workspace_combobox.grid(row=6, column=1, sticky='w')

                # Create a label and dropdown menu for the nodes
                node_label = tk.Label(tab_frame, text="Node: ", font=("Arial", 10, "bold"), fg="black", bg="white")
                node_label.grid(row=7, column=0, sticky='w')

                node_combobox = ttk.Combobox(tab_frame, textvariable=selected_node, values=[], state='readonly')
                node_combobox.grid(row=7, column=1, sticky='w')

                # Update nodes when a workspace is selected
                # Update nodes when a workspace is selected
                def update_nodes(*args):
                    nodes = list_nodes_of_workspace(destination_xml_path, selected_workspace.get())
                    node_combobox['values'] = nodes  # Update the values in the Combobox
                    selected_node.set('')  # Clear the selected node value
                    # If nodes are found, enable the node combobox
                    if nodes:
                        node_combobox.config(state="normal")
                    else:
                        node_combobox.config(state="disabled")  # If no nodes are found, disable the node combobox

                # Run update_nodes whenever selected_workspace changes
                selected_workspace.trace('w', update_nodes)

                # Create a Button for submitting the system to the destination XML file
                submit_button = tk.Button(tab_frame, text="Submit", font=("Arial", 12, "bold"), fg="white",
                                          bg="black",padx=10, pady=3, command=lambda: add_custom_system(sap_system, source_xml_path,
                                                                                        destination_xml_path,
                                                                                        selected_workspace.get(),
                                                                                        selected_node.get()))

                submit_button.grid(row=8, column=0, columnspan=2, pady=10)

                create_exit_restart_buttons(frame)

            def go_to_xml_input(frame):
                clear_frame(frame)
                add_system_window(frame)  # This will take the user back to the XML file paths input

                # Create a separate frame for system information
                message_field = tk.Frame(menu_frame, bg='white')
                message_field.pack(pady=10)  # Pack it after creation

            def get_sap_system(frame):
                try:
                    sap_system = find_custom_system(source_xml_path,
                                                    applicationServer_entry.get(),
                                                    instanceNumber_entry.get(),
                                                    systemID_entry.get())
                    if sap_system is not None:
                        system_info = f"Description: {sap_system.get('name')}\n\n" \
                                      f"Server Address: {sap_system.get('server')}\n\n" \
                                      f"System ID: {sap_system.get('systemid')}\n\n"
                        routerid = sap_system.get('routerid')
                        if routerid is not None:
                            router = find_router(source_xml_path, routerid)
                            router_address = router.get('name')
                            system_info += f"Router: {router_address}\n\n"

                        dialog_text = f"Is this the SAP System you want to add?\n\n{system_info}"
                        dialog_title = "Confirm System Details"

                        if messagebox.askyesno(dialog_title, dialog_text):
                            system_adding_tab(frame, sap_system)
                        else:
                            clear_frame(frame)
                            add_system_window(frame)

                    else:
                        messagebox.showinfo("No matching system found", "Please check your inputs and try again.")
                except Exception as e:
                    messagebox.showwarning("Error in get_sap_system():", str(e))
                    logging.error(f"Error in get_sap_system(): {str(e)}")

            def on_connection_type_change(*args):
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
            create_exit_restart_buttons(button_frame)

            # Attach the handler to the radio button selection variable
            connection_type.trace("w", on_connection_type_change)

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
