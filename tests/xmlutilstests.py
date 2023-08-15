import unittest
import xml.etree.ElementTree as ET

from utils.xml_utils import regenerate_workspace_uuids, regenerate_service_uuids, remove_global_includes, \
    find_custom_system, list_nodes_of_workspace, list_all_workspaces, find_message_server, find_router

# Define the test global XML code
XML_CODE = '''<Landscape version="1" updated="2023-07-26T14:14:41" origin="" generator="RSLSMT"> <Workspaces> 
<Workspace name="Test" uuid="be02f91d-3346-45b8-a882-c4775ceafae4" expanded="0"> <Node 
uuid="bb992700-13ab-4ea8-aef8-7d06709320a1" name="TestNode1" expanded="0" hidden="0"> <Item 
uuid="bf859504-e061-4813-b324-40e55d94cee0" serviceid="41f6868e-a9ec-4904-bf24-62bd0f1929e0"/> </Node> <Node 
uuid="b893ec1d-66dc-46d1-8230-4de8bb78518f" name="TestNode2" expanded="0" hidden="0"> <Item 
uuid="19729f66-988f-4177-9feb-366a08168957" serviceid="639ed096-b42d-481d-8411-2f1d5c2cf8e4"/> </Node> <Node 
uuid="40c0cde5-3562-46d1-9464-98ec85a96f13" name="TestNode3" expanded="0" hidden="0"> <Item 
uuid="706afd61-76ff-4780-addf-7e377f49d945" serviceid="8e7bafac-ecc4-4796-8f3e-93e7c0598df8"/> </Node> <Node 
uuid="d630d047-4e9b-4e04-9454-595a8487fdca" name="TestNode4" expanded="0" hidden="0"> <Item 
uuid="d630d047-4e9b-4e04-9454-595a8487fdca" serviceid="d64963be-1300-4ccb-8825-28c8a1865004"/> </Node> </Workspace> 
</Workspaces> <Services> <Service uuid="80cc5f49-0678-4047-8a9d-9a22d8606f5c" name="Test Service GUI" 
server="555.555.555.555:3200" type="SAPGUI" sncop="-1" mode="1" routerid="40c0cde5-3562-46d1-9464-98ec85a96f13" 
dcpg="2" sapcpg="1100"/> <Service uuid="41f6868e-a9ec-4904-bf24-62bd0f1929e0" name="tEST GUI" 
server="test.sap.shcdc.de:3200" type="SAPGUI" sncop="-1" mode="1" systemid="MK6" 
routerid="b893ec1d-66dc-46d1-8230-4de8bb78518f" dcpg="2" sapcpg="1100"/> <Service 
uuid="639ed096-b42d-481d-8411-2f1d5c2cf8e4" name="Test Service NWBC" type="NWBC" 
url="http://sapservertest.sap.test.test.test:8010/sap/test/nwbc" slc="0"/> <Service 
uuid="8e7bafac-ecc4-4796-8f3e-93e7c0598df8" name="Test Service Fiori" type="FIORI" 
url="https://test.test-test.de:885/nwbc/"/> <Service uuid="d64963be-1300-4ccb-8825-28c8a1865004" 
name="TEST_LOGONGROUP [GROUP]" msid="668e74b2-2915-4500-a557-1743a37b5d96" server="SPACE" type="SAPGUI" sncop="-1" 
systemid="P20" routerid="40c0cde5-3562-46d1-9464-98ec85a96f13" dcpg="2" sapcpg="1100"/> </Services> <Includes> 
<Include url="file:///C:/Users/TESTUSER/AppData/Roaming/SAP/Common/SAPUILandscapeGlobal.xml" index="0" 
description="SAP Reserved"/> </Includes> <Routers> <Router name="/H/sr1.shcdc.eu" 
uuid="40c0cde5-3562-46d1-9464-98ec85a96f13" router="/H/sr1.shcdc.eu" description="/H/sr1.shcdc.eu"/> </Routers> 
<Messageservers> <Messageserver name="P20" uuid="668e74b2-2915-4500-a557-1743a37b5d96" 
host="sapp20ms.sapms.fresenius.de" port="3601"/> </Messageservers> </Landscape>'''


