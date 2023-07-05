from tkinter import messagebox, filedialog


from utils.xml_utils import get_stats, select_xml_file
import tkinter as tk


def show_stats_window(menu_frame):
    """
     Displays a window to provide statistics of an XML file representing the user's system landscape.
     The user inputs an XML file path, either manually or through a file dialog. On selection of the
     'Show Stats' button, the function provides statistics of the XML file.

     Args:
         menu_frame (tk.Frame): The frame where the statistics window will be displayed.
     """
    from gui.menu import clear_frame, create_exit_restart_buttons
    # Clear the main window
    clear_frame(menu_frame)

    def show_stats():
        """
            Displays statistics of the XML file specified in the xml_path_entry field.
            If the entered path does not end with '.xml', a warning message is displayed.
            The statistics are displayed as labels within a frame, and includes the
            total number of entities within the XML file.
            """
        xml_file_path = xml_path_entry.get()
        if xml_file_path.endswith('.xml'):
            clear_frame(menu_frame)  # Clear the window
            file_label = tk.Label(menu_frame, text=f"Statistics: ", font=("Arial", 12, "bold"), bg="white")
            file_label.pack(pady=25)
            # Make a new frame for the stats
            stats_frame = tk.Frame(menu_frame, bg="white")
            stats_frame.pack(pady=25)
            # Get the stats
            stats = get_stats(xml_file_path)
            for i, (k, v) in enumerate(stats.items()):
                stats_label = tk.Label(stats_frame, text=f"{k}: ", font=("Arial", 10, "bold"), bg="white")
                stats_value = tk.Label(stats_frame, text=f"{v}", font=("Arial", 10), bg="white")
                stats_label.grid(row=i, column=0, sticky='w')
                stats_value.grid(row=i, column=1, sticky='w')

            create_exit_restart_buttons(menu_frame)
        else:
            messagebox.showwarning("Invalid File Warning", "Please put the address of an XML file")



    description_label = tk.Label(
        menu_frame,
        text="Warnings:\n\n"
             "1. This function will read your xml file and shows the statistics of your landscape file.\n"
        ,
        font=("Arial", 10, "bold"),
        bg="white",
        anchor='w',
        justify='left'
    )
    description_label.pack(pady=10)
    important_warning = tk.Label(menu_frame, text="IMPORTANT: Please make sure to backup your XML file before\n and"
                                                  " use a copy of it for this function ",
                                 font=("Arial", 10, "bold"),
                                 bg="white",
                                 fg="red",
                                 anchor='w',
                                 justify='left')
    important_warning.pack(pady=10)
    file_label = tk.Label(menu_frame, text="Please put the address of an XML file", font=("Arial", 10, "bold"),
                          bg="white")
    file_label.pack(pady=10)

    entry_frame = tk.Frame(menu_frame)
    entry_frame.pack(pady=10)

    xml_path_entry = tk.Entry(entry_frame, width=50)  # Entry widget to input XML file path
    xml_path_entry.pack(side='left')

    browse_button = tk.Button(entry_frame, text="Browse", command=lambda : select_xml_file(xml_path_entry), background="black",foreground="white")
    browse_button.pack(side='left', padx=5)

    show_stats_button = tk.Button(entry_frame, text="Show Stats", command=show_stats, background="black",foreground="white")
    show_stats_button.pack(side="left", pady=5)

    create_exit_restart_buttons(menu_frame)

