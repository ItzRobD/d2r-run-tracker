<<<<<<< HEAD
# Diablo 2 Resurrected Run Tracker

## Contents
=======
<<<<<<< HEAD
# Diablo 2 Resurrected Run Tracker

## Contents


1. Description
2. Using the tracker  
2.1 Terms used  
2.2 New Session  
2.3 Main Window  
2.4 File Structure  
=======
--------------------------------------
== Diablo 2 Resurrected Run Tracker ==
--------------------------------------
>>>>>>> main


1. Description
<<<<<<< HEAD
2. Using the tracker  
2.1 Terms used  
2.2 New Session  
2.3 Main Window  
2.4 File Structure  
=======
2. Using the tracker
2.1 Terms used
2.2 New Session
2.3 Main Window
2.4 File Structure
>>>>>>> main
>>>>>>> main
3. Contributions / Community / Support
4. Credits


<<<<<<< HEAD
#### 1. Description

=======
<<<<<<< HEAD
#### 1. Description

=======
--------------
1. Description
--------------
>>>>>>> main
>>>>>>> main
D2R Run Tracker is a program to track your magic find progress through various runs. It supports unique, set, and rune items. It can also be used to generate a rudimentary report.
This program was developed in my spare time and as such I can not devote a professional amount of time to its support but
bug reports and suggestions will be appreciated. Suggestions will be taken into consideration. Bug reports will be addressed
as time allows.

<<<<<<< HEAD

#### 2. Using the tracker


##### 2.1 Terms used
--------
=======
<<<<<<< HEAD

#### 2. Using the tracker


##### 2.1 Terms used
--------
=======
--------------------
2. Using the tracker
--------------------

2.1 Terms used
--------------
>>>>>>> main
>>>>>>> main

Run: A run consists of a single game creation. Every time you create a new game this is considered a new run.
Session: A session is a collection of runs. This can be up to your descrition but an example would be every new day or you can 		 	 create a new session after leveling, etc.

<<<<<<< HEAD
##### 2.2 New session
--------
=======
<<<<<<< HEAD
##### 2.2 New session
--------

Upon launch you'll be prompted to choose a session name. The session name cannot be changed once it's set. It is associated with the save files and report file. The default session name is the current date. If the selected session name is already in use the following number will be appended to the end of the name.
 
##### 2.3 Main Window
--------

Interface description:

	* Session Info Group
		* Session Name - Name of the current session - Cannot be changed
		* Players - Number of players in the game during this run
		* Difficulty - Difficulty of the current run
		* Run number - Current run number - cannot be modified, managed by the program
	* Character Info Group
		* Class - Your character's class during the current run
		* Level - Your character's level during the current run
		* MF - Your character's magic find stat during the current run
	* Item Group
		* Type - Unique/Set/Rune - This option will populate the Item drop down box
		* Item - The name of the item you wish to add to the list
		* Quantity - Quantity of the selected item that has been found during a drop
		* Ethereal - Checkbox to indicated whether the selected item is ethereal
		* Add Item - When your item type, item, quantity, and ethereal checkbox have been properly selected clicking add item will
				   add it to the items found list
	* Completions group
		* Checkboxes are listed to indicate popular farming areas and monsters. Each completion has a shorthand listed within 		parentheses
	* Items Found Table
		* Items added will populate this table
	* Lower buttons
		* Remove item - When a row in the Items Found table is selected this button will remove that item from the list. If no row is selected then it will remove the last item added
		* Run Completed - When you finish a run click this button to increment the run number counter. This also saves an encoded 						backup of the current session (see: file structure)
		* Generate Report - Used to generate a report in the form of a text file (see: file structure)
		* Complete Session - When your session is complete click this button to save the session information as a cleartext json file (see: file structure) This action will warn you that doing so will clear the current found item list and delete all run backups. You'll then be asked to create a new session
					
