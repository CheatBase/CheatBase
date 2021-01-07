# This program queries the openvgdb.sqlite database and creates a directory with raw csv data.
# Copyright Noah Keck - All Rights Reserved

import numpy as np
import sqlite3
from pathlib import Path

# Builds a list of format strings to determine whether quotations are needed
def detect_fmt(data: list) -> list:
    fmt = [None] * len(data[0])
    for row in data: # check every row and every column, not efficient but saves space in the csv
        for i, val in enumerate(row):
            if fmt[i] is None and isinstance(val, str) and "," in val:
                # Detects to see if a comma is present
                fmt[i] = "\"%s\""
    for i, temp in enumerate(fmt):
        if temp is None:
            fmt[i] = "%s"
    return fmt

# Create directories
dir = Path().resolve()
for folder in ["cheats", "covers", "metadata", "releases"]:
    Path(str(dir) + "/raw_data/" + folder).mkdir(parents=True, exist_ok=True)

# Setup database connection
conn = sqlite3.connect("openvgdb.sqlite")
cursor = conn.cursor()

# Start exporting data
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
    fmt="%s"
    if not data:
        data = [headers]
    else:
        fmt = detect_fmt(data)
        data = np.vstack(([headers], data))
    np.savetxt(str(dir) + "/raw_data/covers/" + system[1] + ".csv", data, delimiter=',', fmt=fmt, encoding="utf-8")

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
    fmt="%s"
    if not data:
        data = [headers]
    else:
        fmt = detect_fmt(data)
        data = np.vstack(([headers], data))
    np.savetxt(str(dir) + "/raw_data/metadata/" + system[1] + ".csv", data, delimiter=',', fmt=fmt, encoding="utf-8")

    # releases
    cursor.execute("SELECT * FROM RELEASES WHERE romID in (SELECT romID FROM ROMs WHERE systemID = {sysID})".format(sysID = system[0]))
    headers = list(map(lambda x: x[0], cursor.description))
    data = cursor.fetchall()
    fmt = "%s"
    if not data:
        data = [headers]
    else:
        fmt = detect_fmt(data)
        data = np.vstack(([headers], data))
    np.savetxt(str(dir) + "/raw_data/releases/" + system[1] + ".csv", data, delimiter=',', fmt=fmt, encoding="utf-8")
