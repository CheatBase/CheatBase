# First of all, welcome to CheatBase!

Take a look at the README to understand a little more about what the goal of this project is and how to use the files included in the repo.

This article is mostly to explain the setup of the database and how you can submit cheats that fit the format.

## Database table names

| Table Name       | Table Description                                                                           |
|------------------|---------------------------------------------------------------------------------------------|
| ROMs             | The (mostly) complete list of ROMs for every supported system and its technical details.    |
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

Ideally, you should be able to read a **cheatName** and know exactly what the cheat does.

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

This is by far the most complex aspect of the table design. This ID just links to a name and description from the ``cheatCategories`` table.

Cheat categories exist to describe the **function** of the cheat. Meaning, what does the cheat provide for the player that uses it. For example, one of the most commonly used cheat categories is "Infinite Quantity". It applies to every cheat that has the sole purpose of giving the player an infinite quantity of items or an infinite amount of character stats (ie. Infinite Health).

If the function of the cheat doesn't quite match any of the existing categories, it is perfectly within reason to create a new one.

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