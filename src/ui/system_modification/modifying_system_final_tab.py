from tkinter import ttk
import xml.etree.ElementTree as ET

from src.ui.ui_components.ui_utils import UiUtils
import tkinter as tk

from src.utils.xml_utils.system_modification_utils import SystemModification


def system_modification_tab(frame, sap_system, xml_path):
    UiUtils.clear_frame(frame)
    # Create a Frame for the tab
    tab_frame = tk.Frame(frame, bg='white')
    tab_frame.pack(pady=10)

    label_info = [("Selected SAP System: ", sap_system.get('name'))]
    if sap_system.get('type') == 'FIORI' or sap_system.get('type') == 'NWBC':
        label_info.append(("URL: ", sap_system.get('url')))
    elif sap_system.get('type') == 'SAPGUI':
        label_info.append(("Server Address: ", sap_system.get('server')))
        label_info.append(("System ID: ", sap_system.get('systemid')))

    for i, (label_text, value_text) in enumerate(label_info):
        label = tk.Label(tab_frame, text=label_text, font=("Arial", 10, "bold"), fg="black", bg="white")
        value = tk.Label(tab_frame, text=value_text, font=("Arial", 10), fg="black", bg="white")
        label.grid(row=i, column=0, sticky='w')
        value.grid(row=i, column=1, sticky='w')

    sep = ttk.Separator(tab_frame, orient='horizontal')
    sep.grid(row=4, columnspan=2, sticky='ew', pady=(10, 0))

    description_label = ttk.Label(tab_frame, text='Modify the SAP system details below:', font=("Arial", 10, "bold"))
    description_label.grid(row=5, columnspan=2, pady=(10, 0))

    sap_system_str = ET.tostring(sap_system, encoding='unicode')

    new_system_name = tk.StringVar(tab_frame)
    new_system_name.set(sap_system.get('name'))
    new_sys_id = tk.StringVar(tab_frame)
    new_sys_id.set(sap_system.get('systemid'))
    new_server = tk.StringVar(tab_frame)
    new_url = tk.StringVar(tab_frame)

    name_box = ttk.Entry(tab_frame, textvariable=new_system_name)
    systemid_box = ttk.Entry(tab_frame, textvariable=new_sys_id)

    name_box.grid(row=6, column=1, padx=20, pady=(10, 0))
    systemid_box.grid(row=7, column=1, padx=20, pady=(10, 0))

    name_label = tk.Label(tab_frame, text="New Name: ", font=("Arial", 10, "bold"), fg="black", bg="white")
    systemid_label = tk.Label(tab_frame, text="New System ID: ", font=("Arial", 10, "bold"), fg="black", bg="white")

    name_label.grid(row=6, column=0, sticky='w')
    systemid_label.grid(row=7, column=0, sticky='w')

    new_server.set(sap_system.get('server'))
    new_url.set(sap_system.get('url'))

    if sap_system.get('type') == 'SAPGUI':
        server_box = ttk.Entry(tab_frame, textvariable=new_server)
        server_box.grid(row=8, column=1, padx=20, pady=(10, 0))
        server_label = tk.Label(tab_frame, text="New Server: ", font=("Arial", 10, "bold"), fg="black", bg="white")
        server_label.grid(row=8, column=0, sticky='w')
        submit_button = tk.Button(tab_frame, text="Submit Changes", font=("Arial", 12, "bold"), fg="white",
                                  bg="black", padx=10, pady=3,
                                  command=lambda: SystemModification.modify_system(sap_system,
                                                                                   new_system_name.get(),
                                                                                   new_sys_id.get(),
                                                                                   new_server.get(),
                                                                                   sap_system.get('type'),
                                                                                   xml_path=xml_path))
        submit_button.grid(row=9, column=0, columnspan=2, pady=10)

    elif sap_system.get('type') == 'FIORI' or sap_system.get('type') == 'NWBC':
        systemid_box.config(state='disabled')
        url_box = ttk.Entry(tab_frame, textvariable=new_url)
        url_box.grid(row=8, column=1, padx=20, pady=(10, 0))
        url_label = tk.Label(tab_frame, text="New URL: ", font=("Arial", 10, "bold"), fg="black", bg="white")
        url_label.grid(row=8, column=0, sticky='w')
        submit_button = tk.Button(tab_frame, text="Submit Changes", font=("Arial", 12, "bold"), fg="white",
                                  bg="black", padx=10, pady=3,
                                  command=lambda: SystemModification.modify_system(sap_system,
                                                                                   new_system_name.get(),
                                                                                   new_sys_id.get(),
                                                                                   new_url.get(),
                                                                                   'FIORI/NWBC',
                                                                                   xml_path=xml_path))
        submit_button.grid(row=10, column=1, pady=(10, 0))

    UiUtils.create_exit_restart_back_buttons(frame)
