from Models.Permission import Permission
from Services.DbContext import DbContext

class PermissionManager:
    dbContext = DbContext(Permission)

    def getAsync(self):
        return self.dbContext.toListAsync()

    def findByRoleName(self, roleName: str):
        return self.dbContext.firstOrDefaultAsync("name", roleName)
    
    def findById(self, id: str):
        return self.dbContext.findAsync(id)

    def createAsync(self, newPermission: dict):
        self.dbContext.add(newPermission)
        self.dbContext.saveChangesAsync()
        pass

    def updateAsync(self, id: str, updatePermission: dict):
        self.dbContext.update(id, updatePermission)
        self.dbContext.saveChangesAsync()
        pass

    def deleteAsync(self, id: str):
        self.dbContext.remove(id)
        self.dbContext.saveChangesAsync()
        pass