import os
import subprocess
import argparse
import logging
from typing import Optional, List
from argparse import Namespace


# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def check_environment(
    current_path: Optional[str] = "current_environment.txt",
    base_path: Optional[str] = "base_environment",
    remove_path: Optional[str] = "to_remove.txt",
) -> List[str]:
    """
    Check the environment by comparing the target environment with a base environment.

    Args:
        current_path (Optional[str]): The path to the file where the target environment will be written. Defaults to "current_environment.txt".
        base_path (Optional[str]): The path to the file containing the base environment. Defaults to "base_environment".

    Returns:
        bool: True if the write_to_remove function is successful, False otherwise.
    """
    logger.info("Checking the environment")
    if not current_path:
        current_path = "current_environment.txt"
    if not base_path:
        base_path = "base_environment.txt"
    if not remove_path:
        remove_path = "to_remove.txt"

    # Get the environment information and assign it to a variable
    target_environment = subprocess.run(
        ["pip", "freeze"], capture_output=True, text=True, check=True
    ).stdout.split("\n")

    with open(current_path, "w", encoding="utf-8") as file:
        file.writelines(target_environment)

    base_environment = []
    try:
        with open(base_path, "r", encoding="utf-8") as file:
            base_environment = file.readlines()

    except FileNotFoundError as error:
        logger.error("ERROR: %s", error)
        raise FileNotFoundError(f"ERROR: {error}") from error

    logger.debug("Target environment: %s", target_environment)
    logger.debug("Base environment: %s", base_environment)

    to_remove = target_environment
    for line in base_environment:
        against = line.split("\n")[0].strip()
        logger.debug("Against: %s", against)
        for i, target in enumerate(target_environment):
            check = target.split("=")[0].strip()
            logger.debug("Check: %s", check)

            if check == against:
                to_remove[i] = ""
    return write_to_remove(to_remove, remove_path)


def write_to_remove(
    to_remove: List[str], remove_path: Optional[str] = "to_remove.txt"
) -> List[str]:
    """
    Writes a list of strings to a file specified by the `path` parameter.

    Args:
        to_remove (List[str]): The list of strings to be written to the file.
        path (Optional[str], optional): The path of the file. Defaults to "to_remove.txt".

    Returns:
        bool: True if the write operation is successful, False otherwise.
    """
    logger.info("Writing to remove")
    if not remove_path:
        remove_path = "to_remove.txt"
    try:
        if os.path.exists(remove_path):
            os.remove(remove_path)
        with open(remove_path, "a", encoding="utf-8") as file:
            for line in to_remove:
                logger.debug("Line: \n%s", line)
                if line != "":
                    file.write(f"{line}\n")
                else:
                    continue
        return to_remove
    except SystemError as error:
        print(error)
        return to_remove


def clear_environment(
    remove_path: Optional[str] = "to_remove.txt",
    current_path: Optional[str] = "current_environment.txt",
) -> None:
    """
    Clears the environment you are currently in by uninstalling packages listed in "to_remove.txt" file, removing the "to_remove.txt" file itself, and removing the "current_environment.txt" file.

    Parameters:
        remove_path (str, optional): The path of the file. Defaults to "to_remove.txt".
        current_path (str, optional): The path of the file. Defaults to "current_environment.txt".

    Returns:
        None

    Raises:
        SystemError: If there is an error during the execution of the subprocess command.
    """
    logger.info("Clearing the environment")

    if not remove_path:
        remove_path = "to_remove.txt"
    if not current_path:
        current_path = "current_environment.txt"

    try:
        subprocess.run(["pip", "uninstall", "-r", remove_path, "-y"], check=True)
        os.remove(remove_path)
        os.remove(current_path)

    except SystemError as error:
        logger.error("ERROR uninstalling packages: %s", error)
        raise SystemError(f"ERROR uninstalling packages: {error}") from error


def dry_run(
    current_path: Optional[str], base_path: Optional[str], remove_path: Optional[str]
) -> None:
    """
    Perform a dry run to check the list of packages to be removed without actually removing them.

    Parameters:
        current_path (str, optional): The path of the file. Defaults to "current_environment.txt".
        base_path (str, optional): The path of the file. Defaults to "base_environment".

    Returns:
        None

    Raises:
        FileNotFoundError: If the file is not found.
    """
    logger.info("Performing a dry run")
    if not remove_path:
        remove_path = "to_remove.txt"
    try:
        check = check_environment(current_path, base_path, remove_path)
        logger.info(base_path)
        if check:
            logger.info(
                "These are the packages that will be removed\n %s", "".join(check)
            )
            os.remove("to_remove.txt")
    except FileNotFoundError as error:
        logger.error("ERROR: %s", error)
        raise FileNotFoundError(f"ERROR: {error}") from error


def parseargs() -> Namespace:
    """
    Parse the command line arguments and return the parsed arguments.

    :return: The parsed arguments as a Namespace object.
    :rtype: Namespace
    """
    logger.info("Parsing arguments")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        required=False,
        help="Check the list of packages to be removed with out removing them.",
    )
    return parser.parse_args()


def main(
    base_path: Optional[str],
    current_path: Optional[str],
    remove_path: Optional[str],
    do_dry_run: Optional[bool] = False,
) -> str:
    """
    Executes the main logic of the program.

    Args:
        base_path (Optional[str]): The base path for the program.
        current_path (Optional[str]): The path to clear.
        remove_path (Optional[str]): The path to remove.
        do_dry_run (Optional[bool], optional): Flag indicating whether to perform a dry run. Defaults to False.

    Returns:
        str: The result of the main logic.

    Raises:
        RuntimeError: If an error occurs during execution.
    """
    logger.info("Running main")
    try:
        check = check_environment(current_path, base_path, remove_path)
        logger.debug("Check: %s", check)
        logger.debug("do_dry_run: %s", do_dry_run)
        if check and not do_dry_run:
            clear_environment(remove_path, current_path)
            return "Environment cleared"
        else:
            return "Dry run successful"
    except RuntimeError as error:
        logger.error("ERROR: %s", error)
        raise RuntimeError(f"ERROR: {error}") from error


if __name__ == "__main__":
    args = parseargs()
    main(
        base_path="base_environment.txt",
        current_path="current_environment.txt",
        remove_path="to_remove.txt",
        do_dry_run=args.dry_run,
    )
