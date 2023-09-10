# aoc_bootstrapper

aoc_bootstrapper is a command line tool designed to get you up and running quickly on an Advent of Code challenge. The
bootstrapper will automatically download challenge input and generate starter code from user defined templates.

## Installation

TODO: Add installation instructions

## Usage

The bootstrapper has two commands: `generate` and `add`.

### aoc_bootstrapper generate

**Usage:** `aoc_bootstrapper generate <day> <language> <target_dir> [-y year]`

Downloads input and generates starter code for a challenge. The challenge day must be provided. A challenge year may
also optionally be provided, by default the current year is assumed.

#### Arguments

- `day`: The challenge day, 1-25 (inclusive).
- `language`: The lanugage to generate starter code for. This must be a language previously added to the list of known
  languages using `aoc_bootstrapper add`.
- `target_dir`: The directory to place the generated starter code in.

#### Options

- `-y <year>`: Specifies a challenge year.

### aoc_bootstrapper add

**Usage:** `aoc_bootstrapper add <lanugage> <template file>`

Adds a language and an associated template file for the tool to generate code from. Attempting to add a template for a
language that you have previously added a template for will overwrite the existing template.

#### Arguments

- `language`: The target language to add a template for. Case insensitive.
- `template file`: The path to a template file to associate with the language. See the **Template Files** section.

## Template Files

This tool makes use of user defined template files to generate starter code for whatever language you like to use for
the Advent of Code challenges. Templates are tracked using `aoc_bootstrapper add`. Templates are very basic and easy to
use and create. They define a starting point for your code when you begin a challenge. Templates are just code files
written in your target language, with a few optional tiny additions to work with the bootstrapper. Below is a sample
template for Python:

```python
"""
[[CHALLENGE_YEAR]] day [[CHALLENGE_DAY]] challenge
https://adventofcode.com/[[CHALLENGE_YEAR]]/day/[[CHALLENGE_DAY]]
"""

def challenge_part_1() -> None:
    pass

def challenge_part_2() -> None:
    pass


def main() -> None:
    print("Starting challenge")
    print("-------------- PART 1 --------------")
    challenge_part_1()
    print("-------------- PART 2 --------------")
    challenge_part_2()

if __name__ == "__main__":
    main()
```

When you run `aoc_bootstrapper generate`, the bootstrapper will copy this template into your target directory,
replacing the variables in double square brackets with their values. See below for a list of supported template
variables you can use. Anywhere you want to use a template variable in your starter code, simply put the name of the
variable in double square brackets. You are not required to use any variables in your template if you so choose. Template files have the `.tpl` extension by convention, but this is not required for the bootstrapper to work.

### Template Variables

This is a list of available variables you can use in your templates. Variables placed in double square brackets in your
templates will be replaced with their corresponding values.

- `CHALLENGE_DAY`: The challenge day.
- `CHALLENGE_YEAR`: The challenge year.