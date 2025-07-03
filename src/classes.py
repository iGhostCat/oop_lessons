from abc import ABC, abstractmethod
from typing import Dict, Optional, List


class BaseProduct(ABC):

    class BaseProduct(ABC):
        @property
        @abstractmethod
        def price(self) -> float:
            pass

        @price.setter
        @abstractmethod
        def price(self, value: float) -> None:
            pass

        @abstractmethod
        def __str__(self) -> str:
            pass

        @classmethod
        @abstractmethod
        def new_product(cls, product_data: Dict, products_list: Optional[List['BaseProduct']] = None) -> 'BaseProduct':
            pass


class MixinLog:
    ID = 1

    def __init__(self):
        self.id = self.ID
        MixinLog.ID += 1
    @classmethod
    def order_log(cls):
        print('Продукт1', 'Описание продукта', 1200, 10)


class Product(BaseProduct):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт. "

    @property
    def price(self):
        return self.__price

    def __add__(self, other):
        """Сложение продуктов с проверкой типа"""
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")
        return (self.price * self.quantity) + (other.price * other.quantity)

    @price.setter
    def price(self, new_price):
        """Сеттер для установки новой цены"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif self.__price > new_price:
            print("Вы точно хотите снизить цену? y/n")
            down_allowing = input("> ").strip().lower()  # Явный prompt для input
            if down_allowing in ("y", "yes", "да"):
                self.__price = new_price
            else:
                print("Снижение цены отменено")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict, products_list: list = None):
        """Принимает данные нового продукта в словаре"""
        # Проверяем обязательные поля
        required_fields = ["name", "description", "price", "quantity"]
        for field in required_fields:
            if field not in product_data:
                raise ValueError(f"Отсутствует обязательное поле: {field}")

        name = product_data["name"]
        description = product_data["description"]
        price = float(product_data["price"])
        quantity = int(product_data["quantity"])

        # Если передан список товаров для проверки дубликатов
        if products_list is not None:
            for existing_product in products_list:
                if existing_product.name.lower() == name.lower():
                    # Нашли дубликат - обновляем существующий товар
                    existing_product.quantity += quantity
                    existing_product.price = max(existing_product.price, price)
                    if "description" in product_data and product_data["description"]:
                        existing_product.description = product_data["description"]
                    return existing_product

        # Если дубликатов нет или список не передан - создаем новый товар
        return cls(name, description, price, quantity)

    def get_product(self):
        return f"Product({self.name}, {self.price}, {self.quantity})"


class Category:
    _total_categories = 0
    _unique_names = set()
    category_count = 0  # Атрибут уровня класса
    product_count = 0  # Атрибут уровня класса

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products.copy()

        if name not in self._unique_names:
            self._unique_names.add(name)
            Category._total_categories += 1
            Category.category_count = Category._total_categories

        self.product_count = len(products)  # Атрибут экземпляра

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products if isinstance(product, Product))
        return f"{self.name}, количество товаров: {total_quantity} шт."

    @property
    def products(self):
        """Геттер для получения форматированного списка товаров"""
        products_list = []
        for product in self.__products:
            if isinstance(product, Product):
                products_list.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.")
            else:
                # Для обратной совместимости со строками
                products_list.append(str(product))
        return products_list

    def add_product(self, product):
        """Метод для добавления одного продукта"""
        if not isinstance(product, Product):
            raise TypeError
        else:
            self.__products.append(product)
            self.product_count = len(self.__products)

    def add_cls_product(self, product: Product):
        """Добавляет продукт и обновляет счетчик количества продуктов"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")
        self.__products.append(product)
        self.product_count = len(self.__products)


class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other):
        """Сложение с проверкой ТОЧНОГО совпадения классов"""
        if type(self) != type(other):
            raise TypeError
        else:
            return (self.price * self.quantity) + (other.price * other.quantity)


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __add__(self, other):
        """Сложение с проверкой ТОЧНОГО совпадения классов"""
        if type(self) != type(other):
            raise TypeError
        else:
            return (self.price * self.quantity) + (other.price * other.quantity)


"""products_data = [
    {"name": "Samsung Galaxy S23", "description": "Флагманский смартфон Samsung", "price": 79999.0, "quantity": 15},
    {"name": "iPhone 15", "description": "Флагманский смартфон Apple", "price": 89999.0, "quantity": 10},
]

prod_1 = Product.new_product(products_data[0])
print(prod_1.get_product())
prod_2 = Product.new_product(products_data[1])
print(prod_2.get_product())

print(prod_1+prod_2)

cat_1 = Category('Смартфоны', 'Смартфоны до 100 тыс', ['Huawei One Note', 'Xiaomi Redmi 10'])
print(cat_1.products)
cat_1.add_cls_product(Product.new_product(products_data[1]))
print(cat_1.products)
cat_1.add_cls_product(prod_1)
print(cat_1.products)
print(prod_1)

print(cat_1)
"""
