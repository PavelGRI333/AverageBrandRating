import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from main import open_csv_file, main

def test_csv_with_only_file():
    """Тест только с одим csv"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('name,brand,price,rating\n')
        f.write('iphone 15 pro,apple,999,4.9\n')
        f.write('galaxy s23,samsung,899,4.8\n')
        temp_file = f.name

    try:
        data = open_csv_file([temp_file])

        assert len(data) == 2
        assert data[0]['name'] == 'iphone 15 pro'
        assert data[0]['brand'] == 'apple'
        assert data[0]['rating'] == '4.9'
        assert data[1]['name'] == 'galaxy s23'
        assert data[1]['brand'] == 'samsung'
        assert data[1]['rating'] == '4.8'
    finally:
        os.unlink(temp_file)

def test_csv_with_multiple_files():
    """Тест с нексолькими csv"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f1:
        f1.write('name,brand,price,rating\n')
        f1.write('iphone 15 pro,apple,999,4.9\n')
        temp_file1 = f1.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f2:
        f2.write('name,brand,price,rating\n')
        f2.write('galaxy s23,samsung,899,4.8\n')
        temp_file2 = f2.name

    try:
        data = open_csv_file([temp_file1,
                              temp_file2
                              ]
                             )

        assert len(data) == 2
        brands = [elem['brand'] for elem in data]
        assert 'apple' in brands
        assert 'samsung' in brands
    finally:
        os.unlink(temp_file1)
        os.unlink(temp_file2)

def test_empty_file():
    """Тест с пустым csv файлом"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('name,brand,price,rating')
        temp_file = f.name

    try:
        data = open_csv_file([temp_file])
        assert len(data) == 0
    finally:
        os.unlink(temp_file)

def test_csv_file_notfound():
    """Тест csv с неправильным именем"""
    with pytest.raises(FileNotFoundError):
        open_csv_file(['fakefile.csv'])

def test_csv_with_empty_list():
    """Тест с чистым csv"""
    data = open_csv_file([])
    assert data == []


@patch('main.AverageRatingReport')
@patch('main.open_csv_file')
def test_main_success(mock_read_files_func, mock_report_class):
    """Тест успешного выполнения main"""
    mock_data = [
        {'name': 'iphone', 'brand': 'apple', 'rating': '4.9'},
        {'name': 'galaxy', 'brand': 'samsung', 'rating': '4.8'},
    ]
    mock_read_files_func.return_value = mock_data

    mock_report_instance = MagicMock()
    mock_report_instance.generate.return_value = [('apple', 4.9), ('samsung', 4.8)]
    mock_report_class.return_value = mock_report_instance

    test_args = [
        'main.py',
        '--files', 'file1.csv', 'file2.csv',
        '--report', 'average-rating'
    ]

    with patch('sys.argv', test_args):
        with patch('sys.exit') as mock_exit:
            main()

            mock_read_files_func.assert_called_once_with(['file1.csv', 'file2.csv'])
            mock_report_instance.generate.assert_called_once_with(mock_data)
            mock_exit.assert_called_once_with(0)

def test_main_integration_with_real_files():
    """Интеграционный тест с реальными файлами"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f1:
        f1.write('name,brand,price,rating\n')
        f1.write('iphone 15,apple,999,4.9\n')
        f1.write('galaxy s23,samsung,899,4.8\n')
        temp_file1 = f1.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f2:
        f2.write('name,brand,price,rating\n')
        f2.write('redmi note,xiaomi,199,4.6\n')
        temp_file2 = f2.name

    try:
        test_args = [
            'main.py',
            '--files', temp_file1, temp_file2,
            '--report', 'average-rating'
        ]

        with patch('sys.argv', test_args):
            with patch('sys.exit') as mock_exit:
                main()
                mock_exit.assert_called_once_with(0)
    finally:
        os.unlink(temp_file1)
        os.unlink(temp_file2)