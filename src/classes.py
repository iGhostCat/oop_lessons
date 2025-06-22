class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, prod_dict):
        '''Принимает данные нового продукта в словаре'''
        return cls(str(prod_dict["name"]),
                   str(prod_dict["description"]),
                   float(prod_dict["price"]),
                   int(prod_dict["quantity"]))

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

    @property
    def products(self):
        """Геттер для получения списка продуктов"""
        return self.__products.copy()  # Возвращаем копию для защиты от изменений

    def add_product(self, product):
        """Метод для добавления одного продукта"""
        self.__products.append(product)
        self.product_count = len(self.__products)

    def add_cls_product(self, prod_instance):
        self.add_product(prod_instance.name)

products_data = [
    {
        "name": "Samsung Galaxy S23",
        "description": "Флагманский смартфон Samsung",
        "price": 79999.0,
        "quantity": 15
    },
    {
        "name": "iPhone 15",
        "description": "Флагманский смартфон Apple",
        "price": 89999.0,
        "quantity": 10
    }
]
prod_1 = Product.new_product(products_data[0])
print(prod_1.get_product())