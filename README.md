# dd_cleaner
Python script for cleaning DerivedData directories

Searches for DerivedData folders is specified location and clears it's content if requested.

To use:
1. `brew install coreutils` - needed to have 'gsort' shell command
2. `brew install findutils` - needed to have 'gxargs' shell command
3. `pip install tabulate` - needed for printing of founded directories info
4. Download script
5. Cd to folder with script and `python derived_data.py`

OR

5. `chmod +x derived_data.py`
6. Add to PATH 
7. `derived_data.py`

Arguments:

`-f` will clear without confirmation

`-d <directory>` specify top level directory to search for DerivedData, e.g. /Users/<username>/Projects. It's "~" by default

`-l` will only list directories with derived data, without prompt to clear

`-n <directory_name>` specify name of directory containing derived data (in case you use custom one), default is 'DerivedData'

`-a` will clear all found locations, without prompt to select what locations to clear

For example:
`derived_data.py -f -d /Users/onikiforov/dd_test` will list all directories under "dd_test" that contain DerivedData and prompt to clear them without confirmation


Usage:

Assuming found directories are:
-------  ------  ------------------------------------------------------------------
      1  160K    /Users/onikiforov/dd_test/DerivedData
      2  156K    /Users/onikiforov/dd_test/project_1/DerivedData
      3  152K    /Users/onikiforov/dd_test/test/DerivedData
      4  128K    /Users/onikiforov/dd_test/project_test/DerivedData
      5  68K     /Users/onikiforov/dd_test/project_ios_test/DerivedData
      
Entering `0` will clear all listed directories

Entering `1, 2` will clear "/Users/onikiforov/dd_test/DerivedData" and "/Users/onikiforov/dd_test/project_1/DerivedData"

Entering `-4, -5` will clear all directories except "/Users/onikiforov/dd_test/project_test/DerivedData" and "/Users/onikiforov/dd_test/project_ios_test/DerivedData"
