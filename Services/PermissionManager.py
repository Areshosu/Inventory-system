from Models.Permission import Permission
from Services.DbContext import DbContext

class PermissionManager:
    dbContext = DbContext(Permission)

    def findByRoleName(self, role: str):
        return self.dbContext.firstOrDefaultAsync("name", role)
    
    def findById(self, id: str):
        return self.dbContext.findAsync(id)