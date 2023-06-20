import os
import time


# Function to clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Function to display the program header
def display_header():
    clear_screen()
    print("=============================================")
    print("     SAP UI Landscape XML Modifier")
    print("=============================================")
    print()


# Function to display welcome message

def display_wl_msg():
    print("SAP UI Landscape XML Modifier")
    print("This program allows you to modify SAP UI Landscape XML files by regenerating UUIDs for workspaces,")
    print("nodes, services, and items. It also provides the option to remove includes and rename workspaces,")
    print("in order to make them usable as central files.")
    print()


# Function to display prompts and get user input
def get_user_input(prompt):
    user_input = input(prompt)
    user_input = user_input.strip(' "\'')  # Remove spaces, double quotes, and single quotes
    return user_input


# Function to display error messages
def display_error(message):
    print(f"ERROR: {message}")


# Function to display success messages
def display_success(message):
    print(f"SUCCESS: {message}")


# Function to remove double quotes from a string
def remove_quotes(string):
    if string.startswith('"') and string.endswith('"'):
        return string[1:-1]
    return string


def display_loading_bar():
    print("Exporting in progress, Please Wait", end="")
    for _ in range(10):
        time.sleep(0.1)
        print(".", end="", flush=True)
    print()


def display_menu():
    print("Menu Options:")
    print("1. Regenerate UUIDs and export Excel Reports")
    print("2. Export Excel Reports")
    print("3. Remove duplicate entries (still in development)")
    print("4. Show the statistics of your xml file")


def xml_check(file_path):
    while True:
        if not file_path.lower().endswith('.xml'):
            print("Invalid file path. Please make sure the file path ends with '.xml' in lowercase.")
            file_path = get_user_input("Enter the path to the XML file: ")
        else:
            dir_name, file_name = os.path.split(file_path)
            new_file_name = file_name.lower()
            new_file_path = os.path.join(dir_name, new_file_name)
            return new_file_path
