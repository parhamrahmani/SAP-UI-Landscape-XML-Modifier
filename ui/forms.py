import tkinter as tk
from tkinter import ttk

from utils.xml_utils import list_system_ids_for_group_server_connection_entry, find_message_server_based_on_system_id, \
    get_all_routers, get_all_urls, get_all_custom_sap_gui_info, find_all_system_ids_based_on_server_address, \
    find_all_instance_numbers_based_on_server_address

WIDTH = 50
FONT_SIZE = 10


def create_custom_system_form(xml_file_path, frame):
    # Create a separate frame to contain the form
    custom_system_form_frame = tk.Frame(frame, bg='white')
    custom_system_form_frame.pack(pady=40)

    # Create the form fields
    sys_addresses, sys_instances, sys_ids = get_all_custom_sap_gui_info(xml_file_path)
    application_server_combobox = ttk.Combobox(custom_system_form_frame, values=sys_addresses, width=WIDTH)
    application_server_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='we')
    application_server_label = tk.Label(custom_system_form_frame, text="Application Server: ", bg='white', fg='black',
                                        font=("Arial", FONT_SIZE))
    application_server_label.grid(row=0, column=0, padx=5, pady=5)

    instance_options = sys_instances
    instance_number_combobox = ttk.Combobox(custom_system_form_frame, values=instance_options, width=WIDTH)
    instance_number_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='we')
    instance_number_label = tk.Label(custom_system_form_frame, text="Instance Number: ", bg='white', fg='black',
                                     font=("Arial", FONT_SIZE))
    instance_number_label.grid(row=1, column=0, padx=5, pady=5)

    system_id_options = sys_ids
    system_id_combobox = ttk.Combobox(custom_system_form_frame, values=system_id_options, width=WIDTH)
    system_id_combobox.grid(row=2, column=1, padx=5, pady=5, sticky='we')

    system_id_label = tk.Label(custom_system_form_frame, text="System ID: ", bg='white', fg='black',
                               font=("Arial", FONT_SIZE))
    system_id_label.grid(row=2, column=0, padx=5, pady=5)


    def update_instance_numbers_options(*args):
        server_address = application_server_combobox.get()
        instance_numbers = find_all_instance_numbers_based_on_server_address(xml_file_path, server_address)
        instance_number_combobox['values'] = instance_numbers
        # Run update_instance_numbers_options whenever application_server_combobox changes

    application_server_combobox.bind('<KeyRelease>', update_instance_numbers_options)
    application_server_combobox.bind('<<ComboboxSelected>>', update_instance_numbers_options)

    def update_system_id_options(*args):
        server_address = application_server_combobox.get()
        server_instance = instance_number_combobox.get()
        if server_address and server_instance:  # Only proceed if server_address and server_instance are not empty
            system_ids = find_all_system_ids_based_on_server_address(xml_file_path, server_address, server_instance)
            system_id_combobox['values'] = system_ids
        else:  # If server_address or server_instance is empty
            system_id_combobox['values'] = []  # clear the combobox values

    # Run update_system_id_options whenever instance_number_combobox changes
    instance_number_combobox.bind('<KeyRelease>', update_system_id_options)
    instance_number_combobox.bind('<<ComboboxSelected>>', update_system_id_options)

    return application_server_combobox, instance_number_combobox, system_id_combobox, custom_system_form_frame


def create_group_server_form(xml_file_path, frame):
    # Create a separate frame to contain the form
    group_server_form_frame = tk.Frame(frame, bg='white')
    group_server_form_frame.pack(pady=40)

    # Create the form fields
    sysids = list_system_ids_for_group_server_connection_entry(xml_file_path)

    system_id_combobox = ttk.Combobox(group_server_form_frame, values=sysids, font=("Arial", FONT_SIZE), width=WIDTH)
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

    def update_message_server_entry(*args):
        system_id = system_id_combobox.get()
        if system_id:  # Only proceed if system_id is not empty
            message_server = find_message_server_based_on_system_id(xml_file_path, system_id)
            message_server_entry.delete(0, tk.END)  # clear the entry field
            if message_server is not None:
                message_server_entry.insert(0, message_server.get('host'))  # update the entry field
        else:  # If system_id is empty
            message_server_entry.delete(0, tk.END)  # clear the entry field

    # Run update_message_server_entry whenever system_id_combobox changes
    system_id_combobox.bind('<KeyRelease>', update_message_server_entry)
    system_id_combobox.bind('<<ComboboxSelected>>', update_message_server_entry)

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
    fiori_nwbc_name_entry = tk.Entry(fiori_nwbc_form_frame, bg='white', fg='black', font=("Arial", FONT_SIZE),
                                     width=WIDTH)
    fiori_nwbc_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we')
    fiori_nwbc_name_label = tk.Label(fiori_nwbc_form_frame, text="Name: ", bg='white', fg='black',
                                     font=("Arial", FONT_SIZE))
    fiori_nwbc_name_label.grid(row=0, column=0, padx=5, pady=5)

    urls = get_all_urls(xml_file_path)
    url_options = [url.get('url') for url in urls]
    url_combobox = ttk.Combobox(fiori_nwbc_form_frame, values=url_options, font=("Arial", FONT_SIZE), width=WIDTH)
    url_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='we')
    url_label = tk.Label(fiori_nwbc_form_frame, text="URL: ", bg='white', fg='black', font=("Arial", FONT_SIZE))
    url_label.grid(row=1, column=0, padx=5, pady=5)

    def update_name_entry(*args):
        url_address = url_combobox.get()
        url_name = None
        if url_address:  # Only proceed if url_address is not empty
            for url in urls:
                if url.get('url') == url_address:
                    url_name = url.get('name')  #
                    fiori_nwbc_name_entry.delete(0, tk.END)  # clear the entry field
                    if url_name is not None:
                        fiori_nwbc_name_entry.insert(0, url_name)
                    break
        else:  # If system_id is empty
            fiori_nwbc_name_entry.delete(0, tk.END)  # clear the entry field

    url_combobox.bind('<KeyRelease>', update_name_entry)
    url_combobox.bind('<<ComboboxSelected>>', update_name_entry)

    return fiori_nwbc_name_entry, url_combobox, fiori_nwbc_form_frame
