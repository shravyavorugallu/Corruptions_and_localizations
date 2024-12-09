import random
import string
from src.virus import Virus
from src.virus_verifier import VirusVerifier
from src.prepend_localizer import PrependLocalizer
from src.analyzer import Analyzer

def generate_random_string(length=1000):
    """Generate a random string of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_prepend_mutation():
    # Generate random test string
    original = generate_random_string()
    max_prepend_length = 200
    
    # Create mutated string
    # Create virus instance and make an edit
    virus = Virus(original)
    prepend_length = random.randint(1, max_prepend_length)
    prepend_result = virus.single_alter('prepend', prepend_length, 0)
    mutated_string = virus.string
    
    # Verify virus presence
    verifier = VirusVerifier()
    is_infected = verifier.verify_prepend(original, mutated_string)
    
    if not is_infected:
        return
    
    # Locate prepended virus
    localizer = PrependLocalizer()
    virus_location = localizer.localize_prepend(original, mutated_string)
    
    # Analyze mutation
    analyzer = Analyzer()
    accuracy = analyzer.calculate_correctness_percentage(0, prepend_length, 0, virus_location)
    precision = analyzer.calculate_precision(0, prepend_length, 0, virus_location)
    deviation = analyzer.calculate_deviation(0, prepend_length, 0, virus_location)
    print(f"Original: {original}")
    print(f"Mutated: {mutated_string}")
    print(f" Expected Length: {prepend_length}")
    print(f" Actual Length: {virus_location}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Precision: {precision:.2f}%")
    print(f"Deviation: {deviation:.2f}%")


if __name__ == '__main__':
    test_prepend_mutation()
