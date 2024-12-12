import os
import random
import string

class Files:
    @staticmethod
    def create_txt_file(file_path: str, content: str = "") -> bool:
        """
        Create a text file at the specified path with optional content.
        
        Args:
            file_path (str): Path where the file should be created
            content (str): Content to write in the file (default empty)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            dir_path = os.path.dirname(file_path)
            print(f"Attempting to create file at: {file_path}")
            if dir_path and not os.path.exists(dir_path):
                print(f"Creating directory: {dir_path}")
                os.makedirs(dir_path, exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error creating file: {e}")
            return False

    @staticmethod
    def get_files_in_folder(folder_path: str, extension: str = None) -> list:
        """
        Get a list of files in the specified folder.
        
        Args:
            folder_path (str): Path to the folder to scan
            extension (str): Optional file extension filter (e.g., '.txt')
            
        Returns:
            list: List of file names in the folder
        """
        try:
            if not os.path.exists(folder_path):
                return []
            
            files = os.listdir(folder_path)
            if extension:
                files = [f for f in files if f.endswith(extension)]
            return files
        except Exception as e:
            print(f"Error reading folder: {e}")
            return []
