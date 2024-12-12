from src.hashing import StringHasher
import math

class VirusVerifier:
    def __init__(self):
        self.hashing = StringHasher()

    def identify_virus(self, original_file, mutated_file):
        if self.verify_edit(original_file, mutated_file):
            return 'edit'
        elif self.verify_prepend(original_file, mutated_file):
            return 'prepend'
        elif self.verify_append(original_file, mutated_file):
            return 'append'
        elif self.verify_delete(original_file, mutated_file):
            return 'delete'
        elif self.verify_insert(original_file, mutated_file):
            return 'insert'
        else:
            return 'none'

    def verify_edit(self, original_file, mutated_file):
        check_length = len(original_file) == len(mutated_file)
        check_hash = self.hashing.compare_strings(original_file, mutated_file)
        return check_length and not check_hash
    
    def verify_prepend(self, original_file, mutated_file):
        check_length = len(original_file) < len(mutated_file)
        check_hash = original_file[0] == mutated_file[0]
        return check_length and not check_hash
    
    def verify_append(self, original_file, mutated_file):
        check_length = len(original_file) < len(mutated_file)
        check_hash = self.hashing.compare_strings(original_file[-1:], mutated_file[-1:])
        return check_length and not check_hash
    
    def verify_delete(self, original_file, mutated_file):
        check_length = len(original_file) > len(mutated_file)
        return check_length
    
    def verify_insert(self, original_file, mutated_file):
        check_length = len(original_file) < len(mutated_file)
        return check_length