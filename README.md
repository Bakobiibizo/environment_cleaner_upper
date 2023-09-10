# Environment Cleaner Upper

Have you gone and installed a bunch of packages on your main python interpreter? Not sure what you can and cant remove? Well I've done that tons, so I made this Environment Cleaner Upper.

This will uninstall every package in your pip environment if the package does not appear in the `base_environment.txt` file.

Please adjust `base_environment.txt` accordingly. This version is the absolute least you could have in an install and you may want to keep some packages. Just add the packages you want to keep to the file, make sure not to add the verion number and just the name of the package as it appears on a `pip freeze` command.

## Usage

Clone the repo
`git clone https://github.com/bakobiibizo/environment_cleaner_upper.git`

To run the script with a dry run:
`python clear.py --dry-run`

To execute the script:
`python clear.py`

There are two functions in this script and a main that executes those functions.

### Check Environment (check_environment)

This function takes a snapshot of your current Python environment and compares it to a "base" environment that you consider ideal. It then figures out which packages are extra and should be removed. These extra packages are stored in a list for later use.

### Write to Remove List (write_to_remove)

After figuring out which packages are unnecessary, this function writes them to a file. This is your "remove list" and serves as a record of what should be uninstalled.

### Clear Environment (clear_environment)

Once you have your "remove list," this function steps in to actually remove the extra packages. It uninstalls each package on the list and cleans up by removing the files that stored your environments and "remove list."

### Dry Run (dry_run)

If you're not sure you want to go through with the cleaning and want to see what would happen, this function is for you. It performs a "dry run," showing you which packages would be removed without actually doing anything.

### Parse Command Line Arguments (parseargs)

This function allows you to interact with the script using command-line arguments. For example, you can choose to perform a "dry run" by adding a --dry-run flag when you run the script.

### Main Function (main)

This is where the magic happens. It calls all the other functions based on the options you've selected. For instance, if you've chosen to perform a dry run, it will do that; otherwise, it will go ahead and clean your environment.

## Technical

### check_environment(current_path, base_path, remove_path) -> List[str]

Compares the target environment with a base environment and returns a list of packages to be removed.

**Arguments**:

**current_path**: Path to the file where the target environment will be written. Defaults to "current_environment.txt".
**base_path**: Path to the file containing the base environment. Defaults to "base_environment".
**remove_path**: Path to the file where packages to be removed are listed. Defaults to "to_remove.txt".

**Returns**:

A list of packages to be removed.

### write_to_remove(to_remove, remove_path) -> List[str]

Writes a list of packages to a file, specifying which packages should be removed.

**Arguments**:
**to_remove**: The list of packages to be removed.
**remove_path**: The path of the file to which the list will be written. Defaults to "to_remove.txt".

**Returns**:
A list of packages to be removed.
clear_environment(remove_path, current_path) -> None
Clears the Python environment by uninstalling packages and removing specific files.

**Arguments**:
**remove_path**: Path to the file containing packages to be removed. Defaults to "to_remove.txt".
**current_path**: Path to the file representing the current environment. Defaults to "current_environment.txt".

**Returns**:
None

**Raises**:
**SystemError**: If an error occurs during execution.

### dry_run(current_path, base_path, remove_path) -> None

Performs a dry run to see which packages would be removed without actually removing them.

**Arguments**:
**current_path**: Path to the current environment file. Defaults to "current_environment.txt".
**base_path**: Path to the base environment file. Defaults to "base_environment".

**Returns**:
None

**Raises**:
**FileNotFoundError**: If a required file is not found.

### parseargs() -> Namespace

Parses the command-line arguments.

**Returns**:
A Namespace object containing parsed arguments.

### main(base_path, current_path, remove_path, do_dry_run) -> str

Executes the main logic of the program.

**Arguments**:
**base_path**: The base path for the program.
**current_path**: The path to clear.
**remove_path**: The path to remove.
**do_dry_run**: Flag for performing a dry run. Defaults to False.

**Returns**:

A string indicating the result of the main logic.
**Raises**:

**RuntimeError**: If an error occurs during execution.

