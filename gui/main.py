import tkinter as tk
import gui.menu as main_menu

if __name__ == "__main__":
    root_tk = tk.Tk()
    root_tk.geometry("600x600")
    root_tk.resizable(True, True)
    root_tk.configure(bg="white")
    root_tk.title("SAP UI Landscape XML Modifier")

    # Create a title label
    title_label = tk.Label(root_tk, text="SAP UI Landscape XML Modifier", font=("Arial", 12, "bold"), bg="white")
    title_label.pack(pady=20)

    # Create a frame for the menu options buttons
    menu_frame = tk.Frame(root_tk, bg="white")
    menu_frame.pack()

    main_menu.create_main_menu_buttons(menu_frame)

    root_tk.mainloop()
