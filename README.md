# How to use
Before using this console app, please ensure you've ran the compulsary executables like seeders for inital setup

## Initial configuration

```bash
py -m Database.Seeders.Seeder
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
        <pre>
        <code>
        class User (Entity):
            uniques: list[str] = [
                "username"
            ]
        
            localForeigns: list[dict[str, str, str]] = []
        
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
        </code>
        </pre>
    - Register imports and database files in DbContext service
    - Create a new manager to manage dbContext