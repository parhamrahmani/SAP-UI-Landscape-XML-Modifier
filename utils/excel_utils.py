import xml.etree.ElementTree as ET
import pandas as pd

def generate_excel_file(xml_file_path):

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Create a dictionary to store the data
    data_sheet_1 = {

        'Node': [],
        'System Name': [],
        'System Description': [],
        'System Id': [],
        'System Type': [],
        'System Client': [],
        'System URL': [],
        'System Server': [],
        'Router Address': [],
        'Is Duplicate': []
    }
    # Iterate over the nodes
    for node in root.findall('.//Node'):
        node_name = node.get('name')

        # Iterate over the items in the node
        for item_node in node.findall('.//Item'):
            service_id = item_node.get('serviceid')

            # Iterate over Services
            for service in root.findall('.//Service'):
                service_uuid = service.get('uuid')
                service_type = service.get('type')
                if service_uuid == service_id and service_type == 'SAPGUI':
                    service_name = service.get('name')
                    service_description = service.get('description')
                    service_sid = service.get('systemid')
                    service_client = service.get('client')
                    service_url = service.get('url')
                    service_server = service.get('server')

                    # Initialize router_address with an empty string
                    router_address = ''

                    # Find the router based on the router ID
                    for router in root.findall('.//Router'):
                        router_uuid = router.get('uuid')
                        service_router = service.get('routerid')
                        if service_router == router_uuid:
                            router_address = router.get('router')

                    # Add the data to the dictionary
                    data_sheet_1['Node'].append(node_name)
                    data_sheet_1['System Name'].append(service_name)
                    data_sheet_1['System Description'].append(service_description)
                    data_sheet_1['System Id'].append(service_sid)
                    data_sheet_1['System Type'].append(service_type)
                    data_sheet_1['System Client'].append(service_client)
                    data_sheet_1['System URL'].append(service_url)
                    data_sheet_1['System Server'].append(service_server)
                    data_sheet_1['Router Address'].append(router_address)
                    data_sheet_1['Is Duplicate'].append('')

    for service in root.findall('.//Service'):
        servicetype = service.get('type')
        if servicetype != 'SAPGUI':
            servicename = service.get('name')
            servicedescription = service.get('description')
            servicesid = service.get('systemid')
            serviceclient = service.get('client')
            serviceurl = service.get('url')
            serviceserver = service.get('server')

            # Initialize router_address with an empty string
            routeraddress = ''

            # Find the router based on the router ID
            for router in root.findall('.//Router'):
                router_uuid = router.get('uuid')
                service_router = service.get('routerid')
                if service_router == router_uuid:
                    routeraddress = router.get('router')

            # Add the data to the dictionary
            data_sheet_1['Node'].append('*Not included in a node*')
            data_sheet_1['System Name'].append(servicename)
            data_sheet_1['System Description'].append(servicedescription)
            data_sheet_1['System Id'].append(servicesid)
            data_sheet_1['System Type'].append(servicetype)
            data_sheet_1['System Client'].append(serviceclient)
            data_sheet_1['System URL'].append(serviceurl)
            data_sheet_1['System Server'].append(serviceserver)
            data_sheet_1['Router Address'].append(routeraddress)
            data_sheet_1['Is Duplicate'].append('')

    # Create a DataFrame from the data dictionary
    df = pd.DataFrame(data_sheet_1)

    # Mark duplicates in the 'System Server' column if system type is 'SAPGUI'
    df.loc[df['System Type'] == 'SAPGUI', 'Is Duplicate'] = df.duplicated(subset='System Server')

    # Mark duplicates in the 'System URL' column if system type is not 'SAPGUI'
    df.loc[df['System Type'] != 'SAPGUI', 'Is Duplicate'] = df.duplicated(subset='System URL')

    # Save the DataFrame to Excel
    output_file_path = xml_file_path.replace('.xml', '.xlsx')
    df.to_excel(output_file_path, index=False)
    print("Data Dictionary:", data_sheet_1)

    return output_file_path

