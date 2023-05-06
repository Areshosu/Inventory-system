from Models.Entity import Entity
from Models.Category import Category
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
        {"dbName": "Category", "fileName": "CategoriesTable.json"},
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
    def _loadRelatedRecords(self, dbclass: Type[Entity], isParentForeign: bool):
        childOrParentForeign = self.selectedEntity.targetForeigns if isParentForeign == True else self.selectedEntity.localForeigns

        relationshipDB = next((relation for relation in childOrParentForeign if relation["onTable"] == dbclass.__name__), None)
        relationshipTable = next((table for table in self.databases if table["dbName"] == dbclass.__name__), None)
        relationFile = open(f"{self.baseFolder}/{relationshipTable['fileName']}")
        self.retrievedRelationRecords = json.load(relationFile)
        relationFile.close()
        return relationshipDB

    def includeOneToOne(self, dbclass: Type[Entity], isParentForeign: bool = True):
        relationshipDB = self._loadRelatedRecords(dbclass, isParentForeign)
        for row in self.retrievedRecords:
            for relationRow in self.retrievedRelationRecords:
                if relationshipDB is None:
                    raise DbException(f"No such relationship {getCallerName()} ({dbclass.__name__})")

                if row[relationshipDB["column"]] == relationRow[relationshipDB["reference"]]:
                    row.setdefault(f"{dbclass.__name__.lower()}", {}).update(relationRow)
                    break
        return self

    def includeOneToMany(self, dbclass: Type[Entity], isParentForeign: bool = True):
        relationshipDB = self._loadRelatedRecords(dbclass, isParentForeign)
        for row in self.retrievedRecords:
            for relationRow in self.retrievedRelationRecords:
                if relationshipDB is None:
                    raise DbException(f"No such relationship {getCallerName()} ({dbclass.__name__})")

                if relationshipDB is not None and row[relationshipDB["column"]] == relationRow[relationshipDB["reference"]]:
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
        onSavingRecords = self.retrievedRecords

        uniqueConstraints = self.selectedEntity.uniques
        foreigns = [
            self.selectedEntity.localForeigns,
            self.selectedEntity.targetForeigns
        ]

        # Unique constrains
        for uniqueColumn in uniqueConstraints:
            values = [record[uniqueColumn] for record in onSavingRecords]
            if len(values) != len(set(values)):
                raise DbException(f"Duplicated unique constraint ({uniqueColumn})")
        
        # Foreign constrains
        for i, foreignConstrain in enumerate(foreigns):
            isParentForeign = False if i == 0 else True
            for localForeign in foreignConstrain:
                relationEntity = globals()[localForeign["onTable"]]
                relationshipDB = self._loadRelatedRecords(relationEntity, isParentForeign) # load relationRecords & returns relationDB
                for savingRow in onSavingRecords:
                    if (isParentForeign == True):
                        haveValidRelation = False
                        for relation in self.retrievedRelationRecords:
                            if savingRow[relationshipDB["column"]] == relation[relationshipDB["reference"]]:
                                haveValidRelation = True; break
                        if (haveValidRelation == False):
                            raise DbException(f"Relation failed at table {self.selectedEntity.__name__} on {relationEntity.__name__}, at column {relationshipDB['column']} on column {relationshipDB['reference']} ({savingRow[relationshipDB['column']]})")
                    else:
                        haveValidRelation = True
                        for relation in self.retrievedRelationRecords:
                            if savingRow[relationshipDB["column"]] == relation[relationshipDB["reference"]]:
                                haveValidRelation = False; break
                        if (haveValidRelation == False):
                            raise DbException(f"Relation failed at table {self.selectedEntity.__name__} on {relationEntity.__name__}, at column {relationshipDB['column']} on column {relationshipDB['reference']} ({savingRow[relationshipDB['column']]})")
            pass