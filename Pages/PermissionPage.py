import json
from typing import Type
from Services.Console import *
from Services.PermissionManager import PermissionManager

class PermissionPage:
    def __init__(self, permissionManager: Type[PermissionManager]):
        self.permissionManager = permissionManager
        self.menuPage()

    def menuPage(self):
        clear_console()
        option = int(input("How would you like to manage Permissions? \n\n" \
                                "[0] Show Permission List \n" \
                                "[1] Find Permission \n" \
                                "[2] Create Permission \n" \
                                "[3] Update Permission \n" \
                                "[4] Delete Permission \n\n" \
                                "Select Item [0-3] (Default 0): ") or 0)
        
        clear_console()
        if (option == 4):
            self._deletePermissionPage()
        elif (option == 3):
            self._updatePermissionPage()
        elif (option == 2):
            self._createPermissionPage()
        elif (option == 1):
            self._findPermissionPage()
        else:
            self._showPermissionPage()

    def _showPermissionPage(self):
        print("Retrieving permissions ...")
        permissions = self.permissionManager.getAsync()

        clear_console()
        print("Results: \n")
        for i, permission in enumerate(permissions):
            print(f"({i}) - {json.dumps(permission)}")
        input("\nPress any key to continue ...")
        showMessageAndRedirectToMainPage(self, message="Redirecting you to menu page ...")
        pass

    def _findPermissionPage(self):
        print("Retrieving permissions ...")
        permissions = self.permissionManager.getAsync()
        print("Result may vary depending on your query (Leave it blank if you aren't sure) \n")
        
        permissionName = input("What's it permission name (y/n)? ")
        canManagerUser = input("Does it manage user (y/n)? ")
        canManagePermission = input("Does it manage permission (y/n)? ")
        canManageItem = input("Does it manage item (y/n)? ")
        canStockTaking = input("Does it manage stock taking (y/n)? ")
        canSearchItem = input("Does it allow to search item (y/n)? ")
        canViewReplenishStockList = input("Does it allow to view replenish stock (y/n)? ")
        canReplenishStock = input("Does it allow to replenish stock (y/n)? ")
        filtered_permissions = filter(lambda x: 
                                    (not permissionName or x["username"] == permissionName) and
                                    (not canManagerUser or x["canManagerUser"] == canManagerUser) and
                                    (not canManagePermission or x["canManagePermission"] == canManagePermission) and
                                    (not canManageItem or x["canManageItem"] == canManageItem) and
                                    (not canStockTaking or x["canStockTaking"] == canStockTaking) and
                                    (not canSearchItem or x["canSearchItem"] == canSearchItem) and
                                    (not canViewReplenishStockList or x["canViewReplenishStockList"] == canViewReplenishStockList) and
                                    (not canReplenishStock or x["canReplenishStock"] == canReplenishStock),
                                    permissions)
        
        clear_console()
        print("Search results: \n")
        for i, permission in enumerate(filtered_permissions):
            print(f"({i}) - {json.dumps(permission)}")
        input("\nPress any key to continue ...")
        showMessageAndRedirectToMainPage(self, message="Redirecting you to menu page ...")
        
    def _createPermissionPage(self):
        newPermissionName = input(f"New permission name: ")
        newCanManagerUser = input("Can it manage user (y/n)? ")
        newCanManagePermission = input("Can it manage permission (y/n)? ")
        newCanManageItem = input("Can it manage item (y/n)? ")
        newCanStockTaking = input("Can it take stock (y/n)? ")
        newCanSearchItem = input("Can it search item (y/n)? ")
        newCanViewReplenishStockList = input("Can it view replenish stock list (y/n)? ")
        newCanReplenishStock = input("Can it replenish stock (y/n)? ")

        self.permissionManager.createAsync({
                   "name": newPermissionName,
                   "canManageUser": True if newCanManagerUser is "n" else False,
                   "canManagePermission": True if newCanManagePermission is "n" else False,
                   "canManageItem": True if newCanManageItem is "n" else False,
                   "canStockTaking": True if newCanStockTaking is "n" else False,
                   "canSearchItem": True if newCanSearchItem is "n" else False,
                   "canViewReplenishStockList":  True if newCanViewReplenishStockList is "n" else False,
                   "canReplenishStock": True if newCanReplenishStock is "n" else False
        })
        showMessageAndRedirectToMainPage(self, message=f"Permission successfully created ...")

    def _updatePermissionPage(self):
        permissionId = input("Which permission would you like to update, Please input Id: ")
        permission = self.permissionManager.findById(permissionId)

        if (permission is None):
            showMessageAndRedirectToMainPage(self, message=f"Permission ({permissionId}) not found ...")

        updatePermissionName = input(f"New permission name: ") or permission["name"]
        updateCanManagerUser = input("Can it manage user (y/n)? ")
        updateCanManagePermission = input("Can it manage permission (y/n)? ")
        updateCanManageItem = input("Can it manage item (y/n)? ")
        updateCanStockTaking = input("Can it take stock (y/n)? ")
        updateCanSearchItem = input("Can it search item (y/n)? ")
        updateCanViewReplenishStockList = input("Can it view replenish stock list (y/n)? ")
        updateCanReplenishStock = input("Can it replenish stock (y/n)? ")

        self.permissionManager.updateAsync( permissionId, {
                   "name": updatePermissionName,
                   "canManageUser": True if updateCanManagerUser is "n" else False,
                   "canManagePermission": True if updateCanManagePermission is "n" else False,
                   "canManageItem": True if updateCanManageItem is "n" else False,
                   "canStockTaking": True if updateCanStockTaking is "n" else False,
                   "canSearchItem": True if updateCanSearchItem is "n" else False,
                   "canViewReplenishStockList":  True if updateCanViewReplenishStockList is "n" else False,
                   "canReplenishStock": True if updateCanReplenishStock is "n" else False
        })
        showMessageAndRedirectToMainPage(self, message=f"Permission ({permissionId}) successfully updated ...")

    def _deletePermissionPage(self):
        permissionId = input("Which permission would you like to delete, Please input Id: ")
        self.permissionManager.deleteAsync(permissionId)
        showMessageAndRedirectToMainPage(self, message=f"Permission ({permissionId}) successfully removed ...")