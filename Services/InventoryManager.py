from Models.Item import Item
from Services.DbContext import DbContext

class InventoryManager:
    dbContext = DbContext(Item)