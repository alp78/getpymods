# takes a .py filepath as arg = '/Users/alex.pal/Desktop/UVIPR/eu-trd-undervalued-master/airflow/dags/batch_predict_dev.py'

from sys import argv, version_info
from json import dumps
from os import path, walk
from re import findall
from urllib.request import urlopen

walk_dir = argv[1]

try:
    py_version = argv[2]
except:
    py_version = None
    pass

# create a list of all modules of the python standard library 
std_mods = []

if py_version is None:
    py_version = version_info
    py_version = f"{py_version.major}.{py_version.minor}"
url = f"https://docs.python.org/{py_version}/py-modindex.html"
with urlopen(url) as f:
    page = f.read()
modules = set()
for module in findall(r'#module-(.*?)[\'"]', page.decode('ascii', 'replace')):
    module = module.split(".")[0]
    std_mods.append(module)


# extract all import statements from all files in folder and extract modules
walk_dir = path.abspath(walk_dir)
_files = []
_filenames = []
local_modules = []

for root, subfolders, files in walk(walk_dir):
    if path.exists(path.join(root, '__init__.py')):
        dir_name = root.split('/')[-1]
        local_modules.append(dir_name)
    for _file in files:
        if _file.endswith('py') and not _file.startswith('__init__'): 
            filepath = path.join(root, _file)
            _files.append(filepath)
            _filenames.append(_file.split('.')[0])

all_mods = []
for _file in _files:
    with open(_file, 'r') as f:
        statements = f.readlines()

    for line in statements:
        if line.startswith('from'):
            elements = line.split(' ')
            module = elements[1].split('.')[0]
            if module not in all_mods: all_mods.append(module)

        if line.startswith('import'):
            elements = line.split(' ')
            module = elements[1].rstrip('\n').rstrip(',').split('.')[0]
            if module not in all_mods: all_mods.append(module)

mod_dic = {}
std_modules = []
imp_modules = []

for mod in all_mods:
    if mod in std_mods:
        std_modules.append(mod)
    elif not mod in local_modules and not mod in _filenames:
        imp_modules.append(mod)
    

mod_dic['STANDARD'] = sorted(std_modules)
mod_dic['IMPORTED'] = sorted(imp_modules)

output_file = f'IMPORT_MODS.json'

with open(output_file, 'w') as f:
    f.write(dumps(mod_dic, indent=4, sort_keys=False))
