from tkinter import messagebox

from utils.excel_utils import *
import lxml.etree as le
import uuid
import uuid
import xml.etree.ElementTree as ET
from utils.console import *


# Function to regenerate UUIDs for workspaces
def regenerate_workspace_uuids(workspaces):
    regenerate_all_uuids = get_user_input("Do you want to regenerate UUIDs for all workspaces? (y/n): ").lower() == "y"

    for workspace in workspaces:
        if regenerate_all_uuids or get_user_input(
                f"Regenerate UUID for workspace '{workspace.get('name')}'? (y/n): ").lower() == "y":
            workspace.set('uuid', str(uuid.uuid4()))
            workspace.set('expanded', str(0))
            new_workspace_name = get_user_input(f"Enter the new name for workspace '{workspace.get('name')}': ")
            workspace.set('name', new_workspace_name)


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
        prompt_message = "This XML file includes SAPUILandscapeGlobal.xml. In order to make this file " \
                         "into a central file, this inclusion has to be deleted. Do you want to delete it? (y/n): "
        remove_includes = get_user_input(prompt_message).lower() == "y"

        if remove_includes:
            root.findall(".//Includes")[0][:] = filtered_includes
            return True
        else:
            return False
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
            display_success("Global includes removed.")
        else:
            print("No include with URL containing 'SAPUILandscapeGlobal.xml' found.")

        output_path = get_user_input("Enter the output path for the modified XML file: ")
        output_name = get_user_input("Enter the name for your output file: ")
        output_file = os.path.join(output_path, output_name + '.xml')
        for elem in root.iter('address'):
            elem.text = output_file

        tree.write(output_file)
        display_success(f"Modified XML file saved as: {output_file}")

        # Exporting the XML file
        display_loading_bar()
        time.sleep(1)  # Simulating export delay

        # Process the XML file and generate Excel files
        general_excel_file, duplicates_excel_file = generate_excel_files(output_file)
        print("General Excel file generated:", general_excel_file)
        print("Duplicates Excel file generated:", duplicates_excel_file)

    except Exception as e:
        display_error(f"An error occurred while processing the XML file: {str(e)}")


# Function to add a new custom application server type of system to xml file
def add_custom_system_type(xml_file_path_source, xml_file_path_destination, applicationServer, instanceNumber, systemID):
    try:
        # Parse the source XML file
        tree = ET.parse(xml_file_path_source)
        root = tree.getroot()
        # Parse the destination XML file
        tree_destination = ET.parse(xml_file_path_destination)
        root_destination = tree_destination.getroot()









    except Exception as e:
        display_error(f"An error occurred while adding the custom system type to the XML file: {str(e)}")


def extract_from_nodes(xml_file_path):
    try:
        print("Processing XML file...")
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Get all Items
        all_items = root.findall('.//Item')

        # Create a new workspace element
        workspace = ET.SubElement(root.find('.//Workspaces'), 'Workspace')
        workspace.set('name', 'Extracted from Nodes')
        workspace.set('uuid', str(uuid.uuid4()))
        workspace.set('expanded', '0')

        # Move the Item elements to the workspace
        for item in all_items:
            workspace.append(item)

        # Remove other workspaces
        workspaces_to_delete = []
        for ws in root.findall('.//Workspace'):
            if ws.get('name') != 'Extracted from Nodes':
                workspaces_to_delete.append(ws.get('uuid'))

        temp_xml_file_path = r"C:\Users\PR106797\PycharmProjects\uuid_manipulator\cache\temp.xml"
        tree.write(temp_xml_file_path)

        # Modify the temporary XML file
        temp_root = remove_elements_from_xml(temp_xml_file_path, workspaces_to_delete, 'Workspace')

        # Prompt user for output file path and name
        output_file_path = input("Enter the output file path: ")
        output_file_name = input("Enter the output file name: ")

        # Save the modified XML to the specified location
        output_file_path_with_name = os.path.join(output_file_path, output_file_name + '.xml')
        temp_tree = ET.ElementTree(temp_root)
        temp_tree.write(output_file_path_with_name)
        print(f"XML file saved successfully at {output_file_path_with_name}")

    except Exception as e:
        print(f"An error occurred while processing the XML file: {str(e)}")


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
        print("Processing XML file...")
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

        # Get unique UUIDs of duplicate items and services to remove
        item_uuids = duplicates['Item Id'].unique().tolist()
        service_uuids = duplicates['Service Id'].unique().tolist()

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

        # Prompt user for output file path and name
        output_file_path = input("Enter the output file path: ")
        output_file_name = input("Enter the output file name: ")

        # Save the modified XML to the specified location
        output_file_path_with_name = os.path.join(output_file_path, output_file_name + '.xml')
        tree.write(output_file_path_with_name)
        print(f"XML file saved successfully at {output_file_path_with_name}")

    except Exception as e:
        print(f"An error occurred while processing the XML file: {str(e)}")
