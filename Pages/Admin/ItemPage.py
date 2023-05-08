import json
from typing import Type
from Services.Console import *
from Services.CategoryManager import CategoryManager
from Services.ItemManager import ItemManager

class ItemPage:
    def __init__(self, itemManager: Type[ItemManager], 
                        categoryManager: Type[CategoryManager]):
        self.itemManager = itemManager
        self.categoryManager = categoryManager
        self.menuPage()

    def menuPage(self):
        clear_console()
        option = int(input("How would you like to manage Items? \n\n" \
                                "[0] Show Item List \n" \
                                "[1] Find Item \n" \
                                "[2] Create Item \n" \
                                "[3] Update Item \n" \
                                "[4] Delete Item \n" \
                                "[5] Return to Main Menu \n\n" \
                                "Select Item [0-5] (Default 0): ") or 0)
        
        clear_console()
        if (option == 5):
            return
        elif (option == 4):
            self._deleteItemPage()
        elif (option == 3):
            self._updateItemPage()
        elif (option == 2):
            self._createItemPage()
        elif (option == 1):
            self._findItemPage()
        else:
            self._showItemPage()

    def _showItemPage(self):
        print("Retrieving items ...")
        items = self.itemManager.getAsync()

        clear_console()
        print("Results: \n")
        for i, item in enumerate(items):
            print(f"({i}) - {json.dumps(item)}")
        input("\nPress any key to continue ...")
        showMessageAndRedirectToMainPage(self, message="Redirecting you to menu page ...")
        pass

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
        input("\nPress any key to continue ...")
        showMessageAndRedirectToMainPage(self, message="Redirecting you to menu page ...")
        
    def _createItemPage(self):
        newCode = input("What's it code: ")
        newName = input("What's it item name: ")
        newDescription = input("What's it item description: ")
        newUnit = input("What's it item unit: ")
        newPrice = float(input("What's it item price: ") or 0)
        newMinimum = int(input("What's it item minimum: ") or 0)
        categories = self.categoryManager.getAsync()

        if (len(categories) == 0):
            return showMessageAndRedirectToMainPage(self, message="Please create at least a category before proceeding")
        else:
            print("Select categories")

        for i, category in enumerate(categories):
            print(f"({i}) - {json.dumps(category)}")
        newCategorySelection = int(input("Please type in your selection eg. 5: "), 0)

        self.itemManager.createAsync({
                "code": newCode,
                "name": newName,
                "description": newDescription,
                "unit": newUnit,
                "price": newPrice,
                "quantity": 0,
                "minimum": newMinimum,
                "categoryId": categories[newCategorySelection]["Id"]
            })
        input("\nItem created successfully ...")
        showMessageAndRedirectToMainPage(self, message="Redirecting you to menu page ...")

    def _updateItemPage(self):
        itemId = input("Which item would you like to update, Please input Id: ")
        item = self.itemManager.findById(itemId)

        if (item is None):
            return showMessageAndRedirectToMainPage(self, message=f"Item ({itemId}) not found ...")

        print("Please fill up the form, except for those you want it to remain")
        updateCode = input("What's it code: ") or item["code"]
        updateName = input("What's it item name: ") or item["name"]
        updateDescription = input("What's it item description: ") or item["description"]
        updateUnit = input("What's it item unit: ") or item["unit"]
        updatePrice = float(input("What's it item price: ") or item["price"])
        updateMinimum = int(input("What's it item minimum: ") or item["minimum"])
        updateQuantity = item["quantity"] # Quantity are not allow to change
        categories = self.categoryManager.getAsync()

        print("Select categories")
        for i, category in enumerate(categories):
            print(f"({i}) - {json.dumps(category)}")
        updateCategorySelection = int(input("Please type in your selection eg. 5, or leave it blank to remain: ") or 0)

        self.itemManager.updateAsync( itemId, {
                "code": updateCode,
                "name": updateName,
                "description": updateDescription,
                "unit": updateUnit,
                "price": updatePrice,
                "quantity": updateQuantity,
                "minimum": updateMinimum,
                "categoryId": categories[updateCategorySelection]["Id"] or item["categoryId"]
        })
        showMessageAndRedirectToMainPage(self, message=f"Item ({itemId}) successfully updated ...")

    def _deleteItemPage(self):
        itemId = input("Which item would you like to delete, Please input Id: ")
        self.itemManager.deleteAsync(itemId)
        showMessageAndRedirectToMainPage(self, message=f"Item ({itemId}) successfully removed ...")