import pytest
from reports.average_rating import AverageRatingReport


def test_generate_with_valid_data():
    """Тест генерации отчета с валидными данными"""
    report = AverageRatingReport()
    data = [
        {'name': 'iphone 15 pro', 'brand': 'apple', 'price': '999', 'rating': '4.9'},
        {'name': 'iphone 14', 'brand': 'apple', 'price': '799', 'rating': '4.7'},
        {'name': 'galaxy s23', 'brand': 'samsung', 'price': '899', 'rating': '4.8'},
    ]

    result = report.generate(data)

    assert len(result) == 2
    apple_rating = next(r[1] for r in result if r[0] == 'apple')
    assert apple_rating == pytest.approx(4.8)

    samsung_rating = next(r[1] for r in result if r[0] == 'samsung')
    assert samsung_rating == pytest.approx(4.8)


def test_generate_sorting_order():
    """Тест правильности сортировки по убыванию рейтинга"""
    report = AverageRatingReport()
    data = [
        {'name': 'product1', 'brand': 'brand_low', 'price': '100', 'rating': '3.0'},
        {'name': 'product2', 'brand': 'brand_low', 'price': '100', 'rating': '3.0'},
        {'name': 'product3', 'brand': 'brand_high', 'price': '200', 'rating': '5.0'},
        {'name': 'product4', 'brand': 'brand_mid', 'price': '150', 'rating': '4.0'},
    ]

    result = report.generate(data)

    assert result[0][0] == 'brand_high'
    assert result[0][1] == pytest.approx(5.0)
    assert result[1][0] == 'brand_mid'
    assert result[1][1] == pytest.approx(4.0)
    assert result[2][0] == 'brand_low'
    assert result[2][1] == pytest.approx(3.0)


def test_generate_with_invalid_ratings():
    """Тест обработки некорректных рейтингов"""
    report = AverageRatingReport()
    data = [
        {'name': 'valid1', 'brand': 'apple', 'price': '999', 'rating': '4.9'},
        {'name': 'invalid_rating', 'brand': 'apple', 'price': '999', 'rating': 'invalid'},
        {'name': 'missing_rating', 'brand': 'samsung', 'price': '899'},
    ]

    result = report.generate(data)
    assert len(result) == 1
    brands = [r[0] for r in result]
    assert 'apple' in brands
    assert result[0][0] == 'apple'
    assert result[0][1] == 4.9


def test_generate_empty_data():
    """Тест с пустыми данными"""
    report = AverageRatingReport()
    result = report.generate([])
    assert result == []


def test_generate_all_invalid_data():
    """Тест когда все данные некорректны"""
    report = AverageRatingReport()
    data = [
        {'name': 'product1', 'brand': 'brand1', 'price': '100'},
        {'name': 'product2', 'brand': 'brand2', 'price': '200', 'rating': 'invalid'},
    ]

    result = report.generate(data)
    assert result == []


def test_single_product():
    """Тест с одним товаром"""
    report = AverageRatingReport()
    data = [
        {'name': 'single_product', 'brand': 'lonely_brand', 'price': '100', 'rating': '4.5'},
    ]

    result = report.generate(data)

    assert len(result) == 1
    assert result[0] == ('lonely_brand', 4.5)


def test_implements_abstract_method():
    """Тест что класс реализует абстрактный метод"""
    report = AverageRatingReport()
    assert hasattr(report, 'generate')
    assert callable(report.generate)