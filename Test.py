from Models.User import User
from Models.Permission import Permission
from Services.DbContext import DbContext
from Services.DbContextProvider import DbContextProvider

dbContext = DbContext(User)
dbContext.includeOneToOne(Permission)

import json
print(json.dumps(dbContext.toListAsync()))