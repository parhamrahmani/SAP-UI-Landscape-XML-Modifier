import tkinter as tk



"""
This script creates a GUI for SAP UI Landscape XML Modifier. 

When run, it opens a new window with the title "SAP UI Landscape XML Modifier", 
creates a frame for the main menu, and then calls a function to create the main menu buttons.

The `__name__ == "__main__"` block ensures that the GUI is created only when this script is run directly, 
and not when it is imported as a module.
"""

if __name__ == "__main__":
    from ui import menu
    root_tk = tk.Tk()
    root_tk.geometry("600x650")
    root_tk.resizable(True, True)
    root_tk.configure(bg="white")
    root_tk.title("SAP UI Landscape XML Modifier")

    # Create a title label
    title_label = tk.Label(root_tk, text="SAP UI Landscape XML Modifier", font=("Arial", 12, "bold"), bg="white")
    title_label.pack(pady=20)

    # Create a frame for the menu options buttons
    menu_frame = tk.Frame(root_tk, bg="white")
    menu_frame.pack()

    menu.create_main_menu_buttons(menu_frame)

    root_tk.mainloop()
