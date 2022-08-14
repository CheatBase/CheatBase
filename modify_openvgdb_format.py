# This program modifies the openvgdb.sqlite database to use foreign keys when referencing ids from other tables.
# Future development: abstract column names so all data is copied without naming each column
# Copyright Noah Keck - All Rights Reserved

import sqlite3
import shutil

shutil.copy("openvgdb.sqlite", "cheatbase.sqlite")

conn = sqlite3.connect("cheatbase.sqlite")
cursor = conn.cursor()

def alter_orig_tables():
	# Add foreign key association to ROMs

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
			lastModified DATETIME NOT NULL DEFAULT (datetime('now')),
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
	cursor.execute("ALTER TABLE ROMs_dg_tmp RENAME TO ROMS")

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
			lastModified DATETIME NOT NULL DEFAULT (datetime('now')),
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

	# The next two tables only need a single column added, so technically an alter table statement would suffice
	# but I decided that it would be good to have the query to create the table stored here anyways

	# Add lastModified to SYSTEMS
	query = """
		CREATE TABLE SYSTEMS_dg_tmp (
			systemID INTEGER
				PRIMARY KEY AUTOINCREMENT,
			systemName TEXT NOT NULL, 
			systemShortName TEXT NOT NULL, 
			systemHeaderSizeBytes INTEGER, 
			systemHashless INTEGER, 
			systemHeader INTEGER, 
			systemSerial TEXT, 
			systemOEID TEXT,
			lastModified DATETIME NOT NULL DEFAULT (datetime('now'))
		)
	"""
	cursor.execute(query)
	query = """
		INSERT INTO SYSTEMS_dg_tmp(systemID, systemName, systemShortName, systemHeaderSizeBytes, systemHashless, systemHeader, systemSerial, systemOEID)
		SELECT systemID, systemName, systemShortName, systemHeaderSizeBytes, systemHashless, systemHeader, systemSerial, systemOEID
		FROM SYSTEMS
	"""
	cursor.execute(query)
	cursor.execute("DROP TABLE SYSTEMS")
	cursor.execute("ALTER TABLE SYSTEMS_dg_tmp RENAME TO SYSTEMS")

	# Add lastModified to REGIONS
	query = """
		CREATE TABLE REGIONS_dg_tmp (
			regionID INTEGER
				PRIMARY KEY AUTOINCREMENT,
			regionName TEXT NOT NULL, 
			lastModified DATETIME NOT NULL DEFAULT (datetime('now'))
		)
	"""
	cursor.execute(query)
	query = """
		INSERT INTO REGIONS_dg_tmp(regionID, regionName)
		SELECT regionID, regionName
		FROM REGIONS
	"""
	cursor.execute(query)
	cursor.execute("DROP TABLE REGIONS")
	cursor.execute("ALTER TABLE REGIONS_dg_tmp RENAME TO REGIONS")

def add_cheat_tables():
	# drop the tables if somehow they exist
	cursor.executescript("DROP TABLE IF EXISTS CHEATS; DROP TABLE IF EXISTS CHEAT_DEVICES; DROP TABLE IF EXISTS CHEAT_CATEGORIES")

	query = """
		CREATE TABLE CHEAT_DEVICES (
			cheatDeviceID INTEGER
				PRIMARY KEY AUTOINCREMENT,
			systemID INTEGER NOT NULL,
			cheatDeviceName TEXT NOT NULL,
			cheatDeviceBrandName TEXT,
			cheatDeviceFormat TEXT,
			lastModified DATETIME NOT NULL DEFAULT (datetime('now')),
			FOREIGN KEY (systemID)
				REFERENCES SYSTEMS (systemID)
				ON UPDATE CASCADE
				ON DELETE RESTRICT
		)
	"""
	cursor.execute(query)
	query = """
		CREATE TABLE CHEAT_CATEGORIES (
			cheatCategoryID INTEGER
				PRIMARY KEY AUTOINCREMENT,
			cheatCategory TEXT NOT NULL,
			cheatCategoryDescription TEXT,
			lastModified DATETIME NOT NULL DEFAULT (datetime('now'))
		)
	"""
	cursor.execute(query)
	query = """
		CREATE TABLE CHEATS (
			cheatID INTEGER
				PRIMARY KEY AUTOINCREMENT,
			romID INTEGER NOT NULL,
			cheatName TEXT NOT NULL,
			cheatActivation TEXT,
			cheatDescription TEXT,
			cheatSideEffect TEXT,
			cheatFolderName TEXT,
			cheatCategoryID INTEGER NOT NULL,
			cheatCode TEXT NOT NULL,
			cheatDeviceID INTEGER NOT NULL,
			cheatCredit TEXT,
			lastModified DATETIME NOT NULL DEFAULT (datetime('now')),
			FOREIGN KEY (romID)
				REFERENCES ROMs (romID)
				ON UPDATE CASCADE
				ON DELETE RESTRICT
			FOREIGN KEY (cheatCategoryID)
				REFERENCES CHEAT_CATEGORIES (cheatCategoryID)
				ON UPDATE CASCADE
				ON DELETE RESTRICT
			FOREIGN KEY (cheatDeviceID)
				REFERENCES CHEAT_DEVICES (cheatDeviceID)
				ON UPDATE CASCADE
				ON DELETE RESTRICT
		)
	"""
	cursor.execute(query)

