# This program imports the raw cheatcode data in the csv files, manipulates it to make it alphabetical and organized, then adds the data to the openvgdb.sqlite database.
# Copyright Noah Keck - All Rights Reserved

import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path

# Setup database connection
conn = sqlite3.connect("openvgdb.sqlite")
cursor = conn.cursor()
tmp = cursor.execute("SELECT systemShortName FROM SYSTEMS")
systems = []
for sys in cursor.fetchall():
    systems.append(sys[0])

# Import data
dir = Path().resolve()
convertkeys = {0: int, }
allcheats = []
for sys in systems:
    filepath = Path(str(dir) + "/raw_data/cheats/" + sys + ".csv")
    if Path(filepath).is_file():
        df = pd.read_csv(filepath, header=0).replace({np.nan: None})
        allcheats.append(df.values.tolist())

filepath = str(dir) + "/raw_data/cheatDevices.csv"
cheat_devices = pd.read_csv(filepath, header=0).values.tolist()

filepath = str(dir) + "/raw_data/cheatCategories.csv"
cheats_categories = pd.read_csv(filepath, header=0).values.tolist()

# Rearrange data
# TODO: Alphabetize, organize, etc. Have to adjust keys when doing so. Maybe there's a cascade function in Python?

# Export to openvgdb database
print("Setting up cheat tables.")
cursor.executescript("DROP TABLE IF EXISTS CHEATS; DROP TABLE IF EXISTS CHEAT_DEVICES; DROP TABLE IF EXISTS CHEAT_CATEGORIES") # drop cheat tables if they exist
query = """
    CREATE TABLE CHEAT_DEVICES (
        cheatDeviceID INTEGER PRIMARY KEY AUTOINCREMENT,
        systemID INTEGER,
        cheatDeviceName TEXT,
        cheatDeviceBrandName TEXT,
        cheatDeviceFormat TEXT,
        FOREIGN KEY (systemID)
            REFERENCES SYSTEMS (systemID)
            ON UPDATE CASCADE
            ON DELETE SET NULL
    )
"""
cursor.execute(query)
query = """
    CREATE TABLE CHEAT_CATEGORIES (
        cheatCategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
        cheatCategory TEXT,
        cheatCategoryDescription TEXT
    )
"""
cursor.execute(query)
query = """
    CREATE TABLE CHEATS (
        cheatID INTEGER PRIMARY KEY AUTOINCREMENT,
        romID INTEGER,
        cheatName TEXT,
        cheatActivation TEXT,
        cheatDescription TEXT,
        cheatSideEffect TEXT,
        cheatFolderName TEXT,
        cheatCategoryID INTEGER,
        cheatCode TEXT,
        cheatDeviceID INTEGER,
        FOREIGN KEY (romID)
            REFERENCES ROMs (romID)
            ON UPDATE CASCADE
            ON DELETE SET NULL
        FOREIGN KEY (cheatCategoryID)
            REFERENCES CHEAT_CATEGORIES (cheatCategoryID)
            ON UPDATE CASCADE
            ON DELETE SET NULL
        FOREIGN KEY (cheatDeviceID)
            REFERENCES CHEAT_DEVICES (cheatDeviceID)
            ON UPDATE CASCADE
            ON DELETE SET NULL
    )
"""
cursor.execute(query)
conn.commit()

# Insert data
print("Inserting cheat data.")
query = """
    INSERT INTO CHEAT_DEVICES (cheatDeviceID, systemID, cheatDeviceName, cheatDeviceBrandName, cheatDeviceFormat)
    VALUES (:cheatdevid, :sysid, :cheatdevname, :cheatdevbrand, :cheatdevfmt)
"""
cursor.executemany(query, cheat_devices)
query = """
    INSERT INTO CHEAT_CATEGORIES (cheatCategoryID, cheatCategory, cheatCategoryDescription)
    VALUES (:cheatcategoryid, :cheatcategory, :cheatcategorydesc)
"""
cursor.executemany(query, cheats_categories)
query = """
    INSERT INTO CHEATS (romID, cheatName, cheatActivation, cheatDescription, cheatSideEffect, cheatFolderName, cheatCategoryID, cheatCode, cheatDeviceID)
    VALUES (:romid, :cheatname, :cheatactiv, :cheatdesc, :cheatside, :cheatfolder, :cheatcategory, :cheatcode, :cheatdevice)
"""
for cheats in allcheats:
    cursor.executemany(query, cheats)
    conn.commit()

print("All operations completed. Now starting cleanup.")
cursor.execute("VACUUM")
conn.commit()
