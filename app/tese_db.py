from pony.orm import Database, Required

db = Database()
db.bind(provider='sqlite', filename='plants.sqlite', create_db=True)

class Plant(db.Entity):
    naziv = Required(str)

db.generate_mapping(create_tables=True)

print("Tables created successfully.")
