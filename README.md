# SAP UI Landscape XML Modifier

The SAP UI Landscape XML Modifier is a Python program designed to modify SAP UI Landscape XML files. It provides various functionalities to regenerate UUIDs for workspaces, nodes, services, and items, as well as the option to remove includes and rename workspaces. This program is useful for customizing and managing SAP UI Landscape XML files according to specific requirements.

## Features

- Regenerate UUIDs: The program allows you to regenerate UUIDs for workspaces, nodes, services, and items. This helps in creating unique identifiers for each element.

- Rename Workspaces: You can rename workspaces within the XML file. This feature is particularly useful when you want to make the XML file usable as a central file.

- Update Service IDs: The program updates the service IDs of items based on the regenerated UUIDs of services. This ensures proper referencing and consistency within the XML file.

- Remove Includes: If the XML file includes "SAPUILandscapeGlobal.xml", the program provides an option to remove this include. This is necessary to make the XML file a central file that can be used independently.


## Usage

1. **Installation**: Make sure you have Python installed on your system. The program utilizes Python's built-in `xml.etree.ElementTree` module, which is commonly available. No additional external libraries or dependencies are required.

2. **Input XML File**: Prepare the SAP UI Landscape XML file that you want to modify. Ensure that you have appropriate access rights to read and modify the file.

3. **Running the Program**: Execute the Python script `sap_ui_landscape_modifier.py` in a Python-compatible environment, such as a command prompt or an integrated development environment (IDE). Follow the prompts displayed on the screen.

4. **Enter XML File Path**: Provide the path to the XML file when prompted. You can enter the path directly or drag and drop the file into the command prompt or terminal.

5. **UUID Regeneration**: You will be asked if you want to regenerate UUIDs for all workspaces. Answer 'y' to regenerate UUIDs for all workspaces or 'n' to manually choose which workspaces to regenerate UUIDs for.

6. **Workspace Modification**: If you chose to regenerate UUIDs for specific workspaces, you will be prompted for each workspace. You can enter a new name for the workspace or press Enter to keep the existing name.

7. **XML Modification**: The program will proceed to regenerate UUIDs for nodes, services, and items. It will also update the service IDs in items based on the regenerated UUIDs.

8. **Include Removal**: If the XML file includes "SAPUILandscapeGlobal.xml", you will be asked if you want to remove this include. Answer 'y' to remove the include or 'n' to keep it.

9. **Output XML File**: Enter the output path for the modified XML file and provide a name for the output file. The modified XML file will be saved at the specified location with a unique name.

10. **Completed**: Once the program finishes processing, it will display the path where the modified XML file is saved. You can open the file in a text editor or use it as needed.

## Caution

- Always create a backup of your original XML file before running the program. This ensures that you have a copy of the unmodified file in case any issues arise during the modification process.

- Exercise caution when modifying XML files, as incorrect modifications can lead to errors or unexpected behavior in SAP UI Landscape configurations.

- Make sure you have appropriate access rights to read and modify the XML file. Otherwise, the program may encounter permission errors.

