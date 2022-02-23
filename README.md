# getpymods
Extract all modules used in Python files within a nested folder

--> creates a JSON with two keys in script folder:

- IMPORTED: list of all external modules installed
- STANDARD: list of modules part of the Python standard library


USAGE:

- takes two arguments: 
1) project's absolute path (required)
2) Python version (optional)

python3 getpymods.py [dir_absolute_path] [python_version]

python3 getpymods.py /Users/user/project 3.8
