# Welcome to CheatBase!

Here, you will find a plethora of working cheat codes for any number of retro gaming consoles.

## About the cheats in the database

The cheats in this database are each manually assigned a category and sometimes a cheat folder name according to a very specific set of guidelines.

* Cheats only get a cheatFolderName if they meet one of the following conditions:
  * They only apply to a "minigame" found within the ROM. This is most games that market themselves as "100-in-1" or "Minigame collection."
  * A large number of cheats have an identical effect/name with one a tiny difference. I only apply this rule if there are 3 or more "sets" and it would make more sense to the user if they were fully separated from each other.
* Cheat categories are designed to describe the "function" of the cheat.

## About the python scripts

### Setup

First, install Python 3.7.x or newer.

Then install the following packages:

```sh
pip install numpy
pip install pandas
```

### Usage

Running ``modify_openvgdb_format.py`` will rewrite all of the tables in the openvgdb.sqlite database to maintain the following characteristics:
* All foreign keys are programmed in and relationships are maintained. Updates to primary keys will cascade and deletion is restricted as long as the key has a row dependent on it.
* Columns that must have values for the data to be sufficiently complete, are enforced with ``NOT NULL``
* TEMP columns are removed
* A ``lastModified`` column is added to every table
* Every table gets a built in trigger to automatically update the ``lastModified`` column


Running ``export_raw_data.py`` will pull all the data stored in the openvgdb.sqlite database and write it in csv form in the raw_data directory.
Take note of these details:
* The releaseID and cheatID aren't included in the corresponding csv files because there are no tables dependent on them
* The RELEASES and ROMs raw data does not include any of the TEMP column data (since that is all info you can find using more its foreign key relationships)
* The naming of the csv files for CHEATS, RELEASES, and ROMs corresponds to the systemShortName found using their systemID
  * And it's extremely important that they keep this exact name, because that's what ``parse_raw_data.py`` uses to load them

Running ``parse_raw_data.py`` will load all the csv files stored in the raw_data directory and overwrite the tables in the openvgdb.sqlite database with that data.
Essentially, this program is the opposite of ``export_raw_data.py`` and expects the details of that export, to remain true.

You can also specify that the program should 'organize' the data, in which case it will take care of sorting the columns and then cascading primary key changes to the tables that use them.
You can comment out any of the parse method calls, but if you organize a table that has other tables that depend on that primary key, you **must** parse those tables as well.

Additionally, you can specify that the contents should parsed to only add new entries instead of fully overwriting. Note that this is not compatible with organizing the tables.
