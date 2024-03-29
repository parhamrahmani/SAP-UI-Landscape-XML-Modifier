import tkinter as tk

from src.ui.system_addition.adding_system_initial_tab import AddingSystemInitialWindow

from src.ui.excel_export.export_excel_window import export_excel_window
from src.ui.duplication_removal.remove_duplications_window import remove_duplications_window
from src.ui.system_modification.modifying_system_initial_tab import system_modification_initial_tab
from src.ui.system_removal.removing_system_initial_tab import remove_system_window
from src.ui.ui_components.ui_utils import UiUtils

BUTTON_WIDTH = 30
BUTTON_HEIGHT = 2
BUTTON_FONT_SIZE = 12


def create_main_menu_buttons(menu_frame):
    """
        Creates the main menu buttons and adds them to the given frame.

        Args:
            menu_frame (tk.Frame): The frame where the buttons will be added.
        """
    UiUtils.clear_frame(menu_frame)
    add_system_button = tk.Button(
        master=menu_frame,
        text="Add a system from your existing Landscape file to another Landscape file",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: AddingSystemInitialWindow.add_system_window(menu_frame)  # replace with your function
    )
    UiUtils.customize_button(add_system_button)
    add_system_button.pack(pady=10, fill='both')

    remove_system_button = tk.Button(
        master=menu_frame,
        text="Remove a system from your Landscape file",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: remove_system_window(menu_frame)  # replace with your function
    )
    UiUtils.customize_button(remove_system_button)
    remove_system_button.pack(pady=10, fill='both')

    system_modification_button = tk.Button(
        master=menu_frame,
        text="Modify a system from your Landscape file",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: system_modification_initial_tab(menu_frame)
        # replace with your function

    )
    UiUtils.customize_button(system_modification_button)
    system_modification_button.pack(pady=10, fill='both')

    from src.ui.uuid_regen.regenerate_uuids_with_excel_report import regenerate_uuids_with_excel_report
    regenerate_uuids_button = tk.Button(
        master=menu_frame,
        text="Regenerate UUIDs and export Excel Reports",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: regenerate_uuids_with_excel_report(menu_frame)  # replace with your function
    )
    UiUtils.customize_button(regenerate_uuids_button)
    regenerate_uuids_button.pack(pady=10, fill='both')

    remove_duplications_button = tk.Button(
        master=menu_frame,
        text="Remove duplications in your Landscape file",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: remove_duplications_window(menu_frame)  # replace with your function
    )
    UiUtils.customize_button(remove_duplications_button)
    remove_duplications_button.pack(pady=10, fill='both')

    export_excel_button = tk.Button(
        master=menu_frame,
        text="Export Excel Reports of your Landscape file",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: export_excel_window(menu_frame)  # replace with your function
    )
    UiUtils.customize_button(export_excel_button)
    export_excel_button.pack(pady=10, fill='both')

    footer_warning_frame = tk.Frame(menu_frame, bg="white")
    footer_warning_frame.pack(side='bottom', fill='both', expand=True)

    UiUtils.show_red_warning(footer_warning_frame)
    back_button = tk.Button(
        master=menu_frame,
        text="Restart",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=lambda: UiUtils.restart_program()
    )
    UiUtils.customize_button(back_button)
    back_button.pack(side='right', anchor='se', padx=5, pady=5)

    exit_button = tk.Button(
        menu_frame,
        text="Exit",
        background="black",
        foreground="white",
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        command=menu_frame.quit
    )
    UiUtils.customize_button(exit_button)
    exit_button.pack(side='right', anchor='se', padx=5, pady=5)
