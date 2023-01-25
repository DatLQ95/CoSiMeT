"""
Unit tests for the calculator library
"""

from src.DatabaseAgent import DatabaseAgent


db = DatabaseAgent()

# class DatabaseTest:

def test_connection():
    assert True == db.check_connection("dat-mysql", "12345678")

    # def test_subtraction(self):
    #     assert 2 == calculator.subtract(4, 2)