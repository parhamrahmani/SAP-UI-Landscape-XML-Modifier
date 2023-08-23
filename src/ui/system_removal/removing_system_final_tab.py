from tkinter import messagebox

from src.ui.ui_components.ui_utils import UiUtils
import tkinter as tk
import xml.etree.ElementTree as ET

from src.utils.xml_utils.system_removal_utils import SystemRemoval
from src.utils.xml_utils.xml_query import XMLQuery


def system_removal_tab(frame, sap_system, xml_path):
    UiUtils.clear_frame(frame)

    system_to_add = sap_system
    router_bool = sap_system.get('routerid') is not None
    message_server_bool = sap_system.get('msid') is not None
    url_bool = sap_system.get('url') is not None

    # Create a Frame for the tab
    tab_frame = tk.Frame(frame, bg='white')
    tab_frame.pack(pady=10)

    router = XMLQuery.find_router(xml_path, sap_system.get('routerid')) if router_bool else None
    router_address = router.get('name') if router is not None else None
    message_server = XMLQuery.find_message_server(xml_path,
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
        submit_button = tk.Button(tab_frame, text="Remove the system", font=("Arial", 12, "bold"),
                                  fg="white",
                                  bg="black", padx=10, pady=3,
                                  command=lambda: SystemRemoval.remove_a_system(xml_path, sap_system_str))
        submit_button.grid(row=len(label_info) + 3, column=0, columnspan=2, pady=10)
    elif message_server_bool and sap_system.get('server') is not None and sap_system.get(
            'systemid') is not None:
        submit_button = tk.Button(tab_frame, text="Remove the system", font=("Arial", 12, "bold"),
                                  fg="white",
                                  bg="black", padx=10, pady=3,
                                  command=lambda: SystemRemoval.remove_a_system(xml_path, sap_system_str))
        submit_button.grid(row=len(label_info) + 3, column=0, columnspan=2, pady=10)
    elif url_bool:
        submit_button = tk.Button(tab_frame, text="Remove the system", font=("Arial", 12, "bold"),
                                  fg="white",
                                  bg="black", padx=10, pady=3,
                                  command=lambda: SystemRemoval.remove_a_system(xml_path, sap_system_str))
        submit_button.grid(row=len(label_info) + 3, column=0, columnspan=2, pady=10)
    else:
        messagebox.showwarning("Error", "The system you are trying to remove is not supported. ")

    UiUtils.create_exit_restart_back_buttons(frame)
