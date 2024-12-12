from hashlib import sha256

class StringHasher:
    def __init__(self):
        return
    
    def compute_hash(self, input_string: str) -> str:
        """
        Compute the SHA-256 hash of the input string
        
        Args:
            input_string: The string to hash
            
        Returns:
            The SHA-256 hash value of the input string as a hexadecimal string
        """
        if not isinstance(input_string, str):
            raise TypeError("Input must be a string")
            
        computed_hash = sha256(input_string.encode()).hexdigest()
        return computed_hash
    
    def compare_hashes(self, hash1: str, hash2: str) -> bool:
        """
        Compare two hash values
        
        Args:
            hash1: First SHA-256 hash value
            hash2: Second SHA-256 hash value
            
        Returns:
            True if hashes are equal, False otherwise
        """
        return hash1 == hash2
    
    def compare_strings(self, str1: str, str2: str) -> bool:
        """
        Compare two strings by their hash values
        
        Args:
            str1: First string
            str2: Second string
            
        Returns:
            True if string hashes are equal, False otherwise
        """
        hash1 = self.compute_hash(str1)
        hash2 = self.compute_hash(str2)
        return self.compare_hashes(hash1, hash2)
