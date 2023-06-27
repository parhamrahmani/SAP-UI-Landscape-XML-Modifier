import uuid
import xml.etree.ElementTree as ET
from utils.console import *
from utils.excel_utils import *
import lxml.etree as le


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


def add_systems_to_xml(xml_file_path, xml_file_path_destination):
    # Show Warning
    print("Warning: This function will add a system from your existing SAP Logon XML file to another XML file.")
    print("Please make sure that the system you want to add is already added to your existing XML file by SAP Logon")
    print("Please make sure that the destination XML file has the right structure.\n")
    print("----------------------------------------")
    print("Parsing XML file...")
    print("----------------------------------------")
    # Parse the XML file
    tree = le.parse(xml_file_path)
    root = tree.getroot()
    system_uuid = None
    print("Choose the connection type of the system you want to add:")
    print("1. Custom Application Server")
    print("2. Group/Server Selection\n")

    choice = int(input("Enter your choice (1 or 2): "))

    while choice not in [1, 2]:
        print("Invalid choice. Please enter 1 or 2.")
        choice = int(input("Enter your choice (1 or 2): "))

    if choice == 1:
        while True:
            print("Enter the SAP System information:")
            # Prompt user for necessary information
            description = input("Description: ")
            applicationServer = input("*Application Server: ")
            instanceNumber = input("*Instance Number: ")
            systemID = input("*System ID: ")
            SAPRouterString = input("SAP Router String: ")

            # Check if mandatory fields are empty
            if not applicationServer.strip() or not instanceNumber.strip() or not systemID.strip():
                print("Mandatory fields cannot be left blank. Please try again.")
                continue  # Restart the loop

            # Find the SAP system from the root xml file
            print("Processing XML file...")

            # Find the SAP system
            server_address = applicationServer + ":32" + instanceNumber
            print(server_address)

            if description is not None:
                sap_system = root.xpath(f".//Service[@server='{server_address}']")
            else:
                sap_system = root.xpath(f".//Service[@server='{server_address}']")

            if not sap_system:
                print("The SAP system you are trying to add does not exist in your root SAP Logon XML file.")
                add_system = input("Do you want to try again? (y/n): ")
                if add_system.lower() == 'n':
                    break  # Exit the loop if the user chooses not to try again
                continue  # Restart the loop

            sap_system = sap_system[0]  # Select the first matched element

            if sap_system.get('type') == 'SAPGUI':
                print("--------------------------------")
                print("SAP system found. Information:")
                system_uuid = sap_system.get('uuid')
                print("uuid: " + system_uuid)
                print("name: " + sap_system.get('name'))
                print("type: " + sap_system.get('type'))
                print("server" + sap_system.get('server'))
                print("systemid: " + sap_system.get('systemid'))
                routerid = sap_system.get('routerid')
                msid = sap_system.get('msid')
                if routerid is not None:
                    router = root.find(f".//Router[@uuid='{routerid}']")
                    print("uuid: " + router.get('uuid'))
                    print("router: " + router.get('router'))
                elif msid is not None:
                    messageserver = root.find(f".//Messageserver[@uuid='{msid}']")
                    print("uuid: " + messageserver.get('uuid'))
                    print("name: " + messageserver.get('name'))
                    print("host: " + messageserver.get('host'))
                    print("port: " + messageserver.get('port'))

            else:
                print("----------------------------------")
                print("SAP System found. Information:")
                print("uuid: " + sap_system.get('uuid'))
                print("name: " + sap_system.get('name'))
                print("description: " + sap_system.get('description'))
                print("type: " + sap_system.get('type'))
                print("url: " + sap_system.get('url'))
                print("client: " + sap_system.get('client'))

            print("----------------------------------")
            add_system = input("Is this the SAP system you want to add to the central configuration file? (y/n): ")

            if add_system.lower() == 'n':
                print("----------------------------------")
                print("        Please try again.         ")
                print("----------------------------------")
                continue  # Restart the loop to ask for information again

            break  # Exit the loop if the system is confirmed to be added

        # Add the SAP system to the destination XML file
        print("Adding the SAP system to the destination XML file...")
        # Parse the XML file
        tree_dest = le.parse(xml_file_path_destination)
        root_dest = tree.getroot()

        # Add the SAP system to the root
        services = root_dest.xpath('.//Services')

        tree_dest.write(xml_file_path_destination)

    elif choice == 2:
        # Handle choice 2
        print("Choice 2 is selected. Implement the logic for Group/Server Selection.")

    # Continue with the rest of your code


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


def show_stats(xml_file_path):
    try:
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

        print("Statistics for file: " + xml_file_path)
        print("Number of workspaces: " + str(len(workspaces)))
        print("Number of items: " + str(len(all_items)))
        print("Number of items in nodes: " + str(len(node_items)))
        print("Number of items in child nodes: " + str(len(child_node_items)))
        print("Number of services: " + str(len(services)))
        print("Number of routers: " + str(len(routers)))
        print("Number of message servers: " + str(len(messageservers)))

    except Exception as e:
        print(f"An error occurred while processing the XML file: {str(e)}")


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