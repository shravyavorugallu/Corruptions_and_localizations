from src.hashing import StringHasher
from src.prepend_localizer import PrependLocalizer

class AppendLocalizer:
    def __init__(self):
        self.hashing = StringHasher()
    
    def localize_append(self, original, mutated):
        original_reversed = original[::-1]
        mutated_reversed = mutated[::-1]

        localizer = PrependLocalizer()
        return localizer.localize_prepend(original_reversed, mutated_reversed)