class Virus:
    def __init__(self, initial_string):
        self.string = initial_string

    def edit(self, start, end, new_substring):
        original = self.string
        self.string = self.string[:start] + new_substring + self.string[end:]
        return

    def append(self, substring):
        start = len(self.string)
        self.string += substring
        return

    def prepend(self, substring):
        self.string = substring + self.string
        return

    def insert(self, index, substring):
        self.string = self.string[:index] + substring + self.string[index:]
        return

    def delete(self, start, end):
        self.string = self.string[:start] + self.string[end:]
        return

    def _generate_substring(self, mode, length):
        """
        Helper method to generate substrings based on mode and length.
        """
        if mode == 'delete':
            return ''
            
        # Create a base pattern that's easily identifiable for each mode
        patterns = {
            'edit': 'EDIT',
            'append': 'APP',
            'prepend': 'PRE',
            'insert': 'INS'
        }
        
        base = patterns.get(mode, 'MOD')
        # Repeat the pattern to match desired length
        # Calculate how many times to repeat the base pattern
        repeats = length // len(base) + 1
        # Create pattern by repeating base and trim to exact length
        pattern = (base * repeats)[:length]
        return pattern

    def single_alter(self, mode, length, start=None):
        """
        Unified function to modify the string based on different modes.
        Automatically generates appropriate substring based on mode and length.
        
        Args:
            mode (str): Operation type ('edit', 'append', 'prepend', 'insert', 'delete')
            length (int): Length of modification
            start (int, optional): Starting index for operations that need it
            
        Returns:
            tuple: (mode, start_index, end_index, new_substring)
        """
        if length < 0:
            raise ValueError("Length must be non-negative")

        substring = self._generate_substring(mode, length)
        
        if mode == 'edit':
            if start is None:
                raise ValueError("Edit requires start position")
            end = start + length
            self.edit(start, end, substring)
            return (mode, start, start + len(substring), substring)
            
        elif mode == 'append':
            start_pos = len(self.string)
            self.append(substring)
            return (mode, start_pos, start_pos + length, substring)
            
        elif mode == 'prepend':
            self.prepend(substring)
            return (mode, 0, length, substring)
            
        elif mode == 'insert':
            if start is None:
                raise ValueError("Insert requires start position")
            self.insert(start, substring)
            return (mode, start, start + length, substring)
            
        elif mode == 'delete':
            if start is None:
                raise ValueError("Delete requires start position")
            end = start + length
            self.delete(start, end)
            return (mode, start, end, substring)
            
        else:
            raise ValueError(f"Unknown mode: {mode}")
    

