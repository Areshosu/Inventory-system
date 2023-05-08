from Models.Category import Category
from Services.DbContext import DbContext

class CategoryManager:
    dbContext = DbContext(Category)

    def getAsync(self):
        return self.dbContext.toListAsync()

    def findByCategoryName(self, categoryName: str):
        return self.dbContext.firstOrDefaultAsync("name", categoryName)
    
    def findById(self, id: str):
        return self.dbContext.findAsync(id)

    def createAsync(self, newCategory: dict):
        self.dbContext.add(newCategory)
        self.dbContext.saveChangesAsync()
        pass

    def updateAsync(self, id: str, updateCategory: dict):
        self.dbContext.update(id, updateCategory)
        self.dbContext.saveChangesAsync()
        pass

    def deleteAsync(self, id: str):
        self.dbContext.remove(id)
        self.dbContext.saveChangesAsync()
        pass