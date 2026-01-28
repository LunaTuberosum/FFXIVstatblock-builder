# FFXIV TTRPG Stat Block Builder
### By: Luna Tuberosum


Welcome to the program version of the stat block creator. With this using a simple program you can make, customize, and save stat cards to be used in your next FFXIV TTRPG session. You can also export them as a PNG to send to friends.


Within this program there is an example stat sheet (collection of stat cards). This is there to help you understand what is all capable with this program and let you have an easy play ground to learn.


The example stat sheet is based of the ***Minstrel's Ballad: Lord of the Corpse Hall*** by TheVagueOne the FFXIV TTRPG Discord.

links:
* [Minstrel's Ballad: Lord of the Corpse Hall](docs.google.com/document/d/1LtJxy7w1lv_Khc6ugvk2rp1ocL3LZ8DtV0H8K9JPZ2Q/edit?usp=drive_web&ouid=114165381399485093355) by TheVagueOne

If you have any problems please message me on Discord. If you run into a bug please file a report here:

### [Bug Report Form](https://docs.google.com/forms/d/e/1FAIpQLSe2oN-zk-FwVziwDvbi-0u7zkWqfy7GP5lq9_YHEtNKTSROqg/viewform?usp=sf_link)


### **!! WARNING !!**
This current version **(0.93)** it has all the features necessary to make a stat card but may still be buggy and missing QOL features. 1.0 is comming but due to how long 0.93 took me it may take a bit. Please report all bugs and jank. Thank you

### **!! WARNING PT. 2 !!**
If you used this program prior to **Version 0.93** and are updating it. Please BACKUP your saves. The way saves work was changed and there for could cause corruption when the program tries to update them.

To backup your save do the following:

1. Go to the main directory of the program.
2. Duplicate the [saves] folder into another location.
3. Update the program
4. Run program.
5. If all goes well enjoy the update.
6. If the files are corrupt, drag a COPY of your old [saves] into the main directory and try again.
7. If it fails again, contact me.

### How to download


1. Click on the blue/green [<> Code] button in the top right.
2. Click [Download ZIP]
3. Unzip the file in another easy to reach folder.
4. Open the folder and run the EXE named **FFXIV Stat Card Builder**
5. (Optional) You can make a shortcut of this EXE by right clicking it and selecting [Create Shortcut]. **DO NOT** remove the EXE from the folder!
6. Enjoy :)

### How to update

1. Click on the blue/green [<> Code] button in the top right.
2. Click [Download ZIP]
3. Delete all file and folders from your original directory EXCEPT your [saves] folder. (Remember to back that folder up)
4. Extract update files into the directory.
5. Open the folder and run the EXE named **FFXIV Stat Card Builder**
6. (Optional) You can make a shortcut of this EXE by right clicking it and selecting [Create Shortcut]. **DO NOT** remove the EXE from the folder!
7. Enjoy :)


## Changelog
### Version 0.93.1
```
* Added Dawnblooms's Edda Blackblossom bossfight as an example stat sheet
```

### Version 0.93
```
* Rebuilt program from the ground up to improve FPS and workflow

* You must Double Left Click on sheets, folders, and parts of statcards to open them. This is to make easier to not do on accident

* Rebuilt textboxes to be able to: 
    * Be moved through with keyboard and mouse
    * Be able to select, copy, paste, and delete sections of text
    * Be able to scroll through large textboxes
    * Reworked formatting with a new popup on use of Right Click
    * The ability to add custom colors
    * You can Tab through textboxes

* Saves have been updated to better store data and keep track of more things 

* Reworked how you add Effects with a whole new pop out window
    * There are now presets for common types of Effects
    * Effects can be marked as In Line, causing them to render on the previous effects line.

* You can now add an Extra Text to abilities. This is for explanations of how the ability works or flavor text

* Reworked how you add Markers and edit them
    * Redesigned several ui and marker icons
    * Markers now auto tile for cleaner appearance
    * Added more Stake Overlays
    * Added stack Overlays
    * Added tankbuster Overlays

* Added Sound effects

* Added settings window
    * Can change resolution (Needs Restart)
    * Switch between Fullscreen, Windowed, and Windowed full screen (Needs Restart)
    * Switch which display the program opens to (Needs Restart)
    * Can change volume of program

* Added new escape menu
    * Various features listed in it are not available at the moment

* Heavily improved editor FPS and usability
    * Removed Zooming out as it looked bad and want to do it better later
    * Stat card can now be shifted using the context menu
    * Can now rearrange Traits and Abilities via dragging them
    * Stat cards Height variable is now more precise allowing for finer steps
    * Cards no longer render if not seen
    * When exporting as PNG it now makes a folder that exports one with a background and one without (Transparent)
    * When editing a part of the stat card (such as its name) the window no longer disappears when you click
        * This window now always sticks to the right side of the screen instead of the right side of the card
        * This window now can be closed with a small X in the top right (True of all UI windows)
        * The element the window is adjusting now only updates upon pressing the (Apply) button or the (Confirm) Button. This is to save on performance
        * The (Apply) button applies your changes, while the (Confirm) button applies them and closes the window

* You can now make folders on the menu screen
    * You can drag both sheets and folders into other folders

* You can easily rename files instead of them all being called "StatSheet[X]"

* Files can be duplicated

* UI and almost all elements have been updated to look better

* Fixed various bugs, including but not limited to:
    * When closing from editor using the window closing it not longer gives an error
    * The program won't crash if you click to fast (hopefully)
    * Various and many spelling mistakes
    * And all of the jank with the old text boxes
```

### Version 0.92.4
```
* Fixed bug (#6)
* Fixed bug (#7)
```

### Version 0.92.3
```
* Fixed bug (#4)
* Fixed bug (#5)
* Fixed issue where all font was bolded not just the title
```

### Version 0.92.2
```
* Fixed bug (#2)
* Fixed bug (#3)
```

### Version 0.92.1
```
* Fixed bug (#1)
* Readded Icon file
```

### Version 0.92
```
* Able to make Stat Sheets and Stat Cards within
* Able to save Stat Sheets
* Able to export Stat Sheets as PNGs
* Can make abilities INVK abilities
* Types and names on abilities no longer overlap if one is two long
* Can actually leave the program
```
