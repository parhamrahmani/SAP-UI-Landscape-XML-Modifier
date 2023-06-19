

import time
import os
import xml.etree.ElementTree as ET
import pandas as pd
from utils.console import *

from utils.excel_utils import *
from utils.xml_utils import *


def display_loading_bar():
    print("Exporting in progress, Please Wait", end="")
    for _ in range(10):
        time.sleep(0.1)
        print(".", end="", flush=True)
    print()


def main():
    while True:
        display_header()
        display_wl_msg()

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

            # Exporting the Excel files
            display_loading_bar()
            time.sleep(1)  # Simulating export delay



            time.sleep(2)  # Delay for 2 seconds before prompting for input

            choice = get_user_input("Enter 'n' to perform another operation or 'q' to exit: ")
            if choice.lower() == 'q':
                break

        except Exception as e:
            display_error(f"An error occurred while processing the XML file: {str(e)}")


if __name__ == "__main__":
    main()

