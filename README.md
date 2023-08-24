
## SAP UI Landscape XML Modifier v1.0.1

The SAP UI Landscape XML Modifier is a Python programme designed to modify SAP UI Landscape XML "Local" files into "Centralized/Global" landscape files. It provides various functionalities like adding systms from your local xml configuration file into another xml configuartion file, regenerating UUIDs for workspaces, nodes, services, and items, as well as the option to remove inclusions of SAPUILandscapeGlobal from your local file, in order to make it usable as a central file. This programme is useful for customising and managing SAP UI Landscape XML files according to specific requirements.




## Features

- **Add Systems from a Landscape xml file into another one** This feature allows you to easily copy a SAP system/connection from one SAP landscape XML file and move it to another SAP UI landscape file. It's helpful when you have separate XML files for different environments and want to add a system from one environment to another *without directly editing the XML file*. It's also useful for adding a new system to the central/global SAP UI Landscape file. Normally, these global files are read-only in SAP Logon, requiring manual system addition using SLMT or XML editing, which can be inconvenient. 

- **Remove a System from a Landscape file** This feature can find a system in your file and remove it. It is useful in cases when you are dealing with a centralized or gloabl configuration file which is read-only in SAP access tools or you don't have the possibility to work with SAP access tools and have to directly edit the xml.

- **Modify a System in a Landscape File** This feautre can find a system in your file and lets you to edit names, system ids or server addresses/urls. As mentioned above this is useful with scenarios when a configuration file is read-only in SAP access tools. In next updates changing router/message server addresses will be possible or appending new router/message server for a system. 

- **Regenerate UUIDs and Remove SAPUILandscapeGlobal Inclusions:** This feauture is only useful when you want to also use your local file as a global file on a server. The programme allows you to regenerate UUIDs for workspaces, nodes, services, and items and  prevents errors and possible interferences between local and the global file.If the XML file includes "SAPUILandscapeGlobal.xml", the programme provides an option to remove this inclusion. This is necessary to make the XML file a central file that can be used independently.

- ***Exporting an Excel file of all SAP systems:*** Information exported is  system names, SID, system types, system URL (for FIORI or NWBC types) or server address, router address, etc.

- **Exporting an Excel File of Duplicate Systems:** The program identifies and exports duplicate systems seperately in an excel file, providing better visibility and management of system duplicates.

- **Removing duplications from an SAP UI Landscape File**: This feature helps you eliminate duplications in your landscape files. Here are the parameters used to identify duplications (if all are true at the same time):

  - *Duplicate Application Server and Instance Number:* This means that there are multiple entries with the same application server and instance number in your landscape file.

  - *Duplicate System ID:* This refers to having multiple entries with the same system ID in your landscape file.
    
  - If all *three parameters* in one system are duplicates, the function will remove it (except the last occurance)!


## Warnings

- This programme is still in beta and may contain bugs. Please report any bugs or issues you encounter.
- Please make sure you have the standard hierarchy of data in your XML file. Based on [SAP's documentation](https://www.bing.com/ck/a?!&&p=e846a0c56aad6c19JmltdHM9MTY4Njg3MzYwMCZpZ3VpZD0yMWE5YzQxMS05MzNmLTYzOWQtMGRkMy1kNmY5OTIwNzYyZDYmaW5zaWQ9NTE5Nw&ptn=3&hsh=3&fclid=21a9c411-933f-639d-0dd3-d6f9920762d6&psq=sap+ui+landscape+file+configuration+&u=a1aHR0cHM6Ly9oZWxwLnNhcC5jb20vZG9jL2RmNWY3NTJlYjQwMDRiMmM5ZWNhYjc2OWM5ZjcxMjA4Lzc2MC4wMS9lbi1VUy9zYXBfdWlfbGFuZHNjYXBlX2NvbmZfZ3VpZGUucGRm&ntb=1), the expected hierarchy is as follows:
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



