import unittest
import hashlib
import os
from src.insert_localizer import InsertLocalizer

class TestInsertLocalizer(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment by creating temporary files for testing.
        """
        self.prepend_data = "PREPEND_DATA"
        self.append_data = "APPEND_DATA"
        self.chunk_size = 16
        self.localizer = InsertLocalizer(
            prepend_data=self.prepend_data, 
            append_data=self.append_data, 
            chunk_size=self.chunk_size
        )
        
        # Original file content
        self.original_content = b"Original file content."
        self.original_file_path = "original_test_file.txt"
        with open(self.original_file_path, "wb") as f:
            f.write(self.original_content)

        # Create a modified file with insertion
        self.modified_content = b"Original fiINSERT_HEREle content."
        self.modified_file_path = "modified_test_file.txt"
        with open(self.modified_file_path, "wb") as f:
            f.write(self.modified_content)

        # Compute the original hash
        full_data = (
            self.prepend_data.encode('utf-8') + 
            self.original_content + 
            self.append_data.encode('utf-8')
        )
        self.original_hash = hashlib.sha256(full_data).hexdigest()

    def tearDown(self):
        """
        Clean up temporary files.
        """
        if os.path.exists(self.original_file_path):
            os.remove(self.original_file_path)
        if os.path.exists(self.modified_file_path):
            os.remove(self.modified_file_path)

    def test_compute_hash_with_known_data(self):
        """
        Test computing the hash with known data.
        """
        computed_hash = self.localizer.compute_hash_with_known_data(self.original_file_path)
        self.assertEqual(computed_hash, self.original_hash)

    def test_compare_hashes(self):
        """
        Test comparing original and modified hashes.
        """
        modified_hash = self.localizer.compute_hash_with_known_data(self.modified_file_path)
        self.assertFalse(self.localizer.compare_hashes(self.original_hash, modified_hash))

    def test_localize_insertion(self):
        """
        Test localization of the insertion.
        """
        result = self.localizer.localize_insertion(self.modified_file_path, self.original_hash)
        # Expected location of insertion is byte index 12 (after "Original fi")
        self.assertIn("Modification detected at byte 12", result)

    def test_no_modification_detected(self):
        """
        Test behavior when no modification is detected.
        """
        result = self.localizer.localize_insertion(self.original_file_path, self.original_hash)
        self.assertEqual(result, "No modification detected in the file.")

    def test_error_handling(self):
        """
        Test behavior when an invalid file path is provided.
        """
        result = self.localizer.localize_insertion("non_existent_file.txt", self.original_hash)
        self.assertIn("Error processing file for insertion localization", result)

if __name__ == "__main__":
    unittest.main()
