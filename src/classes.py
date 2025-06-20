class Product:
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    _total_categories = 0
    _unique_names = set()
    category_count = 0  # Атрибут уровня класса
    product_count = 0  # Атрибут уровня класса

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products

        if name not in self._unique_names:
            self._unique_names.add(name)
            Category._total_categories += 1
            Category.category_count = Category._total_categories

        self.product_count = len(products)  # Атрибут экземпляра
