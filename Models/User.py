from Models.Entity import Entity

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