'''
Tool to create a starting point for an AOC challenge, including downloading challenge input and creating a code
template.
'''

import argparse
import os
import pickle
import requests
import tomllib
import webbrowser

from datetime import datetime
from enum import Enum
from sys import argv, stderr


AOC_ENDPOINT = "https://www.adventofcode.com"
SAVED_TEMPLATES_FILE_PATH = "data/templates.pkl"
CONFIG_FILE_PATH = "resources/config.toml"
config = {}


class BoostrapperError(Enum):
    TEMPLATE_NOT_FOUND = 1
    BAD_AOC_REQUEST = 2
    INVALID_TEMPLATE_PATH = 3


def generate_challenge(saved_templates: dict[str, str], args: argparse.Namespace) -> None:
    """
    Generates challenge input and starter code for a challenge.

    Parameters:
        `saved_templates`: A dictionary mapping language names to paths of template files for those languages.
        `args`: The command line arguments.
    """

    if args.language.lower() not in saved_templates:
        print(f"Error: The language {args.language} does not have a valid template. Add one with 'bootstrapper add'", file=stderr)
        exit(BoostrapperError.TEMPLATE_NOT_FOUND.value)

    print(f"Generating {args.language} starter code for {args.year} day {args.day} challenge")

    create_input_file(args.day, args.year)

    starter_code_file_path = generate_starter_code(
        saved_templates[args.language.lower()],
        args.target_dir,
        {
            "CHALLENGE_DAY": args.day,
            "CHALLENGE_YEAR": args.year
        }
    )

    print("Done!")

    webbrowser.open(f"https://adventofcode.com/{args.year}/day/{args.day}")

    print(f"Your starter code file is located at {starter_code_file_path}. The challenge page has been opened in your browser. Good luck!")

def create_input_file(day: int, year: int) -> None:
    """
    Download the input for a specific challenge and creates an input file for it in the configured inputs directory.
    
    Paramters:
        `day`: The challenge day.
        `year`: The challenge year.
    """

    print("Creating input file...")

    global config
    
    inputs_dir_path = config["challenge_input_directory"]
    challenge_input_file_path = f"{inputs_dir_path}/{year}/day{day}.txt"

    try:
        challenge_input = get_challenge_input(day, year)
    except ConnectionError as e:
        raise(e)

    if os.path.exists(challenge_input_file_path):
        print(f"{challenge_input_file_path} already exists, skipping")
        return

    inputs_for_year_dir_path = f"{inputs_dir_path}/{year}"

    if not os.path.isdir(inputs_for_year_dir_path):
        os.mkdir(inputs_for_year_dir_path)

    with open(challenge_input_file_path, "w") as input_file:
        input_file.write(challenge_input)

def get_challenge_input(day: int, year: int) -> str:
    """
    Retrieves the input for a specific challenge from adventofcode.
    
    Paramters:
        `day`: The challenge day.
        `year`: The challenge year.
    
    Returns:
        The challenge input content.
    """

    print("Downloading challenge input...")

    global config

    session_cookie = config["session_cookie"]
    request_url = f"{AOC_ENDPOINT}/{year}/day/{day}/input"
    response = requests.get(
        request_url,
        cookies={"session": session_cookie}
    )

    if response.status_code != 200:
        print(f"Error {response.status_code} while fetching {request_url}. Maybe your day or year is invalid, or maybe your session cookie is incorrect or has expired.", file=stderr)
        exit(BoostrapperError.BAD_AOC_REQUEST.value)

    return response.text

def generate_starter_code(template_file_path: str, target_dir: str, template_vars: dict[str, str]) -> str:
    """
    Generate a starter code file in the target directory using the given template.

    Parameters:
        `template_file_path`: The location of the template file.
        `target_dir`: The directory to place the starter code file in.
        `template_args`: A mapping of template variable names to their values.

    Returns:
        The file path of the generated starter code file.
    """

    with open(template_file_path, "r") as template_file:
        template_content = template_file.read()

    print("Parsing template...")

    for template_var in template_vars:
        template_content = template_content.replace(f"[[{template_var}]]", f"{template_vars[template_var]}")

    print("Generating starter code...")

    if template_file_path.endswith(".tpl"):
        starter_code_file_path = f"{target_dir}/{os.path.basename(template_file_path)}"[:-4]
    else:
        starter_code_file_path = f"{target_dir}/{os.path.basename(template_file_path)}"

    with open(starter_code_file_path, "w") as starter_code_file:
        starter_code_file.write(template_content)

    return starter_code_file_path

def load_saved_templates() -> dict[str, str]:
    """
    Loads the template location data from the saved templates file.
    
    Returns:
        A dictionary containing mappings of language names to paths to template files for those languages.
    """

    try:
        with open(SAVED_TEMPLATES_FILE_PATH, "rb") as saved_template_file:
            return pickle.load(saved_template_file)
    except FileNotFoundError:
        return {}
    
def add_template(saved_templates: dict[str, str], args: argparse.Namespace) -> None:
    """
    Adds a user-defined template to the list of tracked templates.

    Parameters:
        `saved_templates`: A dictionary mapping language names to paths of template files for those languages.
        `args`: The command line arguments.
    """

    if not os.path.exists(args.template_file):
        print(f"Not a valid path: {args.template_file}", stderr)
        exit(BoostrapperError.INVALID_TEMPLATE_PATH.value)

    saved_templates[args.language.lower()] = args.template_file

    with open(SAVED_TEMPLATES_FILE_PATH, "wb") as saved_templates_file:
        pickle.dump(saved_templates, saved_templates_file)

    print("Template added successfully.")

def load_config() -> dict:
    """
    Loads the config file.

    Returns:
        The config dictionary.
    """

    with open(CONFIG_FILE_PATH, "rb") as config_file:
        return tomllib.load(config_file)


def main() -> None:

    global config
    config = load_config()
    
    prog_mode = argv[1]
    arg_parser = argparse.ArgumentParser(
        prog="AOC Bootstrapper",
        description="Program to generate templates for AOC challenges"
    )
    saved_templates = load_saved_templates()

    if prog_mode == "generate":

        arg_parser.add_argument("day", type=int)
        arg_parser.add_argument("language")
        arg_parser.add_argument("target_dir")
        arg_parser.add_argument("-y", "--year", default=datetime.now().year, type=int)

        generate_challenge(saved_templates, arg_parser.parse_args(argv[2:]))

    elif prog_mode == "add":

        arg_parser.add_argument("language")
        arg_parser.add_argument("template_file")

        add_template(saved_templates, arg_parser.parse_args(argv[2:]))

if __name__ == "__main__":
    main()