from tkinter import messagebox, filedialog


from utils.xml_utils import get_stats
import tkinter as tk


def show_stats_window(menu_frame):
    from gui.menu import clear_frame, create_exit_restart_buttons
    # Clear the main window
    clear_frame(menu_frame)

    def show_stats():
        xml_file_path = xml_path_entry.get()
        if xml_file_path.endswith('.xml'):
            clear_frame(menu_frame)  # Clear the window
            file_label = tk.Label(menu_frame, text=f"Statistics: ", font=("Arial", 14, "bold"), bg="white")
            file_label.pack(pady=10)
            stats = get_stats(xml_file_path)
            stats_text = "\n".join([f"{k}: {v}" for k, v in stats.items()])
            stats_label = tk.Label(menu_frame, text=stats_text, font=("Arial", 14), bg="white")
            stats_label.pack(pady=10)
            create_exit_restart_buttons(menu_frame)
        else:
            messagebox.showwarning("Invalid File Warning", "Please put the address of an XML file")

    def select_xml_file():
        xml_file_path = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
        if xml_file_path:
            xml_path_entry.delete(0, tk.END)  # Clear the entry field
            xml_path_entry.insert(tk.END, xml_file_path)  # Insert the selected file path

    file_label = tk.Label(menu_frame, text="Please put the address of an XML file", font=("Arial", 14, "bold"),
                          bg="white")
    file_label.pack(pady=10)

    entry_frame = tk.Frame(menu_frame)
    entry_frame.pack(pady=10)

    xml_path_entry = tk.Entry(entry_frame, width=50)  # Entry widget to input XML file path
    xml_path_entry.pack(side='left')

    browse_button = tk.Button(entry_frame, text="Browse", command=select_xml_file, background="black",foreground="white")
    browse_button.pack(side='left', padx=5)

    show_stats_button = tk.Button(entry_frame, text="Show Stats", command=show_stats, background="black",foreground="white")
    show_stats_button.pack(side="left", pady=5)

    create_exit_restart_buttons(menu_frame)