Menu bar description:

	* File > New Session - Create a new session
	* File > Restore Backup - Restore a previous set of runs from a .run file
	* File > Open Session - Opens a previously saved session file from a .json file
	* File > Exit - Closes the program
	
	* Current Session > Complete Session - Performs the same action as the Complete Session button
	* Current Session > Generate Report - Performs the same action as the Generate Report button
	
	* Help > Manual > Opens a web browser to the manual page
	* Help > About > Displays program and version information
	
##### 2.4 File Structure
--------

* Base Directory
	* tracker.log - Contains log data and crash information. Please submit this with any bug or crash reports. File is
		      overwritten whenever the program is opened
* Base Directory/saved
	* Base Directory/saved/runs	
		* Upon completing a run the information will be saved in this folder using the session name and the .run file extension. This file is encoded to prevent modification which would corrupt the backup and prevent restoration
	* Base Directory/saved/sessions
		* Upon completing a session the information will be saved in this folder using the session name and the .json file extension. This file is saved in clear text to allow users to view their results or generate their own reports.
		* Note: When a session is completed the associated .run backup files are deleted to prevent accumulation of useless files

* Base Directory/reports
	* Upon generating a report the information will be placed into a table saved here using the session name and the .txt file extension
		
Note: Future updates of the program may now allow the use of save data from previous versions. If it is not compatible you will be prompted upon trying to load the file.

--------

#### 3. Contributions / Community / Support


The program is being distributed under the GPL 3 License. The source code is available on github located at  
	https://github.com/ItzRobD/d2r-run-tracker  
Any use of the source code must adhere to the GPL 3 License.
The program was developed entirely using Python

* Discord:
	* https://discord.gg/9DSuxWC5KT
* Support emails:
	* Author: itzrobd@slashquitgaming.com
	* Bug reporting: d2r-tracker-bugs@slashquitgaming.com
	* Suggestions: d2r-tracker-suggestions@slashquitgaming.com
	
**_When submitting a crash or bug report please include the tracker.log file contained within the base directory_**

--------

#### 4. Credits


* Author: ItzRobD (Rob Durst)
* Special thanks to ItzDono for testing this and finding all my dumb mistakes

--------

Copyright (C) 2021 - Rob Durst
This file is a part of D2R Run Tracker

D2R Run Tracker is free software. You may redistribute and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation, either
as version 3 of the License, or (at your option) any later version. See the 
GNU General Public License for more details.

D2R Run Tracker is being distributed in the hope that it will be useful and helpful
for Diablo 2 Resurrected players but WITHOUT ANY WARRANTY. This software is NOT
supported by Blizzard Entertainment in any way. This software does NOT interact
 with any other software of game engines and requires manual input
=======
2.2 New session
---------------
>>>>>>> main

Upon launch you'll be prompted to choose a session name. The session name cannot be changed once it's set. It is associated with the save files and report file. The default session name is the current date. If the selected session name is already in use the following number will be appended to the end of the name.
 
##### 2.3 Main Window
--------

Interface description:

	* Session Info Group
		* Session Name - Name of the current session - Cannot be changed
		* Players - Number of players in the game during this run
		* Difficulty - Difficulty of the current run
		* Run number - Current run number - cannot be modified, managed by the program
	* Character Info Group
		* Class - Your character's class during the current run
		* Level - Your character's level during the current run
		* MF - Your character's magic find stat during the current run
	* Item Group
		* Type - Unique/Set/Rune - This option will populate the Item drop down box
		* Item - The name of the item you wish to add to the list
		* Quantity - Quantity of the selected item that has been found during a drop
		* Ethereal - Checkbox to indicated whether the selected item is ethereal
		* Add Item - When your item type, item, quantity, and ethereal checkbox have been properly selected clicking add item will
				   add it to the items found list
	* Completions group
		* Checkboxes are listed to indicate popular farming areas and monsters. Each completion has a shorthand listed within 		parentheses
	* Items Found Table
		* Items added will populate this table
	* Lower buttons
		* Remove item - When a row in the Items Found table is selected this button will remove that item from the list. If no row is selected then it will remove the last item added
		* Run Completed - When you finish a run click this button to increment the run number counter. This also saves an encoded 						backup of the current session (see: file structure)
		* Generate Report - Used to generate a report in the form of a text file (see: file structure)
		* Complete Session - When your session is complete click this button to save the session information as a cleartext json file (see: file structure) This action will warn you that doing so will clear the current found item list and delete all run backups. You'll then be asked to create a new session
					
