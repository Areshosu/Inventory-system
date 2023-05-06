from Services.Console import *
from Models.User import User
from Models.Permission import Permission
from Services.DbContext import DbContext

class UserManager:
    dbContext = DbContext(User)

    def getAsync(self):
        return self.dbContext.toListAsync()

    def findByUserName(self, username: str):
        return self.dbContext.includeOneToOne(Permission).firstOrDefaultAsync("username", username)
    
    def findById(self, id: str):
        return self.dbContext.findAsync(id)

    def createAsync(self, newUser: dict):
        self.dbContext.add(newUser)
        self.dbContext.saveChangesAsync()
        pass

    def updateAsync(self, id: str, updateUser: dict):
        self.dbContext.update(id, updateUser)
        self.dbContext.saveChangesAsync()
        pass

    def deleteAsync(self, id: str):
        self.dbContext.remove(id)
        self.dbContext.saveChangesAsync()
        pass

    def verifyLogin(self, username: str, password: str):
        for user in self.dbContext.toListAsync():
            if (user["username"] == username and user["password"] == password):
                return True
