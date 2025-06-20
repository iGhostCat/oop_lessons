import pytest
from src.classes import Product, Category


# Фикстуры для тестовых данных
@pytest.fixture
def sample_product():
    return Product("Телефон", "Смартфон", 50000, 10)


@pytest.fixture
def sample_products():
    return [Product("Телефон", "Смартфон", 50000, 10), Product("Ноутбук", "Игровой ноутбук", 100000, 5)]


@pytest.fixture
def sample_category(sample_products):
    return Category("Электроника", "Техника", sample_products)


# Тесты для класса Product
class TestProduct:
    def test_product_initialization(self, sample_product):
        assert sample_product.name == "Телефон"
        assert sample_product.description == "Смартфон"
        assert sample_product.price == 50000
        assert sample_product.quantity == 10

    def test_product_attributes_types(self, sample_product):
        assert isinstance(sample_product.name, str)
        assert isinstance(sample_product.description, str)
        assert isinstance(sample_product.price, int)
        assert isinstance(sample_product.quantity, int)


# Тесты для класса Category
class TestCategory:
    def test_category_initialization(self, sample_category):
        assert sample_category.name == "Электроника"
        assert sample_category.description == "Техника"
        assert len(sample_category.products) == 2

    def test_category_count(self, sample_products):
        # Сбросим счетчик перед тестом
        Category._total_categories = 0
        Category._unique_names = set()

        cat1 = Category("Электроника", "Техника", sample_products)
        assert Category.category_count == 1

        cat2 = Category("Одежда", "Модная одежда", [])
        assert Category.category_count == 2

        # Попытка создать категорию с уже существующим именем
        cat3 = Category("Электроника", "Другая электроника", [])
        assert Category.category_count == 2  # Не должно увеличиться

    def test_product_count(self, sample_category, sample_products):
        assert sample_category.product_count == 2  # Атрибут экземпляра
        assert Category.product_count == 0  # Атрибут класса не изменяется

    def test_products_attribute(self, sample_category):
        products = sample_category.products
        assert len(products) == 2
        assert isinstance(products[0], Product)
        assert products[0].name == "Телефон"
        assert products[1].name == "Ноутбук"


# Тесты взаимодействия классов
class TestProductCategoryInteraction:
    def test_add_product_to_category(self, sample_category):
        new_product = Product("Планшет", "Графический планшет", 30000, 8)
        sample_category.products.append(new_product)
        assert len(sample_category.products) == 3
        assert sample_category.product_count == 2  # Не изменяется автоматически
        sample_category.product_count = len(sample_category.products)
        assert sample_category.product_count == 3

    def test_category_with_empty_products(self):
        category = Category("Книги", "Литература", [])
        assert category.product_count == 0
        assert len(category.products) == 0
