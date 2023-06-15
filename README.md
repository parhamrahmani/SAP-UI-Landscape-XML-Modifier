
## SAP UI Landscape XML Modifier

The SAP UI Landscape XML Modifier is a Python programme designed to modify SAP UI Landscape XML "Local" files into "Centralized/Global" landscape files. It provides various functionalities to regenerate UUIDs for workspaces, nodes, services, and items, as well as the option to remove includes and rename workspaces. This programme is useful for customising and managing SAP UI Landscape XML files according to specific requirements.




## Features

- Regenerate UUIDs: The programme allows you to regenerate UUIDs for workspaces, nodes, services, and items. This prevents errors and possible interferences between local and the global file.

- Rename Workspaces: You can rename workspaces within the XML file. This feature is particularly useful when you want to make the XML file usable as a central file. (Renaming the "Local" workspace is a necessity for making a global config file)

- Update Service IDs: The programme updates the service IDs of items based on the regenerated UUIDs of services. This ensures proper referencing and consistency within the XML file.

- Remove SAPUILandscapeGlobal Includes: If the XML file includes "SAPUILandscapeGlobal.xml", the programme provides an option to remove this include. This is necessary to make the XML file a central file that can be used independently.

- Exporting an Excel file of all SAP systems Information exported is node names, system names, SID, system types, system URL (for FIORI or NWBC types) or server address, router address, and marking existing duplicate systems in the configuration file.

## Warnings

- Always create a backup of your original XML file before running the programme. This ensures that you have a copy of the unmodified file in case any issues arise during the modification process.

- Exercise caution when modifying XML files, as incorrect modifications can lead to errors or unexpected behaviour in SAP UI Landscape configurations.

- Make sure you have appropriate access rights to read and modify the XML file. Otherwise, the programme may encounter permission errors.

- Make sure to view the XML file after usage in an XML editor and check if the data is correct, before referencing it to SAP. For example, check if there are still any include sections that include any other global files that may cause duplications. Making a central XML configuration file can't be done 100% automatically.
## Installation


- Make sure you have Python installed on your system. The programme utilises Python's built-in xml.etree.ElementTree module, which is commonly available. Download and install Python from their [Website](https://www.python.org/?downloads) or use package managers such as *Chocolatey* to install it.

```
choco install -y python3
```

- This programme needs some other packages that need to be installed on your PC. To install this. Open PowerShell or cmd **as an administrator** and run this command.
 
 
 *First, ensure you have Python installed*
```bash
py --version
```
*Then ensure you have pip installed*
```bash
py -m ensurepip
```
*Install pandas*
```bash
py -m pip install pandas
```
*Install openpyxl*
```bash
py -m pip install openpyxl
```
- After the reassurance that the packages are installed, you can download the repository as a zip file, extract it, and run *SAPUILandscape_UUID_Manipulator.py*.
You should see this when run correctly:
```bash
=============================================
     SAP UI Landscape XML Modifier
=============================================

SAP UI Landscape XML Modifier
This program allows you to modify SAP UI Landscape XML files by regenerating UUIDs for workspaces,
nodes, services, and items. It also provides the option to remove includes and rename workspaces,
in order to make them usable as central files.
```


## Usage/Examples

- After seeing this message :

```bash
>> Enter the path to the XML file: 
```
Enter the directory of the XML configuration file you want to modify. Use *Copy as Path* option in Windows. Make sure to use a copy of your main local configuration file.

Example: __"C:\Users\User\SAPUILandscapeCopy.xml"__

- You will see afterwards a list of your workspaces and a question asking if you want to regenerate uuids for all of your workspaces or only particular ones. 
*It is recommended to make central config files to regenerate all of your uuids.*

Example: use **y** or **n** as answers.

```bash
List of Workspaces:
1. Local
>> Do you want to regenerate UUIDs for all workspaces? (y/n): 
```
- Afterwards, the programme asks you to rename your workspaces. The only workspace that **must** be renamed for a good result is renaming the **"Local"** workspace. 

Example: write a new name for your workspace like **central**

```bash
>> Enter the new name for workspace 'Local':
```
- In this stage, the programme checks if there are any codes that include **SAPUILandscapeGlobal.xml"**. This section was intended to be in local config files to also include the global file, it is recommended to delete this, because in a central file you won't need to reference the file itself again. This may cause duplications, errors, or even cause SAP Logon to crash. 

Example: You will see this message. Use **y** or **n** as answers.

```bash
>> This XML file includes SAPUILandscapeGlobal.xml. In order to make this file into a central file, this inclusion has to be deleted. Do you want to delete it? (y/n):
```

- Now enter the output path. Make sure to **NOT** use quotation marks ("") while giving the answer.

Example:

*Correct* -> C:\Users\User\Documents  
*Incorrect* -> "C:\Users\User\Documents"

```bash
>> Enter the output path for the modified XML file:
```

- Now enter the name of your output file. In the example, I used 'Mod' as the new file name. After this, you will get a message that reports if the new modified XML file was successfully exported and modified. An excel file will also be reported that lists all of your systems, and it can be very useful to observe what systems you have in your configuration files and if the modified configuration file contains all of them.

*In the end, press Enter to exit the programme.* 
```bash
>> Enter the name for your output file:  Mod
SUCCESS: Modified XML file saved as: C:\Users\User\Documents\Mod.xml
Excel file generated: C:\Users\User\Documents\Mod.xlsx
Press Enter to exit...
```
