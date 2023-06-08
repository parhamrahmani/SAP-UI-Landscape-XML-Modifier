# SAP UI Landscape XML file consists of Items and Services. Each have their own uuid and item refernces uuid of service
# as service id. I want to regenerate uuids of both and update service id of Item accordingly.
import xml.etree.ElementTree as ET
import uuid

# Prompt the user for the XML file path
xml_file_path = input("Enter the XML file path: ")

# Load the XML file
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Get the existing workspaces in the XML file
workspaces = root.findall(".//Workspace")

# Display the includes
includes = root.findall(".//Include")
print("Includes:")
for include in includes:
    print(include.get("file"))

# Prompt the user for include removal
remove_includes = input("Do you want to remove any includes? (y/n): ").lower() == "y"

if remove_includes:
    include_indexes = input("Enter the indexes of the includes to remove (comma-separated): ")
    include_indexes = [int(i) for i in include_indexes.split(",")]
    include_indexes.sort(reverse=True)  # Remove in reverse order to avoid index shifting
    for index in include_indexes:
        del root[index]

# Prompt the user for UUID regeneration for workspaces
regenerate_all_uuids = input("Do you want to regenerate UUIDs for all workspaces? (y/n): ").lower() == "y"

# Regenerate UUIDs for workspaces
for index, workspace in enumerate(workspaces):
    if regenerate_all_uuids or input(f"Regenerate UUID for workspace '{workspace.get('name')}'? (y/n): ").lower() == "y":
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

# Save the modified XML file with a unique name
input_output_path = input("Enter the output path for the modified XML file: ")
input_modified_name = input("Enter the name for your output file: ")
output_file_name = input_output_path + '/' + input_modified_name + '.xml'
tree.write(output_file_name, encoding='utf-8', xml_declaration=True)

print("Modified XML file saved as:", output_file_name)

