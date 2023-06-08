# SAPUILandscape_xml_Manipulator

In SAP Logon the SAP systems that you can log on to, are configured in two xml files in AppData/Roaming/SAP/Common. 
There are two xml files for that matter
SAPUILandscape
SAPUILandscapeGlobal

There first one is for local use. The second one is actually the central/global config file that is should be shared on a shared network/server has to be entered manually in SAP Logon Options.
What is this python script?

In order to create a centralized config file or convert a local file into a global file ready for sharing.

Feature 1: regenerating UUIDs of Items, Nodes, Services and the Workspace "local" and renaming it to input name. 
Feature 2: Merging several local config files and making a single central config file --> In Progress
