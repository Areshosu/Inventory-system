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
    - Register imports and database files in DbContext service
    - Create a new manager to manage dbContext