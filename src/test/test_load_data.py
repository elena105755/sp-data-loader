import unittest

import pytest

from src.main.load_data import validate_row, validate_data_for_date


class TestValidateRow(unittest.TestCase):

    def test_validate_row_success(self):
        row = ['2023-03-29', '/product/product-id-123-456-789', 'cat123', '10']
        error_log = validate_row(row)
        self.assertEqual(error_log, '')

    def test_validate_date_field(self):
        row = ['2023/03/29', '/product/product-id-123-456-789', 'cat123', '10']
        error_log = validate_row(row)
        self.assertIn('date_format', error_log)

    def test_validate_path_prefix(self):
        row = ['2023-03-29', '/product/123-456-789', 'cat123', '10']
        error_log = validate_row(row)
        self.assertIn('path_prefix', error_log)

    def test_validate_path_seq(self):
        row = ['2023-03-29', '/product/product-id-NaN', 'cat123', '10']
        error_log = validate_row(row)
        self.assertIn('path_seq', error_log)

    def test_validate_category_digit(self):
        row = ['2023-03-29', '/product/product-id-123-456-789', 'catabc', '10']
        error_log = validate_row(row)
        self.assertIn('category_digit', error_log)

    def test_validate_category_prefix(self):
        row = ['2023-03-29', '/product/product-id-123-456-789', '123cat', '10']
        error_log = validate_row(row)
        self.assertIn('category_digit', error_log)

    def test_validate_negative_sessions(self):
        row = ['2023-03-29', '/product/product-id-123-456-789', 'cat123', '-10']
        error_log = validate_row(row)
        self.assertIn('sessions_negative', error_log)

    def test_validate_NaN_sessions(self):
        row = ['2023-03-29', '/product/product-id-123-456-789', 'cat123', 'abc']
        error_log = validate_row(row)
        self.assertIn('sessions_NaN', error_log)

    def test_validate_null_date(self):
        row = ['', '/product/product-id-123-456-789', 'cat123', '10']
        error_log = validate_row(row)
        self.assertIn('date_null', error_log)

    def test_validate_null_path(self):
        row = ['2023-03-29', '', 'cat123', '10']
        error_log = validate_row(row)
        self.assertIn('path_null', error_log)

    def test_validate_null_category(self):
        row = ['2023-03-29', '/product/product-id-123-456-789', '', '10']
        error_log = validate_row(row)
        self.assertIn('category_null', error_log)

    def test_validate_null_sessions(self):
        row = ['2023-03-29', '/product/product-id-123-456-789', 'cat123', '']
        error_log = validate_row(row)
        self.assertIn('sessions_null', error_log)


@pytest.mark.parametrize("target_date, expected_result", [
    ("2022-03-28.csv", True),  # valid data file
    ("2022-03-29.csv", False),  # invalid data file
    ("2022-03-30.csv", True),  # valid data file
])
def test_validate_data_for_date(target_date, expected_result):
    assert validate_data_for_date(target_date) == expected_result


@pytest.mark.parametrize("row, expected_result", [
    (['2023-03-29', '/product/product-id-123-456-789', 'cat123', '10'], ""),
    (['2023/03/29', '/product/product-id-123-456-789', 'cat123', '10'], "date_format"),
    (['2023-03-29', '/product/123-456-789', 'cat123', '10'], "path_prefix")
])
def test_validate_data_correctness(row, expected_result):
    error_log = validate_row(row)
    assert expected_result in error_log
