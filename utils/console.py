import os

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
