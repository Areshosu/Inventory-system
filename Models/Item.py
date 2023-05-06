from Models.Entity import Entity

class Item (Entity):
    uniques: list[str] = []
    localForeigns: list[dict[str, str, str]] = []
    targetForeigns: list[dict[str, str, str]] = [
        {"column": "categoryId", "reference": "Id", "onTable": "Category"}
    ]

    def __init__ (self, 
                    category_id: str,
                    code: str, 
                    name: str, 
                    description: str, 
                    unit: str, 
                    price: float, 
                    quantity: int, 
                    minimum: int,
                    Id: str = ""):

        if (len(Id) != 0):
            self.Id   = self.dataAnnotation(Id, str)

        self.category_id =   self.dataAnnotation(category_id, str)
        self.code =          self.dataAnnotation(code, str)
        self.name =          self.dataAnnotation(name, str)
        self.description =   self.dataAnnotation(description, str)
        self.unit =          self.dataAnnotation(unit, str)
        self.price =         self.dataAnnotation(price, float)
        self.quantity =      self.dataAnnotation(quantity, int)
        self.minimum =       self.dataAnnotation(minimum, int)
