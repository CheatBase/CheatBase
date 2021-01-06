# This program imports the raw cheatcode data in the csv files, manipulates it to make it alphabetical and organized, then adds the data to the openvgdb.sqlite database.
# Copyright Noah Keck - All Rights Reserved

import numpy as np
import sqlite3
from pathlib import Path

# Import data


# Rearrange data
# TODO: Alphabetize, organize, etc. Have to adjust keys when doing so. Maybe there's a cascade function in Python?

# Setup database connection
conn = sqlite3.connect("openvgdb.sqlite")
cursor = conn.cursor()

# Insert data
print("Inserting cheat data.")
query = """
    INSERT INTO CHEAT_DEVICES VALUES (:cheatid, :romid, :cheatname, :cheatdesc, :cheatside, :cheatcategory, :cheatcode, :cheatdevice)
"""
cursor.executemany(query, cheat_devices)
query = """
    INSERT INTO CHEAT_CATEGORIES VALUES (:cheatid, :romid, :cheatname, :cheatdesc, :cheatside, :cheatcategory, :cheatcode, :cheatdevice)
"""
cursor.executemany(query, cheats_categories)
query = """
    INSERT INTO CHEATS VALUES (:cheatid, :romid, :cheatname, :cheatdesc, :cheatside, :cheatcategory, :cheatcode, :cheatdevice)
"""
cursor.executemany(query, cheats)
conn.commit()

print("All operations completed. Now starting cleanup.")
cursor.execute("VACUUM")
conn.commit()
