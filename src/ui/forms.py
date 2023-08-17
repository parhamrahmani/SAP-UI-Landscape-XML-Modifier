import tkinter as tk
from tkinter import ttk, messagebox
from ttkwidgets.autocomplete import AutocompleteEntry
from src.utils.xml_utils import list_system_ids_for_group_server_connection_entry, \
    find_message_server_based_on_system_id, \
    get_all_routers, get_all_urls, get_all_custom_sap_gui_info, \
 \
    find_sap_routers_based_on_system_id_message_server, find_system_info_on_system_id, \
    find_system_info_based_on_sid, find_system_names_based_on_server_address, find_all_fiori_nwbc_system_names, \
    find_urls_based_on_name

WIDTH = 50
FONT_SIZE = 10


def create_custom_system_form(xml_file_path, frame):
    sys_addresses, sys_names, sys_ids = get_all_custom_sap_gui_info(xml_file_path)
    # Create a separate frame to contain the form
    custom_system_form_frame = tk.Frame(frame, bg='white')
    custom_system_form_frame.pack(pady=40)

    # Sort sys_names alphabetically
    sorted_names = sorted(sys_names)
    sys_ids = sorted(sys_ids)
    sys_addresses = sorted(sys_addresses)

    # Create the form fields

    names_combobox = ttk.Combobox(custom_system_form_frame, values=sorted_names, width=WIDTH)
    names_combobox.grid(row=2, column=1, padx=5, pady=5, sticky='we')
    name_label = tk.Label(custom_system_form_frame, text="Name: ", bg='white', fg='black',
                          font=("Arial", FONT_SIZE))
    name_label.grid(row=2, column=0, padx=5, pady=5)

    application_server_combobox = ttk.Combobox(custom_system_form_frame,
                                               values=sys_addresses, width=WIDTH)
    application_server_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='we')
    application_server_label = tk.Label(custom_system_form_frame, text="Server Address: ", bg='white', fg='black',
                                        font=("Arial", FONT_SIZE))
    application_server_label.grid(row=1, column=0, padx=5, pady=5)

    system_id_options = [''] + sys_ids[1:]
    system_id_combobox = ttk.Combobox(custom_system_form_frame, values=system_id_options, width=WIDTH)
    system_id_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='we')

    system_id_label = tk.Label(custom_system_form_frame, text="System ID: ", bg='white', fg='black',
                               font=("Arial", FONT_SIZE))
    system_id_label.grid(row=0, column=0, padx=5, pady=5)

    # Define a filter function
    def filter_options(combobox, options):
        filter_text = combobox.get()
        filtered_options = [option for option in options if filter_text.lower() in option.lower()]
        combobox['values'] = filtered_options

    # Define a callback function for filtering options
    def on_combobox_key_release(event):
        filter_options(event.widget, system_id_options)  # Replace name_options with the appropriate options list

    # Bind the callback function to the KeyRelease event for each combo box
    system_id_combobox.bind('<KeyRelease>', on_combobox_key_release)

    def update_options(*args):
        sys_name = names_combobox.get()
        sys_id = system_id_combobox.get()
        server_address = application_server_combobox.get()

        if sys_id and sys_id != '':
            server_addresses, system_names = find_system_info_based_on_sid(xml_file_path, sys_id)
            names_combobox['values'] = system_names
            application_server_combobox['values'] = server_addresses

            if len(server_addresses) == 1 and len(system_names) == 1:
                names_combobox.set(system_names[0])
                application_server_combobox.set(server_addresses[0])
            else:
                sys_name = names_combobox.get()
                server_address = application_server_combobox.get()

                if sys_name in system_names:
                    names_combobox.set(sys_name)
                else:
                    names_combobox.set('')

                if server_address in server_addresses:
                    application_server_combobox.set(server_address)
                    system_names = find_system_names_based_on_server_address(xml_file_path, server_address)
                    names_combobox['values'] = system_names
                    names_combobox.set(system_names[0])
                else:
                    application_server_combobox.set('Please select a server address ')  # Select the first address
                    system_names = find_system_names_based_on_server_address(xml_file_path, server_addresses[0])
                    names_combobox['values'] = system_names
                    names_combobox.set('')

        else:
            application_server_combobox.set('')
            names_combobox.set('')
            system_id_combobox['values'] = [''] + sys_ids[1:]
            application_server_combobox['values'] = sys_addresses
            names_combobox['values'] = sys_names

    # Bind the update_options function to the ComboboxSelected event
    system_id_combobox.bind('<<ComboboxSelected>>', update_options)
    application_server_combobox.bind('<<ComboboxSelected>>', update_options)
    names_combobox.bind('<<ComboboxSelected>>', update_options)

    return application_server_combobox, names_combobox, system_id_combobox, custom_system_form_frame


