#! /usr/bin/env python

# Base Packages
import os
import fnmatch
from collections import Counter

# Pip Packages
import yaml

EXCLUDES = [".venv"]
DIRECTORY = "/home/kism/src/ansible-playbooks/"


def find_name_entries(directory):
    """Get list of name tags in yaml files, and their path"""
    name_entries = []
    for root, dirs, files in os.walk(directory):

        dirs[:] = [d for d in dirs if not d.startswith('.')]


        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                file_rel_path = os.path.relpath(os.path.join(root, file), directory)
                with open(os.path.join(root, file), "r", encoding="utf8") as f:
                    yaml_content = yaml.safe_load(f)
                    if isinstance(yaml_content, list):
                        for entry in yaml_content:
                            if isinstance(entry, dict) and "name" in entry:
                                name_entries.append({'name': entry["name"], 'path': file_rel_path})
    return name_entries


def remove_excluded_paths(results, excludes):
    """Return results that's path is in the excluded paths"""
    filtered_results = []

    for exclude in excludes:
        for result in results:
            print(result)
            if not fnmatch.fnmatch(result['path'], exclude):
                filtered_results.append(result)

    return filtered_results

def create_deduplicated_list(results):
    """Create new data structure for name keys and the files they are in"""
    filtered_results = {}

    for result in results:
        if result['name'] not in filtered_results:
            filtered_results[result['name']] = {'paths': [result['path']], 'count': 1}
        else:
            filtered_results[result['name']]['paths'].append(result['path'])
            filtered_results[result['name']]['count'] += 1

    return filtered_results

def custom_dict_sort(item):
    """For sorting entries"""
    return item[1]['count']

results = find_name_entries(DIRECTORY)
results = remove_excluded_paths(results, EXCLUDES)

deduplicated_dict = create_deduplicated_list(results)

# for key, item in deduplicated_dict.items():
#     print(key, "|", item)


# Sort the dictionary based on the 'order' subkey
sorted_dict = dict(sorted(deduplicated_dict.items(), key=custom_dict_sort))

# Print the sorted dictionary
for key, value in sorted_dict.items():
    print()
    print(key, "|", value)
