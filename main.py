import os
import random
import string
from src.virus import Virus
from src.cltag import CLTag
from src.clverify import CLVerify
from src.files import Files
from src.insert_localizer import InsertLocalizer  # Updated import

def generate_and_mutate_string():
    # Generate random string of length 500
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=500))
    
    # Define different mutation modes
    modes = ['insert', 'delete', 'edit', 'append', 'prepend']
    mutation_size = 30
    
    # Apply mutations for each mode
    mutated_strings = {}
    for mode in modes:
        if mode in ['edit', 'insert', 'delete']:
            mutated = virus_alter(random_string, mode, mutation_size, start=50)
        else:
            mutated = virus_alter(random_string, mode, mutation_size)
        mutated_strings[mode] = mutated
    
    return random_string, mutated_strings

def virus_alter(sequence, mode, size, start=None):
    virus = Virus(sequence)
    virus.single_alter(mode, size, start)
    return virus.string

# Example usage
if __name__ == "__main__":
    original, mutations = generate_and_mutate_string()
    print("\nOriginal string:")
    print(original[:50] + "..." + original[-50:])
    print("\nMutations:")

    # Save original and mutated strings as text files
    original_path = "tmp/original.txt"
    if not Files.create_txt_file(original_path, original):
        print("Error: Original file not created.")
        exit(1)

    print(f"Original file created at: {os.path.abspath(original_path)}")

    for mode, mutated in mutations.items():
        mutation_path = f"tmp/mutated_{mode}.txt"
        if not Files.create_txt_file(mutation_path, mutated):
            print(f"Error: Mutated file for {mode} not created.")
            exit(1)
    
    # Define the known data to prepend and append for localization
    prepend_data = "KNOWN_HEADER_DATA"
    append_data = "KNOWN_FOOTER_DATA"
    
    # Initialize CLTag and CLVerify for hash-based verification
    cl_tag = CLTag(original_path)
    cl_tag.compute_hashes()  # Compute and store hashes
    
    # Initialize InsertLocalizer
    insert_localizer = InsertLocalizer(prepend_data, append_data)  # New

    for mode in mutations:
        mutation_path = f"tmp/mutated_{mode}.txt"
        cl_verify = CLVerify(original_path, mutation_path)
        differences = cl_verify.verify_corruption()
        
        print(f"Verification result for {mode} mutation:")
        if differences:
            print("Hashes differ at the following positions:")
            for idx, original_hash, mutated_hash, mutated_content in differences:
                print(f"  Position {idx}:")
                print(f"    Original hash = {original_hash}")
                print(f"    Mutated hash = {mutated_hash}")
                print(f"    Mutated content snippet: {mutated_content[:50]}...{mutated_content[-50:]}")
        else:
            print("Mutation verified successfully, no differences detected.")
        
        # Localize insertion using InsertLocalizer
        print(f"Localizing insertions for the {mode} mutation:")
        result = insert_localizer.localize_insertion(mutation_path, cl_tag.original_hash)
        print(result)