import hashlib

class CLVerify:
    def __init__(self, original_file_path, mutated_file_path):
        self.original_file_path = original_file_path
        self.mutated_file_path = mutated_file_path

    def compute_hash(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            return [hashlib.sha256(content[i:i+100].encode()).hexdigest() for i in range(0, len(content), 100)]

    def verify_corruption(self):
        original_hashes = self.compute_hash(self.original_file_path)
        mutated_hashes = self.compute_hash(self.mutated_file_path)
        
        # # Compare the hashes
        # corruption_info = []
        # for i, (orig, new) in enumerate(zip(original_hashes, new_hashes)):
        #     if orig != new:
        #         corruption_info.append((i * 100, orig, new))
        
        # return corruption_info if corruption_info else "No corruption detected"
        
        differences = []
        for idx, (original, mutated) in enumerate(zip(original_hashes, mutated_hashes)):
            if original != mutated:
                # Get the content of the mutated file at the position where the hash differs
                mutated_content = self._get_mutated_content(idx)
                differences.append((idx, original, mutated, mutated_content))
        
        return differences
    
    def _get_mutated_content(self, position):
        # Logic to retrieve the content of the mutated file at the specific position
        with open(self.mutated_file_path, 'r') as file:
            content = file.read()
            # Optionally, slice or process the content as needed to display the specific change
            return content