import tkinter as tk
from tkinter import ttk
from src.utils.xml_utils.xml_query import XMLQuery

WIDTH = 50
FONT_SIZE = 10


def create_custom_system_form(xml_file_path, frame):
    sys_addresses, sys_names, sys_ids = XMLQuery.get_all_custom_sap_gui_info(xml_file_path)
    # Create a separate frame to contain the form
    custom_system_form_frame = tk.Frame(frame, bg='white')
    custom_system_form_frame.pack(pady=40)

    # Sort sys_names alphabetically
    sorted_names = sorted(set(sys_names))
    sys_ids = sorted(set(sys_ids))
    sys_addresses = sorted(set(sys_addresses))

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

    system_id_options = [''] + sys_ids[0:]
    system_id_combobox = ttk.Combobox(custom_system_form_frame, values=system_id_options, width=WIDTH)
    system_id_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='we')

    system_id_label = tk.Label(custom_system_form_frame, text="System ID: ", bg='white', fg='black',
                               font=("Arial", FONT_SIZE))
    system_id_label.grid(row=0, column=0, padx=5, pady=5)

    sep = ttk.Separator(custom_system_form_frame, orient='horizontal')
    sep.grid(row=3, column=0, columnspan=2, sticky='we', padx=5, pady=5)

    router_box = ttk.Entry(custom_system_form_frame, width=WIDTH, state='readonly')
    router_box.grid(row=4, column=1, padx=5, pady=5, sticky='we')
    router_label = tk.Label(custom_system_form_frame, text="Router: ", bg='white', fg='black',
                            font=("Arial", FONT_SIZE))
    router_label.grid(row=4, column=0, padx=5, pady=5)

    message_server_box = ttk.Entry(custom_system_form_frame, width=WIDTH, state='readonly')
    message_server_box.grid(row=5, column=1, padx=5, pady=5, sticky='we')
    message_server_label = tk.Label(custom_system_form_frame, text="Message Server: ", bg='white', fg='black',
                                    font=("Arial", FONT_SIZE))
    message_server_label.grid(row=5, column=0, padx=5, pady=5)

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
            server_addresses, system_names = XMLQuery.find_system_info_based_on_sid(xml_file_path, sys_id)
            names_combobox['values'] = sorted(set(system_names))
            application_server_combobox['values'] = sorted(set(server_addresses))

            if len(server_addresses) == 1 and len(system_names) == 1:
                names_combobox.set(system_names[0])
                application_server_combobox.set(server_addresses[0])
                sys_router, sys_ms = XMLQuery.find_router_and_message_server_based_on_sid_and_server_address(xml_file_path,
                                                                                                    sys_id,
                                                                                                    application_server_combobox.get())
                router_box.config(state='normal')
                router_box.delete(0, tk.END)
                router_box.insert(0, sys_router)
                router_box.config(state='readonly')
                message_server_box.config(state='normal')
                message_server_box.delete(0, tk.END)
                message_server_box.insert(0, sys_ms)
                message_server_box.config(state='readonly')

            else:
                sys_name = names_combobox.get()
                server_address = application_server_combobox.get()

                if sys_name in system_names:
                    names_combobox.set(sys_name)
                    sys_router, sys_ms = XMLQuery.find_router_and_message_server_based_on_sid_and_server_address(xml_file_path,
                                                                                                        sys_id,
                                                                                                        server_address)
                    router_box.config(state='normal')
                    router_box.delete(0, tk.END)
                    router_box.insert(0, sys_router)
                    router_box.config(state='readonly')
                    message_server_box.config(state='normal')
                    message_server_box.delete(0, tk.END)
                    message_server_box.insert(0, sys_ms)
                    message_server_box.config(state='readonly')
                else:
                    names_combobox.set('')
                    router_box.config(state='normal')
                    router_box.delete(0, 'end')
                    router_box.config(state='readonly')
                    message_server_box.config(state='normal')
                    message_server_box.delete(0, 'end')
                    message_server_box.config(state='readonly')

                if server_address in server_addresses:
                    application_server_combobox.set(server_address)
                    system_names = XMLQuery.find_system_names_based_on_server_address(xml_file_path, server_address)
                    names_combobox['values'] = sorted(set(system_names))
                    names_combobox.set(system_names[0])
                    sys_router, sys_ms = XMLQuery.find_router_and_message_server_based_on_sid_and_server_address(xml_file_path,
                                                                                                        sys_id,
                                                                                                        server_address)
                    router_box.config(state='normal')
                    router_box.delete(0, tk.END)
                    router_box.insert(0, sys_router)
                    router_box.config(state='readonly')
                    message_server_box.config(state='normal')
                    message_server_box.delete(0, tk.END)
                    message_server_box.insert(0, sys_ms)
                    message_server_box.config(state='readonly')

                else:
                    application_server_combobox.set('Please select a server address ')
                    system_names = XMLQuery.find_system_names_based_on_server_address(xml_file_path, server_addresses[0])
                    names_combobox['values'] = sorted(set(system_names))
                    names_combobox.set('')
                    router_box.config(state='normal')
                    router_box.delete(0, 'end')
                    router_box.config(state='readonly')
                    message_server_box.config(state='normal')
                    message_server_box.delete(0, 'end')
                    message_server_box.config(state='readonly')

        else:
            application_server_combobox.set('')
            names_combobox.set('')
            system_id_combobox['values'] = [''] + sys_ids[0:]
            application_server_combobox['values'] = sys_addresses
            names_combobox['values'] = sys_names
            router_box.config(state='normal')
            router_box.delete(0, 'end')
            router_box.config(state='readonly')
            message_server_box.config(state='normal')
            message_server_box.delete(0, 'end')
            message_server_box.config(state='readonly')

    # Bind the update_options function to the ComboboxSelected event
    system_id_combobox.bind('<<ComboboxSelected>>', update_options)
    application_server_combobox.bind('<<ComboboxSelected>>', update_options)
    names_combobox.bind('<<ComboboxSelected>>', update_options)
    router_box.bind('<<ComboboxSelected>>', update_options)

    return application_server_combobox, names_combobox, system_id_combobox, custom_system_form_frame


