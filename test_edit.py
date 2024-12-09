import random
import string
import time
from src.virus import Virus
from src.edit_localizer import EditLocalizer
from src.virus_verifier import VirusVerifier
from src.analyzer import Analyzer

def analyze_edit_detection(string_length=300, max_edit_start=250, max_edit_length=50):
    # Add timing start
    start_time = time.time()
    
    # Create a random string
    original_string = ''.join(random.choices(string.ascii_letters, k=string_length))

    # Create virus instance and make an edit
    virus = Virus(original_string)
    edit_start = random.randint(0, max_edit_start)
    edit_length = random.randint(1, max_edit_length)
    edit_result = virus.single_alter('edit', edit_length, edit_start)
    mutated_string = virus.string

    # Run edit verifier to detect edit
    localizer = EditLocalizer()
    verifier = VirusVerifier()
    edit_detected = verifier.identify_virus(original_string, mutated_string)

    if not edit_detected:
        return None, None

    # Run edit localizer to get start and end of edit
    localized_indices = localizer.localize_edit(original_string, mutated_string)
    detected_start, detected_end = localized_indices

    # Calculate metrics
    analyzer = Analyzer()
    correctness = analyzer.calculate_correctness_percentage(
        edit_start,
        edit_start + edit_length,
        detected_start,
        detected_end
    )
    precision = analyzer.calculate_precision(
        edit_start,
        edit_start + edit_length,
        detected_start,
        detected_end
    )
    deviation = analyzer.calculate_deviation(
        edit_start,
        edit_start + edit_length,
        detected_start,
        detected_end
    )

    # Add timing end before return
    execution_time = time.time() - start_time
    return correctness, precision, deviation, execution_time

def run_multiple_analyses(string_length=300, max_edit_start=250, max_edit_length=50, num_runs=300):
    total_correctness = 0
    total_precision = 0
    total_deviation = 0
    total_time = 0
    successful_runs = 0

    for _ in range(num_runs):
        correctness, precision, deviation, execution_time = analyze_edit_detection(500, 450, 50)
        
        # Only count successful detections
        if correctness is not None and precision is not None:
            total_correctness += correctness
            total_precision += precision
            total_deviation += deviation
            total_time += execution_time
            successful_runs += 1

    if successful_runs == 0:
        print("No successful edit detections")
        return 0, 0, 0, 0

    avg_correctness = total_correctness / successful_runs
    avg_precision = total_precision / successful_runs
    avg_time = total_time / successful_runs
    avg_deviation = total_deviation / successful_runs
    print(f"Results from {successful_runs} successful runs:")
    print(f"Average Correctness: {avg_correctness:.2f}%")
    print(f"Average Precision: {avg_precision:.2f}%")
    print(f"Average Time: {avg_time:.4f} seconds")
    print(f"Average Deviation: {avg_deviation:.2f}")
    return avg_correctness, avg_precision,avg_deviation, avg_time

def compare_string_lengths():
    string_lengths = [10,50,100,500,1000,5000,10000,50000,100000]
    results = []
    
    print("\nComparing performance across different string lengths:")
    print("=" * 80)
    print(f"{'String Length':<15} {'Success Rate':<15} {'Correctness':<15} {'Precision':<15} {'Deviation':<15} {'Avg Time':<15}")
    print("-" * 80)
    
    for length in string_lengths:
        max_edit_start = length - (length // 10)  # Ensure edit can start within string bounds
        max_edit_length = length // 10  # Edit length is 1/4 of string length
        
        total_correctness = 0
        total_precision = 0
        total_deviation = 0
        total_time = 0
        successful_runs = 0
        num_runs = 50  # Number of tests per string length
        
        for _ in range(num_runs):
            result = analyze_edit_detection(length, max_edit_start, max_edit_length)
            if result[0] is not None:
                total_correctness += result[0]
                total_precision += result[1]
                total_deviation += result[2]
                total_time += result[3]
                successful_runs += 1
        
        if successful_runs > 0:
            success_rate = (successful_runs / num_runs) * 100
            avg_correctness = total_correctness / successful_runs
            avg_precision = total_precision / successful_runs
            avg_time = total_time / successful_runs
            avg_deviation = total_deviation / successful_runs
            print(f"{length:<15} {success_rate:<15.2f} {avg_correctness:<15.2f} {avg_precision:<15.2f} {avg_deviation:<15.2f} {avg_time:<15.7f}")
            results.append({
                'length': length,
                'success_rate': success_rate,
                'correctness': avg_correctness,
                'precision': avg_precision,
                'time': avg_time,
                'deviation': avg_deviation
            })
    
    return results

if __name__ == "__main__":
    compare_string_lengths()


