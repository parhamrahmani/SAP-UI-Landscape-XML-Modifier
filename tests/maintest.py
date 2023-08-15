import unittest
import subprocess
import pyautogui
import time


class TestScriptExecution(unittest.TestCase):
    def test_script_runs_without_error(self):
        try:
            # Start the script in a subprocess
            process = subprocess.Popen(
                ["python", "C:\\Users\\PR106797\\PycharmProjects\\uuid_manipulator\\SAP UI Landscape File Modifier.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True)

            # Wait for a few seconds for the app to open
            time.sleep(1)

            # Simulate pressing Alt+F4 to close the application
            pyautogui.hotkey('alt', 'f4')

            # Wait for the process to complete
            stdout, stderr = process.communicate()

            self.assertEqual(process.returncode, 0, f"Script execution failed:\n{stderr}")
        except Exception as e:
            self.fail(f"Test setup failed: {e}")


if __name__ == "__main__":
    unittest.main()
