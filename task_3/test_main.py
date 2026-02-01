import unittest
import sys
import io
import re
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

from main import display_directory_structure, main

class TestDirectoryVisualizer(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory with a known structure for testing."""
        self.test_dir = Path(tempfile.mkdtemp())
        (self.test_dir / "sub_dir2").mkdir()
        (self.test_dir / "sub_dir1").mkdir()
        (self.test_dir / "file2.log").touch()
        (self.test_dir / "sub_dir1" / "file1.txt").touch()
        (self.test_dir / "a_file.txt").touch()

    def tearDown(self):
        """Remove the temporary directory after tests."""
        shutil.rmtree(self.test_dir)

    def test_display_structure(self):
        """Test the output of the directory structure display function."""
        # Redirect stdout to capture the print output
        captured_output = io.StringIO()
        with patch('sys.stdout', new=captured_output):
            display_directory_structure(self.test_dir)

        # Strip ANSI color codes for a clean comparison
        clean_output = re.sub(r'\x1b\[[0-9;]*m', '', captured_output.getvalue())

        # Define the expected structure (order matters due to sorting)
        expected_structure = (
            "┣━━ sub_dir1\n"
            "┃   ┗━━ file1.txt\n"
            "┣━━ sub_dir2\n"
            "┣━━ a_file.txt\n"
            "┗━━ file2.log\n"
        )

        self.assertEqual(clean_output, expected_structure)

    def test_main_no_args(self):
        """Test main function exits when no arguments are provided."""
        with patch('sys.argv', ['main.py']), \
             self.assertRaises(SystemExit) as cm, \
             patch('sys.stdout', new_callable=io.StringIO):
            main()
        self.assertEqual(cm.exception.code, 1)

    def test_main_non_existent_path(self):
        """Test main function exits for a path that does not exist."""
        with patch('sys.argv', ['main.py', 'non_existent_dir_xyz']), \
             self.assertRaises(SystemExit) as cm, \
             patch('sys.stdout', new_callable=io.StringIO):
            main()
        self.assertEqual(cm.exception.code, 1)

    def test_main_path_is_file(self):
        """Test main function exits for a path that is a file."""
        file_path = self.test_dir / "file2.log"
        with patch('sys.argv', ['main.py', str(file_path)]), \
             self.assertRaises(SystemExit) as cm, \
             patch('sys.stdout', new_callable=io.StringIO):
            main()
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
