from pony.orm import Database, Required, Optional
from datetime import datetime

db = Database()

db.bind(provider='sqlite', filename='plants.sqlite', create_db=True)  # ovo ide PRVO

class Plant(db.Entity):
    naziv = Required(str)
    vrsta = Required(str)
    potrebe_za_svjetlom = Required(str)
    zadnje_zalijevanje = Optional(datetime)
    sljedece_zalijevanje = Optional(datetime)
    zadnja_prihrana = Optional(datetime)
    sljedeca_prihrana = Optional(datetime)
    biljeske = Optional(str)

db.generate_mapping(create_tables=True)  # ovo ide ZADNJE
