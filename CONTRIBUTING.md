# First of all, welcome to CheatBase!

Take a look at the README to understand a little more about what the goal of this project is and how to use the files included in the repo.

This article is mostly to explain the setup of the database and how you can submit cheats that fit the format.

## Database table names

| Table Name       | Table Description                                                                           |
|------------------|---------------------------------------------------------------------------------------------|
| ROMS             | The (mostly) complete list of ROMs for every supported system and its technical details.    |
| RELEASES         | The release info related to a single ROM including cover image, region, and developer data. |
| REGIONS          | A list of every release region which can include a single or multiple countries.            |
| SYSTEMS          | A list of the supported consoles and handhelds and their technical details.                 |
| CHEATS           | The list of cheat codes, their related data, and their usage.                               |
| CHEAT_DEVICES    | The list of various devices that cheat codes were written for.                              |
| CHEAT_CATEGORIES | A working list of the types of functions that cheat codes implement.                        |

## CHEATS table columns explained

### **cheatID**

### **romID**

### **cheatName**

The **cheatName** should describe the function of the cheat as clearly as possible without exceeding more than 7 or so words. Anything more than that can be saved for the **cheatDescription** to more fully describe the cheat's function.

Ideally, you should be able to read a **cheatName** and know exactly what the cheat does while remaining 50 chars or less.

### **cheatActivation**

Describes a series of buttons that or singular button that when pressed or held, activates the cheat codes function in game. Examples: "Press Select+Down to activate." and "Press and hold Select to activate."

If there are specific instances in which the cheat can only be activated, this is also written here. For example, "Press and hold Select while warping to activate." and "Pass through a door to activate."

### **cheatDescription**

### **cheatSideEffect**

Sometimes cheats can have a side effect that bugs out the game or have a scenario where the code should NOT be used or there may be consequences. It can also include mentions of other cheats that should not be simultaneously active. Example: "Enemies are able to kill themselves." and "Don't use this code inside."

### **cheatFolderName**

This column should be used *extremely* sparingly. The idea is that this should be used only when there are a great number of cheats that need to be separated in a custom category of their own. This should be most commonly used for ROMs with lots of "minigames" in one.

It can also be used in scenarios where the same cheat name should be used for **4 or more** cheats, but the target of the cheat is slightly different. So instead of writing the cheat names as "Squad 1: Infinite Ammo", "Squad 2: Infinite Ammo", etc. Instead use the ``cheatFolderName`` column to define which "Squad" the cheat will apply to.

### **cheatCategoryID**

This is by far the most complex aspect of the table design. This ID just links to a name and description from the ``CHEAT_CATEGORIES`` table.

Cheat categories exist to describe the **function** of the cheat. Meaning, what does the cheat provide for the player that uses it. For example, one of the most commonly used cheat categories is "Infinite Quantity". It applies to every cheat that has the sole purpose of giving the player an infinite quantity of items or an infinite amount of character stats (ie. Infinite Health).

If the function of the cheat doesn't quite match any of the existing categories, it is perfectly within reason to create a new one. Often when choosing the category, it will be fairly obvious as certain keywords in the **cheatName** will match the **cheatCategory** name.

### **cheatCode**

Proper spacing of the code should be included as shown by the relevant ``cheatDeviceFormat``.

### **cheatDeviceID**

### **cheatCredit**

This is a name or username field that whoever supplies / created the cheat gets to populate!

## How to submit contributions

The best way to add to the database, is by submitting csv files that contain all the additions made to the cheat database. I will need to also have any additional cheat categories or devices that may have been necessary to add. The most important aspect is making absolutely positive that the romID, cheatDeviceID, and cheatCategoryID all match the appropriate row.

Alternatively, you can commit directly to the SQL database. I will need to see a log of your changes or run a comparison test to create a changelog for review. 

Initial accuracy and consistency of the database is important as the cheat database develops, please keep this in mind when you submit contributions.

And finally, thanks for your help getting this project off the ground!

# Extended Documentation

## Database Table Names

| Table Name       | Table Description                                                                           |
|------------------|---------------------------------------------------------------------------------------------|
| ROMS             | The (mostly) complete list of ROMs for every supported system and its technical details.    |
| RELEASES         | The release info related to a single ROM including cover image, region, and developer data. |
| REGIONS          | A list of every release region which can include a single or multiple countries.            |
| SYSTEMS          | A list of the supported consoles and handhelds and their technical details.                 |
| CHEATS           | The list of cheat codes, their related data, and their usage.                               |
| CHEAT_DEVICES    | The list of various devices that cheat codes were written for.                              |
| CHEAT_CATEGORIES | A working list of the types of functions that cheat codes implement.                        |

## SQL Table Queries

### ROMS

```sql
CREATE TABLE ROMS (
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
);
```

### RELEASES

```sql
CREATE TABLE RELEASES (
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
);
```

### REGIONS

```sql
CREATE TABLE REGIONS (
	regionID INTEGER
		PRIMARY KEY AUTOINCREMENT,
	regionName TEXT NOT NULL, 
	lastModified DATETIME NOT NULL DEFAULT (datetime('now'))
);
```

### SYSTEMS

```sql
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
);
```

### CHEATS

```sql
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
);
```

### CHEAT_DEVICES

```sql
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
);
```

### CHEAT_CATEGORIES

```sql
CREATE TABLE CHEAT_CATEGORIES (
	cheatCategoryID INTEGER
		PRIMARY KEY AUTOINCREMENT,
	cheatCategory TEXT NOT NULL,
	cheatCategoryDescription TEXT,
	lastModified DATETIME NOT NULL DEFAULT (datetime('now'))
);
```

## SQL Triggers

Just as every table already has defined triggers for updates on foreign keys, there is also a custom trigger that applies to every table. The purpose of this trigger is to keep the `lastModified` column populated whenever the row is updated.

```sql
CREATE TRIGGER update_CHEATS_lastModified_trigger
	AFTER UPDATE ON CHEATS
		WHEN datetime('now') > datetime(NEW.lastModified, '+3.0 seconds')
	BEGIN
		UPDATE CHEATS SET lastModified = datetime('now') WHERE cheatID = NEW.cheatID;
	END;
```

The trigger occurs on an update to **any** column of the row, which includes the `lastModified` column itself. Which is why the WHEN condition ensures that the previously recorded timestamp is not within the last 3 seconds. This prevents the endless loop of updates from occurring.
