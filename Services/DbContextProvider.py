from typing import Type
from Models.Entity import Entity
from Services.DbContext import DbContext
import json

# Playground and tests
class DbContextProvider:
    dbContext: DbContext
    selectedRelationEntity: Entity
    retrievedRelationRecords: list

    def __init__(self, dbContext: Type[DbContext]):
        self.dbContext = dbContext

    def includeOneToOne(self, dbclass: Type[Entity]):
        currentEntity = self.dbContext.selectedEntity

        relationship = next((relation for relation in currentEntity.targetForeigns if relation["onTable"] == dbclass.__name__), None)
        relationshipTable = next((table for table in self.dbContext.databases if table["dbName"] == dbclass.__name__), None)
        relationFile = open(f"{self.dbContext.baseFolder}/{relationshipTable['fileName']}")
        self.retrievedRelationRecords = json.load(relationFile)
        relationFile.close()

        for row in self.dbContext.retrievedRecords:
            for relationRow in self.retrievedRelationRecords:
                if row[relationship["column"]] == relationRow[relationship["reference"]]:
                    row.setdefault(f"{dbclass.__name__.lower()}s", []).append(relationRow)
        return self
    
    def test(self):
        return self.dbContext.retrievedRecords