def create_group_server_form(xml_file_path, frame):
    # Create a separate frame to contain the form
    group_server_form_frame = tk.Frame(frame, bg='white')
    group_server_form_frame.pack(pady=40)

    # Create the form fields
    sysids = list_system_ids_for_group_server_connection_entry(xml_file_path)

    system_id_combobox = ttk.Combobox(group_server_form_frame, values=[''] + sysids[1:], font=("Arial", FONT_SIZE),
                                      width=WIDTH)
    system_id_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='we')

    system_id_label = tk.Label(group_server_form_frame, text="System ID", bg='white', fg='black',
                               font=("Arial", FONT_SIZE))
    system_id_label.grid(row=0, column=0, padx=5, pady=5)

    message_server_entry = tk.Entry(group_server_form_frame, bg='white', fg='black', font=("Arial", FONT_SIZE),
                                    width=WIDTH)
    message_server_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')
    message_server_entry.insert(0, 'No message server found')
    message_server_label = tk.Label(group_server_form_frame, text="Message Server: ", bg='white', fg='black',
                                    font=("Arial", FONT_SIZE))
    message_server_label.grid(row=1, column=0, padx=5, pady=5)

    def update_comboboxes(*args):
        system_id = system_id_combobox.get()

        # Update message server
        if system_id and system_id != '':  # Only proceed if system_id is not empty
            message_server = find_message_server_based_on_system_id(xml_file_path, system_id)
            message_server_entry.delete(0, tk.END)  # clear the entry field
            if message_server is not None:
                message_server_entry.insert(0, message_server.get('host'))  # update the entry field
        else:  # If system_id is empty
            message_server_entry.delete(0, tk.END)  # clear the entry field

        # Update router combobox
        if system_id and system_id != '':  # Only proceed if system_id is not empty
            message_server = find_message_server_based_on_system_id(xml_file_path, system_id)
            sap_routers = find_sap_routers_based_on_system_id_message_server(xml_file_path, system_id,
                                                                             message_server.get('uuid'))
            sap_router_combobox.delete(0, tk.END)
            if sap_routers is not None and len(sap_routers) == 1:
                sap_router_combobox.insert(0, sap_routers[0].get('name'))
            else:
                sap_router_combobox['values'] = sap_routers

        else:  # If system_id is empty
            sap_router_combobox.delete(0, tk.END)  # clear the combobox values

    # Run update_comboboxes whenever system_id_combobox changes
    system_id_combobox.bind('<KeyRelease>', update_comboboxes)
    system_id_combobox.bind('<<ComboboxSelected>>', update_comboboxes)

    routers = get_all_routers(xml_file_path)
    router_options = [rt.get('name') for rt in routers]
    sap_router_combobox = ttk.Combobox(group_server_form_frame, values=router_options, font=("Arial", FONT_SIZE),
                                       width=WIDTH)
    sap_router_combobox.grid(row=2, column=1, padx=5, pady=5, sticky='we')
    sap_router_label = tk.Label(group_server_form_frame, text="SAPRouter: ", bg='white', fg='black',
                                font=("Arial", FONT_SIZE))
    sap_router_label.grid(row=2, column=0, padx=5, pady=5)

    return system_id_combobox, message_server_entry, sap_router_combobox, group_server_form_frame


def create_fiori_nwbc_form(xml_file_path, frame):
    # Create a separate frame to contain the form
    fiori_nwbc_form_frame = tk.Frame(frame, bg='white')
    fiori_nwbc_form_frame.pack(pady=40)

    # Create the form fields
    fiori_nwbc_system_options = find_all_fiori_nwbc_system_names(xml_file_path)
    fiori_nwbc_name_combobox = ttk.Combobox(fiori_nwbc_form_frame, values=[''] + fiori_nwbc_system_options[1:],
                                            font=("Arial", FONT_SIZE),
                                            width=WIDTH)
    fiori_nwbc_name_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='we')
    fiori_nwbc_name_label = tk.Label(fiori_nwbc_form_frame, text="Name: ", bg='white', fg='black',
                                     font=("Arial", FONT_SIZE))
    fiori_nwbc_name_label.grid(row=0, column=0, padx=5, pady=5)

    urls = get_all_urls(xml_file_path)

    url_combobox = ttk.Combobox(fiori_nwbc_form_frame, values=urls, font=("Arial", FONT_SIZE),
                                width=WIDTH)
    url_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='we')
    url_label = tk.Label(fiori_nwbc_form_frame, text="URL: ", bg='white', fg='black', font=("Arial", FONT_SIZE))
    url_label.grid(row=1, column=0, padx=5, pady=5)

    def update_options(*args):
        name = fiori_nwbc_name_combobox.get()

        if name and name != '':
            found_urls = find_urls_based_on_name(xml_file_path, name)
            url_combobox['values'] = found_urls

            # Autocomplete the URL if there's only one URL available
            if len(found_urls) == 1:
                url_combobox.set(found_urls[0])
            else:
                url_combobox.set('Please select a url')  # Clear the URL Combobox

        else:
            url_combobox.set('')  # Clear the URL Combobox
    url_combobox.bind('<<ComboboxSelected>>', update_options)
    fiori_nwbc_name_combobox.bind('<<ComboboxSelected>>', update_options)

    return fiori_nwbc_name_combobox, url_combobox, fiori_nwbc_form_frame
