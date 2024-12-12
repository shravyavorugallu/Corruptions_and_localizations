from src.hashing import StringHasher
import math

class PrependLocalizer:
    def __init__(self):
        self.hashing = StringHasher()
    
    def localize_prepend(self, original, mutated):
        # If lengths are equal, no prepend occurred
        if len(original) == len(mutated):
            return 0, len(original)
        
        # Get all segment hashes for both strings
        orig_hashes = self._compute_segment_hashes(original)
        mut_hashes = self._compute_segment_hashes(mutated)
        
        # Find the first matching hash pair to identify where original content starts
        for j in range(len(mut_hashes)):
            if mut_hashes[j][0] in orig_hashes[0] or mut_hashes[j][1] in orig_hashes[0]:
                # Found matching segment - prepended content ends here
                start_pos = min(2 ** (j + 1), len(mutated))
                return start_pos
                
        return len(mutated) - len(original)

    def _compute_segment_hashes(self, text):
        """Compute hashes of segments according to the algorithm."""
        length = len(text)
        if length <= 1:
            return []
        
        results = []
        pos = 0
        
        while pos < length - 1:
            # Compute k where 2^k ≤ length/2
            k = int(math.log2(length/2))
            seg_size = 2 ** k
            
            # Get the two segments
            seg1 = text[pos:pos + seg_size]
            seg2 = text[pos + seg_size:pos + 2*seg_size]
            
            # Compute hashes
            hash1 = self.hashing.compute_hash(seg1)
            hash2 = self.hashing.compute_hash(seg2)
            
            results.append((hash1, hash2))
            
            # Move position for next iteration
            pos += 2 * seg_size
            
        return results
