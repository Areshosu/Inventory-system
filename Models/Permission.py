from Models.Entity import Entity

class Permission (Entity):
    uniques: list[str] = []
    localForeigns: list[dict[str, str, str]] = [
        {"column": "Id", "reference": "permissionId", "onTable": "User"}
    ]
    targetForeigns: list[dict[str, str, str]] = []

    # static var
    availablePermissions = [
        {"Id":"4dcdd026-c5e3-4961-8459-f03d4b417399",
                   "name":"admin",
                   "canManageUser":True,
                   "canManagePermission":True,
                   "canManageItem":True,
                   "canStockTaking":True,
                   "canSearchItem":True,
                   "canViewReplenishStockList": True,
                   "canReplenishStock":True},
        {"Id":"df3aa723-90d0-47a7-96f2-19bffac06c93",
                   "name":"purchaser",
                   "canManageUser":False,
                   "canManagePermission":False,
                   "canManageItem":False,
                   "canStockTaking":True,
                   "canSearchItem":True,
                   "canViewReplenishStockList": False,
                   "canReplenishStock":False},
        {"Id":"e02feaee-2a37-4c96-b508-60a7644e9966",
                   "name":"inventorychecker",
                   "canManageUser":False,
                   "canManagePermission":False,
                   "canManageItem":False,
                   "canStockTaking":False,
                   "canSearchItem":True,
                   "canViewReplenishStockList": True,
                   "canReplenishStock":False}
    ]

    def __init__(self,
                    name: str,
                    canManageUser: bool,
                    canManageItem: bool,
                    canManagePermission: bool,
                    canStockTaking: bool,
                    canSearchItem: bool,
                    canViewReplenishStockList: bool,
                    canReplenishStock: bool,
                    Id: str = ""):
        
        if (len(Id) != 0):
            self.Id   = self.dataAnnotation(Id, str)

        self.name =                      self.dataAnnotation(name, str)
        self.canManageUser =             self.dataAnnotation(canManageUser, bool)
        self.canManagePermission =       self.dataAnnotation(canManagePermission, bool)
        self.canManageItem =             self.dataAnnotation(canManageItem, bool)
        self.canStockTaking =            self.dataAnnotation(canStockTaking, bool)
        self.canSearchItem =             self.dataAnnotation(canSearchItem, bool)
        self.canViewReplenishStockList = self.dataAnnotation(canViewReplenishStockList, bool)
        self.canReplenishStock =         self.dataAnnotation(canReplenishStock, bool)