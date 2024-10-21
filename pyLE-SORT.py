import os
import curses
from curses import wrapper
import utils
from pathlib import Path

def printAscii(stdscr):
    """
    Prints the ASCII logo to the top of the screen.

    PARAM : stdscr : the screen initialised by the curses module, to be drawn to
    """
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN_ON_BLACK = curses.color_pair(1)
    stdscr.addstr(1, 0, "#####################################################")
    stdscr.addstr(2, 11, "__    _____     _____ _____ _____ _____")
    stdscr.addstr(3, 0, "   ___ _ _", GREEN_ON_BLACK)
    stdscr.addstr(4, 0, " _| . | | |", GREEN_ON_BLACK)
    stdscr.addstr(5, 0, "|_|  _|_  |", GREEN_ON_BLACK)
    stdscr.addstr(6, 0, "  |_| |___|", GREEN_ON_BLACK)
    stdscr.addstr(3, 10, "|  |  |   __|___|   __|     | __  |_   _|")
    stdscr.addstr(4, 11, "  |__|   __|___|__   |  |  |    -| | |")
    stdscr.addstr(5, 11, "_____|_____|   |_____|_____|__|__| |_|")
    stdscr.addstr(7, 0, "#####################################################")
    stdscr.refresh()

def Welcome(stdscr):
    mainWin = curses.newwin((curses.LINES - 9), (curses.COLS - 1), 9, 0)
    stdscr.clear()
    printAscii(stdscr)
    mainWin.addstr("Welcome to .pyLE-SORT! This python app is designed to help sort and organise your files for archiving! let's begin!")
    mainWin.addstr("\nPress any key to begin...")
    mainWin.refresh()
    mainWin.getch()
    directorySelect(stdscr, mainWin)

def directorySelect(stdscr, mainWin):
    #TODO: dude u r so thick can u pls just make it call directoryselect() instead of SHUTTING THE PROGRAM AHHAHA
    mainWin.clear()
    mainWin.addstr("Please enter the directory to be sorted. The directory probably looks something like:")
    mainWin.addstr("\nC:\\Users\\[You]\\Desktop\\pyLE-SORT")
    mainWin.addstr("\nOf course, with a different actual location.")
    mainWin.refresh()
    curses.echo()
    directory = Path(mainWin.getstr(4, 0).decode('utf-8'))
    curses.noecho()
    if not directory.exists():
        mainWin.addstr("\nCan't find specified directory.")
        mainWin.addstr("\nIf you're struggling to find the directory, just click the bar at the top of the file explorer and copy that.")
        mainWin.addstr("\nPress any key to exit...")
        mainWin.refresh()
        mainWin.getch()
        return
    else:
        mainWin.addstr("\nDirectory found.")
        mainWin.refresh()
        selectSortType(stdscr, mainWin, directory)

def selectSortType(stdscr, mainWin, directory):
    mainWin.clear()
    options = ["DATE", "FILETYPE", "ALPHABETICAL", "QUIT"]
    selected = 0
    mainWin.keypad(True)
    while True:
        mainWin.clear()
        mainWin.addstr("Please select a sorting method:")
        
        for idx, option in enumerate(options):
            if idx == selected:
                mainWin.addstr(idx + 1, 0, f"> {option}", curses.A_REVERSE)
            else:
                mainWin.addstr(idx + 1, 0, f"  {option}")
        
        key = mainWin.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Enter key
            if options[selected] == "QUIT":
                break
            else:
                backup = ""
                mainWin.addstr(len(options) + 2, 0, f"You selected: {options[selected]}\n")
                mainWin.addstr("WARNING: EVEN WITH A BACKUP, SOME FILE METADATA MAY NOT BE PRESERVED, PLEASE READ THE DOCUMENTATION BEFORE USE", curses.A_BOLD)
                while (backup.upper() not in ["Y", "N"]):
                    mainWin.addstr("\nCreate backup of files? [RECOMMENDED] Y/N: ")
                    mainWin.refresh()
                    curses.echo()
                    backup = mainWin.getstr().decode('utf-8')
                    curses.noecho()
                if backup.upper() == "Y":
                    mainWin.clear()
                    mainWin.addstr("Enter backup directory:\n")
                    curses.echo()
                    backupDirectory = Path(mainWin.getstr().decode('utf-8'))
                    curses.noecho()
                    if backupDirectory == directory:
                        mainWin.addstr("Backup directory cannot be the same as sorting directory.")
                        mainWin.addstr("\nMake sure they are not the same and try again.")
                        mainWin.addstr("\nPress any key to exit...")
                        mainWin.refresh()
                        mainWin.getch()
                    if not backupDirectory.exists():
                        mainWin.addstr("Can't find specified directory.")
                        mainWin.addstr("\nMake sure the directory exists and try again.")
                        mainWin.addstr("\nPress any key to exit...")
                        mainWin.refresh()
                        mainWin.getch()
                        return
                    returnCode = utils.backup(directory, backupDirectory)
                    mainWin.clear()
                    if returnCode == 0:
                        mainWin.addstr("Backup complete.")
                        mainWin.addstr("\nCommencing sort.")
                    else:
                        mainWin.addstr("Something has gone horribly wrong!")
                        mainWin.addstr(f"\nError Code: {returnCode}")
                        mainWin.addstr("\nPlease report this and the steps you took to get here!")
                        mainWin.addstr("\nPress any key to exit...")
                        mainWin.refresh()
                        mainWin.getch()
                        return
                mainWin.clear()
                mainWin.refresh()
                returnCode = utils.sort(directory, options[selected], mainWin)
                if returnCode == 0:
                    #success, program can close
                    mainWin.clear()
                    mainWin.addstr("Sort complete.")
                    mainWin.addstr("\nPress any key to exit...")
                    mainWin.refresh()
                    mainWin.getch()
                    return
                elif returnCode == 1:
                    return
                elif returnCode == 50:
                    mainWin.clear()
                    mainWin.addstr("I'm not sure how, but the unique temp directory name for sorting already exists.")
                    mainWin.addstr(f"\nError Code: {returnCode}")
                    mainWin.addstr("\nRestarting the program should fix this.")
                    mainWin.addstr("\nFeel free to report this though, as this should be exceptionally rare.")
                    mainWin.addstr("\n\nSee: Ostrich Algorithm.")
                    mainWin.addstr("\n\nPress any key to exit...")
                    mainWin.refresh()
                    mainWin.getch()
                    return
                else:
                    #horrible error, what went wrong, oh my god, theyre dead, theyre all dead, the humanity!
                    mainWin.clear()
                    mainWin.addstr("Something has gone horribly wrong!")
                    mainWin.addstr(f"\nError Code: {returnCode}")
                    mainWin.addstr("\nPlease report this and the steps you took to get here!")
                    mainWin.addstr("\n\nPress any key to exit...")
                    mainWin.refresh()
                    mainWin.getch()
                    return
        mainWin.refresh()


wrapper(Welcome)
