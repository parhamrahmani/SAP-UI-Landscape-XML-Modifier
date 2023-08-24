from tkinter import messagebox
import xml.etree.ElementTree as ET

from src.utils.xml_utils.xml_query import XMLQuery


class SystemModification:
    @staticmethod
    def modify_system(sap_system, new_system_name, new_sid, new_address, system_type, xml_path):
        try:
            # Parse the  XML file
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Find the system in the XML file

            if root is not None:

                if system_type == 'SAPGUI':
                    fetched_system = XMLQuery.find_system(root, sap_system.get('systemid'), sap_system.get('server'), 'SAPGUI')
                    if fetched_system is not None:
                        fetched_system.set('name', new_system_name)
                        fetched_system.set('systemid', new_sid)
                        fetched_system.set('server', new_address)
                        tree.write(xml_path)
                        messagebox.showinfo("Success", "System modified successfully"
                                                       "\n System Info: \n\n"
                                                       f"System Name: {fetched_system.get('name')}\n"
                                                       f"SID: {fetched_system.get('systemid')}\n"
                                                       f"Server: {fetched_system.get('server')}\n\n"
                                                       f"Output file saved at: " + xml_path)
                    else:
                        messagebox.showinfo("Error", "System not found")
                elif system_type == 'FIORI/NWBC':
                    fetched_system = XMLQuery.find_system(root, None, sap_system.get('url'), 'FIORI/NWBC')
                    if fetched_system is not None:
                        fetched_system.set('name', new_system_name)
                        fetched_system.set('url', new_address)
                        tree.write(xml_path)
                        messagebox.showinfo("Success", "System modified successfully"
                                                       "\n System Info: \n\n"
                                                       f"System Name: {fetched_system.get('name')}\n"
                                                       f"URL: {fetched_system.get('url')}\n\n"
                                                       f"Output file saved at: " + xml_path)
                    else:
                        messagebox.showinfo("Error", "System not found")

                else:
                    messagebox.showinfo("Error", f"System type not supported: {system_type}")

        except Exception as e:
            messagebox.showinfo("Error", f"Error in modify_system(): {e}")
