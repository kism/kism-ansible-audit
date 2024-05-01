#! /usr/bin/env python

# Base Packages
import os
import fnmatch
from collections import Counter

# Pip Packages
import yaml

EXCLUDES = [".venv"]
DIRECTORY = "/home/kism/src/ansible-playbooks/"


def find_name_entries(directory, excludes):
    """Get list of name tags in yaml files, and their path"""
    name_entries = []
    for root, dirs, files in os.walk(directory):

        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                file_rel_path = os.path.relpath(os.path.join(root, file), directory)
                with open(os.path.join(root, file), "r", encoding="utf8") as f:
                    yaml_content = yaml.safe_load(f)
                    if isinstance(yaml_content, list):
                        for entry in yaml_content:
                            if isinstance(entry, dict) and "name" in entry:
                                name_entries.append({"name": entry["name"], "path": file_rel_path})

    filtered_results = []

    for exclude in excludes:
        for result in name_entries:
            if not fnmatch.fnmatch(result["path"], exclude):
                filtered_results.append(result)

    return name_entries


def custom_dict_sort(item):
    """For sorting entries"""
    return item[1]["count"]


def create_final_results(results):
    """Create new data structure for name keys and the files they are in"""
    filtered_results = {}

    for result in results:
        if result["name"] not in filtered_results:
            filtered_results[result["name"]] = {"paths": [result["path"]], "count": 1}
        else:
            filtered_results[result["name"]]["paths"].append(result["path"])
            filtered_results[result["name"]]["count"] += 1

    filtered_results = {key: value for key, value in filtered_results.items() if value.get("count") != 1}

    sorted_results = dict(sorted(filtered_results.items(), key=custom_dict_sort))

    return sorted_results


results = find_name_entries(DIRECTORY, EXCLUDES)
final_results = create_final_results(results)

# Print the sorted dictionary
for key, value in final_results.items():
    print("- Name:", key)
    print("  Count: ", value["count"])
    for i in value["paths"]:
        print("     ", i)
    print()
