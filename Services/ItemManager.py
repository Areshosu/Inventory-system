from Models.Item import Item
from Services.DbContext import DbContext

class ItemManager:
    dbContext = DbContext(Item)

    def getAsync(self):
        return self.dbContext.toListAsync()

    def findByItemName(self, itemName: str):
        return self.dbContext.firstOrDefaultAsync("name", itemName)
    
    def findById(self, id: str):
        return self.dbContext.findAsync(id)

    def createAsync(self, newItem: dict):
        self.dbContext.add(newItem)
        self.dbContext.saveChangesAsync()
        pass

    def updateAsync(self, id: str, updateItem: dict):
        self.dbContext.update(id, updateItem)
        self.dbContext.saveChangesAsync()
        pass

    def deleteAsync(self, id: str):
        self.dbContext.remove(id)
        self.dbContext.saveChangesAsync()
        pass