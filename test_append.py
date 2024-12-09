import random
import string
from src.virus import Virus
from src.virus_verifier import VirusVerifier
from src.append_localizer import AppendLocalizer
from src.analyzer import Analyzer

def generate_random_string(length=1000):
    """Generate a random string of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_append_mutation():
    # Generate random test string
    original = generate_random_string()
    max_append_length = 200
    
    # Create mutated string
    # Create virus instance and make an edit
    virus = Virus(original)
    append_length = random.randint(1, max_append_length)
    append_result = virus.single_alter('append', append_length, 0)
    mutated_string = virus.string
    
    # Verify virus presence
    verifier = VirusVerifier()
    is_infected = verifier.verify_append(original, mutated_string)
    
    if not is_infected:
        return
    
    # Locate appended virus
    localizer = AppendLocalizer()
    virus_location = localizer.localize_append(original, mutated_string)
    
    # Analyze mutation
    analyzer = Analyzer()
    accuracy = analyzer.calculate_correctness_percentage(append_length, len(mutated_string), virus_location, len(mutated_string))
    precision = analyzer.calculate_precision(append_length, len(mutated_string), virus_location, len(mutated_string))
    deviation = analyzer.calculate_deviation(append_length, len(mutated_string), virus_location, len(mutated_string))
    print(f"Original: {original}")
    print(f"Mutated: {mutated_string}")
    print(f" Expected Length: {append_length}")
    print(f" Actual Length: {virus_location}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Precision: {precision:.2f}%")
    print(f"Deviation: {deviation:.2f}%")


if __name__ == '__main__':
    test_append_mutation()