# utils.py
import os
import shutil
import curses
from pathlib import Path
import uuid
from datetime import datetime

#TODO: probably seperate the sort types into different files.
#TODO: yea probably keep backup() here, make a new createtempfolder(), then move sorting algos to like sort.py or smthn
#TODO: seperate createtempfolder() PLEASE
#TODO: add some error handling or get taken out like a dying animal
#TODO: run through and clean up all functions before publishing
#TODO: Add option to sort by size

#TODO!!!!: CLEAN UP CODE, COMMENTS, VARIABLES, IMPROVE CONSISTENCY, PUBLISH, THEN UPDATE AND MAINTAIN.

def backup(originalDirectory, backupDirectory):
    """
    Create a backup of existing files to a different directory in case something goes wrong causing corruption or data loss.
    This is achieved by iterating over all files in the originalDirectory and copying them using shutil.copy2 into backupDirectory.
    pretty standard ig.

    :param originalDirectory:    the directory to be backed up
    :param backupDirectory:    the target directory to copy files into

    :var originalItem:    the item currently chosen to be copied
    :var backupItem:    the destination file that originalItem will be copied to/as

    :return 0:    success!
    :return -1:    something, and i don't know what, has gone horribly and terribly wrong. this will cause a termination condition

    :TODO: worth considering moving original files to backup and using the copied files to sort, so you're not endangering original files?
           not sure if thats a great thought but it crossed my mind.
    """
    try:
        # iterate over all items in the originalDirectory
        for item in originalDirectory.iterdir():
            originalItem = originalDirectory / item.name
            backupItem = backupDirectory / item.name
            
            # if the item is a directory, copy it recursively, dirs_exist_ok is used to overwrite any existing directory in the backup location
            if item.is_dir():
                shutil.copytree(originalItem, backupItem, dirs_exist_ok=True)
            # otherwise, if its some random file, use copy2 to copy the file & its metadata
            else:
                shutil.copy2(originalItem, backupItem)
        return 0
    except:
        return -1

def sortDate(directory, window):
    """
    Sorts files in "directory" into folders based on last modification date.
    Gives the user the option between "YYYY", "YYYY-MM", and "YYYY-MM-DD".
    ISO-6801

    :param directory:    the directory to be sorted
    :param window:    the curses window to push text to, allowing the user to select options.
    :TODO:    also maybe give users the option to sort only loose files or all files, to preserve folders? MAKE CLEAR IN DOCUMENTATION

    :var selected:    the option from the sorting criteria selected. 0 = YYYY, 1 = YYYY-MM, 2 = YYYY-MM-DD, 3 = Exit. Determines sub-directory depth.
    :var tempDir:    a temporary directory generated at runtime named temp_[32 char uuid] used to prevent attempted creation of duplicate folders.
    :var item:    the thing currently being sorted!
    :var file_date:    the last modified date of the file, got using datetime.

    :return 0:    success!
    :return -1:    something, and i don't know what, has gone horribly and terribly wrong. this will cause a termination condition

    :TODO:    add option for created date rather than modified date?
    :TODO:    add option to rename files based on?
    """
    # available options for sorting depth
    options = [
        "YYYY",
        "YYYY-MM",
        "YYYY-MM-DD",
        "Exit."
    ]
    selected = 0
    window.keypad(True)

    while True:
        window.clear()
        window.addstr("Select the sorting criteria:\n")

        for idx, option in enumerate(options):
            if idx == selected:
                window.addstr(idx + 2, 0, f"> {option}", curses.A_REVERSE)
            else:
                window.addstr(idx + 2, 0, f"  {option}")
        
        key = window.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key == curses.KEY_ENTER or key in [10, 13]:  # the enter key to select
            break
            
    # exit if user selects "Exit."
    if selected == 3:
        # :TODO: change what return the return condition is
        return
    
    # if not, sort based on selected criteria
    window.clear()
    window.addstr("Sorting files by date...\n")
    window.refresh()

    # create a temp directory to avoid existing folder conflicts
    needTempDir = True
    while needTempDir == True:
        tempDirName = f"temp_{uuid.uuid4().hex[:32]}"
        tempDir = directory / tempDirName
        if not tempDir.exists():
            needTempDir = False
    # create the temporary directory
    tempDir.mkdir()

    # move everything from directory -> tempDir
    for item in directory.iterdir():
        if item != tempDir:
            shutil.move(str(item), str(tempDir / item.name))

    for item in tempDir.rglob('*'):  # rglob instead of iterdir to include subdirectories
        if item.is_file():
            file_date = datetime.fromtimestamp(item.stat().st_mtime)  # get "Modified on" date

            # set the targetFolder based on selected criteria
            if selected == 0:  # sort YYYY
                targetFolder = directory / str(file_date.year)
            elif selected == 1:  # sort YYYY-MM
                targetFolder = directory / f"{file_date.year}/{file_date.year}-{file_date.strftime('%m')}"
            elif selected == 2:  # sort YYYY-MM-DD
                targetFolder = directory / f"{file_date.year}/{file_date.year}-{file_date.strftime('%m')}/{file_date.year}-{file_date.strftime('%m')}-{file_date.strftime('%d')}"

            targetFolder.mkdir(parents=True, exist_ok=True)  # if target folder does not exist, create it

            # move the item to targetFolder, sorted!
            shutil.move(str(item), str(targetFolder / item.name))
    
    # delete the tempDir and everything left in it (empty folders) when done.
    shutil.rmtree(tempDir)
    return 0

