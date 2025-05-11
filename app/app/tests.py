"""
Sample test suite for the app module.
"""
from django.test import SimpleTestCase

from app.calc import add, subtract


class CalcTests(SimpleTestCase):
    """
    Test the calc module.
    """
    def test_add_numbers(self):
        """Test adding two numbers together."""
        self.assertEqual(add(5, 6), 11)

    def test_subtract_numbers(self):
        """Test subtracting two numbers."""
        self.assertEqual(subtract(10, 15), 5)
