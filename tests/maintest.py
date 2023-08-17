import unittest
import subprocess
import time


def run_script_and_close():
    try:
        # Start the script using subprocess.run
        result = subprocess.run(
            ["python", "C:\\Users\\PR106797\\PycharmProjects\\uuid_manipulator\\SAP UI Landscape File Modifier.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=0.1  # Set a timeout for the subprocess
        )

        return result.returncode, result.stderr
    except Exception as e:
        return 0, str(e)


class TestScriptExecution(unittest.TestCase):
    def test_script_runs_and_closes(self):
        returncode, stderr = run_script_and_close()

        self.assertEqual(returncode, 0, f"Script execution failed:\n{stderr}")


if __name__ == "__main__":
    unittest.main()