def sortFiletype(directory, window):
    """
    Sorts files in "directory" into folders based on filetype, titled "TXT", "PNG", "XML", for example
    
    :param directory:    the directory to be sorted
    :param window:    currently not used
    :TODO:    maybe "window" should be moved from here and the option select should be done in the def sort() function at the bottom of utils.py
    :TODO:    also maybe give users the option to sort only loose files or all files, to preserve folders? MAKE CLEAR IN DOCUMENTATION
    
    :var tempDir:    this solves a potential problem where directories already exist and have things in them and they don't get sorted properly. to be honest it might not be necessary, investigate.
    :var fileExtension:    gets the item suffix using pathlib, or if that returns "None" checks for the last "." (solves an issue with files like ".txt"), or sets to "OTHER"

    :return 0:    success!
    :return -1:    something, and i don't know what, has gone horribly and terribly wrong. this will cause a termination condition

    :TODO:    go through and clean up variable names, comments, and structure
    :TODO:    add some error handling and more/clearer return conditions
    """

    window.clear()
    window.addstr("Sorting files into filetype folders...\n")
    window.refresh()

    # create a temp directory to avoid existing folder conflicts
    needTempDir = True
    while needTempDir == True:
        tempDirName = f"temp_{uuid.uuid4().hex[:32]}"
        tempDir = directory / tempDirName
        if not tempDir.exists():
            needTempDir = False
    # create the temporary directory
    tempDir.mkdir()

    # move everything from directory -> tempDir
    for item in directory.iterdir():
        if item != tempDir:
            shutil.move(str(item), str(tempDir / item.name))

    for item in tempDir.rglob('*'):
        if item.is_file():
            # get file extension as the item's suffix, if it can't find one, set it as "OTHER"
            # BUG: files such as ".txt" will get sorted as "OTHER" because it can't find a suffix, easy workaround is just finding whats after the dot.
            fileExtension = item.suffix[1:].upper() if item.suffix else 'OTHER'
            # target directory is based on fileExtension
            targetDir = directory / fileExtension
            targetDir.mkdir(exist_ok=True)  # create the folder if it doesn't exist
        
            # move the file, sorted!
            shutil.move(str(item), str(targetDir / item.name))

    # delete tempDir and its leftover content (empty folders) when done
    shutil.rmtree(tempDir)
        
    window.addstr("\nSorting complete. Press any key to return to the main menu.")
    window.refresh()
    window.getch()
    return 0

