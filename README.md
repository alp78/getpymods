# getpymods
Extract all modules from Python files within a nested folder

-> creates a JSON with 3 keys in script folder:

- IMPORTED: list of all external modules installed
- STANDARD: list of modules part of the Python standard library
- POETRY: string to add all external modules in a virtualenv



USAGE:

python3 getpymods.py [dir_absolute_path] [python_version]

python3 getpymods.py /Users/user/project 3.8
