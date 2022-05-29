# This program queries the openvgdb.sqlite database and creates a directory with raw csv data.
# Copyright Noah Keck - All Rights Reserved

import numpy as np
import pandas as pd
import sqlite3
from pathlib import Path

# Create directories
dir = Path().resolve()
for folder in ["cheats", "covers", "metadata", "releases", "roms"]:
    Path(str(dir) + "/raw_data/" + folder).mkdir(parents=True, exist_ok=True)

# Setup database connection
conn = sqlite3.connect("openvgdb.sqlite")
cursor = conn.cursor()

# Start exporting data
for table in ["systems", "regions", "cheat_devices", "cheat_categories"]:
    cursor.execute("SELECT * FROM " + table.upper())
    headers = list(map(lambda x: x[0], cursor.description))
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=headers)
    df.to_csv(str(dir) + "/raw_data/{}.csv".format(table.lower()), index=False, encoding="utf-8")

# Get just systemID and short name for processing data that is separated by system
cursor.execute("SELECT systemID, systemShortName FROM SYSTEMS")
systems = cursor.fetchall()
for system in systems:
    # covers
    query = """
        SELECT releaseTitleName, regionName, releaseCoverFront, releaseCoverBack, releaseReferenceURL
        FROM RELEASES
        LEFT JOIN REGIONS
            ON RELEASES.regionLocalizedID = REGIONS.regionID
        WHERE romID in (SELECT romID FROM ROMs WHERE systemID = {sysID})
        ORDER BY 1
    """.format(sysID = system[0])
    cursor.execute(query)
    headers = ("Title", "CoverRegionName", "CoverFrontURL", "CoverBackURL", "ReferenceURL")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(str(dir) + "/raw_data/covers/" + system[1] + ".csv", index=False, encoding="utf-8")

    # metadata
    query = """
        SELECT releaseTitleName, regionName, releaseGenre, releaseDescription, releaseDeveloper, releasePublisher, releaseDate, releaseReferenceURL
        FROM RELEASES
        LEFT JOIN REGIONS
            ON RELEASES.regionLocalizedID = REGIONS.regionID
        WHERE romID in (SELECT romID FROM ROMs WHERE systemID = {sysID})
        ORDER BY 1
    """.format(sysID = system[0])
    cursor.execute(query)
    headers = ("Title", "Region", "Genres", "Description", "Developer", "Publisher", "ReleaseDate", "ReferenceURL")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(str(dir) + "/raw_data/metadata/" + system[1] + ".csv", index=False, encoding="utf-8")

    # releases (doesn't include releaseID or TEMP columns)
    cursor.execute("SELECT romID, releaseTitleName, regionLocalizedID, releaseCoverFront, releaseCoverBack, releaseCoverCart, releaseCoverDisc, releaseDescription, releaseDeveloper, releasePublisher, releaseGenre, releaseDate, releaseReferenceURL, releaseReferenceImageURL FROM RELEASES WHERE romID in (SELECT romID FROM ROMs WHERE systemID = {sysID})".format(sysID = system[0]))
    headers = list(map(lambda x: x[0], cursor.description))
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(str(dir) + "/raw_data/releases/" + system[1] + ".csv", index=False, encoding="utf-8")

    # roms (doesn't include TEMP columns)
    cursor.execute("SELECT romID, systemID, regionID, romHashCRC, romHashMD5, romHashSHA1, romSize, romFileName, romExtensionlessFileName, romParent, romSerial, romHeader, romLanguage, romDumpSource FROM ROMs WHERE systemID = {sysID}".format(sysID = system[0]))
    headers = list(map(lambda x: x[0], cursor.description))
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(str(dir) + "/raw_data/roms/" + system[1] + ".csv", index=False, encoding="utf-8")

    # cheats (doesn't include cheatID)
    cursor.execute("SELECT romID, cheatName, cheatActivation, cheatDescription, cheatSideEffect, cheatFolderName, cheatCategoryID, cheatCode, cheatDeviceID, cheatCredit FROM CHEATS WHERE romID in (SELECT romID FROM ROMs WHERE systemID = {sysID})".format(sysID = system[0]))
    headers = list(map(lambda x: x[0], cursor.description))
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(str(dir) + "/raw_data/cheats/" + system[1] + ".csv", index=False, encoding="utf-8")
