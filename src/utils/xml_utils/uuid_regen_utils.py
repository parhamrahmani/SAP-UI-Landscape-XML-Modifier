import logging
import os
import uuid
from tkinter import messagebox
from xml.etree import ElementTree as ET

from src.ui.ui_components.dialog_boxes import DialogBoxes
from src.utils.excel_utils.excel_utils import generate_excel_files


class UUIDRegenUtils:
    @staticmethod
    def regenerate_workspace_uuids(workspaces):
        for workspace in workspaces:
            workspace.set('uuid', str(uuid.uuid4()))
            workspace.set('expanded', str(0))
            if workspace.get('name') == "Local" or workspace.get('name') == "local":
                workspace.set('name', "Default")

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def regenerate_uuids_export_excel(xml_file_path):
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            workspaces = root.findall(".//Workspace")

            UUIDRegenUtils.regenerate_workspace_uuids(workspaces)

            # Regenerating UUIDs
            for node in root.findall(".//Node"):
                node.set('uuid', str(uuid.uuid4()))

            UUIDRegenUtils.regenerate_service_uuids(root)

            if UUIDRegenUtils.remove_global_includes(root):
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

            DialogBoxes.open_folder_containing_file(output_file)

        except Exception as e:
            messagebox.showerror("Error!", f"An error occurred while processing the XML file: {str(e)}")
            logging.error(f"An error occurred while processing the XML file: {str(e)}")
