"""Класс тестирования для функции process_data."""
import json
import os
import unittest
from datetime import datetime

from hw2 import process_data

READING = 'r'
JSON_FILE = 'data_hw2.json'


class TestProcessData(unittest.TestCase):
    """Класс содержащий в себе функции тестирования."""

    def test_process_data_overwrite_output_file(self):
        """Тест на корректность изменений в файлах."""
        input_path = os.path.join('data_hw2.json')
        output_path = os.path.join('data_result.json')

        process_data(input_path, output_path)

        with open(output_path, READING) as output_file:
            stats1 = json.load(output_file)

        process_data(input_path, output_path)

        with open(output_path, READING) as output_file2:
            stats2 = json.load(output_file2)

        self.assertEqual(stats1, stats2)

    def test_process_data_create_output_file(self):
        """тест на проверку создания файла."""
        input_path = os.path.join('data_hw2.json')
        output_path = 'new_output_file.json'

        process_data(input_path, output_path)

        self.assertTrue(os.path.exists(output_path))

    def test_process_data_non_existent_input_file(self):
        """Тест на проверку возвращения пустого json."""
        input_path = 'nonexistent_file.json'
        output_path = 'data_result.json'

        with self.assertRaises(FileNotFoundError):
            process_data(input_path, output_path)

    def test_process_data_correctness(self):
        """Тест на возврат идеального варианта."""
        input_path = os.path.join(JSON_FILE)
        output_path = os.path.join('data_result.json')

        process_data(input_path, output_path)
        with open(output_path, READING) as output_file:
            stats = json.load(output_file)

        expected_output = {
            'region_distribution': {
                'Saint-Petersburg': 50,
                'Sochi': 50,
            },
            'registration_years_distribution': {
                '2012': 50,
                '2022': 50,
            },
        }

        self.assertEqual(stats, expected_output)

    def test_keys_exist_in_users(self):
        """Тест на проверку наличия необходимых переменных в этом файле."""
        input_path = os.path.join(JSON_FILE)

        with open(input_path, 'r') as input_file:
            json_data = json.load(input_file)

        for user in json_data.values():
            self.assertIn('region', user)
            self.assertIn('registered', user)

    def test_date_format(self):
        """Тест на проверку форму даты в файле."""
        input_path = os.path.join(JSON_FILE)

        with open(input_path, 'r') as input_file:
            json_data = json.load(input_file)

        for user in json_data.values():
            try:
                datetime.strptime(user['registered'], '%Y-%m-%d')
            except ValueError:
                self.fail(f'Date format incorrect for user {user}')


if __name__ == '__main__':
    unittest.main()
