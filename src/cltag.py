import hashlib
import os

class CLTag:
    def __init__(self, file_path):
        self.file_path = file_path
        self.hashes = {}

    def compute_hashes(self):
        original_path = os.path.abspath("original.txt")
        with open(self.file_path, 'r') as file:
            content = file.read()
            for i in range(0, len(content), 100):
                chunk = content[i:i+100]
                hash_value = hashlib.sha256(chunk.encode()).hexdigest()
                self.hashes[i] = hash_value
        # Save hashes to a file
        with open('hashes.txt', 'w') as f:
            for key, value in self.hashes.items():
                f.write(f"{key}:{value}\n")

    def load_hashes(self, file_path='hashes.txt'):
        self.hashes = {}
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    key, value = line.strip().split(':')
                    self.hashes[int(key)] = value
        except FileNotFoundError:
            print("Hash file not found.")
