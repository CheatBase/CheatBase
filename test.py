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
