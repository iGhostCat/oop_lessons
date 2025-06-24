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


# Тесты для магических методов класса Product
class TestProductMagicMethods:
    def test_product_str_representation(self, sample_product):
        """Тестирование строкового представления продукта"""
        result = str(sample_product)
        assert "Телевизор" in result
        assert "50000" in result
        assert "10" in result
        assert "руб." in result
        assert "Остаток" in result
        assert "шт." in result

    def test_product_addition(self, sample_products):
        """Тестирование сложения двух продуктов"""
        product1, product2 = sample_products
        total_value = product1 + product2
        expected = (50000.0 * 10) + (80000.0 * 5)
        assert total_value == expected

    def test_product_addition_with_non_product(self, sample_product):
        """Тестирование сложения продукта с не-продуктом"""
        with pytest.raises(TypeError) as excinfo:
            result = sample_product + 100
        assert "Можно складывать только объекты класса Product" in str(excinfo.value)

    def test_product_addition_same_product(self, sample_product):
        """Тестирование сложения продукта с самим собой"""
        total_value = sample_product + sample_product
        expected = (50000.0 * 10) * 2
        assert total_value == expected


# Тесты для магических методов класса Category
class TestCategoryMagicMethods:
    def test_category_str_representation(self, sample_products):
        """Тестирование строкового представления категории"""
        category = Category("Электроника", "Техника", sample_products)
        result = str(category)
        assert result == "Электроника, количество товаров: 15 шт."  # 10 + 5

    def test_category_str_with_empty_products(self):
        """Тестирование пустой категории"""
        category = Category("Пустая", "Категория без товаров", [])
        assert str(category) == "Пустая, количество товаров: 0 шт."

    def test_category_str_after_adding_product(self, sample_category):
        """Тестирование изменения после добавления товара"""
        initial_str = str(sample_category)
        assert "15" in initial_str  # Проверяем начальное количество (10 + 5)

        new_product = Product("Смартфон", "Android", 30000, 8)
        sample_category.add_cls_product(new_product)

        new_str = str(sample_category)
        assert new_str == "Электроника, количество товаров: 23 шт."  # 10 + 5 + 8

    def test_category_str_with_mixed_products(self):
        """Тестирование с разными типами товаров"""
        mixed_products = [
            Product("Телевизор", "4K", 50000, 3),
            "Некий товар",  # Строка вместо Product
            Product("Ноутбук", "Игровой", 80000, 2),
        ]
        category = Category("Смешанная", "Категория", mixed_products)
        assert str(category) == "Смешанная, количество товаров: 5 шт."  # 3 + 0 + 2


# Дополнительные тесты для проверки взаимодействия
class TestIntegrationMagicMethods:
    def test_product_str_in_category_products(self, sample_category):
        """Тестирование что строковое представление продукта используется в категории"""
        products_info = sample_category.products
        assert len(products_info) == 2
        assert "Телевизор" in products_info[0]
        assert "50000" in products_info[0]
        assert "10" in products_info[0]
        assert "Ноутбук" in products_info[1]
        assert "80000" in products_info[1]
        assert "5" in products_info[1]

    def test_add_products_from_different_categories(self, sample_category):
        """Тестирование сложения продуктов из разных категорий"""
        # Создаем вторую категорию с другими продуктами
        other_products = [
            Product("Наушники", "Беспроводные", 15000.0, 20),
            Product("Клавиатура", "Механическая", 8000.0, 15),
        ]
        other_category = Category("Аксессуары", "Периферия", other_products)

        # Складываем продукты из разных категорий
        product1 = sample_category._Category__products[0]  # Телевизор
        product2 = other_category._Category__products[1]  # Клавиатура

        total_value = product1 + product2
        expected = (50000.0 * 10) + (8000.0 * 15)
        assert total_value == expected


##############################################
# ТЕСТЫ ДЛЯ КЛАССОВ
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
