from Services.DbContext import DbContext
from Models.Permission import Permission

# py -m Database.Seeders.Seeder
# Seeder for permissions only
dbcontextPermission = DbContext(Permission)
dbcontextPermission.clear()

for permission in Permission.availablePermissions:
    dbcontextPermission.add(permission)

dbcontextPermission.saveChangesAsync()