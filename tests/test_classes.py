import pytest
from src.classes import Product, Category
from datetime import datetime


@pytest.fixture
def sample_products():
    return [
        Product("Samsung Galaxy S23", "256GB, Black", 80000, 5),
        Product("iPhone 15", "512GB, Blue", 90000, 3),
        Product("Xiaomi Redmi Note 12", "128GB, Gray", 30000, 10)
    ]


@pytest.fixture
def sample_category(sample_products):
    return Category("Смартфоны", "Мобильные устройства", sample_products)


def test_product_creation():
    """Тест создания продукта с корректными атрибутами"""
    product = Product("Test Product", "Description", 1000, 5)
    assert product.name == "Test Product"
    assert product.description == "Description"
    assert product.price == 1000
    assert product.quantity == 5


def test_category_creation(sample_products):
    """Тест создания категории с продуктами"""
    category = Category("Телевизоры", "Техника для дома", sample_products)
    assert category.name == "Телевизоры"
    assert category.description == "Техника для дома"
    assert len(category.products) == 3
    assert category.product_count == 3


def test_category_count(sample_category):
    """Тест подсчета количества категорий"""
    # Первая категория уже создана в фикстуре sample_category
    initial_count = Category.category_count

    # Создаем новую категорию
    tv_category = Category("Телевизоры", "4K TVs", [])
    assert Category.category_count == initial_count + 1

    # Создаем категорию с существующим именем (не должна увеличивать счетчик)
    duplicate_category = Category("Телевизоры", "Дубликат", [])
    assert Category.category_count == initial_count + 1


def test_product_count(sample_category, sample_products):
    """Тест подсчета продуктов в категории"""
    assert sample_category.product_count == len(sample_products)

    # Добавляем новый продукт
    new_product = Product("Nokia 3310", "Classic", 5000, 20)
    sample_category.products.append(new_product)
    assert sample_category.product_count == len(sample_products) + 1


def test_unique_products_count(sample_category):
    """Тест что продукты учитываются правильно"""
    assert sample_category.product_count == 3

    # Добавляем дубликат продукта
    duplicate_product = Product("Samsung Galaxy S23", "256GB, Black", 80000, 5)
    sample_category.products.append(duplicate_product)
    assert sample_category.product_count == 4  # Дубликаты считаются как отдельные продукты


def test_category_display(capsys, sample_category):
    """Тест отображения информации о категории"""
    print(sample_category.name)
    print(sample_category.description)
    print(sample_category.product_count)

    captured = capsys.readouterr()
    assert "Смартфоны" in captured.out
    assert "Мобильные устройства" in captured.out
    assert "3" in captured.out  # Количество продуктов


def test_product_display(capsys, sample_products):
    """Тест отображения информации о продукте"""
    product = sample_products[0]
    print(product.name)
    print(product.description)
    print(product.price)
    print(product.quantity)

    captured = capsys.readouterr()
    assert "Samsung Galaxy S23" in captured.out
    assert "256GB, Black" in captured.out
    assert "80000" in captured.out
    assert "5" in captured.out