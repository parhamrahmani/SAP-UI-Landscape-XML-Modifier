from utils.xml_utils import *
from utils.console import *


def main():
    while True:
        display_header()
        display_wl_msg()
        display_menu()
        choice = get_user_input("Enter your choice: ")

        # Prompt the user for the XML file path
        while True:
            xml_file_path = get_user_input("Enter the path to the XML file: ")
            xml_file_path = xml_check(xml_file_path)
            xml_file_path = remove_quotes(xml_file_path)

            if not os.path.isfile(xml_file_path):
                display_error("Invalid XML file path. Please try again.")
            else:
                break

        if choice == '1':
            # Prompt the user for the XML file path
            while True:
                xml_file_path_destination = get_user_input(
                    "Enter the path to the XML file you want to add the system to: \n"
                    "(Attention always use a copy of the original file): ")
                print("\n")
                xml_file_path_destination = xml_check(xml_file_path_destination)
                xml_file_path_destination = remove_quotes(xml_file_path_destination)
                if not os.path.isfile(xml_file_path_destination):
                    display_error("Invalid XML file path. Please try again.")
                else:
                    break
            add_systems_to_xml(xml_file_path, xml_file_path_destination)
        elif choice == '2':
            regenerate_uuids_export_excel(xml_file_path)
        elif choice == '3':
            if not xml_check(xml_file_path):
                display_error("Invalid XML file path. Please try again.")
                continue
            export_excel(xml_file_path)
        elif choice == '4':
            remove_duplicates(xml_file_path)
        elif choice == '5':
          print("now in gui")
        elif choice == '6':
            extract_from_nodes(xml_file_path)

        else:
            display_error("Invalid choice. Please try again.")

        time.sleep(1)  # Delay for 1 second before prompting for input

        user_choice = get_user_input("Enter 'n' to perform another operation or 'q' to exit: ")
        if user_choice.lower() == 'q':
            break


if __name__ == "__main__":
    main()