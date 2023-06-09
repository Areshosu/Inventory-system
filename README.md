# How to use
![Python 3.10.10](https://img.shields.io/badge/python-3.10.10-blue.svg)
![Project Status](https://img.shields.io/badge/status-active-brightgreen.svg)
![Project Stability](https://img.shields.io/badge/stability-stable-brightgreen.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Before using this console app, please ensure you've ran the compulsary executables like seeders for inital setup

## Requirements

- 2 gb ram Windows 10
- Python 3.10.10 or above

## Initial configuration

```bash
py -m Database.Seeders.Seeder
py MainProgram.py # To start the mainApp
py -m MainProgram.py # Incase it doesn't work
```

## Usage
Before login, please register a user, and then select a desirable role/permission

- ADMIN
- Purchaser
- Inventory checker

## Contribution
If you want to contribute, please take note of the current infrastructure
- To add new Tables 
    - You need to add new models under models (Register foreign, unique keys)
        ```python
        class User (Entity):
            # unique constrains
            uniques: list[str] = [
                "username"
            ]
            # local foreign constrains
            localForeigns: list[dict[str, str, str]] = []
        
            # linked foreign constrains
            targetForeigns: list[dict[str, str, str]] = [
                {"column": "permissionId", "reference": "Id", "onTable": "Permission"}
            ]
        
            def __init__(self,
                            username: str,
                            password: str,
                            gender: str,
                            age: int,
                            permissionId: str,
                            Id: str = ""):
        
                if (len(Id) != 0):
                    self.Id   = self.dataAnnotation(Id, str)
        
                self.username     = self.dataAnnotation(username, str)
                self.password     = self.dataAnnotation(password, str)
                self.gender       = self.dataAnnotation(gender, str)
                self.age          = self.dataAnnotation(age, int)
                self.permissionId = self.dataAnnotation(permissionId, str)
        ```

    - Register imports and database files in DbContext service
        ```python
        # Add imports for entities
        from Models.Entity import Entity
        from Models.Item import Item
        from Models.Permission import Permission
        from Models.User import User

        from Services.Console import getCallerName
        from Services.Exception.DbException import DbException
        from typing import Type
        import json
        import uuid

        class DbContext:
            baseFolder: str = "Database"
            selectedEntity: Entity
            selectedDatabase: dict
            retrievedRecords: list

            # Register models
            databases = [
                {"dbName": "Item", "fileName": "ItemsTable.json"},
                {"dbName": "Permission", "fileName": "PermissionsTable.json"},
                {"dbName": "User", "fileName": "UsersTable.json"},
            ]

            def __init__(self, dbclass: Type[Entity]):
        ```

    - Create a new manager to manage dbContext
        ```
        proj/
        ├ mainProgram.py
        ├ Services/
        ├ __init__.py
        │ ├ DbContext.py
        │ └ NewEntityManager.py
        ```