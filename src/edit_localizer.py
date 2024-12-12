from src.hashing import StringHasher
import math

class EditLocalizer:
    def __init__(self):
        self.hashing = StringHasher()
    
    def localize_edit(self, original_file, mutated_file):
        """Comprehensive virus localization algorithm with multi-step refinement"""
        n = len(original_file)
        self.max_iterations = int(math.log2(n)) - 1
        
        initial_bounds = self._localize_step_two(original_file, mutated_file)
        return self._refine_bounds(original_file, mutated_file, initial_bounds)
    
    def _refine_bounds(self, original_file, mutated_file, initial_bounds):
        """Helper method to handle iterative refinement"""
        current_bounds = initial_bounds
        for j in range(3, self.max_iterations + 1):
            current_bounds = self._localize_step_j(
                original_file, mutated_file, current_bounds, j
            )
        return current_bounds

    def _get_segment_content(self, file, start, end, n):
        """Helper method to handle wraparound segments"""
        if end > n:
            return file[start:] + file[:end % n]
        return file[start:end]

    def _compute_segment_hashes(self, segments, original_file, mutated_file, bounds=None):
        """Helper method to compute hashes for segments"""
        n = len(original_file)
        mutated_hashes = {}
        original_hashes = {}
        
        for name, (start, end) in segments.items():
            if bounds and (start < bounds[0] or end > bounds[1]):
                continue
                
            segment = lambda f: self._get_segment_content(f, start, end, n)
            mutated_hashes[name] = self.hashing.compute_hash(segment(mutated_file))
            original_hashes[name] = self.hashing.compute_hash(segment(original_file))
            
        return original_hashes, mutated_hashes

    def _localize_step_j(self, original_file, mutated_file, previous_bounds, j):
        """Perform localization for a specific iteration step j"""
        n = len(original_file)
        lower_bound, upper_bound = previous_bounds
        segment_length = n // (2 ** j)
        
        # Create segments
        segments = self._create_segments(n, j, segment_length)
        
        # Compute hashes
        original_hashes, mutated_hashes = self._compute_segment_hashes(
            segments, original_file, mutated_file, previous_bounds
        )
        
        # Find different segments
        different_segments = [
            (start, end) for name, (start, end) in segments.items()
            if name in original_hashes and original_hashes[name] != mutated_hashes[name]
        ]
        
        return self._refine_bounds_from_segments(
            different_segments, original_file, mutated_file, 
            lower_bound, upper_bound, n
        )

    def _create_segments(self, n, j, segment_length):
        """Helper method to create segments for step j"""
        segments = {}
        for i in range(1, 2**j + 1):
            # Regular segments
            start_regular = (i - 1) * segment_length
            segments[f'S{j},{i}'] = (start_regular, start_regular + segment_length)
            
            # Shifted segments
            start_shifted = ((i - 1) * segment_length + n // (2 ** (j + 1))) % n
            segments[f'S{j},{i+2**j}'] = (
                start_shifted, 
                (start_shifted + segment_length) % n
            )
        return segments

    def _refine_bounds_from_segments(self, different_segments, original_file, 
                                   mutated_file, lower_bound, upper_bound, n):
        """Helper method to refine bounds based on different segments"""
        if not different_segments:
            return [lower_bound, upper_bound]
            
        new_lower = lower_bound
        new_upper = upper_bound
        
        # Find tightest bounds
        for potential_lower in sorted(start for start, _ in different_segments):
            if self._verify_segment_difference(
                original_file, mutated_file, 
                potential_lower, new_upper
            ):
                new_lower = potential_lower
                break
        
        for potential_upper in sorted((end for _, end in different_segments), reverse=True):
            if self._verify_segment_difference(
                original_file, mutated_file,
                new_lower, potential_upper
            ):
                new_upper = potential_upper
                break
        
        # Constrain bounds
        new_lower = max(0, new_lower)
        new_upper = min(n, new_upper)
        
        if new_lower >= new_upper:
            new_upper = min(new_lower + 1, n)
            
        return [new_lower, new_upper]

    def _verify_segment_difference(self, original_file, mutated_file, start, end):
        """Helper method to verify if a segment contains differences"""
        orig_segment = original_file[start:end]
        test_segment = mutated_file[start:end]
        return self.hashing.compute_hash(test_segment) != self.hashing.compute_hash(orig_segment)

    def _localize_step_two(self, original_file, mutated_file):
        n = len(original_file)
        
        # Create segments for iteration 2
        segment_length = n // 4
        segments = {
            # Regular segments
            'S2,1': (0, segment_length),
            'S2,2': (segment_length, 2*segment_length),
            'S2,3': (2*segment_length, 3*segment_length),
            'S2,4': (3*segment_length, n),
            
            # Shifted segments (shifted by n/8)
            'S2,5': (n//8, n//8 + segment_length),
            'S2,6': (n//8 + segment_length, n//8 + 2*segment_length),
            'S2,7': (n//8 + 2*segment_length, n//8 + 3*segment_length),
            'S2,8': (n//8 + 3*segment_length, (n//8 + 4*segment_length) % n),
        }
        
        # Calculate hashes for each segment
        mutated_hashes = {}
        original_hashes = {}
        
        # Compute individual segment hashes
        for name, (start, end) in segments.items():
            # Handle wraparound for shifted segments
            if end > n:
                segment = lambda f: f[start:] + f[:end % n]
            else:
                segment = lambda f: f[start:end]
            
            mutated_hashes[name] = self.hashing.compute_hash(segment(mutated_file))
            original_hashes[name] = self.hashing.compute_hash(segment(original_file))
        
        # Initialize closest found indices
        closest_lower = float('inf')
        closest_upper = -1
        
        # First pass: find rough bounds using all segments
        for i in range(1, 9):
            segment_name = f'S2,{i}'
            if original_hashes[segment_name] != mutated_hashes[segment_name]:
                start, end = segments[segment_name]
                if i <= 4:  # Regular segments
                    closest_lower = min(closest_lower, start)
                    closest_upper = max(closest_upper, end)
                else:  # Shifted segments
                    closest_lower = min(closest_lower, start)
                    closest_upper = max(closest_upper, end)

        # Set initial bounds based on closest found indices
        lower_bound = 0 if closest_lower == float('inf') else closest_lower
        upper_bound = n if closest_upper == -1 else closest_upper

        # Create smaller segments around the identified bounds
        small_segment_length = segment_length // 4
        refined_segments = {}
        
        # Add segments around lower bound
        for i in range(4):
            start = max(0, lower_bound - small_segment_length + (i * small_segment_length//2))
            end = start + small_segment_length
            refined_segments[f'R1,{i}'] = (start, min(end, n))
        
        # Add segments around upper bound
        for i in range(4):
            end = min(n, upper_bound + small_segment_length - (i * small_segment_length//2))
            start = max(0, end - small_segment_length)
            refined_segments[f'R2,{i}'] = (start, end)
        
        # Compute hashes for refined segments
        for name, (start, end) in refined_segments.items():
            segment = lambda f: f[start:end]
            mutated_hashes[name] = self.hashing.compute_hash(segment(mutated_file))
            original_hashes[name] = self.hashing.compute_hash(segment(original_file))
        
        # Reset closest indices for refinement
        closest_lower = float('inf')
        closest_upper = -1

        # Refine bounds using smaller segments
        for name, (start, end) in refined_segments.items():
            if original_hashes[name] != mutated_hashes[name]:
                if name.startswith('R1'):  # Lower bound refinement
                    closest_lower = min(closest_lower, start)
                else:  # Upper bound refinement
                    closest_upper = max(closest_upper, end)

        # Final bounds adjustment
        if closest_lower != float('inf'):
            lower_bound = closest_lower
        if closest_upper != -1:
            upper_bound = closest_upper

        # Ensure end > start
        if upper_bound <= lower_bound:
            upper_bound = min(lower_bound + 1, n)
        
        return [lower_bound, upper_bound]