class XmlUtilsTests(unittest.TestCase):
    def setUp(self):
        self.xml_file_path = "test_xml_file.xml"
        with open(self.xml_file_path, "w") as temp_xml_file:
            temp_xml_file.write(XML_CODE)

    def tearDown(self):
        import os
        os.remove(self.xml_file_path)

    def test_regenerate_workspace_uuids(self):
        # Parse the XML
        root = ET.fromstring(XML_CODE)
        services = root.find('Services').findall('Service')

        # Collect the old UUIDs
        old_service_uuids = [service.get('uuid') for service in services]

        # Call the function
        regenerate_workspace_uuids(services)

        # Check the changes
        for service in services:
            new_uuid_attr = service.get('uuid')
            self.assertIsNotNone(new_uuid_attr)
            self.assertNotEqual(new_uuid_attr, "")
            self.assertNotIn(new_uuid_attr, old_service_uuids)

            expanded_attr = service.get('expanded')
            self.assertEqual(expanded_attr, "0")

            name_attr = service.get('name')
            if name_attr.lower() == "local":
                self.assertEqual(name_attr, "Default")

    def test_regenerate_service_uuids(self):
        # Parse the XML
        root = ET.fromstring(XML_CODE)

        # Collect the old UUIDs
        old_service_uuids = [service.get('uuid') for service in root.findall(".//Service")]
        old_item_uuids = [item.get('uuid') for item in root.findall(".//Item")]

        # Call the function
        regenerate_service_uuids(root)

        # Check if UUIDs have been regenerated
        for service in root.findall(".//Service"):
            new_uuid = service.get('uuid')
            self.assertIsNotNone(new_uuid)
            self.assertNotEqual(new_uuid, "")
            self.assertNotIn(new_uuid, old_service_uuids)

        for item in root.findall(".//Item"):
            new_item_uuid = item.get('uuid')
            self.assertIsNotNone(new_item_uuid)
            self.assertNotEqual(new_item_uuid, "")
            self.assertNotIn(new_item_uuid, old_item_uuids)

    def test_remove_global_includes(self):
        # Parse the XML
        root = ET.fromstring(XML_CODE)
        includes = root.find('Includes')

        # Call the function
        removed = remove_global_includes(root)

        if removed:
            # Check if global includes have been removed
            remaining_includes = includes.findall(".//Include")
            for include in remaining_includes:
                include_url = include.get("url")
                self.assertNotIn("SAPUILandscapeGlobal.xml", include_url)
        else:
            self.fail("Global includes were not removed")

    def test_find_custom_system(self):
        # Create a temporary XML file with the sample XML code
        temp_xml_path = "temp_xml_file.xml"
        with open(temp_xml_path, "w") as temp_xml_file:
            temp_xml_file.write(XML_CODE)

        # Test successful cases

        sap_system = find_custom_system(temp_xml_path, "test.sap.shcdc.de", "00", "MK6")
        self.assertIsNotNone(sap_system)
        self.assertEqual(sap_system.get('server'), "test.sap.shcdc.de:3200")
        self.assertEqual(sap_system.get('systemid'), "MK6")
        print(sap_system.get('server') + " actual\n" + "test.sap.shcdc.de:3200" + " expected\n")

        # Clean up by deleting the temporary XML file
        import os
        os.remove(temp_xml_path)

    def test_find_router(self):
        routerid = "40c0cde5-3562-46d1-9464-98ec85a96f13"
        router = find_router(self.xml_file_path, routerid)
        self.assertIsNotNone(router)
        self.assertEqual(router.get('uuid'), routerid)

    def test_find_message_server(self):
        msid = "668e74b2-2915-4500-a557-1743a37b5d96"
        message_server = find_message_server(self.xml_file_path, msid)
        self.assertIsNotNone(message_server)
        self.assertEqual(message_server.get('uuid'), msid)

    def test_list_all_workspaces_existing(self):
        workspaces = list_all_workspaces(self.xml_file_path)
        self.assertIsNotNone(workspaces)
        self.assertTrue(len(workspaces) > 0)

    def test_list_all_workspaces_non_existing(self):
        empty_xml_path = "empty_xml_file.xml"
        with open(empty_xml_path, "w") as empty_xml_file:
            empty_xml_file.write("<Landscape></Landscape>")
        workspaces = list_all_workspaces(empty_xml_path)
        self.assertIsNotNone(workspaces)
        self.assertEqual(len(workspaces), 0)
        import os
        os.remove(empty_xml_path)

    def test_list_nodes_of_workspace(self):
        workspace_name = "Test"
        node_names = list_nodes_of_workspace(self.xml_file_path, workspace_name)
        expected_node_names = ["TestNode1", "TestNode2", "TestNode3", "TestNode4"]
        self.assertEqual(node_names, expected_node_names)


if __name__ == '__main__':
    unittest.main()