def create_fiori_nwbc_form(xml_file_path, frame):
    # Create a separate frame to contain the form
    fiori_nwbc_form_frame = tk.Frame(frame, bg='white')
    fiori_nwbc_form_frame.pack(pady=40)

    # Create the form fields
    fiori_nwbc_system_options = XMLQuery.find_all_fiori_nwbc_system_names(xml_file_path)
    fiori_nwbc_system_options = sorted(set(fiori_nwbc_system_options))
    fiori_nwbc_name_combobox = ttk.Combobox(fiori_nwbc_form_frame, values=[''] + fiori_nwbc_system_options[0:],
                                            font=("Arial", FONT_SIZE),
                                            width=WIDTH)
    fiori_nwbc_name_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='we')
    fiori_nwbc_name_label = tk.Label(fiori_nwbc_form_frame, text="Name: ", bg='white', fg='black',
                                     font=("Arial", FONT_SIZE))
    fiori_nwbc_name_label.grid(row=0, column=0, padx=5, pady=5)

    urls = XMLQuery.get_all_urls(xml_file_path)

    url_combobox = ttk.Combobox(fiori_nwbc_form_frame, values=urls, font=("Arial", FONT_SIZE),
                                width=WIDTH)
    url_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='we')
    url_label = tk.Label(fiori_nwbc_form_frame, text="URL: ", bg='white', fg='black', font=("Arial", FONT_SIZE))
    url_label.grid(row=1, column=0, padx=5, pady=5)

    def update_options(*args):
        name = fiori_nwbc_name_combobox.get()

        if name and name != '':
            found_urls = XMLQuery.find_urls_based_on_name(xml_file_path, name)
            options = sorted(set(found_urls))
            url_combobox['values'] = options
            url_combobox.set(options[0])

        else:
            url_combobox.set('')  # Clear the URL Combobox

    url_combobox.bind('<<ComboboxSelected>>', update_options)
    fiori_nwbc_name_combobox.bind('<<ComboboxSelected>>', update_options)

    return fiori_nwbc_name_combobox, url_combobox, fiori_nwbc_form_frame
