import logging
import os
import sys
import uuid
from tkinter import messagebox
from xml.etree import ElementTree as ET

from src.ui.ui_components.dialog_boxes import DialogBoxes
from src.utils.xml_utils.xml_query import XMLQuery


class SystemAddition:

    @staticmethod
    def add_system(sap_system, root_xml_path, destination_xml_path, workspace_name, node_name, connection_type,
                   new_name):
        try:
            status = False
            # Parse the destination XML file
            tree = ET.parse(destination_xml_path)
            root = tree.getroot()
            # Parse the root XML file
            source_tree = ET.parse(root_xml_path)
            source_root = source_tree.getroot()

            sap_system.set('name', new_name)

            # Add service to the destination XML file
            if root.find(".//Services") is None:
                services = ET.SubElement(root, 'Services')  # Creates the Services element
                sap_system.set('uuid', str(uuid.uuid4()))
                services.append(sap_system)
            else:
                services = root.find(".//Services")
                sap_system.set('uuid', str(uuid.uuid4()))
                services.append(sap_system)
            # Check if there is a Routers mentioned the SAP system, and they are also in the destination file
            if sap_system.get('routerid') is not None:
                routers = root.find(".//Routers")
                if routers is None:
                    routers = ET.SubElement(root, 'Routers')  # Creates the Routers element if it does not exist

                for router in source_root.findall(".//Router"):
                    # Find the router in the source XML file
                    if router.get('uuid') == sap_system.get('routerid'):
                        # Check if the router is already in the destination file
                        if XMLQuery.find_router(destination_xml_path, router.get('uuid')) is None:
                            routers.append(router)
                            break

            # Check for Message Servers
            if sap_system.get('msid') is not None:
                messageservers = root.find(".//Messageservers")
                if messageservers is None:
                    messageservers = ET.SubElement(root,
                                                   'Messageservers')  # Creates the Messageservers element if it does
                    # not exist

                for ms in source_root.findall(".//Messageserver"):
                    # Find the message server in the source XML file
                    if ms.get('uuid') == sap_system.get('msid'):
                        # Check if the message server is already in the destination file
                        if XMLQuery.find_message_server(destination_xml_path, ms.get('uuid')) is None:
                            messageservers.append(ms)
                            break

            # Creating an Item and adding it to the specified Workspace and Node in the destination XML file
            workspaces = root.find(".//Workspaces")
            if workspaces is None:
                workspaces = ET.SubElement(root, 'Workspaces')

            # Get or create the workspace
            workspace = next((ws for ws in workspaces.findall(".//Workspace") if ws.get('name') == workspace_name),
                             None)
            if workspace is None:
                workspace = ET.SubElement(workspaces, 'Workspace')
                workspace.set('uuid', str(uuid.uuid4()))
                workspace.set('name', workspace_name)
                workspace.set('expanded', "0")
                workspace.set('hidden', "0")

            # Get or create the node
            if node_name is not None and node_name != "":
                node = next((nd for nd in workspace.findall(".//Node") if nd.get('name') == node_name), None)
                if node is None:
                    node = ET.SubElement(workspace, 'Node')
                    node.set('uuid', str(uuid.uuid4()))
                    node.set('name', node_name)
                    node.set('expanded', "0")
                    node.set('hidden', "0")

                item_parent = node
            else:
                item_parent = workspace

            # Create the item
            item = ET.SubElement(item_parent, 'Item')
            item.set('uuid', str(uuid.uuid4()))
            item.set('serviceid', sap_system.get('uuid'))

            # Write the changes to the destination XML file
            tree.write(destination_xml_path)

            # Check if the sap system is successfully added to the destination XML file
            for item in root.findall(".//Item"):
                if item.get('serviceid') == sap_system.get('uuid'):
                    for service in root.findall(".//Service"):
                        if service.get('uuid') == sap_system.get('uuid'):
                            status = True
                            if connection_type == 'Custom Application Server':
                                # router_address = find_router(new_file_path, service.get('routerid')).get('name')
                                messagebox.showinfo("Success",
                                                    "The SAP system is successfully added to the destination XML "
                                                    "file.\n\n"
                                                    "System Info:\n"
                                                    f"System name: {service.get('name')}\n"
                                                    f"System ID: {service.get('systemid')}\n"
                                                    f"Application Server: {service.get('server')}\n"
                                                    # f"Router: {router_address}\n"
                                                    f"Connection Type: {connection_type}\n\n"


                                                    "Output file saved at: " + destination_xml_path)
                            elif connection_type == 'Group/Server Connection':
                                # message_server_address = find_message_server(new_file_path, service.get('msid')).get(
                                # 'host')

                                messagebox.showinfo("Success",
                                                    "The SAP system is successfully added to the destination XML "
                                                    "file.\n\n"
                                                    "System Info:\n"
                                                    f"System name: {service.get('name')}\n"
                                                    f"System ID: {service.get('systemid')}\n"
                                                    f"Application Server: {service.get('server')}\n"
                                                    # f"Message Server: {message_server_address} \n"
                                                    f"Connection Type: {connection_type}\n\n"
                                                    "Output file saved at: " + destination_xml_path)
                            elif connection_type == 'FIORI/NWBC Connection':
                                messagebox.showinfo("Success",
                                                    "The SAP system is successfully added to the destination XML "
                                                    "file.\n\n"
                                                    "System Info:\n"
                                                    f"System name: {service.get('name')}\n"
                                                    f"URL: {service.get('url')}\n"
                                                    f"Connection Type: {connection_type}\n\n"
                                                    "Output file saved at: " + destination_xml_path)
                            else:
                                messagebox.showinfo("Error",
                                                    "The SAP system is not successfully added to the destination XML "
                                                    "file.\n\n")

                            if messagebox.askyesno("Question", "Do you want to open the destination XML file?"):
                                DialogBoxes.open_folder_containing_file(destination_xml_path)
                                python = sys.executable
                                os.execl(python, python, *sys.argv)
                            return status
            return status

        except Exception as e:
            messagebox.showwarning("Error in add_system():", str(e))
            logging.error(f"Error in add_system(): {str(e)}")
            return False
