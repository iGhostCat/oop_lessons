import sys

import pytest

from src.classes import Category, Product


# Фикстуры для тестовых данных
@pytest.fixture
def sample_product():
    return Product("Телевизор", "4K UHD", 50000.0, 10)


@pytest.fixture
def sample_products():
    return [Product("Телевизор", "4K UHD", 50000.0, 10), Product("Ноутбук", "Игровой", 80000.0, 5)]


@pytest.fixture
def sample_category(sample_products):
    return Category("Электроника", "Техника", sample_products)


# Тесты для класса Product
class TestProduct:
    def test_price_property(self, sample_product):
        assert sample_product.price == 50000.0

    def test_price_setter_positive(self, sample_product):
        sample_product.price = 55000.0
        assert sample_product.price == 55000.0

    def test_price_setter_negative(self, sample_product, capsys):
        sample_product.price = -1000.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert sample_product.price == 50000.0

    def test_price_decrease_confirmation(self, sample_product, monkeypatch, capsys):
        # Мокаем input с явным аргументом
        monkeypatch.setattr("builtins.input", lambda prompt: "y")
        sample_product.price = 45000.0
        captured = capsys.readouterr()
        assert "Вы точно хотите снизить цену?" in captured.out
        assert sample_product.price == 45000.0

    def test_price_decrease_cancel(self, sample_product, monkeypatch, capsys):
        # Мокаем input с явным аргументом
        monkeypatch.setattr("builtins.input", lambda prompt: "n")
        sample_product.price = 45000.0
        captured = capsys.readouterr()
        assert "Снижение цены отменено" in captured.out
        assert sample_product.price == 50000.0

    def test_new_product_creation(self):
        product_data = {"name": "Смартфон", "description": "Android 13", "price": "35000.0", "quantity": "15"}
        product = Product.new_product(product_data)
        assert product.name == "Смартфон"
        assert product.price == 35000.0
        assert product.quantity == 15

    def test_new_product_with_duplicate(self, sample_products):
        duplicate_data = {"name": "Телевизор", "description": "4K OLED", "price": "55000.0", "quantity": "5"}
        updated_product = Product.new_product(duplicate_data, sample_products)
        assert updated_product.quantity == 15  # 10 + 5
        assert updated_product.price == 55000.0
        assert updated_product.description == "4K OLED"


# Тесты для класса Category
class TestCategory:
    def add_cls_product(self, product: Product):
        """Добавляет продукт и обновляет счетчик"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")
        self.__products.append(product)
        self.product_count = len(self.__products)  # Явное обновление счетчика

    def test_add_cls_product_method(self):
        # Создаем категорию с 2 начальными продуктами
        initial_products = [Product("Телевизор", "4K", 50000, 10), Product("Ноутбук", "Игровой", 80000, 5)]
        category = Category("Электроника", "Техника", initial_products)

        # Добавляем новый продукт
        new_product = Product("Смартфон", "Android", 30000, 15)
        category.add_cls_product(new_product)

        # Проверяем
        assert category.product_count == 3  # 2 начальных + 1 новый
        assert len(category._Category__products) == 3
        assert any(p.name == "Смартфон" for p in category._Category__products)

    def test_products_property_with_objects(self, sample_category):
        products_info = sample_category.products
        assert len(products_info) == 2
        assert "Телевизор" in products_info[0]
        assert "50000" in products_info[0]

    def test_products_property_with_strings(self):
        category = Category("Тест", "Категория", ["Товар 1", "Товар 2"])
        products_info = category.products
        assert len(products_info) == 2
        assert products_info[0] == "Товар 1"

    def test_mixed_products_in_category(self):
        mixed_products = ["Товар строковый", Product("Товар объект", "Описание", 1000.0, 5)]
        category = Category("Смешанная", "Категория", mixed_products)
        products_info = category.products
        assert len(products_info) == 2
        assert "Товар строковый" in products_info[0]
        assert "Товар объект" in products_info[1]
