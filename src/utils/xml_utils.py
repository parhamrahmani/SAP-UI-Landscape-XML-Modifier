import logging
import os
import sys
from tkinter import messagebox, filedialog
import tkinter as tk

import lxml.etree as le
import uuid
import xml.etree.ElementTree as ET
from src.utils.excel_utils import generate_excel_files
import pandas as pd


# Function to regenerate UUIDs for workspaces
def select_xml_file(xml_path_entry):
    """
        Function for opening a file dialog to select an XML file,
        and populating the xml_path_entry field with the chosen file's path.
        """
    xml_file_path = filedialog.askopenfilename(initialdir="/", title="Select source XML file",
                                               filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
    if xml_file_path:
        xml_path_entry.delete(0, tk.END)  # Clear the entry field
        xml_path_entry.insert(tk.END, xml_file_path)  # Insert the selected file path


def open_folder_containing_file(xml_file_path):
    folder_path = os.path.dirname(xml_file_path)
    os.startfile(folder_path)


def regenerate_workspace_uuids(workspaces):
    for workspace in workspaces:
        workspace.set('uuid', str(uuid.uuid4()))
        workspace.set('expanded', str(0))
        if workspace.get('name') == "Local" or workspace.get('name') == "local":
            workspace.set('name', "Default")


# Function to regenerate UUIDs for services and items
def regenerate_service_uuids(root):
    uuid_mapping = {}

    # Regenerate UUIDs for services
    for service in root.findall(".//Service"):
        old_uuid = service.get('uuid')
        new_uuid = str(uuid.uuid4())
        uuid_mapping[old_uuid] = new_uuid
        service.set('uuid', new_uuid)

    # Regenerate UUIDs for items and update service IDs
    for item in root.findall(".//Item"):
        item_uuid = item.get('uuid')
        new_item_uuid = str(uuid.uuid4())
        uuid_mapping[item_uuid] = new_item_uuid
        item.set('uuid', new_item_uuid)

        service_id = item.get('serviceid')
        if service_id in uuid_mapping:
            new_service_id = uuid_mapping[service_id]
            item.set('serviceid', new_service_id)


# Function to remove includes with URLs containing "SAPUILandscapeGlobal.xml"
def remove_global_includes(root):
    includes = root.findall(".//Include")
    filtered_includes = []

    for include in includes:
        include_url = include.get("url")
        if "SAPUILandscapeGlobal.xml" not in include_url:
            filtered_includes.append(include)

    if len(filtered_includes) < len(includes):

        root.findall(".//Includes")[0][:] = filtered_includes
        return True

    else:
        return False


def regenerate_uuids_export_excel(xml_file_path):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        workspaces = root.findall(".//Workspace")

        regenerate_workspace_uuids(workspaces)

        # Regenerating UUIDs
        for node in root.findall(".//Node"):
            node.set('uuid', str(uuid.uuid4()))

        regenerate_service_uuids(root)

        if remove_global_includes(root):
            messagebox.showinfo("Info", "The Inclusion of an URL containing 'SAPUILandscapeGlobal.xml' has been "
                                        "removed.")
        else:
            messagebox.showinfo("Info", "The XML file does not include 'SAPUILandscapeGlobal.xml'. No changes "
                                        "were made.")

        output_path = os.path.dirname(xml_file_path)
        output_name = os.path.basename(xml_file_path).split('.')[0] + "_modified"
        output_file = os.path.join(output_path, output_name + '.xml')

        for elem in root.iter('address'):
            elem.text = output_file

        tree.write(output_file)

        # Process the XML file and generate Excel files
        general_excel_file, duplicates_excel_file = generate_excel_files(output_file)

        messagebox.showinfo("Info", "The XML file has been successfully exported to: \n" + output_file
                            + "\n\n" + "General Excel file generated: \n" + general_excel_file
                            + "\n\n" + "Duplicates Excel file generated: \n" + duplicates_excel_file)

        open_folder_containing_file(output_file)

    except Exception as e:
        messagebox.showerror("Error!", f"An error occurred while processing the XML file: {str(e)}")
        logging.error(f"An error occurred while processing the XML file: {str(e)}")


# Function to add a new custom application server type of system to xml file
# Your find_custom_system() function is updated to return None when no service is found
def find_custom_system(xml_file_path, applicationServer, instanceNumber, systemID):
    try:
        server_address = applicationServer + ":32" + instanceNumber
        sap_system = None
        service_found = False

        # Parse the source XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        for service in root.findall(".//Service"):
            if service.get('server') == server_address:
                if service.get('systemid') == systemID:
                    sap_system = service
                    service_found = True
                    break
                elif service.get('systemid') is None:
                    raise Exception(f"Service with server address {server_address} "
                                    f"doesn't have a designated system ID")
                else:
                    raise Exception(f"Service with server address {server_address} "
                                    f"has a different system ID: {service.get('systemid')}")

        if not service_found:
            raise Exception(f"Service with server address {server_address} "
                            f"not found in XML file")

        return sap_system

    except Exception as e:
        print("Error in find_custom_system():", str(e))
        return None


def find_router(xml_file_path, routerid):
    # Parse the source XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    for router in root.findall(".//Router"):
        if router.get('uuid') == routerid:
            return router


def find_message_server(xml_file_path, msid):
    # Parse the source XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    for ms in root.findall(".//Messageserver"):
        if ms.get('uuid') == msid:
            return ms


def list_all_workspaces(xml_file_path):
    try:
        # Parse the destination XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        workspaces_el = root.find(".//Workspaces")
        if workspaces_el is not None:
            workspaces = workspaces_el.findall(".//Workspace")
            return workspaces
        else:
            workspaces_el = ET.SubElement(root, "Workspaces")
            workspaces = []
            return workspaces

    except Exception as e:
        messagebox.showwarning("Error in list_all_workspaces():", str(e))
        logging.error(f"Error in list_all_workspaces(): {str(e)}")
        return None


def list_nodes_of_workspace(xml_file_path, workspace_name):
    try:
        # Parse the destination XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        if root.tag != "Landscape":
            messagebox.showwarning("Error in XML structure:",
                                   "The root tag of the XML file should be <Landscape>. Please correct your XML file "
                                   "and try again."
                                   "\n\nThe XML file must be a SAP Landscape File!\n"
                                   "If your destination file is an empty XML file, please edit the xml file and add\n "
                                   "<Landscape> </Landscape> to it!\n")
            return None
        workspaces = root.findall(".//Workspace")
        node_names = []
        for ws in workspaces:
            if ws.get('name') == workspace_name:
                for node in ws.findall(".//Node"):
                    node_names.append(node.get('name'))
        return node_names
    except Exception as e:
        messagebox.showwarning("Error in list_nodes_of_workspace():", str(e))
        logging.error(f"Error in list_nodes_of_workspace(): {str(e)}")
        return []  # Return an empty list instead of None


def add_system(sap_system, root_xml_path, destination_xml_path, workspace_name, node_name, connection_type):
    try:
        status = False
        # Parse the destination XML file
        tree = ET.parse(destination_xml_path)
        root = tree.getroot()
        # Parse the root XML file
        source_tree = ET.parse(root_xml_path)
        source_root = source_tree.getroot()

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
                    if find_router(destination_xml_path, router.get('uuid')) is None:
                        routers.append(router)
                        break

        # Check for Message Servers
        if sap_system.get('msid') is not None:
            messageservers = root.find(".//Messageservers")
            if messageservers is None:
                messageservers = ET.SubElement(root,
                                               'Messageservers')  # Creates the Messageservers element if it does not exist

            for ms in source_root.findall(".//Messageserver"):
                # Find the message server in the source XML file
                if ms.get('uuid') == sap_system.get('msid'):
                    # Check if the message server is already in the destination file
                    if find_message_server(destination_xml_path, ms.get('uuid')) is None:
                        messageservers.append(ms)
                        break

        # Creating an Item and adding it to the specified Workspace and Node in the destination XML file
        workspaces = root.find(".//Workspaces")
        if workspaces is None:
            workspaces = ET.SubElement(root, 'Workspaces')

        # Get or create the workspace
        workspace = next((ws for ws in workspaces.findall(".//Workspace") if ws.get('name') == workspace_name), None)
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
                            open_folder_containing_file(destination_xml_path)
                            python = sys.executable
                            os.execl(python, python, *sys.argv)
                        return status
        return status

    except Exception as e:
        messagebox.showwarning("Error in add_system():", str(e))
        logging.error(f"Error in add_system(): {str(e)}")
        return False


def remove_elements_from_xml(xml_file_path, elements_to_remove, element_name):
    # Parse the XML file
    tree = le.parse(xml_file_path)
    root = tree.getroot()

    # Remove elements
    for elem_id in elements_to_remove:
        elements_to_remove = root.xpath(f".//{element_name}[@uuid='{elem_id}']")
        for elem in elements_to_remove:
            parent = elem.getparent()
            parent.remove(elem)

    return root


def remove_a_system(xml_file_path, sap_system_str):
    try:
        # Parse the sap_system string to get an lxml Element
        sap_system = ET.fromstring(sap_system_str)
        # Parse the XML file
        tree = le.parse(xml_file_path)
        root = tree.getroot()

        uuid_to_remove = sap_system.get('uuid')

        # Remove the matching Service from the XML file
        for service in root.findall(".//Service"):
            if service.get('uuid') == uuid_to_remove:
                # Get parent of the service
                parent = service.getparent()
                # Remove the service
                parent.remove(service)
                # Once we've removed the service, we can break from the loop
                break

        # Remove the matching Item from the XML file
        for item in root.findall(".//Item"):
            if item.get('serviceid') == uuid_to_remove:
                # Get parent of the item
                parent = item.getparent()
                # Remove the item
                parent.remove(item)
                # Once we've removed the item, we can break from the loop
                break

        # Save the XML file
        tree.write(xml_file_path, pretty_print=True)
        messagebox.showinfo("Success", "The SAP system is successfully removed from the XML file.\n\n")

        return True

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while removing the system: {str(e)}")
        logging.error(f"An error occurred while removing the system: {str(e)}")


def get_stats(xml_file_path):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    all_items = root.findall('.//Item')
    node_items = root.findall('.//Node/Item')
    child_node_items = root.findall('.//Node/Node/Item')
    workspaces = root.findall('.//Workspace')
    services = root.findall('.//Service')
    routers = root.findall('.//Router')
    messageservers = root.findall('.//Messageserver')

    stats = {
        "workspaces": len(workspaces),
        "items": len(all_items),
        "items in nodes": len(node_items),
        "items in child nodes": len(child_node_items),
        "services": len(services),
        "routers": len(routers),
        "message servers": len(messageservers)
    }

    return stats


# Function to remove duplications in the XML file
def remove_duplicates(xml_file_path):
    try:

        # Parse the XML file
        tree = le.parse(xml_file_path)
        root = tree.getroot()

        # Create a DataFrame from the XML data
        data = []  # List to store XML data

        for item in root.findall(".//Item"):
            item_id = item.get('uuid')
            service_id = item.get('serviceid')

            for service in root.findall(".//Service"):
                if service.get('uuid') == service_id:
                    service_name = service.get('name')
                    service_sid = service.get('systemid')

                    if service.get('type') == 'SAPGUI':
                        service_server = service.get('server')
                    else:
                        service_server = service.get('url')

                    data.append([
                        item_id,
                        service_id,
                        service_name,
                        service_sid,
                        service_server
                    ])

        df = pd.DataFrame(data, columns=['Item Id', 'Service Id', 'Service Name', 'Service SID', 'Service Server'])

        # Identify duplicate items based on service name, SID, and server
        duplicates = df[df.duplicated(subset=['Service SID', 'Service Server'], keep=False)].copy()

        # Add a new column to indicate the order of each item within its group of duplicates
        duplicates['Duplicate Order'] = duplicates.groupby(['Service SID', 'Service Server']).cumcount()

        # Only consider as duplicates those items that are not the last in their group
        duplicates_to_remove = duplicates[
            duplicates['Duplicate Order'] < duplicates.groupby(['Service SID', 'Service Server'])[
                'Duplicate Order'].transform('max')]

        # Get unique UUIDs of duplicate items and services to remove
        item_uuids = duplicates_to_remove['Item Id'].unique().tolist()
        service_uuids = duplicates_to_remove['Service Id'].unique().tolist()

        # Remove duplicate items and services
        for item_id in item_uuids:
            elements_to_remove = root.xpath(f".//Item[@uuid='{item_id}']")
            for elem in elements_to_remove:
                parent = elem.getparent()
                parent.remove(elem)

        for service_id in service_uuids:
            elements_to_remove = root.xpath(f".//Service[@uuid='{service_id}']")
            for elem in elements_to_remove:
                parent = elem.getparent()
                parent.remove(elem)

        output_path = os.path.dirname(xml_file_path)
        output_name = os.path.basename(xml_file_path).split('.')[0] + "_without_duplications"
        output_file = os.path.join(output_path, output_name + '.xml')
        tree.write(output_file)
        messagebox.showinfo("Success!", f"Duplications removed. Output file saved to: {output_file}")
        open_folder_containing_file(output_file)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while removing duplications: {str(e)}")
        logging.error(f"An error occurred while removing duplications: {str(e)}")


def list_system_ids_for_group_server_connection_entry(xml_file_path):
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        system_ids = []

        for service in root.findall(".//Service"):
            if service.get('msid') is not None:
                system_ids.append(service.get('systemid'))

        return system_ids

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while listing system IDs: {str(e)}")
        logging.error(f"An error occurred while listing system IDs: {str(e)}")


def find_message_server_based_on_system_id(xml_file_path, systemid):
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        message_server_id = None
        message_server = None
        message_servers = root.findall(".//Messageserver")
        services = root.findall(".//Service")

        for service in services:
            if service.get('msid') is not None:
                if service.get('systemid') == systemid:
                    message_server_id = service.get('msid')
                    break
        for ms in message_servers:
            if ms.get('uuid') == message_server_id:
                message_server = ms
                break
        return message_server

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while finding message server: {str(e)}")
        logging.error(f"An error occurred while finding message server: {str(e)}")


def get_all_routers(xml_file_path):
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        routers = root.findall(".//Router")
        return routers

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while finding message server: {str(e)}")
        logging.error(f"An error occurred while finding message server: {str(e)}")


def get_all_urls(xml_file_path):
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        services = root.findall(".//Service")
        urls = []
        for service in services:
            # Assuming the service name is also an attribute of the Service node
            if service.get('url') is not None and service.get('name') is not None:
                urls.append({'name': service.get('name'), 'url': service.get('url')})

        # Return the list of URLs
        return urls

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while finding NWBC/FIORI system urls: {str(e)}")
        logging.error(f"An error occurred while finding NWBC/FIORI system urls: {str(e)}")


def get_all_custom_sap_gui_info(xml_file_path):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    services = root.findall(".//Service")
    sap_gui_server_addresses = []
    sap_gui_system_ids = []
    sap_gui_instance_numbers = []
    for service in services:
        if service.get('type') == 'SAPGUI':
            if service.get('server') is not None:
                server = service.get('server')
                if ':32' in server:
                    address, port_with_extra_32 = server.split(':')
                    port = port_with_extra_32.split("32")[1]
                    sap_gui_server_addresses.append(address)
                    if port not in sap_gui_instance_numbers:
                        sap_gui_instance_numbers.append(port)
                    sap_gui_system_ids.append(service.get('systemid'))

    return sap_gui_server_addresses, sap_gui_instance_numbers, sap_gui_system_ids


def find_all_system_ids_based_on_server_address(xml_file_path, server_address, server_instance_number):
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        server = server_address + ":32" + server_instance_number
        system_ids = []

        for service in root.findall(".//Service"):
            if service.get('server') is not None:
                if service.get('server') == server:
                    system_ids.append(service.get('systemid'))

        return system_ids

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while listing system IDs: {str(e)}")
        logging.error(f"An error occurred while listing system IDs: {str(e)}")


def find_all_instance_numbers_based_on_server_address(xml_file_path, server_address):
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        instance_numbers = []

        for service in root.findall(".//Service"):
            if service.get('server') is not None:
                if server_address in service.get('server'):
                    server = service.get('server')
                    if ':32' in server:
                        address, port_with_extra_32 = server.split(':')
                        port = port_with_extra_32.split("32")[1]
                        if port not in instance_numbers:
                            instance_numbers.append(port)

        return instance_numbers

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while listing instance numbers: {str(e)}")
        logging.error(f"An error occurred while listing instance numbers: {str(e)}")


def find_group_server_connections(xml_file_path, system_id, message_server, router):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        possible_connections = []
        message_server_id = None
        router_id = None
        candidate_connection = None
        final_result = None

        for service in root.findall(".//Service"):
            if service.get('msid') is not None:
                if service.get('systemid') == system_id:
                    possible_connections.append({'serviceid': service.get('uuid'),
                                                 'msid': service.get('msid'),
                                                 'routerid': service.get('routerid')})
        for ms in root.findall(".//Messageserver"):
            if ms.get('host') == message_server:
                message_server_id = ms.get('uuid')
        for rt in root.findall(".//Router"):
            if rt.get('name') == router:
                router_id = rt.get('uuid')
        for gsc in possible_connections:
            if gsc.get('msid') == message_server_id and gsc.get('routerid') == router_id:
                candidate_connection = gsc

        if candidate_connection is not None:  # Add this check
            for service in root.findall(".//Service"):
                if service.get('uuid') == candidate_connection.get('serviceid'):
                    final_result = service

        return final_result, message_server, router

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while finding group/server connection: {str(e)}")
        logging.error(f"An error occurred while finding group/server connection: {str(e)}")


def find_sap_routers_based_on_system_id_message_server(xml_file_path, system_id, message_server_id):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        sap_routers = []

        for service in root.findall(".//Service"):
            if service.get('systemid') == system_id and service.get('msid') == message_server_id:
                sap_router_id = service.get('routerid')

                for router in root.findall(".//Router"):
                    if router.get('uuid') == sap_router_id:
                        sap_routers.append(router)
        return sap_routers

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while finding SAP router: {str(e)}")
        logging.error(f"An error occurred while finding SAP router: {str(e)}")


def find_fiori_nwbc_system(xml_file_path, url):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        fnwbc_system = None

        for service in root.findall(".//Service"):
            if service.get('url') is not None:
                if service.get('url') == url:
                    fnwbc_system = service

        return fnwbc_system

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while finding Fiori/NWBC systems: {str(e)}")
        logging.error(f"An error occurred while finding Fiori/NWBC systems: {str(e)}")


def add_root_tag_to_empty_xml_file(xml_file_path):
    try:
        with open(xml_file_path, 'r') as file:
            content = file.read().strip()  # This will remove leading/trailing whitespaces, newlines etc.

        if not content:
            with open(xml_file_path, 'w') as file:
                file.write("<Landscape></Landscape>")
    except FileNotFoundError:
        print(f"The file {xml_file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