def add_modified_triggers():
	# These triggers will make sure that the lastModified is automatically updated 
	# whenever an update occurs, and only if the time is older than 3 seconds ago

	for tbl in [("CHEAT_CATEGORIES", "cheatCategoryID"), ("CHEAT_DEVICES", "cheatDeviceID"), ("CHEATS", "cheatID"), ("REGIONS", "regionID"), ("RELEASES", "releaseID"), ("ROMS", "romID"), ("SYSTEMS", "systemID")]:
		query = """
			CREATE TRIGGER update_{tableName}_lastModified_trigger
				AFTER UPDATE ON {tableName}
					WHEN datetime('now') > datetime(NEW.lastModified, '+3.0 seconds')
				BEGIN
					UPDATE {tableName} SET lastModified = datetime('now') WHERE {tableID} = NEW.{tableID};
				END;
		""".format(tableName=tbl[0], tableID=tbl[1])
		cursor.execute(query)

def addMissingRoms():
	print("Now adding random missing ROM and RELEASE entries.")
	# Starting with the ROMs
	query = """
		INSERT INTO ROMS (romID, systemID, regionID, romHashCRC, romHashMD5, romHashSHA1, romSize, romFileName, romExtensionlessFileName, romParent, romSerial, romLanguage, romDumpSource)
		VALUES
  			(86150,24,4,'CDF33AD4','58DDFF08BA51075CAF7556EDB7DD5B3B','C9A6F28D3C356810A8D2DF48C540A48A0B80263D',67108864,'007 - Blood Stone (Canada).nds','007 - Blood Stone (Canada)',:null,'BJBX','French','No-Intro'),
  			(86151,24,4,'9731CA72','77F6A9EE5FB0E8C21B74B4A51E1557B7','7EA1FDFE27EBB5C322BE620EB0938FA6E5AB07C1',67108864,'Call of Duty - Black Ops (Canada).nds','Call of Duty - Black Ops (Canada)',:null,'BDYX','French','No-Intro'),
			(86152,24,21,'5751B16B','6766329199537C8035107AC0A901A894','420175FD7901AD3206FE4FD9AD95160C3DE1890A',67108864,'Cats & Dogs - The Revenge of Kitty Galore (USA) (En,Fr,Es).nds','Cats & Dogs - The Revenge of Kitty Galore (USA) (En,Fr,Es)','Cats & Dogs - The Revenge of Kitty Galore - The Videogame (Europe) (En,Fr,De,Es,It,Nl)','BD3E','English/French/Spanish','No-Intro'),
			(86153,24,12,'8E0044A4','E6712F080B391012A49517D1290C81E4','1C104F907950454E815B460345C4B80FD68F1EE2',134217728,'Impara con Pokemon - Avventura Tra i Tasti (Italy).nds','Impara con Pokemon - Avventura Tra i Tasti (Italy)','Learn with Pokemon - Typing Adventure (Europe)','UZPI','Italian','No-Intro'),
   			(86154,24,10,'7641BF1B','595080ADF211F6054A83D363243D326D','D26690A6F9FE81AFC81008818B0E50F0ED2D6C35',134217728,'Lernen mit Pokemon - Tasten-Abenteuer (Germany).nds','Lernen mit Pokemon - Tasten-Abenteuer (Germany)','Learn with Pokemon - Typing Adventure (Europe)','UZPD','German','No-Intro'),
			(86155,24,21,'D5EC81A9','126A96C88A73724EEB3A0C7E19AFD72C','18962DD520DA5DF114A97F334C1F6A6A3A2E5250',67108864,'x107 - Pokemon - Diamond Version + Pokemon - Pearl Version (USA) (Demo) (Kiosk).nds','x107 - Pokemon - Diamond Version + Pokemon - Pearl Version (USA) (Demo) (Kiosk)',:null,'Y23E','English','No-Intro')

	"""
	cursor.execute(query, {'null':None})	

	# Now adding the releases
	query = """
		INSERT INTO RELEASES (romID, releaseTitleName, regionLocalizedID, releaseDate)
		VALUES 
  			(86150,'007: Blood Stone',4,:null),
			(86151,'Call of Duty: Black Ops',4,:null),
			(86152,'Cats & Dogs - The Revenge of Kitty Galore',21,:null),
   			(86153,'Impara con Pokemon - Avventura Tra i Tasti',12,:null),
      		(86154,'Lernen mit Pokemon - Tasten-Abenteuer',10,:null),
        	(86155,'Pokemon - Diamond Version + Pokemon - Pearl Version (Demo) (Kiosk)',21, 'March 2007')
	"""
	cursor.execute(query, {'null':None})

try:
	print("Adding foreign key associations to these tables: ROMS, RELEASES. Additionally adding the lastModified col to all tables.")
	alter_orig_tables()
	print("Adding new cheat related tables: CHEATS, CHEAT_DEVICES, CHEAT_CATEGORIES.")
	add_cheat_tables()
	print("Creating lastModified triggers.")
	add_modified_triggers()
	print("Adding missing ROMS and RELEASE data.")
	addMissingRoms() # written as a separate function to allow it to be commented out
	conn.commit()
	print("Program successful.")
except sqlite3.DatabaseError as err:
    print(f"{type(err).__name__}: {str(err)}")
    print("Rolling back changes. Program unsuccessful.")
    conn.rollback()
finally:
	print("Now starting cleanup.")
	cursor.execute("VACUUM")
	conn.commit()
	conn.close()
	print("Cleanup completed.")
