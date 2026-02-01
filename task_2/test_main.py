import unittest
from pathlib import Path
import sys
import io

from main import get_cats_info

class TestGetCatsInfo(unittest.TestCase):

    def setUp(self):
        """Set up temporary files for testing."""
        self.cats_file = Path("test_cats_data.txt")
        self.cats_file.write_text(
            "60b90c1c13067a15887e1ae1,Tayson,3\n"
            "60b90c2413067a15887e1ae2,Vika,1\n"
        )

        self.empty_file = Path("empty_test_file.txt")
        self.empty_file.touch()

        self.malformed_file = Path("malformed_test_file.txt")
        self.malformed_file.write_text(
            "id1,name1,age1\n"
            "id2,name2\n"
            "id3,name3,age3\n"
        )

    def tearDown(self):
        """Clean up temporary files."""
        self.cats_file.unlink()
        self.empty_file.unlink()
        self.malformed_file.unlink()

    def test_normal_file(self):
        """Test with a correctly formatted file."""
        expected_output = [
            {"id": "60b90c1c13067a15887e1ae1", "name": "Tayson", "age": "3"},
            {"id": "60b90c2413067a15887e1ae2", "name": "Vika", "age": "1"},
        ]
        self.assertEqual(get_cats_info(self.cats_file), expected_output)

    def test_file_not_found(self):
        """Test when the file does not exist."""
        self.assertEqual(get_cats_info("non_existent_file.txt"), [])

    def test_empty_file(self):
        """Test with an empty file."""
        self.assertEqual(get_cats_info(self.empty_file), [])

    def test_malformed_file(self):
        """Test with a file containing malformed lines."""
        expected_output = [
            {"id": "id1", "name": "name1", "age": "age1"},
            {"id": "id3", "name": "name3", "age": "age3"},
        ]
        self.assertEqual(get_cats_info(self.malformed_file), expected_output)

if __name__ == "__main__":
    unittest.main()
