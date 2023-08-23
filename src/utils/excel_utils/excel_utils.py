import shutil
from src.utils.xml_utils.xml_query import *
import pandas as pd


def generate_excel_files(xml_file_path):
    def generate_excel_file(file_path):
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Create a dictionary to store the data
        data_sheet = {
            'Workspace': [],
            'System URL/System Server': [],
            'System Id': [],
            'System Name': [],
            'System Type': [],
            'Instance Number': [],
            'System Client': [],
            'Router Address': [],
            'Message Server Name': [],
            'Message Server Host': [],
            'System Description': [],
            'Parent Node': [],
            'Child Node': [],
            'Item UUID': [],
            'Service UUID': []
        }

        if root is not None:
            all_items = root.findall('.//Item')
            node_items = root.findall('.//Node/Item')
            child_node_items = root.findall('.//Node/Node/Item')
            workspaces = root.findall('.//Workspace')
            services = root.findall('.//Service')
            routers = root.findall('.//Router')
            messageservers = root.findall('.//Messageserver')

            for workspace in workspaces:
                workspace_name = workspace.get('name')

                for node in workspace.findall('.//Node'):
                    parent_node_name = node.get('name')

                    for item_node in node.findall('.//Item'):
                        if item_node not in child_node_items:
                            add_service_data(workspace_name, parent_node_name, '', item_node,
                                             data_sheet,
                                             services,
                                             routers,
                                             messageservers)

                    for child_node in node.findall('.//Node'):
                        child_node_name = child_node.get('name')

                        for child_item_node in child_node.findall('.//Item'):
                            add_service_data(workspace_name, parent_node_name, child_node_name, child_item_node,
                                             data_sheet, services, routers, messageservers)

                for item in all_items:
                    if item not in node_items and item not in child_node_items:
                        add_service_data(workspace_name, '', '', item, data_sheet, services, routers, messageservers)

        # Create a DataFrame from the data dictionary
        df = pd.DataFrame(data_sheet)

        # Save the DataFrame to Excel
        output_file_path = file_path.replace('.xml', '.xlsx')
        df.to_excel(output_file_path, index=False)

        return output_file_path

    # Call the original generate_excel_file function to generate the general Excel file
    general_file_path = generate_excel_file(xml_file_path)

    # Read the general Excel file into a DataFrame
    df = pd.read_excel(general_file_path)

    # Find duplicates based on specific columns
    duplicates = df[df.duplicated(subset=['System Name', 'System Description', 'System Id', 'System Type'],
                                  keep=False)].copy()

    # Generate the duplicate file path
    duplicate_file_path = general_file_path.replace('.xlsx', '_duplicates.xlsx')

    # Save the duplicate DataFrame to a new Excel file
    duplicates.to_excel(duplicate_file_path, index=False)

    return general_file_path, duplicate_file_path


def export_excel(xml_file_path):
    try:
        # Generate the Excel files
        general_excel_file, duplicates_excel_file = generate_excel_files(xml_file_path)

        output_path = os.path.dirname(xml_file_path)
        output_name_gen = os.path.basename(xml_file_path).split('.')[0] + "_general"
        output_name_dupl = os.path.basename(xml_file_path).split('.')[0] + "_duplications"
        output_file_gen = os.path.join(output_path, output_name_gen + '.xlsx')
        output_file_dupl = os.path.join(output_path, output_name_dupl + '.xlsx')
        shutil.move(general_excel_file, output_file_gen)
        shutil.move(duplicates_excel_file, output_file_dupl)

        messagebox.showinfo("Success!", f"General Excel Sheet saved to: \n{output_file_gen}\n"
                                        f"Duplicate System Excel Sheet  saved to: \n{output_file_dupl}")
        os.startfile(output_path)

    except Exception as e:
        messagebox.showerror("Error!", f"Error while generating Excel file: \n{e}")
        logging.error(f"Error while generating Excel file: \n{e}")


def add_service_data(workspace_name, parent_node_name, child_node_name, item, data_sheet,
                     services, routers, messageservers):
    service_id = item.get('serviceid')
    existing_service_uuids = data_sheet['Service UUID']  # Get the existing service UUIDs

    for service in services:
        service_uuid = service.get('uuid')
        if service_uuid == service_id and service_uuid not in existing_service_uuids:
            service_type = service.get('type')
            service_name = service.get('name')
            service_description = service.get('description')
            service_sid = service.get('systemid')
            service_client = service.get('client')
            if service_type == 'SAPGUI':
                service_server = service.get('server')
                instance_number = service_server.split(':')[-1][-2:]
            else:
                service_server = service.get('url')
                instance_number = ''

                router_address = ''
                for router in routers:
                    router_uuid = router.get('uuid')
                    service_router = service.get('routerid')

                    if service_router == router_uuid:
                        router_address = router.get('router')
                        break

                messageserver_address = ''
                messageserver_name = ''
                for messageserver in messageservers:
                    messageserver_uuid = messageserver.get('uuid')
                    service_messageserver = service.get('msid')

                    if service_messageserver == messageserver_uuid:
                        messageserver_address = messageserver.get('host')
                        messageserver_name = messageserver.get('name')
                        break

                data_sheet['Workspace'].append(workspace_name)
                data_sheet['Parent Node'].append(parent_node_name)
                data_sheet['Child Node'].append(child_node_name)
                data_sheet['System Name'].append(service_name)
                data_sheet['System Description'].append(service_description)
                data_sheet['System Id'].append(service_sid)
                data_sheet['System Type'].append(service_type)
                data_sheet['System Client'].append(service_client)
                data_sheet['Instance Number'].append(instance_number)
                data_sheet['System URL/System Server'].append(service_server)
                data_sheet['Router Address'].append(router_address)
                data_sheet['Message Server Name'].append(messageserver_name)
                data_sheet['Message Server Host'].append(messageserver_address)
                data_sheet['Item UUID'].append(item.get('uuid'))
                data_sheet['Service UUID'].append(service_uuid)
