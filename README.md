# dd_cleaner
Python script for cleaning DerivedData directories

Searches for DerivedData folders is specified location and lears it's content if requested.

To use:
1. `brew install coreutils` - needed to have 'gsort' shell command
2. Download script
3. Cd to folder with script and `python derived_data.py`

OR

3. `chmod +x derived_data.py`
4. Add to PATH 
5. `derived_data.py`

Arguments:

`-f` will clear without confiramtion

`-d <directory>` specify top level directory to search for DerivedData, e.g. /Users/<username>/Projects. It's "~" by default
