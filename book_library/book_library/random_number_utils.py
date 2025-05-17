import random
import string

class RandomUtils:
    """
    Class for generation of random IDs
    """
    @staticmethod 
    def generate_random_id() -> str:
        """
        Generate a random ID string of length 6 with uppercase letters
        """
        return "".join(random.choices(string.ascii_uppercase, k=6))

