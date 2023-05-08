import json
from typing import Type
from Services.Console import *
from Services.CategoryManager import CategoryManager

class CategoryPage:
    def __init__(self, categoryManager: Type[CategoryManager]):
        self.categoryManager = categoryManager
        self.menuPage()

    def menuPage(self):
        clear_console()
        option = int(input("How would you like to manage Categories? \n\n" \
                                "[0] Show Category List \n" \
                                "[1] Find Category \n" \
                                "[2] Create Category \n" \
                                "[3] Update Category \n" \
                                "[4] Delete Category \n" \
                                "[5] Return to Main Menu \n\n" \
                                "Select Category [0-5] (Default 0): ") or 0)
        
        clear_console()
        if (option == 5):
            return
        elif (option == 4):
            self._deleteCategoryPage()
        elif (option == 3):
            self._updateCategoryPage()
        elif (option == 2):
            self._createCategoryPage()
        elif (option == 1):
            self._findCategoryPage()
        else:
            self._showCategoryPage()

    def _showCategoryPage(self):
        print("Retrieving categories ...")
        categories = self.categoryManager.getAsync()

        clear_console()
        print("Results: \n")
        for i, category in enumerate(categories):
            print(f"({i}) - {json.dumps(category)}")
        input("\nPress any key to continue ...")
        showMessageAndRedirectToMainPage(self, message="Redirecting you to menu page ...")
        pass

    def _findCategoryPage(self):
        print("Retrieving categories ...")
        categories = self.categoryManager.getAsync()
        print("Result may vary depending on your query (Leave it blank if you aren't sure) \n")
        
        code = input("What's it category code: ")
        name = input("What's it category name: ")
        description = input("What's it category description: ")
        filtered_categories = filter(lambda x: 
                                    (not code or x["code"] == code) and
                                    (not name or x["name"] == name) and
                                    (not description or x["description"] == description), categories)
        
        clear_console()
        print("Search results: \n")
        for i, category in enumerate(filtered_categories):
            print(f"({i}) - {json.dumps(category)}")
        input("\nPress any key to continue ...")
        showMessageAndRedirectToMainPage(self, message="Redirecting you to menu page ...")
        
    def _createCategoryPage(self):
        newCode = input("What's it code: ")
        newName = input("What's it category name: ")
        newDescription = input("What's it category description: ")

        self.categoryManager.createAsync({
                "code": newCode,
                "name": newName,
                "description": newDescription,
            })
        input("\nCategory created successfully ...")
        showMessageAndRedirectToMainPage(self, message="Redirecting you to menu page ...")

    def _updateCategoryPage(self):
        categoryId = input("Which category would you like to update, Please input Id: ")
        category = self.categoryManager.findById(categoryId)

        if (category is None):
            showMessageAndRedirectToMainPage(self, message=f"Category ({categoryId}) not found ...")

        print("Please fill up the form, except for those you want it to remain")
        updateCode = input("What's it code: ") or category["code"]
        updateName = input("What's it category name: ") or category["name"]
        updateDescription = input("What's it category description: ") or category["description"]

        self.categoryManager.updateAsync( categoryId, {
                "code": updateCode,
                "name": updateName,
                "description": updateDescription,
        })
        showMessageAndRedirectToMainPage(self, message=f"Category ({categoryId}) successfully updated ...")

    def _deleteCategoryPage(self):
        categoryId = input("Which category would you like to delete, Please input Id: ")
        self.categoryManager.deleteAsync(categoryId)
        showMessageAndRedirectToMainPage(self, message=f"Category ({categoryId}) successfully removed ...")