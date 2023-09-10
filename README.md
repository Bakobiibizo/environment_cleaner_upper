# Environment Cleaner Upper

This will uninstall every package in your pip environment if the package does not appear in the `base_environment.txt` file.

## Usage

There are two functions in this script and a main that executes those functions.

### check_environemnt

    Checks the current environment against the `base_environment.txt` file and generates a `clear.txt` file that lists the packages that need to be removed.

### clear_environment

    Clears the environment you are currently in by uninstalling packages listed in `to_remove.txt` file, removing the `to_remove.txt` file itself, and removing the `clear.txt` file. `Raises SystemError` if there is an error during the execution of the subprocess command.
