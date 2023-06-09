# SAP UI Landscape XML file consists of Items and Services. Each have their own uuid and item refernces uuid of service
# as service id. I want to regenerate uuids of both and update service id of Item accordingly.
import xml.etree.ElementTree as ET
import uuid

# Description of the program
description = """
SAP UI Landscape XML Modifier:
This program allows you to modify SAP UI Landscape XML files by regenerating UUIDs for workspaces, 
nodes, services, and items. It also provides the option to remove includes and rename workspaces, in order 
make them usable as central files

Note: Make sure to backup your XML file before making any modifications.

"""

print(description)

# Prompt the user for the XML file path
xml_file_path = input("Enter the XML file path: ")

# Load the XML file
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Get the existing workspaces in the XML file
workspaces = root.findall(".//Workspace")

# Show a list of workspaces
print("List of Workspaces:")
for index, workspace in enumerate(workspaces):
    print(f"{index + 1}. {workspace.get('name')}")

# Prompt the user for UUID regeneration for workspaces
regenerate_all_uuids = input("Do you want to regenerate UUIDs for all workspaces? (y/n): ").lower() == "y"

# Regenerate UUIDs for workspaces
for index, workspace in enumerate(workspaces):
    if regenerate_all_uuids or input(
            f"Regenerate UUID for workspace '{workspace.get('name')}'? (y/n): ").lower() == "y":
        workspace.set('uuid', str(uuid.uuid4()))
        new_workspace_name = input(f"Enter the new name for workspace '{workspace.get('name')}': ")
        workspace.set('name', new_workspace_name)

# Regenerate UUIDs for Node elements
for node in root.findall(".//Node"):
    node.set('uuid', str(uuid.uuid4()))

# Create a mapping of old service IDs to new UUIDs
service_mapping = {}

# Regenerate UUIDs for Service elements and update service IDs in Item elements
for service in root.findall(".//Service"):
    old_uuid = service.get('uuid')
    new_uuid = str(uuid.uuid4())
    service_mapping[old_uuid] = new_uuid
    service.set('uuid', new_uuid)

    # Update the serviceid in Item elements
    for item in root.findall(".//Item[@serviceid='" + old_uuid + "']"):
        item.set('serviceid', new_uuid)

# Regenerate UUIDs for Item elements
for item in root.findall(".//Item"):
    item.set('uuid', str(uuid.uuid4()))

# Check if there is an include with the URL containing "SAPUILandscapeGlobal.xml"
includes = root.findall(".//Include")
is_global_include_present = any("SAPUILandscapeGlobal.xml" in include.get("url") for include in includes)

if is_global_include_present:
    removing_include = input("This XML file includes SAPUILandscapeGlobal.xml in it. In order to make this "
                             "file into a central file, this inclusion has to be deleted. Do you "
                             "want to delete it? (y/n): ").lower() == "y"

    if removing_include:
        filtered_includes = []

        # Remove includes with URLs containing "SAPUILandscapeGlobal.xml"
        for include in includes:
            include_url = include.get("url")
            if "SAPUILandscapeGlobal.xml" not in include_url:
                filtered_includes.append(include)

        # Replace the include elements with the filtered list
        root.findall(".//Includes")[0][:] = filtered_includes
else:
    print("No include with URL containing 'SAPUILandscapeGlobal.xml' found.")

# Save the modified XML file with a unique name
input_output_path = input("Enter the output path for the modified XML file: ")
input_modified_name = input("Enter the name for your output file: ")
output_file_name = input_output_path + '/' + input_modified_name + '.xml'
tree.write(output_file_name, encoding='utf-8', xml_declaration=True)

print("Modified XML file saved as:", output_file_name)
