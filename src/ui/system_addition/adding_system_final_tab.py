from tkinter import messagebox
from tkinter import ttk

from src.ui.ui_components.ui_utils import UiUtils
from src.utils.xml_utils.xml_query import XMLQuery
from src.utils.xml_utils.system_addition_utils import SystemAddition
import tkinter as tk


def system_adding_tab(frame, sap_system, source_xml_path, destination_xml_path):
    """
    Creates a new tab in the GUI for adding an SAP system to a workspace and node.

    Parameters
    ----------
    frame : tk.Frame
        The parent tkinter frame where the new tab will be created.

    sap_system : dict
        A dictionary containing SAP system details. The dictionary includes 'name', 'server', 'systemid' and
        optional 'routerid' for the system to be added.
    """

    # Clear the frame
    UiUtils.clear_frame(frame)

    workspaces = XMLQuery.find_all_workspaces(destination_xml_path)
    system_to_add = sap_system
    router_bool = sap_system.get('routerid') is not None
    message_server_bool = sap_system.get('msid') is not None
    url_bool = sap_system.get('url') is not None

    # Create a Frame for the tab
    tab_frame = tk.Frame(frame, bg='white')
    tab_frame.pack(pady=10)

    selected_workspace = tk.StringVar(tab_frame)
    selected_node = tk.StringVar(tab_frame)
    new_name = tk.StringVar(tab_frame)

    router = XMLQuery.find_router(source_xml_path, sap_system.get('routerid')) if router_bool else None
    router_address = router.get('name') if router is not None else None
    message_server = XMLQuery.find_message_server(source_xml_path,
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

    # Create a label for a new name
    new_name_label = tk.Label(tab_frame,
                              text=f"Please enter a new name for the system:"
                                   f" (Default = {sap_system.get('name')}) ",
                              font=("Arial", 10, "bold"), fg="black", bg="white")
    new_name_label.grid(row=len(label_info), column=0, columnspan=2, pady=10)

    # Create a label and text entry box for the new name
    new_name_entry_label = tk.Label(tab_frame, text="New Name: ", font=("Arial", 10, "bold"), fg="black",
                                    bg="white")
    new_name_entry_label.grid(row=len(label_info) + 1, column=0, sticky='w')
    name_options = [system_to_add.get('name')]
    new_name_combobox = ttk.Combobox(tab_frame, textvariable=new_name, values=name_options,
                                     state='normal')
    new_name_combobox.grid(row=len(label_info) + 1, column=1, sticky='w')
    new_name_combobox.current(0)

    # Create a label for source file
    tab_label = tk.Label(tab_frame,
                         text=f"Please select which Workspace and Node You want to add the system to: ",
                         font=("Arial", 10, "bold"), fg="black", bg="white")
    tab_label.grid(row=len(label_info) + 2, column=0, columnspan=2, pady=10)

    # Create a label and dropdown menu for the workspaces
    workspace_label = tk.Label(tab_frame, text="Workspace: ", font=("Arial", 10, "bold"), fg="black",
                               bg="white")
    workspace_label.grid(row=len(label_info) + 3, column=0, sticky='w')

    workspace_options = [ws.get('name') for ws in workspaces]
    workspace_combobox = ttk.Combobox(tab_frame, textvariable=selected_workspace, values=workspace_options,
                                      state='normal')  # Change state to 'normal'
    workspace_combobox.grid(row=len(label_info) + 3, column=1, sticky='w')
    workspace_combobox.current(0)

    # Create a label and dropdown menu for the nodes
    node_label = tk.Label(tab_frame, text="Node: ", font=("Arial", 10, "bold"), fg="black", bg="white")
    node_label.grid(row=len(label_info) + 4, column=0, sticky='w')

    node_combobox = ttk.Combobox(tab_frame, textvariable=selected_node, values=[],
                                 state='normal')  # Change state to 'normal'
    node_combobox.grid(row=len(label_info) + 4, column=1, sticky='w')

    def update_nodes(*args):
        """
        Updates the node dropdown menu in the GUI when a new workspace is selected. This function is
        meant to be used as a callback when the selected workspace changes. It lists all the nodes
        associated with the selected workspace, populates them into the node dropdown menu, and enables
        or disables the menu based on whether nodes are available.
        """
        nodes = XMLQuery.find_all_nodes_of_workspace(destination_xml_path, selected_workspace.get())
        node_combobox['values'] = nodes  # Update the values in the Combobox
        if len(nodes) == 1:
            selected_node.set(nodes[0])  # Clear the selected node value
        if nodes:
            node_combobox.config(state="normal")
        else:
            node_combobox.config(state="normal")

    selected_workspace.trace('w', update_nodes)

    if not message_server_bool and sap_system.get('server') is not None:
        submit_button = tk.Button(tab_frame, text="Submit", font=("Arial", 12, "bold"), fg="white",
                                  bg="black", padx=10, pady=3,
                                  command=lambda: SystemAddition.add_system(sap_system, source_xml_path,
                                                                            destination_xml_path,
                                                                            selected_workspace.get(),
                                                                            selected_node.get(),
                                                                            'Custom Application Server',
                                                                            new_name.get()))
        submit_button.grid(row=len(label_info) + 5, column=0, columnspan=2, pady=10)
    elif message_server_bool and sap_system.get('server') is not None and sap_system.get(
            'systemid') is not None:
        submit_button = tk.Button(tab_frame, text="Submit", font=("Arial", 12, "bold"), fg="white",
                                  bg="black", padx=10, pady=3,
                                  command=lambda: SystemAddition.add_system(sap_system, source_xml_path,
                                                                            destination_xml_path,
                                                                            selected_workspace.get(),
                                                                            selected_node.get(),
                                                                            'Group/Server Connection',
                                                                            new_name.get()))
        submit_button.grid(row=len(label_info) + 5, column=0, columnspan=2, pady=10)
    elif url_bool:
        submit_button = tk.Button(tab_frame, text="Submit", font=("Arial", 12, "bold"), fg="white",
                                  bg="black", padx=10, pady=3,
                                  command=lambda: SystemAddition.add_system(sap_system, source_xml_path,
                                                                            destination_xml_path,
                                                                            selected_workspace.get(),
                                                                            selected_node.get(),
                                                                            'FIORI/NWBC Connection',
                                                                            new_name.get()))
        submit_button.grid(row=len(label_info) + 5, column=0, columnspan=2, pady=10)
    else:
        messagebox.showwarning("Error", "The system you are trying to add is not supported. ")

    UiUtils.create_exit_restart_back_buttons(frame)
