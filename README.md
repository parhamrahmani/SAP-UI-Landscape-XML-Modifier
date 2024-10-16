
# SAP UI Landscape XML Modifier v1.1

The SAP UI Landscape XML Modifier is a Python programme designed to modify SAP UI Landscape XML "Local" files into "Centralized/Global" landscape files. It provides various functionalities like adding systms from your local xml configuration file into another xml configuartion file, regenerating UUIDs for workspaces, nodes, services, and items, as well as the option to remove inclusions of SAPUILandscapeGlobal from your local file, in order to make it usable as a central file. This programme is useful for customising and managing SAP UI Landscape XML files according to specific requirements.

## Content
- [Intro](#sap-ui-landscape-xml-modifier-v11)
- [Features](#features)
- [Warnings](#warnings)
- [Installation](#installation)
- [How to Use](#how-to-use)
- [Support and a Personal Note](#support-and-a-personal-note)




## Features

- **Add Systems from a Landscape xml file into another one**:

This feature allows you to easily copy a SAP system/connection from one SAP landscape XML file and move it to another SAP UI landscape file. It's helpful when you have separate XML files for different environments and want to add a system from one environment to another *without directly editing the XML file*. It's also useful for adding a new system to the central/global SAP UI Landscape file. Normally, these global files are read-only in SAP Logon, requiring manual system addition using SLMT or XML editing, which can be inconvenient. 

- **Remove a System from a Landscape file**:

This feature can find a system in your file and remove it. It is useful in cases when you are dealing with a centralized or gloabl configuration file which is read-only in SAP access tools or you don't have the possibility to work with SAP access tools and have to directly edit the xml.

- **Modify a System in a Landscape File**:

This feautre can find a system in your file and lets you to edit names, system ids or server addresses/urls. As mentioned above this is useful with scenarios when a configuration file is read-only in SAP access tools. In next updates changing router/message server addresses will be possible or appending new router/message server for a system. 

- **Regenerate UUIDs and Remove SAPUILandscapeGlobal Inclusions:**:

This feauture is only useful when you want to also use your local file as a global file on a server. The programme allows you to regenerate UUIDs for workspaces, nodes, services, and items and  prevents errors and possible interferences between local and the global file.If the XML file includes "SAPUILandscapeGlobal.xml", the programme provides an option to remove this inclusion. This is necessary to make the XML file a central file that can be used independently.

- ***Exporting an Excel file of all SAP systems:***:

Information exported is  system names, SID, system types, system URL (for FIORI or NWBC types) or server address, router address, etc.

- **Exporting an Excel File of Duplicate Systems:**:

The program identifies and exports duplicate systems seperately in an excel file, providing better visibility and management of system duplicates.

- **Removing duplications from an SAP UI Landscape File**: This feature helps you eliminate duplications in your landscape files. Here are the parameters used to identify duplications (if all are true at the same time):

    - *Duplicate Application Server and Instance Number:* This means that there are multiple entries with the same application server and instance number in your landscape file.

    - *Duplicate System ID:* This refers to having multiple entries with the same system ID in your landscape file.
    
    - If all *three parameters* in one system are duplicates, the function will remove it (except the last occurance)!


## Warnings

- This programme is still in beta and may contain bugs. Please report any bugs or issues you encounter.
- Please make sure you have the standard hierarchy of data in your XML file. Based on [SAP's documentation](https://help.sap.com/doc/df5f752eb4004b2c9ecab769c9f71208/760.01/en-US/sap_ui_landscape_conf_guide.pdf), the expected hierarchy is as follows:
```
<Landscape>
   <Workspaces>
       <Workspace>
               <Node>
                    <Item>
               </Node>
               <Item>
       </Workspace>   
   </Workspaces>
   <Services>
           <Service>
                  <Memo></Memo>
           </Service>
   </Services>
   <Messageservers>
           <Messageserver>
   </Messageservers> 
   <Routers>
           <Router>
   </Routers>
   <Includes>
            <Include>
   </Includes>
   <Configuration>
       <Parameter> 
   </Configuration> 
</Landscape>
```

The programme will not work properly if the hierarchy is not as expected.


- This programme is not intended to be used for SAP UI Landscape XML files that are already in use. It is recommended to
use this programme on a copy of your original XML file. Always create a backup of your original XML file before running the programme. This ensures that you have a copy of the unmodified file in case any issues arise during the modification process.

- Exercise caution when modifying XML files, as incorrect modifications can lead to errors or unexpected behaviour in SAP UI Landscape configurations.

- Make sure you have appropriate access rights to read and modify the XML file. Otherwise, the programme may encounter permission errors.

- Make sure to view the XML file after usage in an XML editor and check if the data is correct, before referencing it to SAP. For example, check if there are still any include sections that include any other global files that may cause duplications. Making a central XML configuration file can't be done 100% automatically.


## Installation


- Simply download the last release from the "Releases" tab and run the .exe file. The main menu should look like this:
  
![alt text](https://github.com/parhamrahmani/SAP-UI-Landscape-XML-Modifier/blob/master/Screenshot%202023-08-24%20130119.png)

### How to Use
#### Adding a System to the Central File
- Add the system to your local configuration via the  SAP Logon/SAP Business Client software.
- To add a system from your local file to the central file, you'll need this tool. Download the SAP UI Landscape File Modifier and open the tool and select "Add a System" from the main menu.
- Choose your local config file as the source XML and the central config file as the destination XML. Click "Next".
- Find your system based on its type (e.g., SAPGUI or NWBC/FIORI). The tool should autocomplete entries based on system ID or name. Click "Find SAP System".
- Verify the information provided and confirm if correct.
- On the final page, you can rename the system for the central file if desired. Select or create a workspace as needed.
- Click "Submit" to add the system to the central file. The tool will confirm if the process was successful.
- Restart your SAP Logon or SAP Business Client software to see the changes.

**Note: You can basically move any SAP system information/configuration between xml config files with this. Just choose the source and destination file correctly**
**Note 2: Make suer your xml file exactly has the information like server address, etc. This tool doesn't find 'favourite' enteries, since they are only links to other services and don't have information on them**

#### Removing a System from the Central File
- Open the SAP UI Landscape File Modifier and choose "Remove a System".
- Select your configuration file or give its address. 
- Find the system you want to delete by choosing or giving its system ID or name. 
- Confirm the removal of the system.
- Restart your SAP Logon or SAP Business Client software to see the changes.

#### Modifying a System in the Central File
- Open the SAP UI Landscape File Modifier and choose "Modify a System".
- Select your central configuration file.
- Find the system you want to modify. The tool should autocomplete entries based on system ID or name.
- Update the desired fields, leaving unchanged fields as they are.
- Confirm the modifications.
- Restart your SAP Logon or SAP Business Client software to see the changes.

#### Other Features
These feauters are clear and have the same procedure as others. Be careful with these, specially with **Removing duplications from an SAP UI Landscape File**. This will try to remove duplicate systems from your config file and use this on a copy only!

## Support and a Personal Note
This repository won't be maintained for now, because of time and lack of knowledge and interest in ``tkinter``. This app was developed as my very first python project and has some major programming flaws, but it works fortunately well for its job. 
Feel free to fork this and make a pull request for changes and better features or UI. 
### Alternatives to this Application - [``SLMT``](https://itsiti.com/slmt-sap-ui-landscape-maintenance-tool/)
If you want a tool to generate or edit and modify SAP XML config files and don't want to use this app. You can use the ``SLMT`` transaction in a SAP system. Using SLMT is more difficult since it doesn't provide any form of automation (like UUID generation, referencing router and message server IDs, etc.) unlike this application. The second option is to download the ``SAPUILandscapeGlobal.xml`` from the shared network you have the config file on, copy it to ``C:\Users\<yourusername>\AppData\Roaming\SAP\Common``, rename it to a local configuration file as ``SAPUILandscape.xml`` and use a copy global xml as a local xml and after editing it, copying it back to the global xml file on server and overwriting it, which can be very time-consuming. 
### Possible Advancements and Issues
- for modifying services, router addresses and message services can't be edited directly.
- fixing UI bugs and mistakes
- the xml file gets parsed multiple times because of some major programming mistakes, this isn't a bug but makes the programm slower and less performant. 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