Menu bar description:

	* File > New Session - Create a new session
	* File > Restore Backup - Restore a previous set of runs from a .run file
	* File > Open Session - Opens a previously saved session file from a .json file
	* File > Exit - Closes the program
	
	* Current Session > Complete Session - Performs the same action as the Complete Session button
	* Current Session > Generate Report - Performs the same action as the Generate Report button
	
	* Help > Manual > Opens a web browser to the manual page
	* Help > About > Displays program and version information
	
##### 2.4 File Structure
--------

* Base Directory
	* tracker.log - Contains log data and crash information. Please submit this with any bug or crash reports. File is
		      overwritten whenever the program is opened
* Base Directory/saved
	* Base Directory/saved/runs	
		* Upon completing a run the information will be saved in this folder using the session name and the .run file extension. This file is encoded to prevent modification which would corrupt the backup and prevent restoration
	* Base Directory/saved/sessions
		* Upon completing a session the information will be saved in this folder using the session name and the .json file extension. This file is saved in clear text to allow users to view their results or generate their own reports.
		* Note: When a session is completed the associated .run backup files are deleted to prevent accumulation of useless files

* Base Directory/reports
	* Upon generating a report the information will be placed into a table saved here using the session name and the .txt file extension
		
Note: Future updates of the program may now allow the use of save data from previous versions. If it is not compatible you will be prompted upon trying to load the file.

--------

#### 3. Contributions / Community / Support


The program is being distributed under the GPL 3 License. The source code is available on github located at  
	https://github.com/ItzRobD/d2r-run-tracker  
Any use of the source code must adhere to the GPL 3 License.
The program was developed entirely using Python

* Discord:
	* https://discord.gg/9DSuxWC5KT
* Support emails:
	* Author: itzrobd@slashquitgaming.com
	* Bug reporting: d2r-tracker-bugs@slashquitgaming.com
	* Suggestions: d2r-tracker-suggestions@slashquitgaming.com
	
<<<<<<< HEAD
**_When submitting a crash or bug report please include the tracker.log file contained within the base directory_**

--------

#### 4. Credits


* Author: ItzRobD (Rob Durst)
* Special thanks to ItzDono for testing this and finding all my dumb mistakes

--------

Copyright (C) 2021 - Rob Durst
This file is a part of D2R Run Tracker

D2R Run Tracker is free software. You may redistribute and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation, either
as version 3 of the License, or (at your option) any later version. See the 
GNU General Public License for more details.

D2R Run Tracker is being distributed in the hope that it will be useful and helpful
for Diablo 2 Resurrected players but WITHOUT ANY WARRANTY. This software is NOT
supported by Blizzard Entertainment in any way. This software does NOT interact
 with any other software of game engines and requires manual input
=======
When submitting a crash or bug report please include the tracker.log file contained within the base directory
	
-------------
4. Credits
-------------

Author: ItzRobD (Rob Durst)
Special thanks to ItzDono for testing this and finding all my dumb mistakes

# Copyright (C) 2021 - Rob Durst
# This file is a part of D2R Run Tracker
#
# D2R Run Tracker is free software. You may redistribute and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either
# as version 3 of the License, or (at your option) any later version. See the 
# GNU General Public License for more details.
#
# D2R Run Tracker is being distributed in the hope that it will be useful and helpful
# for Diablo 2 Resurrected players but WITHOUT ANY WARRANTY. This software is NOT
# supported by Blizzard Entertainment in any way. This software does NOT interact
# with any other software of game engines and requires manual input
>>>>>>> main
>>>>>>> main
