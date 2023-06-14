# SAP UI Landscape XML file consists of Items and Services. Each have their own uuid and item refernces uuid of service
# as service id. I want to regenerate uuids of both and update service id of Item accordingly.
import os
import xml.etree.ElementTree as ET
import uuid
import pandas as pd


# Function to clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Function to display the program header
def display_header():
    clear_screen()
    print("=============================================")
    print("     SAP UI Landscape XML Modifier")
    print("=============================================")
    print()


# Function to display prompts and get user input
def get_user_input(prompt):
    return input(f">> {prompt} ")


# Function to display error messages
def display_error(message):
    print(f"ERROR: {message}")


# Function to display success messages
def display_success(message):
    print(f"SUCCESS: {message}")


# Function to remove double quotes from a string
def remove_quotes(string):
    return string.strip('"')


# Function to regenerate UUIDs for workspaces
def regenerate_workspace_uuids(workspaces):
    regenerate_all_uuids = get_user_input("Do you want to regenerate UUIDs for all workspaces? (y/n): ").lower() == "y"

    for workspace in workspaces:
        if regenerate_all_uuids or get_user_input(
                f"Regenerate UUID for workspace '{workspace.get('name')}'? (y/n): ").lower() == "y":
            workspace.set('uuid', str(uuid.uuid4()))
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


def generate_excel_file(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    # Create a dictionary to store the data
    data_sheet_1 = {
        'Node': [],
        'System Name': [],
        'System Description': [],
        'System Id': [],
        'System Type': [],
        'System Client': [],
        'System URL': [],
        'System Server': [],
        'Router Address': [],
        'Is Duplicate': []
    }

    # Iterate over the nodes
    for node in root.findall('.//Node'):
        node_name = node.get('name')

        # Iterate over the items in the node
        for item_node in node.findall('.//Item'):
            service_id = item_node.get('serviceid')

            # Iterate over Services
            for service in root.findall('.//Service'):
                service_uuid = service.get('uuid')
                service_type = service.get('type')
                if service_uuid == service_id and service_type == 'SAPGUI':
                    service_name = service.get('name')
                    service_description = service.get('description')
                    service_sid = service.get('systemid')
                    service_client = service.get('client')
                    service_url = service.get('url')
                    service_server = service.get('server')

                    # Initialize router_address with an empty string
                    router_address = ''

                    # Find the router based on the router ID
                    for router in root.findall('.//Router'):
                        router_uuid = router.get('uuid')
                        service_router = service.get('routerid')
                        if service_router == router_uuid:
                            router_address = router.get('router')



                    # Add the data to the dictionary
                    data_sheet_1['Node'].append(node_name)
                    data_sheet_1['System Name'].append(service_name)
                    data_sheet_1['System Description'].append(service_description)
                    data_sheet_1['System Id'].append(service_sid)
                    data_sheet_1['System Type'].append(service_type)
                    data_sheet_1['System Client'].append(service_client)
                    data_sheet_1['System URL'].append(service_url)
                    data_sheet_1['System Server'].append(service_server)
                    data_sheet_1['Router Address'].append(router_address)
                    data_sheet_1['Is Duplicate'].append('')

    for service in root.findall('.//Service'):
        servicetype = service.get('type')
        if servicetype != 'SAPGUI':
            servicename = service.get('name')
            servicedescription = service.get('description')
            servicesid = service.get('systemid')
            serviceclient = service.get('client')
            serviceurl = service.get('url')
            serviceserver = service.get('server')

            # Initialize router_address with an empty string
            routeraddress = ''

            # Find the router based on the router ID
            for router in root.findall('.//Router'):
                router_uuid = router.get('uuid')
                service_router = service.get('routerid')
                if service_router == router_uuid:
                    routeraddress = router.get('router')

            # Add the data to the dictionary
            data_sheet_1['Node'].append('*Not included in a node*')
            data_sheet_1['System Name'].append(servicename)
            data_sheet_1['System Description'].append(servicedescription)
            data_sheet_1['System Id'].append(servicesid)
            data_sheet_1['System Type'].append(servicetype)
            data_sheet_1['System Client'].append(serviceclient)
            data_sheet_1['System URL'].append(serviceurl)
            data_sheet_1['System Server'].append(serviceserver)
            data_sheet_1['Router Address'].append(routeraddress)
            data_sheet_1['Is Duplicate'].append('')

    # Create a DataFrame from the data dictionary
    df = pd.DataFrame(data_sheet_1)

    # Mark duplicates in the 'System Server' column if system type is 'SAPGUI'
    df.loc[df['System Type'] == 'SAPGUI', 'Is Duplicate'] = df.duplicated(subset='System Server')

    # Mark duplicates in the 'System URL' column if system type is not 'SAPGUI'
    df.loc[df['System Type'] != 'SAPGUI', 'Is Duplicate'] = df.duplicated(subset='System URL')

    # Save the DataFrame to Excel
    output_file_path = xml_file_path.replace('.xml', '.xlsx')
    df.to_excel(output_file_path, index=False)

    return output_file_path


def main():
    display_header()
    print("SAP UI Landscape XML Modifier")
    print("This program allows you to modify SAP UI Landscape XML files by regenerating UUIDs for workspaces,")
    print("nodes, services, and items. It also provides the option to remove includes and rename workspaces,")
    print("in order to make them usable as central files.")
    print()

    # Prompt the user for the XML file path
    while True:
        xml_file_path = get_user_input("Enter the path to the XML file: ")
        xml_file_path = remove_quotes(xml_file_path)

        if not os.path.isfile(xml_file_path):
            display_error("Invalid XML file path. Please try again.")
        else:
            break

    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        workspaces = root.findall(".//Workspace")

        print("List of Workspaces:")
        for index, workspace in enumerate(workspaces):
            print(f"{index + 1}. {workspace.get('name')}")

        regenerate_workspace_uuids(workspaces)

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
        tree.write(output_file, encoding='utf-8', xml_declaration=True)

        display_success(f"Modified XML file saved as: {output_file}")

        # Process the XML file and generate Excel file
        output_file_path = generate_excel_file(output_file)
        print("Excel file generated:", output_file_path)

    except Exception as e:
        display_error(f"An error occurred while processing the XML file: {str(e)}")

    input("Press Enter to exit...")


# Start the program
if __name__ == "__main__":
    main()
