from Models.Entity import Entity

class Category (Entity):
    uniques: list[str] = [
        "name"
    ]
    localForeigns: list[dict[str, str, str]] = [
        {"column": "Id", "reference": "categoryId", "onTable": "Item"}
    ]
    targetForeigns: list[dict[str, str, str]] = []

    def __init__ (self, 
                    code: str, 
                    name: str, 
                    description: str, 
                    Id: str = ""):

        if (len(Id) != 0):
            self.Id   = self.dataAnnotation(Id, str)

        self.code =          self.dataAnnotation(code, str)
        self.name =          self.dataAnnotation(name, str)
        self.description =   self.dataAnnotation(description, str)
