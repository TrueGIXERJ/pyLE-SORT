# pyLE-SORT
pyLE-SORT is a simple python-based file sorting utility created to help organise directories by various criteria. It offers a simple CLI using the `curses` python library to streamline the process.

## Features
pyLE-SORT is ever a work in progress, primarily for personal use, its feature set currently consists of the following:

* Backup Functionality
  - pyLE-SORT offers the creation of a backup of your files before any sorting operation takes place to ensure data safety.
  - The backup process is not perfect, and may fail or lose some metadata during the process - ensure you check your backup before continuing.
  - The backup process uses the `shutil` library, as with much of the project.
* Date-based Sorting
  - Files can be organised by their *Last Modified Date*
  - Multiple options for sort depth
    - `YYYY`
    - `YYYY-MM`
    - `YYYY-MM-DD`
  - Sorts using [ISO-8601](https://www.iso.org/iso-8601-date-and-time-format.html)
* File-type Sorting
  - Organise files based on their extension (TXT, PNG, XML, ETC.)
* Alphabetical Sorting
  - Sort files or folders alphabetically
  - 2 Options for sort method
    - Remove files from subdirectories and sort
    - Sort subdirectories and ignore internal files
    
## Installation
### Prerequisites
* Python 3.7+
* curses
  - The `curses` library may be installed by default on Unix-based systems, though windows users may have to install the `windows-curses` package.
### Steps
1. Ensure `curses` is installed
   * To verify that curses is installed, simply try importing it in python by running the following in your command line: `python3 -c "import curses; print('curses is installed.')"`. If you get an error when running this, you will need to install curses.
2. Install `curses` if necessary
   * On Unix systems, install curses by running `pip install curses` in your command line.
   * On windows systems, install curses by running `pip install windows-curses` in your command line.
   * Following installation, verify that the  module is installed as directed above.
3. Clone the repository!
   * `git clone https://github.com/TrueGIXERJ/pyLE-SORT.git`
   * `cd pyLE-SORT`
   * Or simply download the .zip from github.
## Usage
Use the arrow keys and enter to navigate the CLI, it is relatively self explanatory. If you have any issues let me know.
## Known Issues
* Files beginning with special characters (such as `.something.txt`) do not sort when sorting alphabetically.
* Files with non-names (such as `.txt`) will sort as `OTHER` when sorting by file type.
## Planned Features
* Additional sorting methods
  - Sorting by file size
* Additional sorting options for existing methods
  - Options to only sort loose files + folders to preserve subdirectories
  - Option to rename files based on date/time `YYYY-MM-DD-HH-MM-SS
  - Option in Date sort to sort based on created date rather than modified date
* Optimisations when sorting large directories
* Improvements to code quality
* More verbose error handling/reporting/logging
## Contributing
I happily welcome contributions to improving pyLE-SORT with new features, bug-fixes, and optimisations.
If you would like to contact me you can do so by opening an issue on the [GitHub Repository](https://github.com/TrueGIXERJ/pyLE-SORT) or by shouting at me loudly on my public [Discord](discord.gg/zkhuwD5).
