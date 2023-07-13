import logging
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import xml.etree.ElementTree as ET

from ui.forms import create_custom_system_form, create_group_server_form, create_fiori_nwbc_form
from ui.ui_utils import clear_frame, create_exit_restart_back_buttons
from utils.xml_utils import select_xml_file, find_custom_system, find_router, find_group_server_connections, \
    find_fiori_nwbc_system, find_message_server, remove_a_system


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
        xml_path = xml_path_entry.get()  # Retrieve the value from the entry widget when needed
        if xml_path == "" or not xml_path.endswith(".xml"):
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
                                           font=("Arial", 8, "bold"), variable=connection_type,
                                           value=1)
            radiobutton_1.grid(row=0, column=0, padx=10)  # pack replaced with grid

            radiobutton_2 = tk.Radiobutton(radio_button_frame, bg="white", fg="black", text="2. Group/Server Selection",
                                           font=("Arial", 8, "bold"), variable=connection_type,
                                           value=2)
            radiobutton_2.grid(row=0, column=1, padx=10)
            radiobutton_3 = tk.Radiobutton(radio_button_frame, bg="white", fg="black", text="3. FIORI/NWBC System",
                                           font=("Arial", 8, "bold"), variable=connection_type,
                                           value=3)
            radiobutton_3.grid(row=0, column=2, padx=10)
            app_server_entry, instance_num_entry, sys_id_entry, custom_system_form_frame = create_custom_system_form(
                xml_path,
                menu_frame)
            system_id_combobox, message_server_entry, sap_router_combobox, group_server_form_frame = create_group_server_form(
                xml_path, menu_frame)
            fiori_nwbc_name, fiori_nwbc_urls, fiori_nwbc_frame = create_fiori_nwbc_form(xml_path,
                                                                                        menu_frame)

            # Configuring the column's weight to ensure they take up the full space
            custom_system_form_frame.grid_columnconfigure(1, weight=1)

            # Create a button to send information to the next function
            # The command associated with this button is determined by def on_connection_type_change(*args)
            next_button_custom = tk.Button(custom_system_form_frame, text="Find SAP System", background="black",
                                           foreground="white",
                                           width=40, height=2)
            next_button_custom.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='we')
            # The command associated with this button is determined by def on_connection_type_change(*args)
            next_button_gsc = tk.Button(group_server_form_frame, text="Find SAP System", background="black",
                                        foreground="white",
                                        width=40, height=2)
            next_button_gsc.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='we')
            # The command associated with this button is determined by def on_connection_type_change(*args)
            next_button_fnwbc = tk.Button(fiori_nwbc_frame, text="Find SAP System", background="black",
                                          foreground="white",
                                          width=40, height=2)
            next_button_fnwbc.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='we')

            # Initially hide the form
            custom_system_form_frame.pack_forget()
            group_server_form_frame.pack_forget()
            fiori_nwbc_frame.pack_forget()

            def system_removal_tab(frame, sap_system):
                clear_frame(frame)

                system_to_add = sap_system
                router_bool = sap_system.get('routerid') is not None
                message_server_bool = sap_system.get('msid') is not None
                url_bool = sap_system.get('url') is not None

                # Create a Frame for the tab
                tab_frame = tk.Frame(frame, bg='white')
                tab_frame.pack(pady=10)

                router = find_router(xml_path, sap_system.get('routerid')) if router_bool else None
                router_address = router.get('name') if router is not None else None
                message_server = find_message_server(xml_path,
                                                     sap_system.get('msid')) if message_server_bool else None
                message_server_address = message_server.get('host') if message_server is not None else None

                label_info = [("Selected SAP System: ", system_to_add.get('name'))]
                if url_bool:
                    label_info.append(("URL: ", system_to_add.get('url')))
                else:
                    label_info.append(("System ID: ", system_to_add.get('systemid')))
                if router_bool:
                    label_info.append(("Router: ", router_address))
                if message_server_bool:
                    label_info.append(("Message Server: ", message_server_address))
                if not message_server_bool and sap_system.get('server') is not None:
                    label_info.append(("Server Address: ", system_to_add.get('server')))

                for i, (label_text, value_text) in enumerate(label_info):
                    label = tk.Label(tab_frame, text=label_text, font=("Arial", 10, "bold"), fg="black", bg="white")
                    value = tk.Label(tab_frame, text=value_text, font=("Arial", 10), fg="black", bg="white")
                    label.grid(row=i, column=0, sticky='w')
                    value.grid(row=i, column=1, sticky='w')

                sap_system_str = ET.tostring(sap_system, encoding='unicode')

                if not message_server_bool and sap_system.get('server') is not None:
                    submit_button = tk.Button(tab_frame, text="Remove the system", font=("Arial", 12, "bold"), fg="white",
                                              bg="black", padx=10, pady=3,
                                              command=lambda: remove_a_system(xml_path, sap_system_str))
                    submit_button.grid(row=len(label_info) + 3, column=0, columnspan=2, pady=10)
                elif message_server_bool and sap_system.get('server') is not None and sap_system.get(
                        'systemid') is not None:
                    submit_button = tk.Button(tab_frame, text="Remove the system", font=("Arial", 12, "bold"), fg="white",
                                              bg="black", padx=10, pady=3,
                                              command=lambda: remove_a_system(xml_path, sap_system_str))
                    submit_button.grid(row=len(label_info) + 3, column=0, columnspan=2, pady=10)
                elif url_bool:
                    submit_button = tk.Button(tab_frame, text="Remove the system", font=("Arial", 12, "bold"), fg="white",
                                              bg="black", padx=10, pady=3,
                                              command=lambda: remove_a_system(xml_path, sap_system_str))
                    submit_button.grid(row=len(label_info) + 3, column=0, columnspan=2, pady=10)
                else:
                    messagebox.showwarning("Error", "The system you are trying to add is not supported. ")

                create_exit_restart_back_buttons(frame)







            def get_custom_sap_system(frame):
                """
                Fetches details of an SAP system based on input parameters and asks for user confirmation. If the SAP
                system is found, it fetches the details and presents it to the user in a dialog box. User is asked to
                confirm if this is the SAP system they want to add. If confirmed, the system is then added to the
                system adding tab. In case of any exception during this process, it displays a warning message with
                exception details.
                """
                try:
                    sap_system = find_custom_system(xml_path,
                                                    app_server_entry.get(),
                                                    instance_num_entry.get(),
                                                    sys_id_entry.get())
                    if sap_system is not None:
                        system_info = f"Description: {sap_system.get('name')}\n\n" \
                                      f"Server Address: {sap_system.get('server')}\n\n" \
                                      f"System ID: {sap_system.get('systemid')}\n\n"
                        routerid = sap_system.get('routerid')
                        if routerid is not None:
                            router = find_router(xml_path_entry.get(), routerid)
                            router_address = router.get('name')
                            system_info += f"Router: {router_address}\n\n"

                        dialog_text = f"Is this the SAP System you want to add?\n\n{system_info}"
                        dialog_title = "Confirm System Details"

                        if messagebox.askyesno(dialog_title, dialog_text):
                            system_removal_tab(frame, sap_system)

                    else:
                        messagebox.showinfo("No matching system found", "Please check your inputs and try again.")
                except Exception as e:
                    messagebox.showwarning("Error in get_sap_system():", str(e))
                    logging.error(f"Error in get_sap_system(): {str(e)}")

            def get_group_server_system(frame):
                try:
                    sap_system, message_server, router = find_group_server_connections(xml_path,
                                                                                       system_id_combobox.get(),
                                                                                       message_server_entry.get(),
                                                                                       sap_router_combobox.get())
                    if sap_system is not None:
                        system_info = f"Description: {sap_system.get('name')}\n\n" \
                                      f"System ID: {sap_system.get('systemid')}\n\n" \
                                      f"Message Server Host: {message_server}\n\n" \
                                      f"SAPRouter: {router}\n\n"
                        dialog_text = f"Is this the SAP System you want to add?\n\n{system_info}"
                        dialog_title = "Confirm System Details"

                        if messagebox.askyesno(dialog_title, dialog_text):
                            system_removal_tab(frame, sap_system)

                    else:
                        messagebox.showinfo("No matching system found", "Please check your inputs and try again.")

                except Exception as e:
                    messagebox.showwarning("Error in get_group_server_system():", str(e))
                    logging.error(f"Error in get_group_server_system(): {str(e)}")

            def get_fnwbc_system(frame):
                try:
                    sap_system = find_fiori_nwbc_system(xml_path, fiori_nwbc_urls.get())
                    if sap_system is not None:
                        system_info = f"Description: {sap_system.get('name')}\n\n" \
                                      f"URL: {sap_system.get('url')}\n\n"
                        dialog_text = f"Is this the SAP System you want to add?\n\n{system_info}"
                        dialog_title = "Confirm System Details"

                        if messagebox.askyesno(dialog_title, dialog_text):
                            system_removal_tab(frame, sap_system)
                    else:
                        messagebox.showinfo("No matching system found", "Please check your inputs and try again.")

                except Exception as e:
                    messagebox.showwarning("Error in get_fnwbc_system():", str(e))
                    logging.error(f"Error in get_fnwbc_system(): {str(e)}")

            def on_connection_type_change(*args):
                if connection_type.get() == 1:
                    custom_system_form_frame.pack()  # Show the custom system form
                    group_server_form_frame.pack_forget()  # Hide the group server form
                    fiori_nwbc_frame.pack_forget()

                    next_button_custom.config(command=lambda: get_custom_sap_system(menu_frame))

                elif connection_type.get() == 2:
                    custom_system_form_frame.pack_forget()  # Hide the custom system form
                    fiori_nwbc_frame.pack_forget()

                    group_server_form_frame.pack()  # Show the group server form
                    next_button_gsc.config(command=lambda: get_group_server_system(menu_frame))
                elif connection_type.get() == 3:
                    custom_system_form_frame.pack_forget()
                    group_server_form_frame.pack_forget()
                    fiori_nwbc_frame.pack()

                    next_button_fnwbc.config(command=lambda: get_fnwbc_system(menu_frame))

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
