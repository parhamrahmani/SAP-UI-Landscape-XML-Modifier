import logging
import os
import sys
from tkinter import messagebox
import lxml.etree as le
import uuid
import xml.etree.ElementTree as ET


class XMLQuery:
    @staticmethod
    def find_custom_system(xml_file_path, server_address, systemid):
        try:
            sap_system = None
            service_found = False

            # Parse the source XML file
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            for service in root.findall(".//Service"):
                if service.get('server') == server_address:
                    if service.get('systemid') == systemid:
                        sap_system = service
                        service_found = True
                        break
                    elif service.get('systemid') is None:
                        messagebox.showwarning("Warning!\n\n System ID undefined. \n\n",
                                               f"Service with server address {server_address} "
                                               f"doesn't have a designated system ID\n\n"
                                               f"System Info: {service.get('name')}\n"
                                               f"Server Address: {service.get('server')}\n")
                        sap_system = service
                        service_found = True
                        break
                    else:
                        raise Exception(f"Service with \nserver address: {server_address}\n "
                                        f"has a different \nsystem ID: {service.get('systemid')}")

            if not service_found:
                raise Exception(f"Service with server address {server_address} "
                                f"not found in XML file")

            return sap_system

        except Exception as e:
            print("Error in find_custom_system():", str(e))
            logging.error("Error in find_custom_system():", str(e))
            messagebox.showerror("Error!", f"An error occurred while processing the XML file:\n{str(e)}")
            return None

    @staticmethod
    def find_router(xml_file_path, routerid):
        # Parse the source XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        for router in root.findall(".//Router"):
            if router.get('uuid') == routerid:
                return router

    @staticmethod
    def find_message_server(xml_file_path, msid):
        # Parse the source XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        for ms in root.findall(".//Messageserver"):
            if ms.get('uuid') == msid:
                return ms

    @staticmethod
    def find_all_workspaces(xml_file_path):
        try:
            # Parse the destination XML file
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            workspaces_el = root.find(".//Workspaces")
            if workspaces_el is not None:
                workspaces = workspaces_el.findall(".//Workspace")
                return workspaces
            else:
                workspaces_el = ET.SubElement(root, "Workspaces")
                workspaces = []
                return workspaces

        except Exception as e:
            messagebox.showwarning("Error in list_all_workspaces():", str(e))
            logging.error(f"Error in list_all_workspaces(): {str(e)}")
            return None

    @staticmethod
    def find_all_nodes_of_workspace(xml_file_path, workspace_name):
        try:
            # Parse the destination XML file
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            if root.tag != "Landscape":
                messagebox.showwarning("Error in XML structure:",
                                       "The root tag of the XML file should be <Landscape>. Please correct your XML file "
                                       "and try again."
                                       "\n\nThe XML file must be a SAP Landscape File!\n"
                                       "If your destination file is an empty XML file, please edit the xml file and add\n "
                                       "<Landscape> </Landscape> to it!\n")
                return None
            workspaces = root.findall(".//Workspace")
            node_names = []
            for ws in workspaces:
                if ws.get('name') == workspace_name:
                    for node in ws.findall(".//Node"):
                        node_names.append(node.get('name'))
            return node_names
        except Exception as e:
            messagebox.showwarning("Error in list_nodes_of_workspace():", str(e))
            logging.error(f"Error in list_nodes_of_workspace(): {str(e)}")
            return []  # Return an empty list instead of None

    @staticmethod
    def get_stats(xml_file_path):
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        all_items = root.findall('.//Item')
        node_items = root.findall('.//Node/Item')
        child_node_items = root.findall('.//Node/Node/Item')
        workspaces = root.findall('.//Workspace')
        services = root.findall('.//Service')
        routers = root.findall('.//Router')
        messageservers = root.findall('.//Messageserver')

        stats = {
            "workspaces": len(workspaces),
            "items": len(all_items),
            "items in nodes": len(node_items),
            "items in child nodes": len(child_node_items),
            "services": len(services),
            "routers": len(routers),
            "message servers": len(messageservers)
        }

        return stats

    @staticmethod
    def list_system_ids_for_group_server_connection_entry(xml_file_path):
        try:
            # Parse the XML file
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            system_ids = []

            for service in root.findall(".//Service"):
                if service.get('msid') is not None:
                    system_ids.append(service.get('systemid'))

            return system_ids

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while listing system IDs: {str(e)}")
            logging.error(f"An error occurred while listing system IDs: {str(e)}")

    @staticmethod
    def find_message_server_based_on_system_id(xml_file_path, systemid):
        try:
            # Parse the XML file
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            message_server_id = None
            message_server = None
            message_servers = root.findall(".//Messageserver")
            services = root.findall(".//Service")

            for service in services:
                if service.get('msid') is not None:
                    if service.get('systemid') == systemid:
                        message_server_id = service.get('msid')
                        break
            for ms in message_servers:
                if ms.get('uuid') == message_server_id:
                    message_server = ms
                    break
            return message_server

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while finding message server: {str(e)}")
            logging.error(f"An error occurred while finding message server: {str(e)}")

    @staticmethod
    def get_all_routers(xml_file_path):
        try:
            # Parse the XML file
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            routers = root.findall(".//Router")
            return routers

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while finding message server: {str(e)}")
            logging.error(f"An error occurred while finding message server: {str(e)}")

    @staticmethod
    def get_all_urls(xml_file_path):
        try:
            # Parse the XML file
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            services = root.findall(".//Service")
            urls = []
            for service in services:
                # Assuming the service name is also an attribute of the Service node
                if service.get('url'):
                    urls.append(service.get('url'))

            # Return the list of URLs
            return urls

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while finding NWBC/FIORI system urls: {str(e)}")
            logging.error(f"An error occurred while finding NWBC/FIORI system urls: {str(e)}")

    @staticmethod
    def get_all_custom_sap_gui_info(xml_file_path):
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        services = root.findall(".//Service")
        sap_gui_names = []
        sap_gui_server_addresses = []
        sap_gui_system_ids = []

        for service in services:
            if service.get('type') == 'SAPGUI':
                if service.get('server') is not None:
                    server = service.get('server')
                    name = service.get('name')
                    systemid = None
                    if service.get('systemid') is not None:
                        systemid = service.get('systemid')
                    if server not in sap_gui_server_addresses:
                        if systemid is not None and systemid not in sap_gui_system_ids:
                            sap_gui_server_addresses.append(server)
                            sap_gui_names.append(name)
                            sap_gui_system_ids.append(systemid)
                        else:
                            sap_gui_server_addresses.append(server)
                            sap_gui_names.append(name)

        return sap_gui_server_addresses, sap_gui_names, sap_gui_system_ids

    @staticmethod
    def find_system_names_based_on_server_address(xml_file_path, server_address):
        try:
            # Parse the XML file
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            sys_names = []

            for service in root.findall(".//Service"):
                if service.get('server') is not None:
                    if service.get('server') == server_address:
                        sys_names.append(service.get('name'))

            return sys_names

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while listing system IDs: {str(e)}")
            logging.error(f"An error occurred while listing system IDs: {str(e)}")

    @staticmethod
    def find_system_info_based_on_sid(xml_file_path, sid):
        try:
            # Parse the XML file
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            server_addresses = []
            system_names = []

            for service in root.findall(".//Service"):
                if service.get('systemid') is not None:
                    if service.get('systemid') == sid:
                        server_addresses.append(service.get('server'))
                        system_names.append(service.get('name'))

            return server_addresses, system_names
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while listing server addresses: {str(e)}")
            logging.error(f"An error occurred while listing instance numbers: {str(e)}")
            return None

    @staticmethod
    def find_all_fiori_nwbc_system_names(xml_file_path):
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            fnwbc_system_names = []

            for service in root.findall(".//Service"):
                if service.get('type') == 'FIORI' or service.get('type') == 'NWBC':
                    fnwbc_system_names.append(service.get('name'))

            return fnwbc_system_names

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while getting Fiori/NWBC system names: {str(e)}")
            logging.error(f"An error occurred while getting Fiori/NWBC system names: {str(e)}")

    # def find_url_based_on_name(xml_file_path, name):

    @staticmethod
    def find_fiori_nwbc_system(xml_file_path, url):
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            fnwbc_system = None

            for service in root.findall(".//Service"):
                if service.get('url') is not None:
                    if service.get('url') == url:
                        fnwbc_system = service

            return fnwbc_system

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while finding Fiori/NWBC systems: {str(e)}")
            logging.error(f"An error occurred while finding Fiori/NWBC systems: {str(e)}")

    @staticmethod
    def add_root_tag_to_empty_xml_file(xml_file_path):
        try:
            with open(xml_file_path, 'r') as file:
                content = file.read().strip()  # This will remove leading/trailing whitespaces, newlines etc.

            if not content:
                with open(xml_file_path, 'w') as file:
                    file.write("<Landscape></Landscape>")
        except FileNotFoundError:
            print(f"The file {xml_file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def find_system_info_on_system_id(xml_file_path, system_id):
        try:
            # Parse the XML file
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            server_addresses = []
            names = []
            for service in root.findall(".//Service"):
                if service.get('server') is not None and service.get('systemid') is not None:
                    if service.get('systemid') == system_id:
                        server_addresses.append(service.get('server'))
                        names.append(service.get('name'))

            return server_addresses, names

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while listing server addresses: {str(e)}")
            logging.error(f"An error occurred while listing server addresses: {str(e)}")

    @staticmethod
    def find_urls_based_on_name(xml_file_path, name):
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            urls = []

            for service in root.findall(".//Service"):
                if service.get('name') == name:
                    urls.append(service.get('url'))

            return urls

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while finding URL: {str(e)}")
            logging.error(f"An error occurred while finding URL: {str(e)}")

    @staticmethod
    def find_router_and_message_server_based_on_sid_and_server_address(xml_file_path, sid, server_address):
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            router = None
            message_server = None

            for service in root.findall(".//Service"):
                if service.get('server') == server_address and service.get('systemid') == sid:
                    if service.get('routerid') is not None:
                        router_uuid = service.get('routerid')
                        router = XMLQuery.find_router(xml_file_path, router_uuid).get('name')
                    else:
                        router = 'Not Found'
                    if service.get('msid') is not None:
                        ms_uuid = service.get('msid')
                        message_server_name = XMLQuery.find_message_server(xml_file_path, ms_uuid).get('name')
                        message_server_host = XMLQuery.find_message_server(xml_file_path, ms_uuid).get('host')
                        message_server = f"{message_server_name} - {message_server_host}"

                    else:
                        message_server = 'Not Found'

            return router, message_server

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while finding router and message server: {str(e)}")
            logging.error(f"An error occurred while finding router and message server: {str(e)}")

    @staticmethod
    def find_system(root,system_id,address,system_type):
        try:

            system = None

            for service in root.findall(".//Service"):
                if system_type == 'SAPGUI':
                    if service.get('server') == address and service.get('systemid') == system_id:
                        system = service
                elif system_type == 'FIORI/NWBC':
                    if service.get('url') == address:
                        system = service
                else:
                    messagebox.showerror("Error", f"Unsupported System Type: {system_type}")

            return system

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while finding system: {str(e)}")
            logging.error(f"An error occurred while finding system: {str(e)}")