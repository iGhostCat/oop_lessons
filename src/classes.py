class Product:
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
        return f"{self.name}, количество продуктов: {len(self.__products)} шт."

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
        self.__products.append(product)
        self.product_count = len(self.__products)

    def add_cls_product(self, product: Product):
        """Добавляет продукт и обновляет счетчик количества продуктов"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")
        self.__products.append(product)
        self.product_count = len(self.__products)


"""
products_data = [
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
print()"""
