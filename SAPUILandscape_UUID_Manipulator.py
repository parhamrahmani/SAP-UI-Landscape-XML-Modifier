
from utils.xml_utils import *
from utils.console import *


def main():
    while True:
        display_header()
        display_wl_msg()

        # Prompt the user for the XML file path
        while True:
            xml_file_path = get_user_input("Enter the path to the XML file: ")
            xml_file_path = remove_quotes(xml_file_path)

            if not os.path.isfile(xml_file_path):
                display_error("Invalid XML file path. Please try again.")
            else:
                break

        display_menu()
        choice = get_user_input("Enter your choice (1 or 2): ")

        if choice == '1':
            regenerate_uuids_export_excel(xml_file_path)
        elif choice == '2':
            export_excel(xml_file_path)
        else:
            display_error("Invalid choice. Please try again.")

        time.sleep(1)  # Delay for 1 second before prompting for input

        user_choice = get_user_input("Enter 'n' to perform another operation or 'q' to exit: ")
        if user_choice.lower() == 'q':
            break


if __name__ == "__main__":
    main()
