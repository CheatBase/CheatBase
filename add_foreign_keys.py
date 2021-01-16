# This program modifies the openvgdb.sqlite database to use foreign keys when referencing ids from other tables.
# Future development: abstract column names so all data is copied without naming each column
# Copyright Noah Keck - All Rights Reserved

import sqlite3

conn = sqlite3.connect("openvgdb.sqlite")
cursor = conn.cursor()

# Add foreign key association to ROMs
print("Adding foreign key associations to these tables: ROMs, RELEASES.")
cursor.executescript("DROP TABLE IF EXISTS ROMs_dg_tmp; DROP TABLE IF EXISTS RELEASES_dg_tmp") # drop temp tables if they exist (for some strange reason)
query = """
    CREATE TABLE ROMs_dg_tmp (
    	romID INTEGER
    		PRIMARY KEY AUTOINCREMENT,
    	systemID INTEGER NOT NULL,
    	regionID INTEGER NOT NULL,
    	romHashCRC TEXT,
    	romHashMD5 TEXT,
    	romHashSHA1 TEXT,
    	romSize INTEGER,
    	romFileName TEXT NOT NULL,
    	romExtensionlessFileName TEXT NOT NULL,
    	romParent TEXT,
    	romSerial TEXT,
    	romHeader TEXT,
    	romLanguage TEXT,
    	romDumpSource TEXT NOT NULL,
    	FOREIGN KEY (systemID)
            REFERENCES SYSTEMS (systemID)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
        FOREIGN KEY (regionID)
            REFERENCES REGIONS (regionID)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
    )
"""
cursor.execute(query)
query = """
    INSERT INTO ROMs_dg_tmp(romID, systemID, regionID, romHashCRC, romHashMD5, romHashSHA1, romSize, romFileName, romExtensionlessFileName, romParent, romSerial, romHeader, romLanguage, romDumpSource)
    SELECT romID, systemID, regionID, romHashCRC, romHashMD5, romHashSHA1, romSize, romFileName, romExtensionlessFileName, romParent, romSerial, romHeader, romLanguage, romDumpSource
    FROM ROMs
"""
cursor.execute(query)
cursor.execute("DROP TABLE ROMs")
cursor.execute("ALTER TABLE ROMs_dg_tmp RENAME TO ROMs")

# Add foreign key association to RELEASES
query = """
    CREATE TABLE RELEASES_dg_tmp (
    	releaseID INTEGER
    		PRIMARY KEY AUTOINCREMENT,
    	romID INTEGER NOT NULL,
    	releaseTitleName TEXT NOT NULL,
    	regionLocalizedID INTEGER NOT NULL,
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
            ON DELETE RESTRICT
    )
"""
cursor.execute(query)
query = """
    INSERT INTO RELEASES_dg_tmp(releaseID, romID, releaseTitleName, regionLocalizedID, releaseCoverFront, releaseCoverBack, releaseCoverCart, releaseCoverDisc, releaseDescription, releaseDeveloper, releasePublisher, releaseGenre, releaseDate, releaseReferenceURL, releaseReferenceImageURL)
    SELECT releaseID, romID, releaseTitleName, regionLocalizedID, releaseCoverFront, releaseCoverBack, releaseCoverCart, releaseCoverDisc, releaseDescription, releaseDeveloper, releasePublisher, releaseGenre, releaseDate, releaseReferenceURL, releaseReferenceImageURL
    FROM RELEASES
"""
cursor.execute(query)
cursor.execute("DROP TABLE RELEASES")
cursor.execute("ALTER TABLE RELEASES_dg_tmp RENAME TO RELEASES")
conn.commit()
print("Foreign key associations added. Now starting cleanup.")
cursor.execute("VACUUM")
conn.commit()
print("Cleanup completed.")
