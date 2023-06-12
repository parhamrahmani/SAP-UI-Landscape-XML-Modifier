# SAP UI Landscape XML file consists of Items and Services. Each have their own uuid and item refernces uuid of service
# as service id. I want to regenerate uuids of both and update service id of Item accordingly.
import os
import xml.etree.ElementTree as ET
import uuid


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
        prompt_message = "This XML file includes SAPUILandscapeGlobal.xml. In order to make this file into a central file, this inclusion has to be deleted. Do you want to delete it? (y/n): "
        remove_includes = get_user_input(prompt_message).lower() == "y"

        if remove_includes:
            root.findall(".//Includes")[0][:] = filtered_includes
            return True
        else:
            return False
    else:
        return False


# Main program
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

    except Exception as e:
        display_error(f"An error occurred while processing the XML file: {str(e)}")

    input("Press Enter to exit...")


# Start the program
if __name__ == "__main__":
    main()



