# This program modifies the openvgdb.sqlite database to use foreign keys when referencing ids from other tables.
# Future development: abstract column names so all data is copied without naming each column
# Copyright Noah Keck - All Rights Reserved

import sqlite3

conn = sqlite3.connect("openvgdb.sqlite")
cursor = conn.cursor()

# Add foreign key association to ROMs
print("Adding foreign key associations to these tables: ROMs, RELEASES.")
cursor.execute("DROP TABLE IF EXISTS ROMs_dg_tmp, RELEASES_dg_tmp") # drop temp tables if they exist (for some strange reason)
query = """
    create table ROMs_dg_tmp (
    	romID INTEGER
    		primary key autoincrement,
    	systemID INTEGER,
    	regionID INTEGER,
    	romHashCRC TEXT,
    	romHashMD5 TEXT,
    	romHashSHA1 TEXT,
    	romSize INTEGER,
    	romFileName TEXT,
    	romExtensionlessFileName TEXT,
    	romParent TEXT,
    	romSerial TEXT,
    	romHeader TEXT,
    	romLanguage TEXT,
    	TEMPromRegion TEXT,
    	romDumpSource TEXT,
    	FOREIGN KEY (systemID)
            REFERENCES SYSTEMS (systemID)
            ON UPDATE CASCADE
            ON DELETE SET NULL
        FOREIGN KEY (regionID)
            REFERENCES REGIONS (regionID)
            ON UPDATE CASCADE
            ON DELETE SET NULL
    )
"""
cursor.execute(query)
query = """
    insert into ROMs_dg_tmp(romID, systemID, regionID, romHashCRC, romHashMD5, romHashSHA1, romSize, romFileName, romExtensionlessFileName, romParent, romSerial, romHeader, romLanguage, TEMPromRegion, romDumpSource) select romID, systemID, regionID, romHashCRC, romHashMD5, romHashSHA1, romSize, romFileName, romExtensionlessFileName, romParent, romSerial, romHeader, romLanguage, TEMPromRegion, romDumpSource from ROMs
"""
cursor.execute(query)
cursor.execute("drop table ROMs")
cursor.execute("alter table ROMs_dg_tmp rename to ROMs")

# Add foreign key association to RELEASES
query = """
    create table RELEASES_dg_tmp (
    	releaseID INTEGER
    		primary key autoincrement,
    	romID INTEGER,
    	releaseTitleName TEXT,
    	regionLocalizedID INTEGER,
    	TEMPregionLocalizedName TEXT,
    	TEMPsystemShortName TEXT,
    	TEMPsystemName TEXT,
    	releaseCoverFront TEXT,
    	releaseCoverBack TEXT,
    	releaseCoverCart TEXT,
    	releaseCoverDisc TEXT,
    	releaseDescription TEXT,
    	releaseDeveloper TEXT,
    	releasePublisher TEXT,
    	releaseGenre TEXT,
    	releaseDate TEXT,
    	releaseReferenceURL TEXT,
    	releaseReferenceImageURL TEXT,
    	FOREIGN KEY (romID)
            REFERENCES ROMs (romID)
            ON UPDATE CASCADE
            ON DELETE SET NULL
    )
"""
cursor.execute(query)
query = """
    insert into RELEASES_dg_tmp(releaseID, romID, releaseTitleName, regionLocalizedID, TEMPregionLocalizedName, TEMPsystemShortName, TEMPsystemName, releaseCoverFront, releaseCoverBack, releaseCoverCart, releaseCoverDisc, releaseDescription, releaseDeveloper, releasePublisher, releaseGenre, releaseDate, releaseReferenceURL, releaseReferenceImageURL) select releaseID, romID, releaseTitleName, regionLocalizedID, TEMPregionLocalizedName, TEMPsystemShortName, TEMPsystemName, releaseCoverFront, releaseCoverBack, releaseCoverCart, releaseCoverDisc, releaseDescription, releaseDeveloper, releasePublisher, releaseGenre, releaseDate, releaseReferenceURL, releaseReferenceImageURL from RELEASES
"""
cursor.execute(query)
cursor.execute("drop table RELEASES")
cursor.execute("alter table RELEASES_dg_tmp rename to RELEASES")
conn.commit()
print("Foreign key associations added. Now starting cleanup.")
cursor.execute("VACUUM")
conn.commit()
print("Cleanup completed.")
