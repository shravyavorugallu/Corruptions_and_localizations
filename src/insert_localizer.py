import hashlib

class InsertLocalizer:
    def __init__(self, prepend_data: str, append_data: str, chunk_size: int = 1024):
        """
        Initialize the InsertLocalizer with known data and chunk size.
        
        Args:
            prepend_data (str): Known data to prepend to the file.
            append_data (str): Known data to append to the file.
            chunk_size (int): Size of chunks to split the file for comparison. Default is 1024 bytes.
        """
        self.prepend_data = prepend_data
        self.append_data = append_data
        self.chunk_size = chunk_size

    def compute_hash_with_known_data(self, file_path: str) -> str:
        """
        Compute the SHA-256 hash of the file with prepended and appended known data.
        
        Args:
            file_path (str): Path to the file to check.
        
        Returns:
            str: The SHA-256 hash of the modified file content.
        """
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()

            # Concatenate known data and the file content
            full_data = (self.prepend_data.encode('utf-8') + file_data + self.append_data.encode('utf-8'))
            
            return hashlib.sha256(full_data).hexdigest()
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return None

    def compare_hashes(self, original_hash: str, modified_hash: str) -> bool:
        """
        Compare the original and modified hashes to determine if there is corruption.
        
        Args:
            original_hash (str): The original file hash before modification.
            modified_hash (str): The hash after the file has been modified.
        
        Returns:
            bool: True if the hashes match, False if they differ.
        """
        return original_hash == modified_hash

    def localize_insertion(self, file_path: str, original_hash: str) -> str:
        """
        Localize the insertion or corruption within the file based on hash mismatch.
        
        This function splits the file into chunks and checks for differences in hashes.
        
        Args:
            file_path (str): The path to the file to check.
            original_hash (str): The original hash of the file.
        
        Returns:
            str: A message indicating where the insertion or corruption occurred.
        """
        # Compute the modified file hash
        modified_hash = self.compute_hash_with_known_data(file_path)

        # Compare the hashes
        if modified_hash is None:
            return "Error processing file for insertion localization."

        if self.compare_hashes(original_hash, modified_hash):
            return "No modification detected in the file."

        # If hashes differ, attempt to localize where the insertion occurred
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()

            # Prepend and append data for comparison
            full_data = self.prepend_data.encode('utf-8') + file_data + self.append_data.encode('utf-8')

            # Split the full data into chunks and compare each chunk's hash
            chunk_start = len(self.prepend_data)
            chunk_end = len(full_data) - len(self.append_data)

            for i in range(chunk_start, chunk_end, self.chunk_size):
                chunk = full_data[i:i + self.chunk_size]
                chunk_hash = hashlib.sha256(chunk).hexdigest()

                # If hash of this chunk doesn't match, further narrow down the modification position
                if chunk_hash != hashlib.sha256(file_data[i:i + self.chunk_size]).hexdigest():
                    # Now we compare each byte within the chunk for precise localization
                    for j in range(len(chunk)):
                        if chunk[j] != file_data[i + j]:
                            return f"Modification detected at byte {i + j}."
                
                    return f"Modification detected in chunk starting at byte {i}."

            return "Modification detected, but could not pinpoint exact location."

        except Exception as e:
            return f"Error processing file for insertion localization: {e}"