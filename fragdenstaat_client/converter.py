"""
fragdenstaat_client.converted - CSV conversion utilities module
"""
import json
import csv
from typing import Any, List, Dict
from pathlib import Path



def extract_objects_from_fragdenstaat_json_data(data: dict) -> List[dict]:
    """extracts the object list from a fragdenstaat json response"""
    return data.get("objects") or []


def prefix_dict_keys(prefix: str, data: dict) -> dict:
    """returns a copy of the given dictionary with its key names prefixed with the given prefix.
    :param prefix: the string with the prefix
    :param data: the source dictionary
    """
    result = {}
    for key, value in data.items():
        result[f"{prefix}_{key}"] = value
    return result


def flatten_item(item: Dict[str, Any]) -> Dict[str, str]:
    """flattens a dictionary containing anything as value to a dictionary of strings only as value.
    This is necessary because CSV does not support nested data
    """
    result = {}
    for key, value in item.items():
        if not isinstance(value, dict) and not isinstance(value, (str, bytes)):
            # if the value type is not a dictionary and not a string then we convert it
            # to string using the json imperative. We obviously cant really have complex 
            # json data structures in the csv but here we just convert simple types 
            # such as: numbers, booleans and null.
            result[key] = json.dumps(value)

        elif isinstance(value, (str, bytes)):  
            # if the value is a string then we just assign the key to `result`
            result[key] = value

        elif key == "public_body" and isinstance(value, dict):
            # here we extract the nested data about the public_body prefixing each key with "institution_"
            nested = prefix_dict_keys("institution", value)
            # here we make a recursive call to flatten_item to convert numbers, booleans and null
            # then we finally merge the nested data with teh final result by calling .update()
            result.update(flatten_item(nested))
        else: # this condition should never be reached unless eventually fragdenstaat adds another nested dictionary to its data
            # the logic here is mostly the same as above except that rather than hardcoding we use the original dictionary key as prefix
            nested = prefix_dict_keys(key, value)
            result.update(flatten_item(nested))  


    return result


def json_to_csv(fd_read, fd_write, write_header: bool = True):
    """reads json data from a file-descriptor and writes csv data to another file descriptor.
    """
    # instantiate python's built-in csv.writer class pointing to write file-descriptor
    writer = csv.writer(fd_write, delimiter=",", strict=True)
    # loads the json data from the "read" file-descriptor
    data = json.load(fd_read)

    # the json data wraps the data we want in some metadata, so here we need to "extract" the list of requests
    # prior to writing data to the CSV file
    request_list = extract_objects_from_fragdenstaat_json_data(data)
    # the request list contains a nested object under the field "public_body", 
    # so we need to "flatten" each item on the list using the flatten_item function
    objects = map(flatten_item, request_list)

    for index, obj in enumerate(objects):
        if write_header and index is 0:  # write the keys to the first line of the CSV
            writer.writerow(obj.keys())

        # for each request in the list we write them as a new line in the CSV file
        writer.writerow(obj.values())


def convert_multiple_json_to_csv(target_path: Path, *args):
    """
    :param target_path: the path to the csv file
    :param args: list of json file names
    """
    # first we open the csv file in "append mode" if the csv file already exists we just append data to its end
    with target_path.open("a", encoding="utf-8-sig", newline="") as fd_write:
        # for each json file name (source_path)
        for index, source_path in enumerate(args):
            # we need to know when to write the headerof the CSV (first line) which contains the field names
            is_first_file = index == 0
            
            with source_path.open("r") as fd_read:
                # read a json file and convert to csv
                print(f"adding json data from {source_path} to {target_path}")
                json_to_csv(fd_read, fd_write, write_header=is_first_file)


def validate_file_names(names: List[Path]) -> List[Path]:
    """ensures that each given file name exists, quits the program in case of failure.
    This prevents us running into a problem in case of typo in the command line

    :param names: a list of filenames
    """
    paths = list(map(Path, names))
    for path in paths:
        if not path.exists():
            print(f"{path} does not exist")
            raise SystemExit(1)

        if not path.is_file():
            print(f"{path} exists but is not a file")
            raise SystemExit(1)

    return paths
