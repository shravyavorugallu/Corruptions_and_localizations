class Analyzer:
    def calculate_correctness_percentage(self, expected_start, expected_end, start, end):
        """
        Calculates the correctness percentage based on the overlap between expected and actual ranges.

        Parameters:
            expected_start (int): The expected start position.
            expected_end (int): The expected end position.
            start (int): The actual start position.
            end (int): The actual end position.

        Returns:
            float: The correctness percentage.
        """
        expected_length = expected_end - expected_start
        if expected_length <= 0:
            return 0.0

        intersection_start = max(expected_start, start)
        intersection_end = min(expected_end, end)
        intersection = intersection_end - intersection_start

        if intersection <= 0:
            return 0.0

        correctness = (intersection / expected_length) * 100
        return correctness

    def calculate_precision(self, expected_start, expected_end, start, end):
        """
        Calculates the precision percentage based on the overlap between actual and expected ranges.

        Precision is defined as the ratio of the correctly identified elements to the total elements identified.

        Parameters:
            expected_start (int): The expected start position.
            expected_end (int): The expected end position.
            start (int): The actual start position.
            end (int): The actual end position.

        Returns:
            float: The precision percentage.
        """
        actual_length = end - start
        if actual_length <= 0:
            return 0.0

        intersection_start = max(expected_start, start)
        intersection_end = min(expected_end, end)
        intersection = intersection_end - intersection_start

        if intersection <= 0:
            return 0.0

        precision = (intersection / actual_length) * 100
        return precision

    def calculate_deviation(self, expected_start, expected_end, start, end):
        """
        Calculates the absolute deviation (Manhattan distance) between expected and actual ranges.

        The deviation is the sum of the absolute differences between:
        1. Expected and actual start positions
        2. Expected and actual end positions

        Parameters:
            expected_start (int): The expected start position.
            expected_end (int): The expected end position.
            start (int): The actual start position.
            end (int): The actual end position.

        Returns:
            int: The total deviation (Manhattan distance) between the ranges.
        """
        start_deviation = abs(expected_start - start)
        end_deviation = abs(expected_end - end)
        return start_deviation + end_deviation
