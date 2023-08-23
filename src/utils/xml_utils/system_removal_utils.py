import logging
import os
from tkinter import messagebox

import lxml.etree as le
import xml.etree.ElementTree as ET
import pandas as pd

from src.ui.ui_components.dialog_boxes import DialogBoxes


class SystemRemoval:
    # Function to remove duplications in the XML file
    @staticmethod
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
            DialogBoxes.open_folder_containing_file(output_file)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while removing duplications: {str(e)}")
            logging.error(f"An error occurred while removing duplications: {str(e)}")

    @staticmethod
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

    @staticmethod
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
