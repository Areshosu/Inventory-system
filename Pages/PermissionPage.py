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
                                    (not permissionName or x["name"] == permissionName) and
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
        newCanManageCategory = input("Can it manage category (y/n)? ")
        newCanStockTaking = input("Can it take stock (y/n)? ")
        newCanSearchItem = input("Can it search item (y/n)? ")
        newCanViewReplenishStockList = input("Can it view replenish stock list (y/n)? ")
        newCanReplenishStock = input("Can it replenish stock (y/n)? ")

        self.permissionManager.createAsync({
                   "name": newPermissionName,
                   "canManageUser": self._yesOrNoConvertToBool(newCanManagerUser),
                   "canManagePermission": self._yesOrNoConvertToBool(newCanManagePermission),
                   "canManageItem": self._yesOrNoConvertToBool(newCanManageItem),
                   "canManageCategory": self._yesOrNoConvertToBool(newCanManageCategory),
                   "canStockTaking": self._yesOrNoConvertToBool(newCanStockTaking),
                   "canSearchItem": self._yesOrNoConvertToBool(newCanSearchItem),
                   "canViewReplenishStockList":  self._yesOrNoConvertToBool(newCanViewReplenishStockList),
                   "canReplenishStock": self._yesOrNoConvertToBool(newCanReplenishStock)
        })
        showMessageAndRedirectToMainPage(self, message=f"Permission successfully created ...")

    def _updatePermissionPage(self):
        permissionId = input("Which permission would you like to update, Please input Id: ")
        permission = self.permissionManager.findById(permissionId)

        if (permission is None):
            showMessageAndRedirectToMainPage(self, message=f"Permission ({permissionId}) not found ...")

        updatePermissionName = input("Update permission name: ") or permission["name"]
        updateCanManagerUser = input("Can it manage user (y/n)? ") or self._boolConvertToYesOrNo(permission["canManageUser"])
        updateCanManagePermission = input("Can it manage permission (y/n)? ") or self._boolConvertToYesOrNo(permission["canManagePermission"])
        updateCanManageItem = input("Can it manage item (y/n)? ") or self._boolConvertToYesOrNo(permission["canManageItem"])
        updateCanManageCategory = input("Can it manage category (y/n)? ") or self._boolConvertToYesOrNo(permission["canManageCategory"])
        updateCanStockTaking = input("Can it take stock (y/n)? ") or self._boolConvertToYesOrNo(permission["canStockTaking"])
        updateCanSearchItem = input("Can it search item (y/n)? ") or self._boolConvertToYesOrNo(permission["canSearchItem"])
        updateCanViewReplenishStockList = input("Can it view replenish stock list (y/n)? ") or self._boolConvertToYesOrNo(permission["canViewReplenishStockList"])
        updateCanReplenishStock = input("Can it replenish stock (y/n)? ") or self._boolConvertToYesOrNo(permission["canReplenishStock"])

        self.permissionManager.updateAsync( permissionId, {
                   "name": updatePermissionName,
                   "canManageUser": self._yesOrNoConvertToBool(updateCanManagerUser),
                   "canManagePermission": self._yesOrNoConvertToBool(updateCanManagePermission),
                   "canManageItem": self._yesOrNoConvertToBool(updateCanManageItem),
                   "canManageCategory": self._yesOrNoConvertToBool(updateCanManageCategory),
                   "canStockTaking": self._yesOrNoConvertToBool(updateCanStockTaking),
                   "canSearchItem": self._yesOrNoConvertToBool(updateCanSearchItem),
                   "canViewReplenishStockList":  self._yesOrNoConvertToBool(updateCanViewReplenishStockList),
                   "canReplenishStock": self._yesOrNoConvertToBool(updateCanReplenishStock)
        })
        showMessageAndRedirectToMainPage(self, message=f"Permission ({permissionId}) successfully updated ...")

    def _deletePermissionPage(self):
        permissionId = input("Which permission would you like to delete, Please input Id: ")
        self.permissionManager.deleteAsync(permissionId)
        showMessageAndRedirectToMainPage(self, message=f"Permission ({permissionId}) successfully removed ...")

    def _yesOrNoConvertToBool(self, option: str):
        if (option is "y" or "Y"):
            return True
        else:
            return False
        
    def _boolConvertToYesOrNo(self, option: bool):
        if (option is True):
            return "y"
        else:
            return "n"