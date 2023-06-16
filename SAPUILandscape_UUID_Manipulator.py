import time
from utils.console import *
from utils.excel_utils import *
from utils.xml_utils import *
import xml.etree.ElementTree as ET
import pandas as pd


def main():
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

        # regenerating
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

        # Process the XML file and generate Excel file
        output_file_path = generate_excel_file(output_file)
        print("Excel file generated:", output_file_path)

        time.sleep(5)  # Delay for 5 seconds before prompting for input

        input("Press Enter to exit...")

    except Exception as e:
        display_error(f"An error occurred while processing the XML file: {str(e)}")


# Start the program
if __name__ == "__main__":
    main()
    input("Press Enter to exit...")
