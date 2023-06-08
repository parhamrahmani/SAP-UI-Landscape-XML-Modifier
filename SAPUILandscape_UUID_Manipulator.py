# SAP UI Landscape XML file consists of Items and Services. Each have their own uuid and item refernces uuid of service
# as service id. I want to regenerate uuids of both and update service id of Item accordingly.
import xml.etree.ElementTree as ET
import uuid
import random

# Prompt the user for the XML file path
xml_file_path = input("Enter the XML file path: ")

# Load the XML file
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Find the Workspace element with the name "Local" and update its name attribute
for workspace in root.findall(".//Workspace[@name='Local']"):
    workspace.set('name', 'Central - Technology and Managed Services')

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
random_number = str(random.randint(10000000, 99999999))
output_file_name = 'C:/Users/PR106797/Downloads/modified_xml_' + random_number + '.xml'
tree.write(output_file_name, encoding='utf-8', xml_declaration=True)

print("Modified XML file saved as:", output_file_name)


