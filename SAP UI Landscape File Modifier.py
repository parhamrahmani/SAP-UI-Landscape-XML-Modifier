import unittest
import tkinter as tk

from tests.maintest import TestScriptExecution
from tests.xmlutilstests import XmlUtilsTests
from src.ui import menu


def run_tests():
    # Create a test loader
    test_loader = unittest.TestLoader()

    # Load test cases from the test classes
    test_suite = unittest.TestSuite([
        test_loader.loadTestsFromTestCase(TestScriptExecution),
        test_loader.loadTestsFromTestCase(XmlUtilsTests),
    ])

    # Run the test suite
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)


if __name__ == "__main__":
    # Run all tests
    run_tests()

    # Create the GUI window
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