def sortAlphabetical(directory, window):
    """
    Sorts files in "directory" alphabetically, gives the user 2 options.
    To remove files from subdirectories and sort them, or to ignore files in subdirectories and sort the subdirectories.

    :param directory:    the directory to be sorted
    :param window:    the window to push text to, maybe rudimentary way of letting user select between 2 options
    :TODO:    maybe "window" should be moved from here and the option select should be done in the def sort() function at the bottom of utils.py
    
    :var alpahbetFolder:    a post-sort directory titled a single letter "A", "B", "C", etc. where files are moved into based on name[0] (their first letter)
    :var tempDir:    a temporary directory generated at runtime named temp_[32 char uuid] used to prevent attempted creation of duplicate folders (cant move folder "D" into itself)
    :var item:    the file/subdirectory currently being sorted

    :return 0:    success!
    :return -1:    something, and i don't know what, has gone horribly and terribly wrong. this will cause a termination condition
    
    :TODO:    either reimpliment return code 50 or totally remove it
    :return 50:    temp directory already exists

    :TODO:    add some error handling and more/clearer return conditions
    """
    # sorting preference between leaving files in folders and sorting the folders, or pulling them out and trashing the folders
    options = [
        "Remove files from folders and then sort.",
        "Sort folders, ignoring their content.",
        "Exit."
    ]
    selected = 0
    window.keypad(True)

    while True:
        window.clear()
        window.addstr("Select the sorting criteria:\n")

        for idx, option in enumerate(options):
            if idx == selected:
                window.addstr(idx + 2, 0, f"> {option}", curses.A_REVERSE)
            else:
                window.addstr(idx + 2, 0, f"  {option}")
        
        key = window.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key == curses.KEY_ENTER or key in [10, 13]:  # the enter key
            break

    # close if the user selects to exit
    if selected == 2:
        # :TODO: change what return the return condition is
        return

    # sort based on choice
    # selected == 0: remove items from folders and sort them
    # selected == 1: keep items in folders and sort the folders
    if selected == 0:
        window.clear()
        window.addstr("Sorting files and folders alphabetically, removing items from folders...\n")
        window.refresh()

        for item in directory.rglob('*'):  # rglob to include subdirectories
            if item.is_file():
                firstLetter = item.name[0].upper()
                alphabetFolder = directory / firstLetter
                if not alphabetFolder.exists():
                    alphabetFolder.mkdir()
                shutil.move(str(item), str(alphabetFolder / item.name))

        for item in directory.rglob('*'):
            if item.is_dir() and not any(item.iterdir()):
                item.rmdir()
        
    elif selected == 1:
        window.clear()
        window.addstr("Sorting folders alphabetically, ignoring their contents...\n")
        window.refresh()

        # tempDir again...
        # TODO: defo seperate this
        needTempDir = True
        while needTempDir == True:
            tempDirName = f"temp_{uuid.uuid4().hex[:32]}"
            tempDir = directory / tempDirName
            if not tempDir.exists():
                needTempDir = False
        tempDir.mkdir()

        # move everything into the tempDir to prevent existing folder conflicts
        for item in directory.iterdir():
            if item != tempDir:
                shutil.move(str(item), str(tempDir / item.name))

        # now go through tempDir and sort that into alphabet folders
        for item in tempDir.iterdir():
            # if a file is just called ".txt" or similar, this sorts them into a folder called "NAMELESS"
            if item.name.startswith("."):
                specialFolder = directory / "NAMELESS"
                if not specialFolder.exists():
                    specialFolder.mkdir()
                shutil.move(str(item),str(specialFolder/item.name))
            else:
                alphabetFolder = directory / item.name[0].upper()
                if not alphabetFolder.exists():
                    alphabetFolder.mkdir()
                shutil.move(str(item), str(alphabetFolder / item.name))

        # now get rid of tempDir, again...
        shutil.rmtree(tempDir)

    window.addstr("\nSorting complete. Press any key to return to the main menu.")
    window.refresh()
    window.getch()
    return 0

# rather than calling a sort algorithm directly, the main function passes it as a parameter to this function which then finds the relevant
# sort function. i'm sure there is an easier way to do this but it works.
def sort(directory, sortType, window):
    if sortType == "DATE":
        return sortDate(directory, window)
    elif sortType == "FILETYPE":
        return sortFiletype(directory, window)
    elif sortType == "ALPHABETICAL":
        return sortAlphabetical(directory, window)
    else:
        return -1
    