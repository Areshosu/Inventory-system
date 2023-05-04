from Models.Entity import Entity
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
        dbName = dbclass.__name__

        for database in self.databases:
            if database["dbName"] == dbName:
                self.selectedDatabase = database
                self.selectedEntity = dbclass
                break

        if (self.selectedDatabase == None):
            raise ValueError("Database not found.")
        
        self.load()
        pass

    def load(self):
        file = open(f"{self.baseFolder}/{self.selectedDatabase['fileName']}")
        self.retrievedRecords = json.load(file)
        file.close()

    # Retrieve

    def findAsync(self, id):
        return next((data for data in self.retrievedRecords if data["Id"] == id), None)

    def toListAsync(self):
        return self.retrievedRecords
    
    def firstOrDefaultAsync(self, columnName: str="", value: str=""):
        if (len(self.retrievedRecords) == 0):
            return

        if isinstance(columnName, str):
            return next((data for data in self.retrievedRecords if data[columnName] == value), None)
                
        return self.retrievedRecords[0]
    
    # Relationship
    def includeOneToOne(self, dbclass: Type[Entity]):
        currentEntity = self.selectedEntity

        relationship = next((relation for relation in currentEntity.targetForeigns if relation["onTable"] == dbclass.__name__), None)
        relationshipTable = next((table for table in self.databases if table["dbName"] == dbclass.__name__), None)
        relationFile = open(f"{self.baseFolder}/{relationshipTable['fileName']}")
        self.retrievedRelationRecords = json.load(relationFile)
        relationFile.close()

        for row in self.retrievedRecords:
            for relationRow in self.retrievedRelationRecords:
                if row[relationship["column"]] == relationRow[relationship["reference"]]:
                    row.setdefault(f"{dbclass.__name__.lower()}", {}).update(relationRow)
                    break
        return self
    
    def includeOneToMany(self, dbclass: Type[Entity]):
        currentEntity = self.selectedEntity

        relationship = next((relation for relation in currentEntity.targetForeigns if relation["onTable"] == dbclass.__name__), None)
        relationshipTable = next((table for table in self.databases if table["dbName"] == dbclass.__name__), None)
        relationFile = open(f"{self.baseFolder}/{relationshipTable['fileName']}")
        self.retrievedRelationRecords = json.load(relationFile)
        relationFile.close()

        for row in self.retrievedRecords:
            for relationRow in self.retrievedRelationRecords:
                if row[relationship["column"]] == relationRow[relationship["reference"]]:
                    row.setdefault(f"{dbclass.__name__.lower()}s", []).append(relationRow)
        return self
    
    # Modification
    def add(self, values: dict):

        newData = self.selectedEntity(**values)
        if (hasattr(newData, "Id") == False):
            newData.Id = self._generateId()

        self.retrievedRecords.append(newData.__dict__)

    def update(self, id: str, values: dict):
        EditingEntityId = id
        
        if (EditingEntityId is None):
            raise ValueError("Update Entity Id not found.")
        
        [data.update(values) for data in self.retrievedRecords if data["Id"] == EditingEntityId]

    def remove(self, id: str):
        [self.retrievedRecords.remove(data) for data in self.retrievedRecords if data["Id"] == id]

    def removeAll(self, columnName: str, value: str):
        [self.retrievedRecords.remove(data) for data in self.retrievedRecords if data[columnName] == value]

    def clear(self):
        self.retrievedRecords.clear()

    def saveChangesAsync(self):
        self._validate()
        file = open(f"{self.baseFolder}/{self.selectedDatabase['fileName']}", mode="w")
        file.write(json.dumps(self.retrievedRecords))
        file.close()

    # Helper methods
    def _generateId(self):
        while True:
            newId = str(uuid.uuid4())
            if not any(item.get("Id") == newId for item in self.retrievedRecords):
                return newId
            
    def _validate(self):
        # @TODO
        # Foreign constrains

        uniqueConstraints = self.selectedEntity.uniques
        localForeignConstraints = self.selectedEntity.localForeigns
        targetForeignConstraints = self.selectedEntity.targetForeigns

        for uniqueColumn in uniqueConstraints:
            values = [record[uniqueColumn] for record in self.retrievedRecords]
            if len(values) != len(set(values)):
                raise ValueError(f"Duplicated unique constraint ({uniqueColumn})")
        pass