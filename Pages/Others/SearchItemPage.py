import json
from typing import Type
from Services.Console import *
from Services.CategoryManager import CategoryManager
from Services.ItemManager import ItemManager

class SearchItemPage:
    def __init__(self, itemManager: Type[ItemManager], 
                        categoryManager: Type[CategoryManager]):
        self.itemManager = itemManager
        self.categoryManager = categoryManager
        self._findItemPage()

    def _findItemPage(self):
        print("Retrieving items ...")
        items = self.itemManager.getAsync()
        print("Result may vary depending on your query (Leave it blank if you aren't sure) \n")
        
        code = input("What's it item code: ")
        name = input("What's it item name: ")
        description = input("What's it item description: ")
        unit = input("What's it item unit: ")
        price = float(input("What's it item price: ") or 0)
        minimum = int(input("What's it item minimum: ") or 0)
        filtered_items = filter(lambda x: 
                                    (not code or x["code"] == code) and
                                    (not name or x["name"] == name) and
                                    (not description or x["description"] == description) and
                                    (not unit or x["unit"] == unit) and
                                    (not price or x["price"] == price)and
                                    (not minimum or x["minimum"] == minimum), items)
        
        clear_console()
        print("Search results: \n")
        for i, item in enumerate(filtered_items):
            print(f"({i}) - {json.dumps(item)}")
        return input("\nPress any key to continue ...")
        